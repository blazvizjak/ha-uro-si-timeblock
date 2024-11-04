# Slovenian Electrical Grid Time Block Sensor for Home Assistant

This integration provides a sensor that determines the current time block based on Slovenian energy pricing periods. It takes into account:
- High season (November-February) and low season (March-October)
- Workdays and non-workdays (including weekends and holidays)
- Slovenian national holidays (including Easter-dependent holidays)

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on Integrations
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Add"
7. Search for "URO SI TimeBlock" in HACS
8. Click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/uro_si_timeblock` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: uro_si_timeblock
```

## Usage

The sensor will be created as `sensor.uro_si_timeblock` with the following attributes:
- `state`: Current block number (1-5)
- `is_workday`: Whether current day is a workday
- `is_high_season`: Whether current month is in high season
- `current_time`: Current time in decimal format
- `month`: Current month
- `hour`: Current hour
- `minute`: Current minute

### Time Blocks

The sensor determines the current block (1-5) based on:
1. Season (high/low)
2. Day type (workday/non-workday)
3. Time of day

For example, in high season on workdays:
- Block 1: 7:00-14:00 and 16:00-20:00
- Block 2: 6:00-7:00, 14:00-16:00, and 20:00-22:00
- Block 3: 0:00-6:00 and 22:00-24:00

See the full schedule in the code documentation.

## Contributing

Feel free to contribute to this project by opening issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.