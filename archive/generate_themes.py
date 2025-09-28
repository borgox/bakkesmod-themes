"""
Theme generator for the first themes ever created by me.
Used only once to quickly set up light/dark versions of themes.
Will not be used again.
"""

import json
import os
import shutil

# Define the theme mappings and their characteristics
themes = {
    'cyberpunk': {
        'base': 'cybperpunk.json',
        'is_dark': True,
        'description': 'A futuristic neon theme with cyberpunk highlights',
        'accent_colors': {'r': 0.8, 'g': 0.2, 'b': 1.0}  # Pink/purple neon
    },
    'nyanpastel': {
        'base': 'nyanpastel.json', 
        'is_dark': False,
        'description': 'A soft pastel theme inspired by Nyan Cat',
        'accent_colors': {'r': 0.85, 'g': 0.55, 'b': 0.7}  # Pastel pink
    },
    'overcast': {
        'base': 'overcast.json',
        'is_dark': True,
        'description': 'Very minimal dark theme',
        'accent_colors': {'r': 0.5, 'g': 0.5, 'b': 0.5}  # Neutral gray
    },
    'retrowave': {
        'base': 'retrowave.json',
        'is_dark': True,
        'description': '80s-inspired vaporwave theme with pink, purple, and turquoise',
        'accent_colors': {'r': 1.0, 'g': 0.3, 'b': 0.8}  # Hot pink
    },
    'frostbyte': {
        'base': 'frostbyte.json',
        'is_dark': True,
        'description': 'Cold ice-inspired theme with blue and white tones',
        'accent_colors': {'r': 0.3, 'g': 0.7, 'b': 1.0}  # Ice blue
    },
    'neonpulse': {
        'base': 'neonpulse.json',
        'is_dark': True,  
        'description': 'High-contrast neon theme with purple and cyan accents',
        'accent_colors': {'r': 0.5, 'g': 0.9, 'b': 1.0}  # Cyan
    },
    'nyanrgb': {
        'base': 'nyanrgb.json',
        'is_dark': True,
        'description': 'RGB theme inspired by Nyan Cat meme',
        'accent_colors': {'r': 1.0, 'g': 0.5, 'b': 0.8}  # Rainbow pink
    },
    'solarflare': {
        'base': 'solarflare.json',
        'is_dark': True,
        'description': 'Fiery theme with warm orange and yellow tones inspired by the sun',
        'accent_colors': {'r': 1.0, 'g': 0.6, 'b': 0.2}  # Solar orange
    },
    'visibility': {
        'base': 'visibility.json',
        'is_dark': True,
        'description': 'Accessibility focused theme with high contrast',
        'accent_colors': {'r': 1.0, 'g': 1.0, 'b': 0.2}  # High contrast yellow
    }
}

def invert_color_value(value, is_background=False):
    """Invert color values for light/dark conversion"""
    if is_background:
        # For background colors, invert more dramatically
        return 1.0 - value if value < 0.5 else max(0.85, 1.0 - value)
    else:
        # For other colors, softer inversion
        return 1.0 - value

def create_complementary_theme(base_theme_data, theme_name, theme_info):
    """Create light version of dark theme or dark version of light theme"""
    new_theme = json.loads(json.dumps(base_theme_data))  # Deep copy
    
    is_base_dark = theme_info['is_dark']
    variant_name = f"{theme_name.title()} Light" if is_base_dark else f"{theme_name.title()}"
    variant_description = f"A {'light' if is_base_dark else 'dark'} version of the {theme_name} theme"
    
    # Update metadata for new theme
    new_theme['metadata']['name'] = variant_name
    new_theme['metadata']['description'] = variant_description
    
    # Get accent colors for this theme
    accent = theme_info['accent_colors']
    
    # Transform colors based on whether we're making light or dark version
    for color_key, color_data in new_theme['imgui'].items():
        if 'WindowBg' in color_key or 'ChildBg' in color_key or 'PopupBg' in color_key or 'MenuBarBg' in color_key:
            # Background colors - invert dramatically
            if is_base_dark:  # Making light version
                color_data['r'] = min(0.95, 0.9 + color_data['r'] * 0.1)
                color_data['g'] = min(0.95, 0.9 + color_data['g'] * 0.1) 
                color_data['b'] = min(0.95, 0.9 + color_data['b'] * 0.1)
            else:  # Making dark version
                color_data['r'] = max(0.05, color_data['r'] * 0.1)
                color_data['g'] = max(0.05, color_data['g'] * 0.1)
                color_data['b'] = max(0.05, color_data['b'] * 0.1)
        
        elif 'Text' in color_key and 'Selected' not in color_key:
            # Text colors - invert for readability
            if is_base_dark:  # Making light version
                color_data['r'] = max(0.1, 1.0 - color_data['r'])
                color_data['g'] = max(0.1, 1.0 - color_data['g'])
                color_data['b'] = max(0.1, 1.0 - color_data['b'])
            else:  # Making dark version  
                color_data['r'] = min(0.9, 1.0 - color_data['r'])
                color_data['g'] = min(0.9, 1.0 - color_data['g'])
                color_data['b'] = min(0.9, 1.0 - color_data['b'])
        
        elif 'Button' in color_key or 'Header' in color_key or 'Tab' in color_key and 'Active' not in color_key:
            # Interactive elements - use theme accent colors
            if is_base_dark:  # Making light version
                color_data['r'] = min(0.9, accent['r'] * 0.8 + 0.1)
                color_data['g'] = min(0.9, accent['g'] * 0.8 + 0.1)
                color_data['b'] = min(0.9, accent['b'] * 0.8 + 0.1)
            else:  # Making dark version
                color_data['r'] = max(0.1, accent['r'] * 0.6)
                color_data['g'] = max(0.1, accent['g'] * 0.6)
                color_data['b'] = max(0.1, accent['b'] * 0.6)
    
    return new_theme

def process_all_themes():
    """Process all themes and create light/dark variants"""
    base_path = "."
    themes_path = os.path.join(base_path, "themes")
    
    for theme_name, theme_info in themes.items():
        print(f"Processing {theme_name}...")
        
        # Read base theme
        base_file = os.path.join(base_path, theme_info['base'])
        if not os.path.exists(base_file):
            print(f"Warning: {base_file} not found, skipping...")
            continue
            
        with open(base_file, 'r') as f:
            base_theme_data = json.load(f)
        
        # Create theme folder
        theme_folder = os.path.join(themes_path, theme_name)
        os.makedirs(theme_folder, exist_ok=True)
        
        # Save original theme with proper name
        original_name = f"{theme_name}.json"
        original_path = os.path.join(theme_folder, original_name)
        with open(original_path, 'w') as f:
            json.dump(base_theme_data, f, indent=2)
        
        # Create complementary version
        complementary_theme = create_complementary_theme(base_theme_data, theme_name, theme_info)
        complement_name = f"{theme_name}_light.json" if theme_info['is_dark'] else f"{theme_name}_dark.json"
        complement_path = os.path.join(theme_folder, complement_name)
        
        with open(complement_path, 'w') as f:
            json.dump(complementary_theme, f, indent=2)
        
        print(f"Created {original_name} and {complement_name}")

if __name__ == "__main__":
    process_all_themes()
    print("Theme processing complete!")