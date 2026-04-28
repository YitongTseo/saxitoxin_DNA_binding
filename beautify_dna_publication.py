#!/usr/bin/env python
"""
Publication-Standard DNA-Ligand PyMOL Script
Uses PyMOL's built-in nucleic acid representation modes
"""

from pymol import cmd, stored

# meridian_green
def beautify_dna_ligand(dna_color="brick_red"):
    """
    Create publication-quality DNA-ligand visualization

    Args:
        dna_color (str): "light_purple", "brick_red", "ruddy_orange", "meridian_green"
    """
    print("🧬✨ PUBLICATION-STANDARD DNA-LIGAND VISUALIZATION")
    print("=" * 60)

    # Define custom colors in PyMOL
    cmd.set_color("light_purple", [0.694, 0.612, 0.851])
    cmd.set_color("brick_red", [0.698, 0.133, 0.133])
    cmd.set_color("ruddy_orange", [1.0, 0.388, 0.278])
    cmd.set_color("meridian_green", [0.133, 0.545, 0.133])

    valid_colors = ["light_purple", "brick_red", "ruddy_orange", "meridian_green"]
    if dna_color not in valid_colors:
        dna_color = "light_purple"

    print(f"🎨 Using DNA color: {dna_color}")

    # Get all objects
    objects = cmd.get_object_list()
    if not objects:
        print("❌ No structures loaded!")
        return

    all_atoms = " or ".join(objects)

    # Beautiful scene setup
    cmd.bg_color("white")
    cmd.set("depth_cue", 0)
    cmd.set("ray_trace_mode", 1)
    cmd.set("antialias", 2)
    cmd.hide("everything")

    # ====================================
    # PUBLICATION-STANDARD DNA
    # ====================================
    cmd.select("dna", "resn DA+DT+DG+DC+A+T+G+C+U")

    if cmd.count_atoms("dna") > 0:
        print("🧬 Styling DNA with publication standards...")

        # Show DNA as cartoon (this is the standard)
        cmd.show("cartoon", "dna")
        cmd.color(dna_color, "dna")

        # PUBLICATION-QUALITY NUCLEIC ACID SETTINGS
        # Apply settings to the specific DNA selection

        # Mode 4: Shows bases as simple plates between backbone strands
        cmd.set("cartoon_nucleic_acid_mode", 4, "dna")

        # Ring mode 2: Clean, simple base representation
        cmd.set("cartoon_ring_mode", 2, "dna")

        # Ladder mode 2: Beautiful rungs between strands
        cmd.set("cartoon_ladder_mode", 2, "dna")

        # Enhanced settings for publication quality
        cmd.set("cartoon_ring_finder", 2, "dna")           # Better ring detection
        cmd.set("cartoon_tube_radius", 1.2, "dna")         # Visible backbone
        cmd.set("cartoon_ring_width", 0.3, "dna")          # Base thickness
        cmd.set("cartoon_smooth_loops", 1, "dna")          # Smooth curves
        cmd.set("cartoon_flat_sheets", 0, "dna")           # No flattening

        print("  ✅ DNA backbone: Professional cartoon representation")
        print("  ✅ DNA bases: Clean plates (publication standard)")

    # ====================================
    # LIGAND DETECTION AND STYLING (FIXED FOR SAX)
    # ====================================

    # Comprehensive ligand selection including SAX (saxitoxin)
    cmd.select("ligands", f"({all_atoms}) and not (dna or resn HOH+WAT+SOL or polymer.protein)")

    # Add specific ligand residues that might be missed
    cmd.select("ligands", "ligands or resn SAX+STX+SXN+ATP+ADP+GTP+GDP+NAD+FAD+COA+HEM")

    # Also try organic molecules
    cmd.select("ligands", "ligands or organic")

    # Debug: check what we found
    ligand_count = cmd.count_atoms("ligands")
    print(f"🔍 Ligand detection: {ligand_count} atoms found")

    if ligand_count > 0:
        print(f"⚗️ Styling {ligand_count} ligand atoms...")

        # Beautiful ligand representation (from working improved script)
        cmd.show("sticks", "ligands")
        cmd.show("spheres", "ligands")

        # CPK coloring for ligands (classic molecular colors)
        cmd.color("gray50", "ligands and elem C")    # Carbon = gray
        cmd.color("red", "ligands and elem O")       # Oxygen = red
        cmd.color("blue", "ligands and elem N")      # Nitrogen = blue
        cmd.color("yellow", "ligands and elem S")    # Sulfur = yellow
        cmd.color("orange", "ligands and elem P")    # Phosphorus = orange
        cmd.color("white", "ligands and elem H")     # Hydrogen = white

        # Beautiful sizing (same as working version)
        cmd.set("stick_radius", 0.25, "ligands")
        cmd.set("sphere_scale", 0.3, "ligands")
        cmd.set("sphere_transparency", 0.1, "ligands")

        print("  ✅ Ligands: CPK colored sticks + spheres (like normal molecules)")

        # Show what ligand we found
        cmd.iterate("ligands", "print(f'  Found: {resn} (residue {resi})')")

    else:
        print("❌ No ligands detected - trying manual SAX selection...")
        cmd.select("ligands", "resn SAX")
        ligand_count = cmd.count_atoms("ligands")

        if ligand_count > 0:
            print(f"✅ Found SAX manually: {ligand_count} atoms")
            # Apply same styling as above
            cmd.show("sticks", "ligands")
            cmd.show("spheres", "ligands")
            cmd.color("gray50", "ligands and elem C")
            cmd.color("red", "ligands and elem O")
            cmd.color("blue", "ligands and elem N")
            cmd.color("yellow", "ligands and elem S")
            cmd.color("orange", "ligands and elem P")
            cmd.color("white", "ligands and elem H")
            cmd.set("stick_radius", 0.25, "ligands")
            cmd.set("sphere_scale", 0.3, "ligands")
            cmd.set("sphere_transparency", 0.1, "ligands")
        else:
            print("❌ Still no ligands found")

    # ====================================
    # CLEAN INTERACTIONS
    # ====================================
    if cmd.count_atoms("dna") > 0 and cmd.count_atoms("ligands") > 0:
        print("🤝 Adding clean hydrogen bonds...")

        # Hydrogen bonds
        cmd.distance("hydrogen_bonds",
                    "dna and (elem N or elem O)",
                    "ligands and (elem N or elem O)",
                    cutoff=3.5, mode=2)

        # Clean hydrogen bond styling
        cmd.set("dash_color", "yellow", "hydrogen_bonds")
        cmd.set("dash_width", 3.0, "hydrogen_bonds")
        cmd.set("dash_gap", 0.15, "hydrogen_bonds")
        cmd.set("dash_length", 0.6, "hydrogen_bonds")

        # Remove all distance labels
        cmd.hide("labels", "hydrogen_bonds")
        cmd.set("label_size", 0, "hydrogen_bonds")

        print("  ✅ Hydrogen bonds: Clean yellow dashes (no numbers)")

    # ====================================
    # PUBLICATION VIEW SETUP
    # ====================================
    if cmd.count_atoms("ligands") > 0:
        cmd.zoom("ligands", buffer=8)
    elif cmd.count_atoms("dna") > 0:
        cmd.zoom("dna", buffer=8)

    # Standard publication angle
    cmd.turn("x", -15)
    cmd.turn("y", 25)
    cmd.turn("z", 5)

    # Publication-quality rendering
    cmd.set("ray_shadows", "on")
    cmd.set("ambient", 0.15)
    cmd.set("direct", 0.7)
    cmd.set("reflect", 0.1)
    cmd.set("shininess", 30)

    print("\n✨ PUBLICATION-READY VISUALIZATION COMPLETE!")
    print("\n📚 Standard Publication Features:")
    print("  🧬 DNA: Cartoon representation with base plates")
    print("  ⚗️ Ligands: CPK colored sticks + spheres")
    print("  💛 Interactions: Clean yellow hydrogen bonds")
    print("  📸 Publication-quality rendering settings")

