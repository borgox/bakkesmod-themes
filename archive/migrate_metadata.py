"""
This was used to add the auto generated flag to all themes
Will not ever be used again.
"""

import json
import glob
import os

def add_autogen_flags():
    """Add auto-generated flag to non-light variant themes"""

    # Grab all JSON themes
    all_themes = glob.glob('themes/*/*.json')

    # Keep only those that are NOT *_light.json
    normal_themes = [t for t in all_themes if not t.endswith('_light.json')]

    for theme_path in normal_themes:
        print(f"Adding auto-generated flag to {theme_path}")
        
        with open(theme_path, 'r') as f:
            theme = json.load(f)
        
        # Add auto-generated metadata
        theme['metadata']['auto_generated'] = False
        theme['metadata']['note'] = "No note specified."
        with open(theme_path, 'w') as f:
            json.dump(theme, f, indent=2)
    
    print("✅ Added auto-generated flags to all non-light themes!")

if __name__ == "__main__":
    add_autogen_flags()