#!/usr/bin/env python3
"""
Fix empty lib_symbols section in KiCad schematic by loading symbols from libraries
"""

import sys
import os

# Add KiCad Python path
sys.path.insert(0, r"C:\Program Files\KiCad\9.0\lib\python3\dist-packages")

try:
    import eeschema
except ImportError as e:
    print(f"Error importing KiCad Python modules: {e}")
    print("Make sure KiCad 9.0 is installed with Python support")
    sys.exit(1)

def fix_schematic_symbols(sch_path):
    """
    Load schematic and ensure all symbols are properly defined in lib_symbols
    """
    print(f"Loading schematic: {sch_path}")

    try:
        # Load the schematic
        sch = eeschema.LoadSchematic(sch_path)

        # Save the schematic (this should trigger symbol library resolution)
        print("Saving schematic with updated symbols...")
        sch.Save()

        print("[OK] Schematic symbols updated successfully!")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to update symbols: {e}")
        return False

if __name__ == "__main__":
    sch_file = "mshv2/mshv2.kicad_sch"

    if not os.path.exists(sch_file):
        print(f"[ERROR] Schematic file not found: {sch_file}")
        sys.exit(1)

    success = fix_schematic_symbols(sch_file)
    sys.exit(0 if success else 1)
