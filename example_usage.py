#!/usr/bin/env python3
"""
Smart Home System Usage Examples
This script demonstrates how to use the smart home system programmatically
"""

from smart_home import SmartHomeSystem, SmartLight, SmartThermostat, SmartSensor, AutomationRule
import time

def main():
    print("🏠 Smart Home System - Usage Examples")
    print("=====================================")
    
    # Create a new smart home system
    smart_home = SmartHomeSystem()
    
    print("\n1. System Overview:")
    print(f"   Total devices: {len(smart_home.devices)}")
    print(f"   Automation rules: {len(smart_home.automation_rules)}")
    
    # Display all devices
    print("\n2. Current Devices:")
    devices = smart_home.get_all_devices()
    for device_id, device_info in devices.items():
        status = "ON" if device_info['is_on'] else "OFF"
        print(f"   - {device_info['name']} ({device_info['type']}) - {status}")
        
        # Show device properties
        for prop, value in device_info['properties'].items():
            print(f"     {prop}: {value}")
    
    # Demonstrate device control
    print("\n3. Device Control Examples:")
    
    # Control a light
    living_room_light = smart_home.get_device("light_001")
    if living_room_light:
        print(f"   Controlling {living_room_light.name}:")
        living_room_light.turn_on()
        living_room_light.set_brightness(75)
        living_room_light.set_color("#FFD700")  # Gold color
        print(f"   - Turned on, brightness: {living_room_light.properties['brightness']}%")
        print(f"   - Color: {living_room_light.properties['color']}")
    
    # Control thermostat
    thermostat = smart_home.get_device("thermo_001")
    if thermostat:
        print(f"   Controlling {thermostat.name}:")
        thermostat.set_temperature(24)
        thermostat.set_mode("heat")
        print(f"   - Target temperature: {thermostat.properties['target_temperature']}°C")
        print(f"   - Mode: {thermostat.properties['mode']}")
    
    # Add a new device
    print("\n4. Adding a New Device:")
    kitchen_light = SmartLight("light_003", "Kitchen Light")
    smart_home.add_device(kitchen_light)
    kitchen_light.turn_on()
    kitchen_light.set_brightness(50)
    print(f"   Added and configured {kitchen_light.name}")
    
    # Create a custom automation rule
    print("\n5. Creating Custom Automation Rule:")
    custom_rule = AutomationRule(
        "rule_004",
        "Kitchen Light Auto-Off",
        {
            'type': 'sensor_threshold',
            'device_id': 'sensor_002',  # Temperature sensor
            'threshold': 28,
            'operator': '>'
        },
        {
            'type': 'turn_off',
            'device_id': 'light_003'  # Kitchen light
        }
    )
    smart_home.add_automation_rule(custom_rule)
    print(f"   Created rule: {custom_rule.name}")
    print(f"   - Condition: Turn off kitchen light when temperature > 28°C")
    
    # Start automation system
    print("\n6. Starting Automation System:")
    smart_home.start_automation()
    print("   Automation system started - rules will be checked every 10 seconds")
    
    # Monitor system for a short time
    print("\n7. Monitoring System (30 seconds):")
    print("   Watch for sensor updates and rule triggers...")
    
    for i in range(6):  # Monitor for 30 seconds (6 * 5 seconds)
        time.sleep(5)
        
        # Show current system status
        status = smart_home.get_system_status()
        print(f"   Status update {i+1}/6:")
        print(f"   - Devices on: {status['devices_on']}/{status['total_devices']}")
        print(f"   - Active rules: {status['active_rules']}")
        
        # Show sensor readings
        temp_sensor = smart_home.get_device("sensor_002")
        motion_sensor = smart_home.get_device("sensor_001")
        if temp_sensor and motion_sensor:
            print(f"   - Temperature: {temp_sensor.properties['value']}°C")
            print(f"   - Motion detected: {motion_sensor.properties['value']}")
    
    # Save configuration
    print("\n8. Saving Configuration:")
    smart_home.save_config("example_config.json")
    print("   Configuration saved to example_config.json")
    
    # Stop automation
    print("\n9. Stopping System:")
    smart_home.stop_automation()
    print("   Automation system stopped")
    
    # Final system overview
    print("\n10. Final System State:")
    final_devices = smart_home.get_all_devices()
    for device_id, device_info in final_devices.items():
        status = "ON" if device_info['is_on'] else "OFF"
        print(f"    - {device_info['name']}: {status}")
    
    print("\n✅ Example completed successfully!")
    print("\nNext steps:")
    print("- Run 'python smart_home.py' for command-line interface")
    print("- Run 'python web_interface.py' for web interface")
    print("- Modify this script to experiment with different scenarios")

if __name__ == "__main__":
    main()