#!/usr/bin/env python3
"""
Smart Home Web Interface
A simple web interface for the smart home system
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime
from smart_home import SmartHomeSystem, SmartLight, SmartThermostat, SmartSensor, AutomationRule

app = Flask(__name__)
smart_home = SmartHomeSystem()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/devices')
def get_devices():
    """API endpoint to get all devices"""
    devices = smart_home.get_all_devices()
    return jsonify(devices)

@app.route('/api/devices/<device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    """API endpoint to toggle device on/off"""
    device = smart_home.get_device(device_id)
    if device:
        if device.is_on:
            device.turn_off()
        else:
            device.turn_on()
        return jsonify({'success': True, 'status': device.get_status()})
    return jsonify({'success': False, 'error': 'Device not found'}), 404

@app.route('/api/devices/<device_id>/brightness', methods=['POST'])
def set_brightness(device_id):
    """API endpoint to set light brightness"""
    device = smart_home.get_device(device_id)
    if device and isinstance(device, SmartLight):
        brightness = request.json.get('brightness', 50)
        device.set_brightness(brightness)
        return jsonify({'success': True, 'status': device.get_status()})
    return jsonify({'success': False, 'error': 'Device not found or not a light'}), 404

@app.route('/api/devices/<device_id>/temperature', methods=['POST'])
def set_temperature(device_id):
    """API endpoint to set thermostat temperature"""
    device = smart_home.get_device(device_id)
    if device and isinstance(device, SmartThermostat):
        temperature = request.json.get('temperature', 22)
        device.set_temperature(temperature)
        return jsonify({'success': True, 'status': device.get_status()})
    return jsonify({'success': False, 'error': 'Device not found or not a thermostat'}), 404

@app.route('/api/system/status')
def get_system_status():
    """API endpoint to get system status"""
    return jsonify(smart_home.get_system_status())

@app.route('/api/automation/start', methods=['POST'])
def start_automation():
    """API endpoint to start automation"""
    smart_home.start_automation()
    return jsonify({'success': True, 'message': 'Automation started'})

@app.route('/api/automation/stop', methods=['POST'])
def stop_automation():
    """API endpoint to stop automation"""
    smart_home.stop_automation()
    return jsonify({'success': True, 'message': 'Automation stopped'})

@app.route('/api/rules')
def get_rules():
    """API endpoint to get automation rules"""
    rules = {}
    for rule_id, rule in smart_home.automation_rules.items():
        rules[rule_id] = {
            'name': rule.name,
            'condition': rule.condition,
            'action': rule.action,
            'is_active': rule.is_active,
            'last_triggered': rule.last_triggered.isoformat() if rule.last_triggered else None
        }
    return jsonify(rules)

if __name__ == '__main__':
    # Start the automation system
    smart_home.start_automation()
    
    try:
        print("🏠 Smart Home Web Interface")
        print("===========================")
        print("Starting web server on http://localhost:5000")
        print("Press Ctrl+C to stop")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    finally:
        smart_home.stop_automation()
        print("Smart home system stopped.")