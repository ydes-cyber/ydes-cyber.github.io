#!/usr/bin/env python3
"""
Smart Home Intelligent System
A beginner-friendly intelligent system for managing smart home devices
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SmartDevice:
    """Base class for all smart devices"""
    
    def __init__(self, device_id: str, name: str, device_type: str):
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        self.is_on = False
        self.last_updated = datetime.now()
        self.properties = {}
    
    def turn_on(self):
        """Turn the device on"""
        self.is_on = True
        self.last_updated = datetime.now()
        logger.info(f"{self.name} ({self.device_type}) turned ON")
    
    def turn_off(self):
        """Turn the device off"""
        self.is_on = False
        self.last_updated = datetime.now()
        logger.info(f"{self.name} ({self.device_type}) turned OFF")
    
    def get_status(self) -> Dict[str, Any]:
        """Get device status"""
        return {
            'device_id': self.device_id,
            'name': self.name,
            'type': self.device_type,
            'is_on': self.is_on,
            'last_updated': self.last_updated.isoformat(),
            'properties': self.properties
        }

class SmartLight(SmartDevice):
    """Smart light with brightness and color control"""
    
    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name, "light")
        self.properties = {
            'brightness': 100,  # 0-100%
            'color': '#FFFFFF'  # Hex color code
        }
    
    def set_brightness(self, brightness: int):
        """Set light brightness (0-100)"""
        self.properties['brightness'] = max(0, min(100, brightness))
        logger.info(f"{self.name} brightness set to {self.properties['brightness']}%")
    
    def set_color(self, color: str):
        """Set light color (hex code)"""
        self.properties['color'] = color
        logger.info(f"{self.name} color set to {color}")

class SmartThermostat(SmartDevice):
    """Smart thermostat with temperature control"""
    
    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name, "thermostat")
        self.properties = {
            'target_temperature': 22,  # Celsius
            'current_temperature': 20,
            'mode': 'auto'  # auto, heat, cool, off
        }
    
    def set_temperature(self, temperature: int):
        """Set target temperature"""
        self.properties['target_temperature'] = temperature
        logger.info(f"{self.name} target temperature set to {temperature}°C")
    
    def set_mode(self, mode: str):
        """Set thermostat mode"""
        if mode in ['auto', 'heat', 'cool', 'off']:
            self.properties['mode'] = mode
            logger.info(f"{self.name} mode set to {mode}")

class SmartSensor(SmartDevice):
    """Smart sensor for monitoring environment"""
    
    def __init__(self, device_id: str, name: str, sensor_type: str):
        super().__init__(device_id, name, f"sensor_{sensor_type}")
        self.properties = {
            'sensor_type': sensor_type,
            'value': 0,
            'unit': self._get_unit(sensor_type)
        }
    
    def _get_unit(self, sensor_type: str) -> str:
        """Get appropriate unit for sensor type"""
        units = {
            'temperature': '°C',
            'humidity': '%',
            'motion': 'detected',
            'light': 'lux',
            'door': 'open/closed'
        }
        return units.get(sensor_type, '')
    
    def update_value(self, value):
        """Update sensor reading"""
        self.properties['value'] = value
        self.last_updated = datetime.now()
        logger.info(f"{self.name} reading: {value} {self.properties['unit']}")

class AutomationRule:
    """Automation rule for smart home intelligence"""
    
    def __init__(self, rule_id: str, name: str, condition: Dict, action: Dict):
        self.rule_id = rule_id
        self.name = name
        self.condition = condition
        self.action = action
        self.is_active = True
        self.last_triggered = None
    
    def check_condition(self, devices: Dict[str, SmartDevice]) -> bool:
        """Check if rule condition is met"""
        try:
            condition_type = self.condition.get('type')
            
            if condition_type == 'time':
                current_time = datetime.now().strftime('%H:%M')
                return current_time == self.condition.get('time')
            
            elif condition_type == 'device_state':
                device_id = self.condition.get('device_id')
                device = devices.get(device_id)
                if device:
                    if self.condition.get('property') == 'is_on':
                        return device.is_on == self.condition.get('value')
                    else:
                        prop_value = device.properties.get(self.condition.get('property'))
                        return prop_value == self.condition.get('value')
            
            elif condition_type == 'sensor_threshold':
                device_id = self.condition.get('device_id')
                device = devices.get(device_id)
                if device and 'sensor' in device.device_type:
                    sensor_value = device.properties.get('value', 0)
                    threshold = self.condition.get('threshold')
                    operator = self.condition.get('operator', '>')
                    
                    if operator == '>':
                        return sensor_value > threshold
                    elif operator == '<':
                        return sensor_value < threshold
                    elif operator == '==':
                        return sensor_value == threshold
            
            return False
        except Exception as e:
            logger.error(f"Error checking condition for rule {self.name}: {e}")
            return False
    
    def execute_action(self, devices: Dict[str, SmartDevice]):
        """Execute the rule action"""
        try:
            action_type = self.action.get('type')
            device_id = self.action.get('device_id')
            device = devices.get(device_id)
            
            if not device:
                return
            
            if action_type == 'turn_on':
                device.turn_on()
            elif action_type == 'turn_off':
                device.turn_off()
            elif action_type == 'set_property':
                property_name = self.action.get('property')
                value = self.action.get('value')
                
                if hasattr(device, f'set_{property_name}'):
                    getattr(device, f'set_{property_name}')(value)
                else:
                    device.properties[property_name] = value
            
            self.last_triggered = datetime.now()
            logger.info(f"Automation rule '{self.name}' executed successfully")
            
        except Exception as e:
            logger.error(f"Error executing action for rule {self.name}: {e}")

class SmartHomeSystem:
    """Main smart home system controller"""
    
    def __init__(self):
        self.devices: Dict[str, SmartDevice] = {}
        self.automation_rules: Dict[str, AutomationRule] = {}
        self.is_running = False
        self.automation_thread = None
        
        # Initialize with some sample devices
        self._initialize_sample_devices()
        self._initialize_sample_rules()
    
    def _initialize_sample_devices(self):
        """Initialize with sample devices for demonstration"""
        # Add sample lights
        living_room_light = SmartLight("light_001", "Living Room Light")
        bedroom_light = SmartLight("light_002", "Bedroom Light")
        
        # Add sample thermostat
        main_thermostat = SmartThermostat("thermo_001", "Main Thermostat")
        
        # Add sample sensors
        motion_sensor = SmartSensor("sensor_001", "Living Room Motion", "motion")
        temp_sensor = SmartSensor("sensor_002", "Outdoor Temperature", "temperature")
        door_sensor = SmartSensor("sensor_003", "Front Door", "door")
        
        # Add devices to system
        for device in [living_room_light, bedroom_light, main_thermostat, 
                      motion_sensor, temp_sensor, door_sensor]:
            self.add_device(device)
    
    def _initialize_sample_rules(self):
        """Initialize with sample automation rules"""
        # Rule 1: Turn on living room light when motion detected
        motion_rule = AutomationRule(
            "rule_001",
            "Motion Activated Lighting",
            {
                'type': 'sensor_threshold',
                'device_id': 'sensor_001',
                'threshold': 0,
                'operator': '>'
            },
            {
                'type': 'turn_on',
                'device_id': 'light_001'
            }
        )
        
        # Rule 2: Evening lighting automation
        evening_rule = AutomationRule(
            "rule_002",
            "Evening Lighting",
            {
                'type': 'time',
                'time': '18:00'
            },
            {
                'type': 'turn_on',
                'device_id': 'light_001'
            }
        )
        
        # Rule 3: Energy saving - turn off lights at night
        night_rule = AutomationRule(
            "rule_003",
            "Night Energy Saving",
            {
                'type': 'time',
                'time': '23:00'
            },
            {
                'type': 'turn_off',
                'device_id': 'light_001'
            }
        )
        
        for rule in [motion_rule, evening_rule, night_rule]:
            self.add_automation_rule(rule)
    
    def add_device(self, device: SmartDevice):
        """Add a device to the system"""
        self.devices[device.device_id] = device
        logger.info(f"Device added: {device.name} ({device.device_type})")
    
    def remove_device(self, device_id: str):
        """Remove a device from the system"""
        if device_id in self.devices:
            device = self.devices.pop(device_id)
            logger.info(f"Device removed: {device.name}")
    
    def get_device(self, device_id: str) -> SmartDevice:
        """Get a device by ID"""
        return self.devices.get(device_id)
    
    def get_all_devices(self) -> Dict[str, Dict]:
        """Get status of all devices"""
        return {device_id: device.get_status() 
                for device_id, device in self.devices.items()}
    
    def add_automation_rule(self, rule: AutomationRule):
        """Add an automation rule"""
        self.automation_rules[rule.rule_id] = rule
        logger.info(f"Automation rule added: {rule.name}")
    
    def remove_automation_rule(self, rule_id: str):
        """Remove an automation rule"""
        if rule_id in self.automation_rules:
            rule = self.automation_rules.pop(rule_id)
            logger.info(f"Automation rule removed: {rule.name}")
    
    def _automation_loop(self):
        """Main automation loop"""
        while self.is_running:
            try:
                for rule in self.automation_rules.values():
                    if rule.is_active and rule.check_condition(self.devices):
                        # Prevent rule from triggering too frequently
                        if (rule.last_triggered is None or 
                            datetime.now() - rule.last_triggered > timedelta(minutes=1)):
                            rule.execute_action(self.devices)
                
                # Simulate sensor updates (in real system, these would come from actual sensors)
                self._simulate_sensor_updates()
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in automation loop: {e}")
                time.sleep(10)
    
    def _simulate_sensor_updates(self):
        """Simulate sensor data updates for demonstration"""
        import random
        
        for device in self.devices.values():
            if 'sensor' in device.device_type:
                if device.properties['sensor_type'] == 'temperature':
                    # Simulate temperature between 15-30°C
                    device.update_value(round(random.uniform(15, 30), 1))
                elif device.properties['sensor_type'] == 'motion':
                    # Randomly detect motion
                    device.update_value(1 if random.random() > 0.8 else 0)
                elif device.properties['sensor_type'] == 'door':
                    # Rarely change door state
                    if random.random() > 0.95:
                        device.update_value('open' if device.properties['value'] == 'closed' else 'closed')
    
    def start_automation(self):
        """Start the automation system"""
        if not self.is_running:
            self.is_running = True
            self.automation_thread = threading.Thread(target=self._automation_loop)
            self.automation_thread.daemon = True
            self.automation_thread.start()
            logger.info("Smart home automation system started")
    
    def stop_automation(self):
        """Stop the automation system"""
        self.is_running = False
        if self.automation_thread:
            self.automation_thread.join(timeout=5)
        logger.info("Smart home automation system stopped")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            'is_running': self.is_running,
            'total_devices': len(self.devices),
            'total_rules': len(self.automation_rules),
            'active_rules': sum(1 for rule in self.automation_rules.values() if rule.is_active),
            'devices_on': sum(1 for device in self.devices.values() if device.is_on),
            'last_update': datetime.now().isoformat()
        }
    
    def save_config(self, filename: str = 'smart_home_config.json'):
        """Save system configuration to file"""
        config = {
            'devices': {},
            'automation_rules': {}
        }
        
        # Save device configurations
        for device_id, device in self.devices.items():
            config['devices'][device_id] = {
                'name': device.name,
                'type': device.device_type,
                'properties': device.properties
            }
        
        # Save automation rules
        for rule_id, rule in self.automation_rules.items():
            config['automation_rules'][rule_id] = {
                'name': rule.name,
                'condition': rule.condition,
                'action': rule.action,
                'is_active': rule.is_active
            }
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Configuration saved to {filename}")

# Command-line interface for testing
def main():
    """Main function for command-line testing"""
    smart_home = SmartHomeSystem()
    
    print("🏠 Smart Home Intelligent System")
    print("================================")
    print("Starting automation system...")
    
    smart_home.start_automation()
    
    try:
        while True:
            print("\nAvailable commands:")
            print("1. Show all devices")
            print("2. Control device")
            print("3. Show system status")
            print("4. Add automation rule")
            print("5. Save configuration")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                devices = smart_home.get_all_devices()
                print("\n📱 All Devices:")
                for device_id, status in devices.items():
                    print(f"  {status['name']} ({status['type']}) - {'ON' if status['is_on'] else 'OFF'}")
                    if status['properties']:
                        for prop, value in status['properties'].items():
                            print(f"    {prop}: {value}")
            
            elif choice == '2':
                device_id = input("Enter device ID: ").strip()
                device = smart_home.get_device(device_id)
                if device:
                    action = input("Enter action (on/off): ").strip().lower()
                    if action == 'on':
                        device.turn_on()
                    elif action == 'off':
                        device.turn_off()
                    else:
                        print("Invalid action")
                else:
                    print("Device not found")
            
            elif choice == '3':
                status = smart_home.get_system_status()
                print("\n🏠 System Status:")
                for key, value in status.items():
                    print(f"  {key}: {value}")
            
            elif choice == '4':
                print("This is a simplified interface. Check the code for automation rule examples.")
            
            elif choice == '5':
                smart_home.save_config()
                print("Configuration saved!")
            
            elif choice == '6':
                break
            
            else:
                print("Invalid choice")
    
    except KeyboardInterrupt:
        pass
    
    finally:
        print("\nShutting down smart home system...")
        smart_home.stop_automation()
        print("Goodbye! 👋")

if __name__ == "__main__":
    main()