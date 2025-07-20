# 🏠 Smart Home Intelligent System

A beginner-friendly intelligent system for managing smart home devices with automation capabilities.

## Features

- **Device Management**: Control various smart home devices (lights, thermostats, sensors)
- **Intelligent Automation**: Rule-based automation system with time and sensor triggers
- **Web Interface**: Beautiful, responsive web dashboard for device control
- **Real-time Monitoring**: Live sensor data simulation and device status updates
- **Extensible Architecture**: Easy to add new device types and automation rules

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd smart-home
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the System

#### Option 1: Command Line Interface
```bash
python smart_home.py
```

This will start the system with a simple command-line interface where you can:
- View all devices
- Control individual devices
- Monitor system status
- Save configuration

#### Option 2: Web Interface (Recommended)
```bash
python web_interface.py
```

Then open your web browser and go to: `http://localhost:5000`

The web interface provides:
- Real-time device dashboard
- Interactive device controls
- System status monitoring
- Automation rule overview

## System Architecture

### Core Components

1. **SmartDevice**: Base class for all smart home devices
2. **SmartLight**: Light devices with brightness and color control
3. **SmartThermostat**: Temperature control devices
4. **SmartSensor**: Environmental monitoring sensors
5. **AutomationRule**: Intelligence system for automated actions
6. **SmartHomeSystem**: Main controller managing all components

### Pre-configured Devices

The system comes with sample devices:
- Living Room Light (controllable brightness)
- Bedroom Light
- Main Thermostat (temperature control)
- Living Room Motion Sensor
- Outdoor Temperature Sensor
- Front Door Sensor

### Pre-configured Automation Rules

1. **Motion Activated Lighting**: Turns on living room light when motion detected
2. **Evening Lighting**: Automatically turns on lights at 6:00 PM
3. **Night Energy Saving**: Turns off lights at 11:00 PM

## Usage Examples

### Adding a New Device (Python Code)

```python
from smart_home import SmartHomeSystem, SmartLight

# Create system instance
smart_home = SmartHomeSystem()

# Add a new light
kitchen_light = SmartLight("light_003", "Kitchen Light")
smart_home.add_device(kitchen_light)

# Control the device
kitchen_light.turn_on()
kitchen_light.set_brightness(75)
```

### Creating Custom Automation Rules

```python
from smart_home import AutomationRule

# Create a custom rule
energy_saving_rule = AutomationRule(
    "rule_004",
    "Temperature-based Lighting",
    {
        'type': 'sensor_threshold',
        'device_id': 'sensor_002',  # Temperature sensor
        'threshold': 25,
        'operator': '>'
    },
    {
        'type': 'turn_off',
        'device_id': 'light_001'  # Turn off light when hot
    }
)

# Add rule to system
smart_home.add_automation_rule(energy_saving_rule)
```

## API Endpoints (Web Interface)

- `GET /api/devices` - Get all devices
- `POST /api/devices/<id>/toggle` - Toggle device on/off
- `POST /api/devices/<id>/brightness` - Set light brightness
- `POST /api/devices/<id>/temperature` - Set thermostat temperature
- `GET /api/system/status` - Get system status
- `POST /api/automation/start` - Start automation
- `POST /api/automation/stop` - Stop automation
- `GET /api/rules` - Get automation rules

## Configuration

The system automatically saves configuration to `smart_home_config.json`. This includes:
- Device settings and properties
- Automation rules
- System preferences

## Extending the System

### Adding New Device Types

1. Create a new class inheriting from `SmartDevice`
2. Implement device-specific methods
3. Add to the system using `add_device()`

### Adding New Automation Conditions

Extend the `check_condition()` method in `AutomationRule` class to support new condition types.

### Adding New Actions

Extend the `execute_action()` method in `AutomationRule` class to support new action types.

## Troubleshooting

### Common Issues

1. **Port 5000 already in use**: Change the port in `web_interface.py`
2. **Module not found**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Permission errors**: Make sure Python has write permissions for configuration files

### Logging

The system uses Python's logging module. Logs include:
- Device state changes
- Automation rule triggers
- System status updates
- Error messages

## Learning Resources

This project demonstrates several programming concepts:
- Object-Oriented Programming (OOP)
- Threading for concurrent operations
- REST API design with Flask
- Real-time web interfaces
- JSON data handling
- Logging and error handling

## Future Enhancements

Potential improvements for learning:
- Database integration for persistent storage
- User authentication and authorization
- Mobile app interface
- Voice control integration
- Machine learning for predictive automation
- Integration with real IoT devices
- Energy usage monitoring
- Security features (cameras, alarms)

## Contributing

This is a learning project! Feel free to:
1. Add new device types
2. Create more intelligent automation rules
3. Improve the web interface
4. Add new features
5. Fix bugs and optimize performance

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check the code comments for detailed explanations
2. Review the examples in this README
3. Experiment with the web interface
4. Modify the code to learn how it works

Happy coding! 🚀 
