# Stagg EKG+ Home Assistant Integration

A Home Assistant integration for the Fellow Stagg EKG+ electric kettle. Control and monitor your kettle directly from Home Assistant.

## Features

- Control kettle power (on/off)
- Set target temperature
- Monitor current temperature
- Automatic temperature updates
- Bluetooth discovery support

## Installation

### Option 1: HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz) installed
2. Add this repository as a custom repository in HACS:
   - Click the menu icon in the top right of HACS
   - Select "Custom repositories"
   - Add `levi/stagg-ekg-plus-ha` with category "Integration"
3. Click "Download" on the Stagg EKG+ integration
4. Restart Home Assistant
5. Go to Settings -> Devices & Services -> Add Integration
6. Search for "Stagg EKG+"
7. Follow the configuration steps

### Option 2: Manual Installation

1. Copy the `custom_components/stagg_ekg` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Go to Settings -> Devices & Services -> Add Integration
4. Search for "Stagg EKG+"
5. Follow the configuration steps

## Configuration

The integration can be set up in two ways:

1. **Automatic Discovery**: The kettle will be automatically discovered if Bluetooth is enabled in Home Assistant
2. **Manual Configuration**: You can manually add the kettle by providing its MAC address

## Usage

Once configured, the kettle will appear as a climate entity in Home Assistant. You can:

- Turn the kettle on/off using the climate entity
- Set the target temperature using the temperature slider
- Monitor the current temperature
- See the heating status (heating/idle)

## Requirements

- Home Assistant 2024.1.0 or newer
- Home Assistant Community Store (HACS) for easy installation
- Bluetooth support in your Home Assistant instance
- A Fellow Stagg EKG+ kettle

## Troubleshooting

If you experience connection issues:
1. Ensure the kettle is within Bluetooth range of your Home Assistant device
2. Check that Bluetooth is enabled and working in Home Assistant
3. Verify the MAC address if manually configured
4. Check the Home Assistant logs for detailed error messages

## Development

### Running with Docker Compose

The easiest way to test changes is with Docker Compose, which runs an isolated Home Assistant instance with the integration mounted in.

#### Prerequisites

- Docker and Docker Compose v2+

#### Quick start

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Start Home Assistant:
   ```bash
   docker compose up -d
   ```

3. Open http://localhost:8123 in your browser.

4. On first run, create an owner account, then go to
   **Settings > Devices & Services > Add Integration** and search
   for "Fellow Stagg".

#### Development workflow

- Edit files under `custom_components/fellow_stagg/` as usual.
- Restart to pick up changes:
  ```bash
  docker compose restart
  ```
- View logs:
  ```bash
  docker compose logs -f homeassistant
  ```
- Stop:
  ```bash
  docker compose down
  ```

#### Testing against a specific HA version

Edit `.env` and set:
```
HA_VERSION=2025.3.4
```
Then `docker compose up -d` (it will pull the new image).

#### Resetting state

The `config/` directory stores Home Assistant runtime state (database,
authentication, etc.) and is gitignored. Only `config/configuration.yaml`
is tracked. To start fresh, stop the container and delete the `config/`
directory contents (except `configuration.yaml`).

### Running natively

If you prefer running Home Assistant directly (without Docker):

1. Install dependencies:
   ```bash
   scripts/setup
   ```

2. Start Home Assistant with debug logging:
   ```bash
   scripts/develop
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details
