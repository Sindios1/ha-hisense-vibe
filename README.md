# Hisense Vibe

Professional Home Assistant integration for Hisense TVs (2019+ models with VIDAA OS). Created by **Mr. Jesus**.

## Features

- **Built-in Pairing**: No manual service calls. Setup the TV via a simple UI PIN entry.
- **Local Control**: Works completely over your local network using MQTT.
- **Power Control**: Turn on via Wake-on-LAN and turn off via MQTT.
- **Source Selection**: Switch between HDMI inputs.
- **Czech Localization**: Full support for Czech and English languages.

## Installation

### Method 1: HACS (Recommended)

1. Open **HACS** in Home Assistant.
2. Click on **Integrations** -> **Three dots (top right)** -> **Custom repositories**.
3. Add `https://github.com/Sindios1/ha-hisense-vibe` with category `Integration`.
4. Click **Download**.
5. Restart Home Assistant.

### Method 2: Manual

1. Copy the `custom_components/hisense_vibe` folder to your HA `custom_components` directory.
2. Restart Home Assistant.

## Configuration

1. Go to **Settings** -> **Devices & Services**.
2. Click **Add Integration** and search for **Hisense Vibe**.
3. Follow the on-screen instructions (IP, MAC Address, PIN).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