# Alternative DNA representation modes
def dna_mode_simple():
    """Ultra-simple DNA representation"""
    cmd.select("dna", "resn DA+DT+DG+DC+A+T+G+C+U")
    cmd.set("cartoon_nucleic_acid_mode", 0, "dna")  # Simple tube
    print("🧬 DNA mode: Simple tube")

def dna_mode_ladder():
    """DNA with visible base pairs"""
    cmd.select("dna", "resn DA+DT+DG+DC+A+T+G+C+U")
    cmd.set("cartoon_nucleic_acid_mode", 1, "dna")  # Ladder
    print("🧬 DNA mode: Ladder with base pairs")

def dna_mode_plates():
    """DNA with base plates (publication standard)"""
    cmd.select("dna", "resn DA+DT+DG+DC+A+T+G+C+U")
    cmd.set("cartoon_nucleic_acid_mode", 4, "dna")  # Plates
    print("🧬 DNA mode: Base plates (publication standard)")

def take_picture(filename="dna_ligand", width=1600, height=1200, dpi=300):
    """
    Take a high-quality publication picture

    Args:
        filename (str): Output filename (without extension)
        width (int): Image width in pixels
        height (int): Image height in pixels
        dpi (int): DPI for print quality
    """
    print(f"📸 Taking high-quality picture: {filename}")

    # Set up for best quality
    cmd.set("ray_shadows", "on")
    cmd.set("ambient", 0.15)
    cmd.set("direct", 0.7)
    cmd.set("antialias", 3)
    cmd.set("ray_trace_mode", 1)

    # Render and save
    cmd.ray(width, height)
    cmd.png(f"{filename}.png", dpi=dpi)

    print(f"✅ Picture saved: {filename}.png ({width}x{height}, {dpi} DPI)")
    print("📁 Perfect for publications!")

