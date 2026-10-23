import matplotlib.pyplot as plt
import matplotlib.patches as patches

import profileData

def munsell_to_hex(munsell_str):
    munsell_map = {
        # Add munsell colors here if needed 
        '10YR 2/1': '#211C18',
        '10YR 2/2': '#32251A',
        '10YR 3/1': '#463D35',
        '10YR 3/2': '#4A3B2C',
        '10YR 3/3': '#533E2B',
        '10YR 3/4': '#62411B',
        '10YR 3/6': '#73430C',
        '10YR 4/2': '#695A4B',
        '10YR 4/3': '#6D563D',
        '10YR 4/4': '#77572E',
        '10YR 4/6': '#8A581A',
        '10YR 5/3': '#8B7761',
        '10YR 5/4': '#93744B',
        '10YR 5/6': '#A27129',
        '7.5YR 2.5/1': '#2B2420',
        '7.5YR 2.5/2': '#362A22',
        '7.5YR 3/2': '#4E3827',
    }
    cleaned = munsell_str.strip().upper().replace('YR', 'YR ')
    cleaned = " ".join(cleaned.split())
    return munsell_map.get(cleaned, '#4A3B2C')

def generate_soil_profile(title, horizons, output_filename):
    fig, ax = plt.subplots(figsize=(10, 9), dpi=300)
    
    max_depth = max(h["bottom"] for h in horizons)
    
    box_left = 1.8
    box_width = 3.5
    box_right = box_left + box_width
    
    ax.set_xlim(0, 11.0)
    ax.set_ylim(max_depth + 10, -15)
    ax.axis('off')
    
    # Title
    ax.text(box_left + box_width/2, -8, title, 
            fontsize=22, fontweight='bold', family='serif', ha='center', va='center')
    
    drawn_depths = set()
    
    for h in horizons:
        top = h["top"]
        bottom = h["bottom"]
        height = bottom - top
        
        color_val = h["color"]
        if not color_val.startswith("#"):
            color_val = munsell_to_hex(color_val)
            
        # Draw horizon block
        rect = patches.Rectangle(
            (box_left, top), box_width, height,
            linewidth=1.5, edgecolor='white', facecolor=color_val
        )
        ax.add_patch(rect)
        
        # Horizon designation label in center of block
        ax.text(box_left + box_width/2, top + height/2, h["horizon"],
                color='white', fontsize=16, fontweight='bold',
                ha='center', va='center')
        
        # Depth labels on left
        for depth in (top, bottom):
            if depth not in drawn_depths:
                depth_str = "150+ CM" if depth == 181 and h["name"] == "C" else f"{depth} CM"
                ax.text(box_left - 0.3, depth, depth_str,
                        fontsize=9.5, fontweight='bold', ha='right', va='center')
                drawn_depths.add(depth)
                
        # Description text on right
        desc_lines = h.get("description", [])
        if desc_lines:
            desc_text = "\n".join(desc_lines)
            ax.text(box_right + 0.3, top + height/2, desc_text,
                    fontsize=14, fontweight='normal', ha='left', va='center', linespacing=1.25)
            
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved soil profile to {output_filename}")


# Run generator for each profile
generate_soil_profile("Site 1", profileData.profile_data, "p1.png")