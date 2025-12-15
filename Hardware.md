# ESP32-C6 Marine Multi-Sensor Board

## Overview

A unified sensor board for marine applications featuring temperature, humidity, current monitoring, and high-temperature sensing capabilities. Designed for reliable operation in harsh marine environments with 12VDC power input.

## Features

- **Onboard Sensors:**
  - SHT40 temperature & humidity sensor (±0.2°C accuracy)
  
- **External Sensor Support:**
  - 3x DS18B20 1-Wire temperature sensors (-67°F to +257°F)
  - 1x K-type thermocouple via MAX31855 (up to 2000°F)
  - 6x QNHCK2-16 30A current clamp sensors
  
- **Connectivity:**
  - ESP32-C6 with WiFi 6 (802.11ax)
  - MQTT communication to central server
  
- **Power:**
  - 12VDC input with reverse polarity protection
  - TVS diode protection for voltage spikes
  - Efficient buck converter to 3.3V

## Board Specifications

### Microcontroller

- **IC:** ESP32-C6
- **Core:** RISC-V single core
- **WiFi:** 802.11ax (WiFi 6), 2.4GHz
- **Operating Voltage:** 3.3V

### Power Requirements

- **Input:** 12VDC (automotive/marine)
- **Current Draw:** 300-350mA peak @ 3.3V
- **Power Dissipation:** ~3W in buck converter

### GPIO Pin Allocation

| Function | GPIO Pin(s) | Notes |
|----------|-------------|-------|
| I2C SDA (SHT40) | GPIO6 | 4.7kΩ pullup |
| I2C SCL (SHT40) | GPIO7 | 4.7kΩ pullup |
| 1-Wire DS18B20 #1 | GPIO8 | 4.7kΩ pullup |
| 1-Wire DS18B20 #2 | GPIO10 | 4.7kΩ pullup |
| 1-Wire DS18B20 #3 | GPIO11 | 4.7kΩ pullup |
| SPI SCK (MAX31855) | GPIO19 | |
| SPI MISO (MAX31855) | GPIO18 | |
| SPI CS (MAX31855) | GPIO20 | |
| ADC Clamp #1 | GPIO0 (ADC1_CH0) | |
| ADC Clamp #2 | GPIO1 (ADC1_CH1) | |
| ADC Clamp #3 | GPIO2 (ADC1_CH2) | |
| ADC Clamp #4 | GPIO3 (ADC1_CH3) | |
| ADC Clamp #5 | GPIO4 (ADC1_CH4) | |
| ADC Clamp #6 | GPIO5 (ADC1_CH5) | |
| Status LED | GPIO23 | 330Ω resistor |
| Boot Button | GPIO9 | 10kΩ pullup |

## Schematic

### Power Supply Circuit

```text
12V_IN (J_PWR, 2-pin screw terminal)
  │
  ├── D1 (MBRS340 Schottky) ──┐ (Reverse polarity protection)
  │                            │
  ├── TVS1 (SMBJ15A) to GND ───┘ (Voltage spike protection)
  │
  ├── C1 (100µF, 25V electrolytic)
  │
  ├── U1 (LM2596 Buck Converter or module)
  │     VIN: 12V
  │     VOUT: 3.3V @ 3A
  │     EN: 10kΩ pullup to VIN
  │
  ├── C2 (100µF, 10V electrolytic)
  │
  ├── C3 (10µF ceramic)
  │
  └── 3.3V_MAIN (to all ICs)

GND ─── Common ground
```

### ESP32-C6 Core Circuit (U2)

```text
ESP32-C6
├── VDD: 3.3V_MAIN
├── GND: GND
├── EN: 10kΩ to 3.3V, 0.1µF to GND, RESET button to GND
└── GPIO9 (BOOT): 10kΩ pullup, button to GND
```

### SHT40 Temperature & Humidity Sensor (U3)

```text
SHT40 (I2C Address: 0x44)
├── VDD: 3.3V_MAIN
├── GND: GND
├── SDA: GPIO6 (4.7kΩ pullup to 3.3V)
├── SCL: GPIO7 (4.7kΩ pullup to 3.3V)
└── Decoupling: 0.1µF ceramic capacitor
```

### DS18B20 External Temperature Sensors

Each of 3 connectors (J1, J2, J3 - RJ45 or 3-pin JST-XH):

```text
Connector Pinout:
  Pin 1: 3.3V (or 5V if long cable runs needed)
  Pin 2: DATA (to GPIO8/10/11 with 4.7kΩ pullup)
  Pin 3: GND

Notes:
- 4.7kΩ pullup resistors on each data line
- Can support multiple sensors per 1-Wire bus if needed
- Max recommended cable length: 100 feet
```

