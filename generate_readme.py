import json
import os
from datetime import datetime

def get_theme_info(theme_folder_path):
    """Extract theme information from JSON files"""
    themes = []
    
    for file in os.listdir(theme_folder_path):
        if file.endswith('.json'):
            file_path = os.path.join(theme_folder_path, file)
            try:
                with open(file_path, 'r') as f:
                    theme_data = json.load(f)
                
                theme_name = file.replace('.json', '')
                variant = 'dark'
                if 'light' in theme_name.lower():
                    variant = 'light'
                
                themes.append({
                    'name': theme_data['metadata']['name'],
                    'filename': file,
                    'image': file.replace('.json', '.png'),
                    'author': theme_data['metadata']['author'],
                    'description': theme_data['metadata'].get('description', ''),
                    'variant': variant,
                    'theme_folder': os.path.basename(theme_folder_path),
                    'auto_generated': theme_data['metadata'].get('auto_generated', False)
                })
            except Exception as e:
                print(f"Error reading {file}: {e}")
    
    return themes

def generate_readme():
    """Generate README.md with theme information and downloads"""
    
    readme_content = f"""# 🎨 BakkesMod Theme Collection

A curated collection of custom themes for BakkesMod, featuring various color schemes from dark cyberpunk aesthetics to light pastel designs.

*Generated on {datetime.now().strftime('%B %d, %Y')}*

## 📦 Quick Installation

1. **Download** your desired theme(s) from the links below
2. **Copy** the `.json` file to your BakkesMod themes directory:
   ```
   %APPDATA%\\bakkesmod\\bakkesmod\\data\\themes\\
   ```
3. **Apply** the theme by opening console (F6) and typing:
   ```
   theme_load [theme_name]
   ```
   For themes in subfolders (like this collection):
   ```
   theme_load /themes/cyberpunk/cyberpunk_light
   ```

## 🎭 Available Themes

Each theme may include both light and dark variants. Click the download links below to get the `.json` files directly.

"""

    themes_path = "themes"
    
    # Process each theme folder
    for theme_folder in sorted(os.listdir(themes_path)):
        folder_path = os.path.join(themes_path, theme_folder)
        if not os.path.isdir(folder_path):
            continue
        
        theme_info = get_theme_info(folder_path)
        if not theme_info:
            continue
        
        # Get the main theme info (usually the dark version)
        main_theme = next((t for t in theme_info if t['variant'] == 'dark'), theme_info[0])
        
        readme_content += f"""## 🌟 {main_theme['name'].replace(' Dark', '').replace(' Light', '')}

**Author:** {main_theme['author']}  
**Description:** {main_theme['description']}

"""
        
        # Add each variant with your requested format
        for theme in sorted(theme_info, key=lambda x: x['variant']):
            variant_emoji = "🌙" if theme['variant'] == 'dark' else "☀️"
            variant_name = theme['variant'].title()
            
            autogen_note = ""
            if theme['auto_generated']:
                autogen_note = " *(Auto-generated - may need adjustments)*"
            
            readme_content += f"""### {variant_emoji} **{variant_name}** | <a href="themes/{theme['theme_folder']}/{theme['filename']}" target="_blank">`{theme['filename']}`</a>{autogen_note}

![{theme['name']}](themes/{theme['theme_folder']}/{theme['image']})

----

"""
        
        readme_content += "\n--------------\n\n"
    
    # Add footer with updated information
    readme_content += f"""## 🛠️ Theme Development

### Creating Custom Themes

Each theme follows this standard theme format:

```json
{{
  // Added metadata that bakkesmod doesn't care about
  "metadata": {{
    "name": "Your Theme Name",
    "author": "Your Name", 
    "version": "1.0",
    "description": "Theme description"
  }},
  "imgui": {{ // Bakkesmod ImGUI theme config
    "ImGuiCol_WindowBg": {{ "r": 0.1, "g": 0.1, "b": 0.1, "a": 1.0 }},
    // ... other color definitions
  }}
}}
```

You can use <a href="defaults/default.json" target="_blank">`/defaults/default.json`</a> as a base for your theme.

## 🎯 Theme Categories

### 🌙 Dark Themes
Perfect for users who prefer darker interfaces with minimal eye strain during long gaming sessions.

### ☀️ Light Themes  
Bright, clean themes for users who prefer lighter color schemes and better visibility in bright environments.

### 🎨 Colorful Themes
Bold, vibrant themes with distinctive color palettes and unique visual flair.

### ♿ Accessibility
High contrast themes designed for better visibility and accessibility compliance.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** this repository
2. **Create** your theme following our format
3. **Test** thoroughly with BakkesMod
4. **Capture** a preview screenshot of your theme in action
5. **Update** the README.md with your theme information
6. **Submit** a pull request with clear description

### Contribution Guidelines

- Follow the established folder structure: `/themes/themename/`
- Include both `.json` theme file and `.png` preview
- Provide both light and dark variants when possible
- Use descriptive theme names and clear descriptions
- Test themes extensively before submitting
- Update README.md with your theme details before submitting

## 📋 Requirements

- **BakkesMod** (latest version recommended)
- **Rocket League** (Steam/Epic Games)

## 🐛 Issues & Support

Having problems with a theme? 

1. Check that the theme file is in the correct directory
2. Ensure BakkesMod is updated to the latest version
3. Try restarting BakkesMod/Rocket League
4. Use console command: `theme_load [theme_name]`
5. Create an issue in this repository with details

## 📄 License

This collection is open source. Individual themes may have different licenses - check each theme's metadata for specific author information.

## 🙏 Credits

- **<a href="https://github.com/borgox" target="_blank">borgox</a> | <a href="https://discord.com/users/@borghettoo" target="_blank">@borghettoo</a>** - Theme development and collection curation
- **bakkesmod.com** - Platform and default themes

---

*Made with ❤️ for the BakkesMod community*

**Total Themes:** {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))])} themes with variants
"""

    # Write README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README.md generated successfully!")
    print(f"Found {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))])} themes")

if __name__ == "__main__":
    generate_readme()