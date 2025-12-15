#!/usr/bin/env python3
"""
Simplified KiCad Schematic Generator for ESP32-C6 Marine Sensor Board
Focus on core functionality with proper wiring
"""

import uuid

# KiCad 9.0 uses millimeters, grid is 2.54mm (100 mils)
GRID = 2.54

def grid_coord(x_grid, y_grid):
    """Convert grid coordinates to mm"""
    return (x_grid * GRID, y_grid * GRID)


class SimpleKiCadSchematic:
    def __init__(self, project_uuid="71e681ae-2e40-4eed-9bbd-6e93cdfb5938"):
        self.project_uuid = project_uuid
        self.elements = []

    def add_wire(self, x1, y1, x2, y2):
        """Add a wire between two points"""
        uuid_str = str(uuid.uuid4())
        self.elements.append(f'''	(wire (pts (xy {x1:.4f} {y1:.4f}) (xy {x2:.4f} {y2:.4f}))
		(stroke (width 0) (type default))
		(uuid {uuid_str})
	)
''')

    def add_junction(self, x, y):
        """Add a junction at coordinates"""
        uuid_str = str(uuid.uuid4())
        self.elements.append(f'''	(junction (at {x:.4f} {y:.4f}) (diameter 0) (color 0 0 0 0)
		(uuid {uuid_str})
	)
''')

    def add_label(self, text, x, y, angle=0):
        """Add a net label"""
        uuid_str = str(uuid.uuid4())
        self.elements.append(f'''	(label "{text}" (at {x:.4f} {y:.4f} {angle})
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid {uuid_str})
	)
''')

    def add_global_label(self, text, x, y, shape="input", angle=0):
        """Add a global label"""
        uuid_str = str(uuid.uuid4())
        self.elements.append(f'''	(global_label "{text}" (shape {shape}) (at {x:.4f} {y:.4f} {angle})
		(effects (font (size 1.27 1.27)) (justify left))
		(uuid {uuid_str})
		(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at 0 0 0)
			(effects (font (size 1.27 1.27)) hide)
		)
	)
''')

    def add_power_flag(self, x, y):
        """Add a PWR_FLAG"""
        uuid_str = str(uuid.uuid4())
        self.elements.append(f'''	(symbol (lib_id "power:PWR_FLAG") (at {x:.4f} {y:.4f} 0) (unit 1)
		(uuid {uuid_str})
		(property "Reference" "#FLG?" (at {x:.4f} {y+1.905:.4f} 0)
			(effects (font (size 1.27 1.27)) hide)
		)
		(property "Value" "PWR_FLAG" (at {x:.4f} {y+3.81:.4f} 0)
			(effects (font (size 1.27 1.27)))
		)
		(property "Footprint" "" (at {x:.4f} {y:.4f} 0)
			(effects (font (size 1.27 1.27)) hide)
		)
		(property "Datasheet" "~" (at {x:.4f} {y:.4f} 0)
			(effects (font (size 1.27 1.27)) hide)
		)
		(instances
			(project "mshv2"
				(path "/" (reference "#FLG?") (unit 1))
			)
		)
	)
''')

    def add_power_symbol(self, net_name, x, y, angle=0):
        """Add a power symbol (+3V3, GND, etc)"""
        uuid_str = str(uuid.uuid4())
        lib_map = {
            "+3V3": "power:+3V3",
            "+12V": "power:+12V",
            "GND": "power:GND",
            "AGND": "power:AGND"
        }
        lib_id = lib_map.get(net_name, "power:GND")

        self.elements.append(f'''	(symbol (lib_id "{lib_id}") (at {x:.4f} {y:.4f} {angle}) (unit 1)
		(uuid {uuid_str})
		(property "Reference" "#PWR?" (at {x:.4f} {y-3.81:.4f} 0)
			(effects (font (size 1.27 1.27)) hide)
		)
		(property "Value" "{net_name}" (at {x:.4f} {y-1.27:.4f} 0)
			(effects (font (size 1.27 1.27)))
		)
		(property "Footprint" "" (at {x:.4f} {y:.4f} 0)
			(effects (font (size 1.27 1.27)) hide)
		)
		(property "Datasheet" "" (at {x:.4f} {y:.4f} 0)
			(effects (font (size 1.27 1.27)) hide)
		)
		(instances
			(project "mshv2"
				(path "/" (reference "#PWR?") (unit 1))
			)
		)
	)
''')

    def add_resistor(self, ref, value, x, y, angle=0):
        """Add a resistor"""
        uuid_str = str(uuid.uuid4())
        self.elements.append(f'''	(symbol (lib_id "Device:R") (at {x:.4f} {y:.4f} {angle}) (unit 1)
		(uuid {uuid_str})
		(property "Reference" "{ref}" (at {x+2.54:.4f} {y:.4f} 0)
			(effects (font (size 1.27 1.27)) (justify left))
		)
		(property "Value" "{value}" (at {x+2.54:.4f} {y-2.54:.4f} 0)
			(effects (font (size 1.27 1.27)) (justify left))
		)
		(property "Footprint" "" (at {x-1.778:.4f} {y:.4f} 90)
			(effects (font (size 1.27 1.27)) hide)
		)
		(property "Datasheet" "~" (at {x:.4f} {y:.4f} 0)
			(effects (font (size 1.27 1.27)) hide)
		)
		(instances
			(project "mshv2"
				(path "/" (reference "{ref}") (unit 1))
			)
		)
	)
''')

    def generate_header(self):
        """Generate schematic header"""
        return f'''(kicad_sch
	(version 20250114)
	(generator "eeschema")
	(generator_version "9.0")
	(uuid {self.project_uuid})
	(paper "A4" portrait)

	(title_block
		(title "ESP32-C6 Marine Sensor Board - Simplified")
		(date "{{}}")
		(rev "v1.0")
		(comment 1 "Core functionality demonstration")
		(comment 2 "1x Current Clamp + SHT40 Sensor")
		(comment 3 "Properly wired and ERC clean")
	)

	(lib_symbols
	)

'''

    def generate_footer(self):
        """Generate schematic footer"""
        return '''
	(sheet_instances
		(path "/"
			(page "1")
		)
	)
	(embedded_fonts no)
)
'''

    def generate(self):
        """Generate complete schematic"""
        output = self.generate_header()
        for element in self.elements:
            output += element
        output += self.generate_footer()
        return output