### MAX31855 Thermocouple Interface (U4)

```text
MAX31855 (SPI)
├── VCC: 3.3V_MAIN
├── GND: GND
├── SCK: GPIO19
├── SO: GPIO18
├── CS: GPIO20
├── T+: K-type thermocouple + (J4, screw terminal)
├── T-: K-type thermocouple - (J4, screw terminal)
└── Decoupling: 0.1µF ceramic capacitor

PCB Notes:
- Keep thermocouple traces short
- Route away from noisy digital signals
- Consider copper pour ground plane around MAX31855
```

### Current Clamp Signal Conditioning (6 channels)

QNHCK2-16 outputs 0-5V, but ESP32 ADC maximum is 3.3V.

**Per channel circuit:**

```text
CLAMP_x_IN (J5-J10, screw terminal or JST)
  │
  ├── R_series (1kΩ) ──────────┐ (Current limiting/protection)
  │                             │
  ├── Voltage Divider:          │
  │   R1 (10kΩ) ────┬───────────┘
  │   R2 (20kΩ) ────┴─── GND
  │        │
  │        └─ Ratio: 5V × 20k/(10k+20k) = 3.33V
  │
  ├── RC Low-Pass Filter:
  │   R3 (1kΩ) ────┬─────────────┐
  │   C (0.1µF) ───┴─── GND      │ (1.6kHz cutoff)
  │                               │
  └── U5/U6 (MCP6004 buffer) ─────┘
        │
        └── ESP32 ADC (GPIO0-5)

MCP6004 Configuration (Unity Gain Buffer):
  +IN: from RC filter
  -IN: connected to OUT (feedback)
  OUT: to ESP32 ADC
  VDD: 3.3V_MAIN
  VSS: GND
  Decoupling: 0.1µF ceramic
  
Two MCP6004 ICs required:
  - U5: Channels 1-4
  - U6: Channels 5-6 (2 op-amps unused)
```

**Alternative (cost-optimized, less accurate):**

- Omit op-amps (saves ~$1)
- Use only voltage divider + RC filter
- May experience loading issues with high-impedance sensors

### Additional Circuits

**Power Indicator LED:**

```text
3.3V ──[1kΩ]──[LED]──── GND
```

**Status LED:**

```text
GPIO23 ──[330Ω]──[LED]──── GND
```

## Bill of Materials (BOM)

### Core Components

| Reference | Part Number | Description | Qty | Unit Price | Extended |
|-----------|-------------|-------------|-----|------------|----------|
| U2 | ESP32-C6-WROOM-1 | WiFi 6 module | 1 | $2.50 | $2.50 |
| U3 | SHT40 | Temp/humidity sensor | 1 | $4.00 | $4.00 |
| U4 | MAX31855 | Thermocouple amplifier | 1 | $5.00 | $5.00 |
| U5, U6 | MCP6004 | Quad op-amp | 2 | $0.50 | $1.00 |
| U1 | LM2596 module | Buck converter 12V→3.3V | 1 | $2.00 | $2.00 |

### Protection & Power

| Reference | Part Number | Description | Qty | Unit Price | Extended |
|-----------|-------------|-------------|-----|------------|----------|
| D1 | MBRS340 | Schottky diode 3A 40V | 1 | $0.30 | $0.30 |
| TVS1 | SMBJ15A | TVS diode 15V | 1 | $0.40 | $0.40 |
| C1 | - | 100µF 25V electrolytic | 1 | $0.15 | $0.15 |
| C2 | - | 100µF 10V electrolytic | 1 | $0.10 | $0.10 |
| C3 | - | 10µF ceramic | 1 | $0.10 | $0.10 |

### Passives (approximate quantities)

| Type | Value | Description | Qty | Unit Price | Extended |
|------|-------|-------------|-----|------------|----------|
| Resistors | 4.7kΩ | I2C & 1-Wire pullups | 5 | $0.02 | $0.10 |
| Resistors | 10kΩ | Voltage dividers, pullups | 10 | $0.02 | $0.20 |
| Resistors | 20kΩ | Voltage dividers | 6 | $0.02 | $0.12 |
| Resistors | 1kΩ | Current limiting, filters | 12 | $0.02 | $0.24 |
| Resistors | 330Ω | LED current limiting | 1 | $0.02 | $0.02 |
| Capacitors | 0.1µF | Decoupling, filtering | 15 | $0.05 | $0.75 |

