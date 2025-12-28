# ESP32-C6 Marine Sensor Hub

A WiFi-enabled multi-sensor board designed for marine applications, featuring
temperature monitoring, humidity sensing, and current measurement capabilities.

![License](https://img.shields.io/badge/license-Open%20Source-blue)
![Status](https://img.shields.io/badge/status-In%20Development-yellow)

## Overview

The Marine Sensor Hub is a compact, ruggedized sensor platform built around
the ESP32-C6 microcontroller. It's designed to monitor critical systems on
boats and marine vessels, providing real-time data over WiFi 6 to a central
server via MQTT.

### Key Features

- **ESP32-C6 with WiFi 6** - Low-power RISC-V microcontroller with 8MB flash
- **Multiple Sensor Interfaces:**
  - Onboard SHT40 temperature & humidity sensor (±0.2°C accuracy)
  - Multiple DS18B20 1-Wire temperature sensors on shared bus (-67°F to +257°F)
  - 3× K-type thermocouple inputs (up to 2000°F via MAX31855)
  - 5× 30A current clamp inputs (QNHCK2-16 compatible, 6th channel reserved)
- **Dual Power System:**
  - 12VDC input (automotive/marine standard)
  - USB-C for programming and bench testing
  - Automatic power source selection with OR-ing diodes
- **Marine-Hardened Design:**
  - Reverse polarity protection
  - Voltage spike protection (TVS diode)
  - Conformal coating compatible
  - Wide operating temperature range

## Use Cases

- **Engine Room Monitoring:** Track engine temperature, exhaust temperature,
  and alternator current
- **Battery Bank Management:** Monitor charging current across multiple banks
- **HVAC Monitoring:** Track refrigerator/freezer performance and cabin
  temperature/humidity
- **Safety Systems:** High-temperature alarms for exhaust systems and engine
  components

## Project Status

Currently in schematic design phase:

- ✅ Hardware requirements defined
- ✅ Component selection complete
- ✅ Dual power system designed
- 🚧 KiCad schematic in progress (Part 2.6 - RGB LED)
- ⏳ PCB layout pending
- ⏳ Firmware development pending

## Hardware Specifications

### Microcontroller

- **IC:** ESP32-C6-WROOM-1-N8 (8MB flash)
- **Core:** RISC-V single core @ 160MHz
- **WiFi:** 802.11ax (WiFi 6), 2.4GHz
- **Operating Voltage:** 3.3V

### Power Requirements

- **Input:** 12VDC nominal (9-16V range)
- **Current Draw:** 300-350mA peak @ 3.3V
- **USB-C:** 5V input with 3.3V LDO regulator
- **Power Dissipation:** ~3W maximum

### Sensors

| Sensor | Interface | Quantity | Range |
| ------ | --------- | -------- | ----- |
| SHT40 | I2C | 1 (onboard) | -40°C to +125°C, 0-100% RH |
| DS18B20 | 1-Wire | Multiple (shared bus) | -55°C to +125°C |
| MAX31855 | SPI | 3 | -270°C to +1372°C (K-type) |
| QNHCK2-16 | Analog | 5 (6th reserved) | 0-30A AC/DC |

### Connectivity

- **WiFi:** 802.11ax (2.4GHz), WPA3 support
- **Protocol:** MQTT over TCP/IP
- **Programming:** USB-C (native ESP32-C6 USB Serial/JTAG)

## Repository Structure

```text
esp32-marine-sensorhub-v2/
├── README.md                 # This file
├── Hardware.md              # Complete hardware design document
├── Requirements.md          # KiCad schematic requirements
├── hardware/
│   ├── KICAD_SCHEMATIC_GUIDE.md  # Step-by-step build guide
│   └── mshv2/               # KiCad project files
│       ├── mshv2.kicad_pro
│       └── mshv2.kicad_sch
├── firmware/                # (TBD) ESP-IDF firmware
└── docs/                    # Additional documentation
```

## Getting Started

### For Hardware Developers

1. **Review the design:**
   - Read [Hardware.md](Hardware.md) for complete circuit details
   - Check [Requirements.md](Requirements.md) for specifications

2. **Build the schematic:**
   - Follow [hardware/KICAD_SCHEMATIC_GUIDE.md](hardware/KICAD_SCHEMATIC_GUIDE.md)
   - Use KiCad 9.0 or later
   - Open `hardware/mshv2/mshv2.kicad_pro`

3. **Order components:**
   - See BOM in [Hardware.md](Hardware.md#bill-of-materials-bom)
   - Estimated cost: ~$32.85 per board (components only)

### For Firmware Developers

**Coming soon** - firmware development will use ESP-IDF:

- MQTT client implementation
- Sensor polling and calibration
- WiFi connection management
- Watchdog and fault detection

## Technical Highlights

### Dual Power Design

The board features an innovative dual power system that allows operation from
either 12V marine power or USB-C:

```text
12V Path: 12V → LM2596S → 3.3V → D_BUCK → +3V3 rail
USB Path: 5V VBUS → AMS1117 → 3.3V → D_USB → +3V3 rail
```

Schottky diodes (B5819W) automatically select the power source without conflict
or backfeeding.

### Current Clamp Signal Conditioning

Each of the 5 current clamp channels features precision signal conditioning:

- Input protection (1kΩ series resistor)
- Voltage divider (5V → 3.3V range)
- RC low-pass filter (1.6kHz cutoff)
- Unity-gain op-amp buffer (MCP6004) for all channels
- Direct connection to ESP32 ADC (GPIO0-4)

Two MCP6004 quad op-amps provide buffering:

- U5 (channels 1-4)
- U6 (channel 5 + reserved channel 6)

Note: GPIO5 (ADC1_CH5) reserved for 6th clamp expansion with U6B.

### Marine Environment Protection

- Reverse polarity protection (MBRS340 Schottky diode)
- Voltage spike protection (SMBJ15A TVS diode)
- Conformal coating compatible PCB design
- Wide trace spacing for moisture resistance
- Mounting holes for secure installation

## Bill of Materials

Estimated component cost: **~$32.85** per board (quantity 1-10)

### Key Components

- ESP32-C6-WROOM-1-N8: $2.50
- SHT40 temperature/humidity sensor: $4.00
- MAX31855 thermocouple amplifier (3×): $15.00
- MCP6004 quad op-amp (2×): $1.00
- LM2596 buck converter module: $2.00
- AMS1117-3.3 LDO regulator: ~$0.50
- Passive components & connectors: ~$7.85

See [Hardware.md](Hardware.md#bill-of-materials-bom) for complete BOM.

## Design Documents

- **[Hardware.md](Hardware.md)** - Complete hardware design, schematics,
  and specifications
- **[Requirements.md](Requirements.md)** - KiCad schematic requirements and
  PCB guidelines
- **[KICAD_SCHEMATIC_GUIDE.md](hardware/KICAD_SCHEMATIC_GUIDE.md)** -
  Step-by-step schematic creation guide

## MQTT Topic Structure

```text
boat/sensors/{location}/{sensor_type}

Examples:
  boat/sensors/engine_room/temperature
  boat/sensors/engine_room/wet_exhaust_temp
  boat/sensors/galley/fridge_temp
  boat/sensors/salon/humidity
  boat/sensors/battery_bank/current_1
```

## Safety Considerations

### Important Safety Information

⚠️ **Warning:**

- This board is designed for 12V automotive/marine applications
- Ensure proper fusing and circuit protection in your installation
- High-temperature sensors must be installed per manufacturer specifications
- This design has **not** been certified for safety-critical applications
- Implement proper watchdog and fault detection in firmware
- Use conformal coating for marine environments
- Regular inspection and maintenance required

## Contributing

This is an open-source hardware project. Contributions are welcome!

- Report issues or suggest improvements via GitHub Issues
- Submit pull requests for documentation or design improvements
- Share your build photos and experiences

## License

This design is open-source hardware. License to be specified (MIT, Apache 2.0,
or CERN-OHL).

## Acknowledgments

- ESP32-C6 datasheet and design guidelines from Espressif Systems
- KiCad open-source EDA software
- Marine sensor community feedback and requirements

## Contact & Support

- **GitHub Repository:** <https://github.com/dpmcgarry/esp32-marine-sensorhub-v2>
- **Issues:** <https://github.com/dpmcgarry/esp32-marine-sensorhub-v2/issues>
- **Discussions:** <https://github.com/dpmcgarry/esp32-marine-sensorhub-v2/discussions>

---

Built with ❤️ for the marine community