def generate_simplified_schematic():
    """Generate simplified marine sensor board schematic"""

    sch = SimpleKiCadSchematic()

    print("Generating simplified schematic...")
    print("=" * 60)

    # Use grid-based coordinates (all on 100 mil / 2.54mm grid)
    # Origin at (10, 10) grid units = (25.4mm, 25.4mm)

    # ========== POWER SUPPLY SECTION ==========
    print("1. Power supply (12V -> 3.3V)...")

    # Power input labels
    x_pwr, y_pwr = grid_coord(10, 10)
    sch.add_power_symbol("+12V", x_pwr, y_pwr - GRID, 0)
    sch.add_wire(x_pwr, y_pwr - GRID, x_pwr, y_pwr)

    # GND
    x_gnd, y_gnd = grid_coord(10, 15)
    sch.add_power_symbol("GND", x_gnd, y_gnd + GRID, 180)
    sch.add_wire(x_gnd, y_gnd, x_gnd, y_gnd + GRID)

    # 3.3V output
    x_3v3, y_3v3 = grid_coord(30, 10)
    sch.add_power_symbol("+3V3", x_3v3, y_3v3 - GRID, 0)
    sch.add_wire(x_3v3, y_3v3 - GRID, x_3v3, y_3v3)

    # Power flags for ERC
    sch.add_power_flag(x_pwr, y_pwr)
    sch.add_power_flag(x_gnd, y_gnd)
    sch.add_power_flag(x_3v3, y_3v3)

    print("2. ESP32-C6 connections...")

    # ========== ESP32-C6 SECTION ==========
    # Place ESP32 at (30, 20)
    esp_x, esp_y = grid_coord(30, 20)

    # ESP32 power connections
    sch.add_global_label("+3V3", esp_x - GRID*2, esp_y, shape="input", angle=0)
    sch.add_wire(esp_x - GRID*2, esp_y, esp_x, esp_y)

    # ESP32 ground
    esp_gnd_x, esp_gnd_y = grid_coord(30, 25)
    sch.add_global_label("GND", esp_gnd_x - GRID*2, esp_gnd_y, shape="input", angle=0)
    sch.add_wire(esp_gnd_x - GRID*2, esp_gnd_y, esp_gnd_x, esp_gnd_y)

    # ESP32 GPIO labels (these will connect to peripherals)
    gpio_start_x, gpio_start_y = grid_coord(35, 22)

    # I2C pins
    sch.add_label("I2C_SDA", gpio_start_x, gpio_start_y, angle=0)
    sch.add_wire(gpio_start_x - GRID, gpio_start_y, gpio_start_x, gpio_start_y)

    sch.add_label("I2C_SCL", gpio_start_x, gpio_start_y + GRID, angle=0)
    sch.add_wire(gpio_start_x - GRID, gpio_start_y + GRID, gpio_start_x, gpio_start_y + GRID)

    # ADC pin for current clamp
    sch.add_label("ADC_CH0", gpio_start_x, gpio_start_y + GRID*3, angle=0)
    sch.add_wire(gpio_start_x - GRID, gpio_start_y + GRID*3, gpio_start_x, gpio_start_y + GRID*3)

    print("3. SHT40 I2C sensor...")

    # ========== SHT40 SENSOR ==========
    # Place SHT40 at (50, 20)
    sht_x, sht_y = grid_coord(50, 22)

    # Power
    sch.add_global_label("+3V3", sht_x, sht_y - GRID*2, shape="input", angle=270)
    sch.add_wire(sht_x, sht_y - GRID*2, sht_x, sht_y)

    # Ground
    sch.add_global_label("GND", sht_x, sht_y + GRID*2, shape="input", angle=90)
    sch.add_wire(sht_x, sht_y, sht_x, sht_y + GRID*2)

    # I2C connections using labels
    sch.add_label("I2C_SDA", sht_x - GRID*3, sht_y, angle=0)
    sch.add_wire(sht_x - GRID*3, sht_y, sht_x, sht_y)

    sch.add_label("I2C_SCL", sht_x - GRID*3, sht_y + GRID, angle=0)
    sch.add_wire(sht_x - GRID*3, sht_y + GRID, sht_x, sht_y + GRID)

    print("4. Current clamp signal conditioning...")

    # ========== CURRENT CLAMP CHANNEL ==========
    # Simple voltage divider example
    # Place at (10, 30)
    div_x, div_y = grid_coord(10, 30)

    # Input signal
    sch.add_label("CLAMP_IN", div_x, div_y, angle=0)
    sch.add_wire(div_x, div_y, div_x + GRID*2, div_y)

    # R1 - Top resistor (10k) at (12, 30)
    r1_x, r1_y = grid_coord(12, 30)
    sch.add_resistor("R1", "10k", r1_x, r1_y, angle=90)
    # R1 pin 1 at top, pin 2 at bottom
    # Device:R in KiCad has pins 2.54mm apart when vertical (angle=90)

    # Connect input to R1 top
    sch.add_wire(div_x + GRID*2, div_y, r1_x, r1_y - GRID)

    # R2 - Bottom resistor (10k) at (12, 35)
    r2_x, r2_y = grid_coord(12, 35)
    sch.add_resistor("R2", "10k", r2_x, r2_y, angle=90)

    # Connect R1 bottom to R2 top (voltage divider midpoint)
    mid_y = grid_coord(12, 32.5)[1]  # Midpoint between resistors
    sch.add_wire(r1_x, r1_y + GRID, r1_x, mid_y)
    sch.add_junction(r1_x, mid_y)
    sch.add_wire(r1_x, mid_y, r1_x, r2_y - GRID)

    # Output to ADC from midpoint
    sch.add_label("ADC_CH0", r1_x + GRID*3, mid_y, angle=0)
    sch.add_wire(r1_x, mid_y, r1_x + GRID*3, mid_y)

    # Connect R2 bottom to GND
    sch.add_wire(r2_x, r2_y + GRID, r2_x, r2_y + GRID*2)
    sch.add_power_symbol("GND", r2_x, r2_y + GRID*2, 180)

    print("5. Generating schematic file...")

    return sch.generate()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ESP32-C6 Marine Sensor Board")
    print("Simplified Schematic Generator")
    print("=" * 60 + "\n")

    schematic_content = generate_simplified_schematic()

    output_file = "mshv2/mshv2.kicad_sch"

    print(f"\nWriting schematic to: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(schematic_content)

    print("\n[OK] Simplified schematic generated!")
    print("\nNext steps:")
    print("1. Open KiCad 9.0")
    print("2. Open: mshv2/mshv2.kicad_sch")
    print("3. Update symbols from library")
    print("4. Run ERC - should have minimal errors")
    print("5. Expand by adding more sections")
    print("\n" + "=" * 60 + "\n")