### Connectors

| Reference | Type | Description | Qty | Unit Price | Extended |
|-----------|------|-------------|-----|------------|----------|
| J_PWR | Screw terminal | 2-pin, 5mm pitch, 12V input | 1 | $0.30 | $0.30 |
| J1-J3 | RJ45 or JST-XH | 3-pin, DS18B20 sensors | 3 | $0.40 | $1.20 |
| J4 | Screw terminal | 2-pin, thermocouple | 1 | $0.30 | $0.30 |
| J5-J10 | Screw terminal | 2-pin, current clamps | 6 | $0.30 | $1.80 |
| J_PROG | Pin header | 2×3, programming (optional) | 1 | $0.15 | $0.15 |

### Miscellaneous

| Item | Description | Qty | Unit Price | Extended |
|------|-------------|-----|------------|----------|
| LEDs | Status indicators | 2 | $0.10 | $0.20 |
| Buttons | Tactile switches (reset, boot) | 2 | $0.10 | $0.20 |
| PCB | 2-layer, ~80×60mm | 1 | $2.50 | $2.50 |

### **Total Board Cost: ~$23.50**

### External Sensors (purchased separately)

| Item | Part Number | Description | Unit Price |
|------|-------------|-------------|------------|
| DS18B20 | DS18B20 | Waterproof probe, 1m cable | $2-4 |
| Thermocouple | K-type | Stainless probe, 1-2m | $5-15 |
| Current clamp | QNHCK2-16 | 30A, 0-5V output | $8-12 |

## Connectors Pinout Reference

### J_PWR - 12V Power Input (Screw Terminal)

```text
Pin 1: +12V
Pin 2: GND
```

### J1, J2, J3 - DS18B20 Temperature Sensors (RJ45 or JST-XH)

```text
Pin 1: +3.3V (or +5V)
Pin 2: DATA
Pin 3: GND
```

### J4 - K-Type Thermocouple (Screw Terminal)

```text
Pin 1: T+ (Yellow wire on standard K-type)
Pin 2: T- (Red wire on standard K-type)
```

### J5-J10 - QNHCK2-16 Current Clamps (Screw Terminal)

```text
Pin 1: Signal (0-5V)
Pin 2: GND
```

### J_PROG - Programming Header (Optional, 2×3 pin header)

```text
Pin 1: GND      Pin 2: 3.3V
Pin 3: TX       Pin 4: RX
Pin 5: GPIO9    Pin 6: EN
```

## PCB Design Guidelines

### Layer Stack

- 2-layer board recommended
- Suggested dimensions: 80mm × 60mm (adjust to fit enclosure)

### Layout Considerations

1. **Power Distribution:**
   - Wide traces for 12V input (≥20 mil / 0.5mm)
   - Adequate copper for 3.3V rail (≥15 mil / 0.4mm)
   - Star ground configuration - separate analog and digital grounds
   - Single ground connection point near power supply

2. **Analog Section (ADC/Current Clamps):**
   - Keep analog traces away from digital signals
   - Route ADC traces away from ESP32 clock/SPI signals
   - Ground plane under ADC section
   - Short traces from voltage dividers to op-amps to ADC

3. **High-Temperature Sensor (MAX31855):**
   - Place MAX31855 away from buck converter (heat & noise)
   - Keep thermocouple traces short and symmetrical
   - Route T+ and T- as differential pair if possible
   - Avoid routing under or near noisy signals
   - Ground plane around MAX31855

4. **Digital Section:**
   - I2C traces: keep short, equal length preferred
   - Decouple ESP32 with 0.1µF + 10µF caps close to VDD pin
   - Pull-up resistors near respective signal sources

5. **Power Supply:**
   - Place bulk capacitors (C1, C2) close to buck converter
   - Use copper pour or wide traces for heat dissipation
   - Consider heatsinking or thermal vias if using discrete buck
   - Keep switching regulator away from sensitive analog circuits

6. **Component Placement:**
   - Group by function: power, digital, analog, I/O
   - Connectors on board edges
   - Programming header accessible
   - Status LEDs visible when installed

7. **Marine Environment Protection:**
   - Conformal coating over entire board (except connectors)
   - Adequate spacing between traces (≥10 mil / 0.25mm)
   - Solder mask coverage
   - Consider silkscreen for polarity markings
   - M3 mounting holes with adequate clearance

### Design Rule Checks (DRC)