def quick_picture():
    """Take a quick picture with standard settings"""
    take_picture("dna_ligand_quick", 1200, 900, 300)

def publication_picture():
    """Take a high-resolution publication picture"""
    take_picture("dna_ligand_publication", 2400, 1800, 300)

def poster_picture():
    """Take a very high-resolution picture for posters"""
    take_picture("dna_ligand_poster", 3600, 2700, 300)

def find_ligands():
    """Helper function to manually find and select ligands"""
    print("🔍 Searching for ligands in current structure...")

    # Show all non-DNA, non-water residues
    cmd.select("temp_selection", "not (polymer.nucleic or resn HOH+WAT+SOL)")

    if cmd.count_atoms("temp_selection") > 0:
        print("📋 Non-DNA/water residues found:")
        cmd.iterate("temp_selection", "print(f'  - {resn} {resi}')")
        print("💡 To select manually: select ligands, resn YOUR_LIGAND_NAME")
    else:
        print("❌ No potential ligands found")

    cmd.delete("temp_selection")

# Register commands - fixed
try:
    cmd.extend("beautify", beautify_dna_ligand)
    cmd.extend("dna_simple", dna_mode_simple)
    cmd.extend("dna_ladder", dna_mode_ladder)
    cmd.extend("dna_plates", dna_mode_plates)
    cmd.extend("take_picture", take_picture)
    cmd.extend("quick_pic", quick_picture)
    cmd.extend("publication_pic", publication_picture)
    cmd.extend("poster_pic", poster_picture)
    cmd.extend("find_ligands", find_ligands)
    print("✅ All commands registered successfully")
except Exception as e:
    print(f"❌ Command registration error: {e}")

print("\n🚀 Publication-Standard DNA Visualization Loaded!")
print("\n⌨️ Visualization Commands:")
print("  beautify()              - Publication-quality DNA + ligand")
print("  beautify('brick_red')   - With different DNA color")
print("  dna_simple()            - Simple DNA tube")
print("  dna_ladder()            - DNA with base pair ladder")
print("  dna_plates()            - DNA with base plates (standard)")
print("  find_ligands()          - Help find ligands if missing")

print("\n📸 Photography Commands:")
print("  quick_pic()             - Quick picture (1200x900)")
print("  publication_pic()       - High-res for papers (2400x1800)")
print("  poster_pic()            - Ultra high-res for posters (3600x2700)")
print("  take_picture('name')    - Custom picture with filename")

print("\n🎯 Applying publication-standard visualization...")
try:
    beautify_dna_ligand(dna_color="brick_red")
except Exception as e:
    print(f"❌ Auto-beautify error: {e}")
    print("💡 Try running: beautify() manually")