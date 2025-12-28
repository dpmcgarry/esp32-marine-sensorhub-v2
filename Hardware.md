# ESP32-C6 Marine Multi-Sensor Board

## Overview

A unified sensor board for marine applications featuring temperature, humidity,
current monitoring, and high-temperature sensing capabilities. Designed for
reliable operation in harsh marine environments with 12VDC power input.

## Features

- **Onboard Sensors:**
  - SHT40 temperature & humidity sensor (±0.2°C accuracy)

- **External Sensor Support:**
  - Multiple DS18B20 1-Wire temperature sensors on shared bus (-67°F to +257°F)
  - 3x K-type thermocouples via MAX31855 (up to 2000°F each)
  - 5x QNHCK2-16 30A current clamp sensors (6th channel reserved)

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
| -------- | ----------- | ----- |
| I2C SDA (SHT40) | GPIO6 | 4.7kΩ pullup |
| I2C SCL (SHT40) | GPIO7 | 4.7kΩ pullup |
| RGB LED | GPIO8 | WS2812B (matches DevKitC) |
| 1-Wire (DS18B20) | GPIO10 | 4.7kΩ pullup, multi-drop bus |
| SPI SCK (MAX31855) | GPIO19 | Shared by all 3 MAX31855 |
| SPI MISO (MAX31855) | GPIO18 | Shared by all 3 MAX31855 |
| SPI CS MAX31855 #1 | GPIO20 | Thermocouple 1 |
| SPI CS MAX31855 #2 | GPIO21 | Thermocouple 2 |
| SPI CS MAX31855 #3 | GPIO22 | Thermocouple 3 |
| ADC Clamp #1 | GPIO0 (ADC1_CH0) | |
| ADC Clamp #2 | GPIO1 (ADC1_CH1) | |
| ADC Clamp #3 | GPIO2 (ADC1_CH2) | |
| ADC Clamp #4 | GPIO3 (ADC1_CH3) | |
| ADC Clamp #5 | GPIO4 (ADC1_CH4) | |
| Reserved (Clamp #6) | GPIO5 (ADC1_CH5) | Future expansion |
| Status LED | GPIO23 | 330Ω resistor |
| Boot Button | GPIO9 | 10kΩ pullup |

## Schematic

### Power Supply Circuit

```text
12V_IN (J_MAIN Pin 1, from 11-pin consolidated screw terminal)
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

GND ─── Common ground (J_MAIN Pin 2)
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

Multiple sensors share a single 1-Wire bus on GPIO10.
Connectors via J_MAIN (Pins 3-11, supporting 3 sensors):

```text
J_MAIN Pinout for DS18B20 Sensors:
  Sensor 1: Pin 3 (3.3V), Pin 4 (DATA), Pin 5 (GND)
  Sensor 2: Pin 6 (3.3V), Pin 7 (DATA), Pin 8 (GND)
  Sensor 3: Pin 9 (3.3V), Pin 10 (DATA), Pin 11 (GND)

Notes:
- Single 4.7kΩ pullup resistor on GPIO10
- All DATA pins (4, 7, 10) connected together to GPIO10 (shared 1-Wire bus)
- All GND pins (5, 8, 11) connected together
- Can use 5V instead of 3.3V for long cable runs
- Each sensor has a unique 64-bit address
- Max recommended cable length: 100 feet
- Supports up to 10-20 sensors on one bus
```

### MAX31855 Thermocouple Interface (3× ICs for 3 thermocouples)

The design uses three MAX31855 ICs (U4, U7, U8) sharing a common SPI bus
with individual chip select lines:

```text
MAX31855 #1 (U4) - Thermocouple 1
├── VCC: 3.3V_MAIN
├── GND: GND
├── SCK: GPIO19 (shared SPI clock)
├── SO: GPIO18 (shared SPI MISO)
├── CS: GPIO20 (dedicated chip select)
├── T+: K-type thermocouple + (J_TC Pin 1)
├── T-: K-type thermocouple - (J_TC Pin 2)
└── Decoupling: C_TC1 (0.1µF ceramic capacitor)

MAX31855 #2 (U7) - Thermocouple 2
├── VCC: 3.3V_MAIN
├── GND: GND
├── SCK: GPIO19 (shared SPI clock)
├── SO: GPIO18 (shared SPI MISO)
├── CS: GPIO21 (dedicated chip select)
├── T+: K-type thermocouple + (J_TC Pin 3)
├── T-: K-type thermocouple - (J_TC Pin 4)
└── Decoupling: C_TC2 (0.1µF ceramic capacitor)

MAX31855 #3 (U8) - Thermocouple 3
├── VCC: 3.3V_MAIN
├── GND: GND
├── SCK: GPIO19 (shared SPI clock)
├── SO: GPIO18 (shared SPI MISO)
├── CS: GPIO22 (dedicated chip select)
├── T+: K-type thermocouple + (J_TC Pin 5)
├── T-: K-type thermocouple - (J_TC Pin 6)
└── Decoupling: C_TC3 (0.1µF ceramic capacitor)

SPI Bus Configuration:
- All three MAX31855 share SCK (GPIO19) and MISO (GPIO18)
- Each has its own CS line (GPIO20, GPIO21, GPIO22)
- Software selects which IC to read by pulling its CS line low
- Temperature range: -270°C to +1372°C (-454°F to +2501°F)
- Resolution: 0.25°C (14-bit)
- Cold junction compensation included

PCB Notes:
- Keep thermocouple traces short and symmetrical
- Route away from noisy digital signals
- Consider copper pour ground plane around all MAX31855 ICs
- Place decoupling caps close to VCC pins
```

### Current Clamp Signal Conditioning (5 channels + 1 reserved)

QNHCK2-16 outputs 0-5V, but ESP32 ADC maximum is 3.3V.

**Per channel circuit:**

```text
CLAMP_x_IN (J_CLAMP consolidated 10-pin connector)
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
  └── U5/U6 (MCP6004 buffer) ──────┘
        │
        └── ESP32 ADC (GPIO0-4)

MCP6004 Configuration (Unity Gain Buffer):
  +IN: from RC filter
  -IN: connected to OUT (feedback)
  OUT: to ESP32 ADC
  VDD: 3.3V_MAIN
  VSS: GND
  Decoupling: 0.1µF ceramic

Two MCP6004 ICs required for 5 channels + 1 reserved:

- U5A: Clamp 1 → GPIO0 (ADC1_CH0)
- U5B: Clamp 2 → GPIO1 (ADC1_CH1)
- U5C: Clamp 3 → GPIO2 (ADC1_CH2)
- U5D: Clamp 4 → GPIO3 (ADC1_CH3)
- U6A: Clamp 5 → GPIO4 (ADC1_CH4)
- U6B: Reserved for Clamp 6 → GPIO5 (ADC1_CH5) - future expansion
- U6C, U6D: Unused
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
| --------- | ----------- | ----------- | --- | ---------- | -------- |
| U2 | ESP32-C6-WROOM-1 | WiFi 6 module | 1 | $2.50 | $2.50 |
| U3 | SHT40 | Temp/humidity sensor | 1 | $4.00 | $4.00 |
| U4, U7, U8 | MAX31855 | Thermocouple amplifier | 3 | $5.00 | $15.00 |
| U5, U6 | MCP6004 | Quad op-amp | 2 | $0.50 | $1.00 |
| U1 | LM2596 module | Buck converter 12V→3.3V | 1 | $2.00 | $2.00 |

### Protection & Power

| Reference | Part Number | Description | Qty | Unit Price | Extended |
| --------- | ----------- | ----------- | --- | ---------- | -------- |
| D1 | MBRS340 | Schottky diode 3A 40V | 1 | $0.30 | $0.30 |
| TVS1 | SMBJ15A | TVS diode 15V | 1 | $0.40 | $0.40 |
| C1 | - | 100µF 25V electrolytic | 1 | $0.15 | $0.15 |
| C2 | - | 100µF 10V electrolytic | 1 | $0.10 | $0.10 |
| C3 | - | 10µF ceramic | 1 | $0.10 | $0.10 |

### Passives (approximate quantities)

| Type | Value | Description | Qty | Unit Price | Extended |
| ---- | ----- | ----------- | --- | ---------- | -------- |
| Resistors | 4.7kΩ | I2C & 1-Wire pullups | 3 | $0.02 | $0.06 |
| Resistors | 10kΩ | Voltage dividers, pullups | 9 | $0.02 | $0.18 |
| Resistors | 20kΩ | Voltage dividers | 5 | $0.02 | $0.10 |
| Resistors | 1kΩ | Current limiting, filters | 12 | $0.02 | $0.24 |
| Resistors | 330Ω | LED/RGB current limiting | 2 | $0.02 | $0.04 |
| Capacitors | 0.1µF | Decoupling, filtering | 15 | $0.05 | $0.75 |

### Connectors

| Reference | Type | Description | Qty | Unit Price | Extended |
| --------- | ---- | ----------- | --- | ---------- | -------- |
| J_MAIN | Screw terminal | 11-pin, 5mm pitch, power + DS18B20 | 1 | $0.90 | $0.90 |
| J_TC | Screw terminal | 6-pin, 5mm pitch, thermocouples | 1 | $0.60 | $0.60 |
| J_CLAMP | Screw terminal | 10-pin, 5mm pitch, current clamps | 1 | $0.85 | $0.85 |
| J_USB | USB-C receptacle | 16-pin, USB 2.0 | 1 | $0.50 | $0.50 |

### Miscellaneous

| Item | Description | Qty | Unit Price | Extended |
| ---- | ----------- | --- | ---------- | -------- |
| LEDs | Status indicators | 2 | $0.10 | $0.20 |
| Buttons | Tactile switches (reset, boot) | 2 | $0.10 | $0.20 |
| PCB | 2-layer, ~80×60mm | 1 | $2.50 | $2.50 |

### **Total Board Cost: ~$32.85**

### External Sensors (purchased separately)

| Item | Part Number | Description | Unit Price |
| ---- | ----------- | ----------- | ---------- |
| DS18B20 | DS18B20 | Waterproof probe, 1m cable | $2-4 |
| Thermocouple | K-type | Stainless probe, 1-2m | $5-15 |
| Current clamp | QNHCK2-16 | 30A, 0-5V output | $8-12 |

## Connectors Pinout Reference

### J_MAIN - Main Power & DS18B20 Connector (11-pin Screw Terminal, 5mm pitch)

Consolidated connector for 12V power input and three DS18B20 1-Wire sensors:

```text
Pin 1:  +12V (power input)
Pin 2:  GND (power ground)
Pin 3:  +3.3V (DS18B20 sensor 1)
Pin 4:  DATA (DS18B20 sensor 1 → GPIO10, 4.7kΩ pullup)
Pin 5:  GND (DS18B20 sensor 1)
Pin 6:  +3.3V (DS18B20 sensor 2)
Pin 7:  DATA (DS18B20 sensor 2 → GPIO10, shared bus)
Pin 8:  GND (DS18B20 sensor 2)
Pin 9:  +3.3V (DS18B20 sensor 3)
Pin 10: DATA (DS18B20 sensor 3 → GPIO10, shared bus)
Pin 11: GND (DS18B20 sensor 3)

Notes:
- All DATA pins (4, 7, 10) connected together to GPIO10 with single 4.7kΩ pullup
- Can use +5V instead of +3.3V for long cable runs (pins 3, 6, 9)
- All GND pins (2, 5, 8, 11) connected together
```

### J_TC - Thermocouple Connector (6-pin Screw Terminal, 5mm pitch)

Consolidated connector for three K-type thermocouples:

```text
Pin 1: TC1_T+ (Thermocouple 1 +, Yellow) → MAX31855 #1 (U4) → GPIO20 (CS)
Pin 2: TC1_T- (Thermocouple 1 -, Red)
Pin 3: TC2_T+ (Thermocouple 2 +, Yellow) → MAX31855 #2 (U7) → GPIO21 (CS)
Pin 4: TC2_T- (Thermocouple 2 -, Red)
Pin 5: TC3_T+ (Thermocouple 3 +, Yellow) → MAX31855 #3 (U8) → GPIO22 (CS)
Pin 6: TC3_T- (Thermocouple 3 -, Red)

Temperature Range: -270°C to +1372°C (-454°F to +2501°F)
Resolution: 0.25°C (14-bit) with cold junction compensation
```

### J_CLAMP - Current Clamp Connector (10-pin Screw Terminal, 5mm pitch)

Consolidated connector for five QNHCK2-16 current clamps:

```text
Pin 1:  CLAMP1_SIG (0-5V) → Conditioning → GPIO0 (ADC1_CH0)
Pin 2:  CLAMP1_GND
Pin 3:  CLAMP2_SIG (0-5V) → Conditioning → GPIO1 (ADC1_CH1)
Pin 4:  CLAMP2_GND
Pin 5:  CLAMP3_SIG (0-5V) → Conditioning → GPIO2 (ADC1_CH2)
Pin 6:  CLAMP3_GND
Pin 7:  CLAMP4_SIG (0-5V) → Conditioning → GPIO3 (ADC1_CH3)
Pin 8:  CLAMP4_GND
Pin 9:  CLAMP5_SIG (0-5V) → Conditioning → GPIO4 (ADC1_CH4)
Pin 10: CLAMP5_GND

Signal conditioning: voltage divider → RC filter → MCP6004 buffer → ESP32 ADC
Note: GPIO5 (ADC1_CH5) reserved for 6th clamp expansion
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
5. **Conformal coating:** After full testing, apply to bottom of board only
   (avoid connectors)

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

| Version | Date       | Changes                 |
| ------- | ---------- | ----------------------- |
| 1.0     | 2024-12-14 | Initial design document |

## License

This design is open-source hardware. Please specify your preferred license
(e.g., MIT, Apache 2.0, CERN-OHL).

## Support & Contact

- GitHub Repository: [Your repo URL here]
- Issues: [Your issues URL here]
- Discussions: [Your discussions URL here]

---

**Safety Warning:** This board is designed for 12V automotive/marine
applications. Ensure proper fusing and circuit protection in your installation.
High-temperature sensors should be installed per manufacturer specifications.
This design has not been certified for safety-critical applications.
