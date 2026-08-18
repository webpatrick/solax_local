# SolaX Local - Home Assistant Integration

A Fork from: 
- https://github.com/Knetus56/solax_local

A [Home Assistant](https://www.home-assistant.io/) integration to control and monitor your **SolaX** inverter locally over HTTP.

## 🌟 Features

- 📊 **Real-time monitoring**: MPPT power, energy production, temperature
- 🔄 **Inverter control**: Power on/off via switch
- 📈 **Production tracking**: Daily and cumulative production
- 🕐 **History**: Timestamp of the last update
- 🌍 **Multi-inverter support**: X1 Micro 2-in-1
- 🔐 **Local connection**: No cloud, fully local
- 🇬🇧 **Localized interface**: English and French

## 📋 Sensors

| Sensor | Description | Unit |
|--------|-------------|------|
| `mppt1_puissance` | MPPT 1 power | W |
| `mppt1_voltage` | MPPT 1 voltage | V |
| `mppt1_intensite` | MPPT 1 current | A |
| `mppt2_puissance` | MPPT 2 power | W |
| `mppt2_voltage` | MPPT 2 voltage | V |
| `mppt2_intensite` | MPPT 2 current | A |
| `inverter_voltage` | Inverter output voltage | V |
| `inverter_intensite` | Inverter output current | A |
| `inverter_puissance` | Inverter output power | W |
| `inverter_freq` | Inverter frequency | Hz |
| `temp` | Inverter temperature | °C |
| `prod_auj` | Daily production | kWh |
| `prod_total` | Total cumulative production | kWh |
| `mode` | Operating mode | WaitMode/CheckMode/NormalMode |
| `ip` | Inverter IP address | - |
| `num_inverter` | Serial number | - |
| `last_update` | Last update | timestamp |

## 🔌 Control Entities

- **Binary Sensor**: Online/offline state
- **Switch**: Inverter power on/off

## 🔄 Services

### Refresh all inverters

Service: `solax_local.refresh_all`

Forces an immediate update of all configured inverters without waiting for the scan interval.

**Usage in an automation**:
```yaml
service: solax_local.refresh_all
```

**Or in the Developer Tools**:
1. **Developer Tools** > **Services**
2. Select `SolaX Local: Refresh all inverters`
3. Click **Execute**

## 🚀 Installation

### Requirements

- Home Assistant 2023.12+
- Network access to the SolaX inverter
- Inverter IP address and serial number

### Via HACS (recommended)

**Direct HACS link**:

[![Open je Home Assistant instantie en voeg deze repository toe aan HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=webpatrick&repository=solax_local&category=integration)

Or manually:
1. Open Home Assistant
2. Go to **HACS** > **Integrations**
3. Click the **menu** (⋯) > **Custom repositories**
4. Add the URL: `https://github.com/webpatrick/solax_local`
5. Search for "SolaX Local"
6. Click **Install**
7. Restart Home Assistant

### Manual installation

1. Download the latest [release](https://github.com/Knetus56/solax_local/releases)
2. Extract it into `custom_components/solax_local/`
3. Restart Home Assistant

## ⚙️ Configuration

### Via Home Assistant UI

1. **Settings** > **Devices & Services** > **Integrations**
2. Click **Add Integration**
3. Search for and select **SolaX Local**
4. Enter the following information:
   - **IP**: Inverter IP address (example: `192.168.1.100`)
   - **Inverter type**: Select the model
   - **Serial number**: Inverter serial number
   - **Scan interval** (optional): Update frequency in seconds (default: 300s)

## 🔧 Advanced configuration

### Update interval

By default, the integration polls the inverter every **300 seconds** (5 minutes). You can adjust this in configuration.

### DIAGNOSTIC entities

The following entities are hidden by default (Advanced tab):
- Mode state
- IP address
- Serial number
- Last update

To display them: **Settings** > **Devices & Services** > Select the device > **Show hidden entities**

### Sensors show "Unknown"

- Check that the IP address is correct
- Check that the inverter is **online** and **powered**
- Check the **network connectivity** between HA and the inverter
- Increase the `scan interval` in case of network timeout

### The integration does not load

- Check the logs: **Settings** > **System** > **Logs**
- Look for connection errors
- Restart Home Assistant

### The device does not show the model

- This means the selected model is not recognized
- Check the selection during configuration

## ✨ What changed in this fork

This fork is specifically aligned with the SolaX X1 Micro 2-in-1 inverter family using firmware versions Wi‑Fi 011.00 and DSP 012.00. Compared with the upstream project, the protocol parsing and sensor mapping were adjusted to match the request/response format used by these units, making the integration work with the firmware variant used in this setup.

In addition, the integration now keeps the Total production and Daily production values stable across short offline periods and Home Assistant restarts. Instead of dropping back to zero when the inverter briefly reports empty or reset-like values, the last valid totals are retained so graphs and history remain accurate.

## 📦 Versions

This fork is tuned for the SolaX X1 Micro 2-in-1 inverter family using firmware versions Wi‑Fi 011.00 and DSP 012.00. Compared with the upstream project, the protocol parsing and sensor mapping were adjusted to match the request/response layout used by these units, so the integration works with the firmware variant in use here instead of the generic/default implementation.

Additionally, the cumulative production values are kept stable across short offline periods and Home Assistant restarts. The Total production and Daily production sensors retain their last valid values instead of dropping back to zero when the inverter temporarily reports empty or reset-like values, which avoids misleading resets in the history graphs.

- **2026-08-17** - Fork adjustments for X1 Micro 2-in-1 firmware (Wi‑Fi 011.00 / DSP 012.00), improved model compatibility, and stable handling of Total/Daily production values across offline/restart conditions
- **v1.2.2** (2026-07-22) - Added custom icon for HACS
- **v1.2.1** (2026-07-22) - Added refresh_all service to refresh all inverters
- **v1.2.0** (2026-07-22) - Added MPPT voltage/current sensors and inverter metrics
- **v1.1.0** (2026-07-22) - Fix MPPT keys and model initialization

## 🙏 Credits

- https://github.com/CurlyMoo thanks to this reverse engineering: https://github.com/squishykid/solax/issues/191