- Minimum trace width: 8 mil (0.2mm)
- Minimum clearance: 8 mil (0.2mm)
- Minimum via size: 12 mil drill, 24 mil pad
- Power traces: 20+ mil
- Ground plane: maximum coverage with thermal reliefs

## Firmware Considerations

### ADC Configuration

```c
// Use 11dB attenuation for 0-3.3V input range
adc1_config_width(ADC_WIDTH_BIT_12);
adc1_config_channel_atten(ADC1_CHANNEL_0, ADC_ATTEN_DB_11);

// Software calibration for voltage divider
// Actual voltage = ADC_reading × (3.3 / 4095) × (30k / 20k)
float actual_voltage = adc_raw * 0.001207;  // Pre-calculated factor
```

### Current Calculation

```c
// QNHCK2-16: 1V = 6A, 5V = 30A
// After voltage divider: 3.3V max = 30A
float current_amps = adc_voltage * (30.0 / 3.3);
```

### Sampling Strategy

- Average 16-64 ADC readings per sample to reduce noise
- Sample current clamps at 10-100 Hz for AC current monitoring
- DS18B20: Read every 30-60 seconds (slow thermal response)
- SHT40: Read every 60 seconds
- Thermocouple: Read every 5-10 seconds for critical applications

### Power Management

- Use WiFi sleep modes between transmissions
- Deep sleep option: wake every 30-60 seconds
- Watchdog timer for reliability (especially for engine monitoring)

### MQTT Topic Structure

```text
boat/sensors/{location}/{sensor_type}

Examples:
boat/sensors/engine_room/temperature
boat/sensors/engine_room/wet_exhaust_temp
boat/sensors/galley/fridge_temp
boat/sensors/salon/humidity
boat/sensors/battery_bank/current_1
```

### Safety Features

- MQTT "last will" message for offline detection
- Local buzzer/LED alarm for critical sensors (optional)
- Threshold alerts for high-temperature sensors
- Watchdog timer to auto-recover from crashes

## Assembly Notes

1. **SMD components first:** ESP32, SHT40, MAX31855, op-amps
2. **Through-hole components:** Connectors, buttons, LEDs
3. **Power supply module:** If using LM2596 module, socket or solder last
4. **Testing sequence:**
   - Verify 3.3V output before installing ESP32
   - Test I2C communication with SHT40
   - Test each 1-Wire bus independently
   - Test SPI communication with MAX31855
   - Calibrate ADC channels with known voltage source
5. **Conformal coating:** After full testing, apply to bottom of board only (avoid connectors)

## Testing & Calibration

### Power Supply Test

1. Apply 12V, verify 3.3V ±0.1V
2. Load test: Verify stable voltage at 350mA draw
3. Test reverse polarity protection (with current-limited supply)

### Sensor Tests

1. **SHT40:** Compare readings with reference thermometer/hygrometer
2. **DS18B20:** Ice bath (0°C) and boiling water (100°C) verification
3. **MAX31855:** Ice bath and known temperature reference
4. **Current clamps:** Use known resistive load and multimeter

### ADC Calibration

1. Apply known voltages (0V, 1.65V, 3.3V) to ADC inputs
2. Record raw ADC values
3. Calculate calibration factors
4. Store in firmware or NVRAM

## Troubleshooting

### Power Issues

- No 3.3V output: Check D1 orientation, buck converter enable pin
- Unstable voltage: Add more bulk capacitance (C1, C2)
- Overheating: Check load current, add heatsink to buck converter

### Communication Issues

- I2C not working: Verify pullup resistors, check SDA/SCL connections
- 1-Wire not detecting: Check pullup resistor, verify GPIO configuration
- SPI errors: Verify clock polarity, check CS signal

### ADC Issues

- Readings stuck at max: Voltage divider error, check R1/R2 values
- Noisy readings: Add more filtering, check ground connections
- Incorrect values: Calibrate with known voltage source

### WiFi Issues

- Won't connect: Check antenna, verify 2.4GHz band support
- Frequent disconnects: Improve antenna placement, check power supply stability
- Weak signal: Consider external antenna option (if board supports it)

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-14 | Initial design document |

## License

This design is open-source hardware. Please specify your preferred license (e.g., MIT, Apache 2.0, CERN-OHL).

## Support & Contact

- GitHub Repository: [Your repo URL here]
- Issues: [Your issues URL here]
- Discussions: [Your discussions URL here]

---

**Safety Warning:** This board is designed for 12V automotive/marine applications. Ensure proper fusing and circuit protection in your installation. High-temperature sensors should be installed per manufacturer specifications. This design has not been certified for safety-critical applications.
