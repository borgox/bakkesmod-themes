import json
import os

# Define all the fixes
fixes = {
    'themes/neonpulse/neonpulse_light.json': {
        'ImGuiCol_Text': {"a": 1, "r": 0.05, "g": 0.05, "b": 0.1},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.4, "g": 0.4, "b": 0.5},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.98, "g": 0.98, "b": 0.95}
    },
    'themes/nyanpastel/nyanpastel.json': {
        'ImGuiCol_Text': {"a": 1, "r": 0.9, "g": 0.9, "b": 0.85},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.6, "g": 0.6, "b": 0.55},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.08, "g": 0.08, "b": 0.09}
    },
    'themes/nyanpastel/nyanpastel_light.json': {
        # Already good, keep existing values
    },
    'themes/nyanrgb/nyanrgb.json': {
        'ImGuiCol_Text': {"a": 1, "r": 1.0, "g": 1.0, "b": 1.0},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.7, "g": 0.7, "b": 0.7},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.05, "g": 0.05, "b": 0.05}
    },
    'themes/nyanrgb/nyanrgb_light.json': {
        'ImGuiCol_Text': {"a": 1, "r": 0.1, "g": 0.1, "b": 0.1},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.5, "g": 0.5, "b": 0.5},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.95, "g": 0.95, "b": 0.95}
    },
    'themes/retrowave/retrowave.json': {
        'ImGuiCol_Text': {"a": 1, "r": 0.95, "g": 0.85, "b": 0.95},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.6, "g": 0.5, "b": 0.6},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.06, "g": 0.02, "b": 0.12}
    },
    'themes/retrowave/retrowave_light.json': {
        'ImGuiCol_Text': {"a": 1, "r": 0.1, "g": 0.05, "b": 0.15},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.4, "g": 0.3, "b": 0.5},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.98, "g": 0.95, "b": 0.98}
    },
    'themes/solarflare/solarflare.json': {
        'ImGuiCol_Text': {"a": 1, "r": 1.0, "g": 0.9, "b": 0.8},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.6, "g": 0.5, "b": 0.4},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.08, "g": 0.03, "b": 0.0}
    },
    'themes/solarflare/solarflare_light.json': {
        'ImGuiCol_Text': {"a": 1, "r": 0.15, "g": 0.1, "b": 0.05},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.5, "g": 0.4, "b": 0.3},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.98, "g": 0.96, "b": 0.94}
    },
    'themes/frostbyte/frostbyte.json': {
        'ImGuiCol_Text': {"a": 1, "r": 0.9, "g": 0.95, "b": 1.0},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.5, "g": 0.6, "b": 0.7},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.03, "g": 0.07, "b": 0.12}
    },
    'themes/frostbyte/frostbyte_light.json': {
        'ImGuiCol_Text': {"a": 1, "r": 0.05, "g": 0.1, "b": 0.2},
        'ImGuiCol_TextDisabled': {"a": 1, "r": 0.3, "g": 0.4, "b": 0.5},
        'ImGuiCol_ChildBg': {"a": 1, "r": 0.96, "g": 0.98, "b": 1.0}
    }
}

def apply_fixes():
    for theme_path, theme_fixes in fixes.items():
        if not theme_fixes:  # Skip empty fixes
            continue
            
        print(f"Fixing {theme_path}...")
        
        try:
            with open(theme_path, 'r') as f:
                theme = json.load(f)
            
            # Apply fixes
            for color_key, color_value in theme_fixes.items():
                if color_key in theme['imgui']:
                    theme['imgui'][color_key] = color_value
                    print(f"  Updated {color_key}")
            
            with open(theme_path, 'w') as f:
                json.dump(theme, f, indent=2)
                
            print(f"  ✅ Fixed {theme_path}")
            
        except Exception as e:
            print(f"  ❌ Error fixing {theme_path}: {e}")

if __name__ == "__main__":
    apply_fixes()
    print("🎉 All console text visibility fixes applied!")