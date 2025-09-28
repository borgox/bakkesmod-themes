import json
import os
from datetime import datetime

def get_theme_info(theme_folder_path):
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
    
    for theme_folder in sorted(os.listdir(themes_path)):
        folder_path = os.path.join(themes_path, theme_folder)
        if not os.path.isdir(folder_path):
            continue
        
        theme_info = get_theme_info(folder_path)
        if not theme_info:
            continue
        
        main_theme = next((t for t in theme_info if t['variant'] == 'dark'), theme_info[0])
        
        readme_content += f"""## 🌟 {main_theme['name'].replace(' Dark', '').replace(' Light', '')}

**Author:** {main_theme['author']}  
**Description:** {main_theme['description']}

"""
        
        for theme in sorted(theme_info, key=lambda x: x['variant']):
            variant_emoji = "🌙" if theme['variant'] == 'dark' else "☀️"
            variant_name = theme['variant'].title()
            
            autogen_note = ""
            if theme['auto_generated']:
                autogen_note = " *(Auto-generated - may need adjustments)*"
            
            readme_content += f"""### {variant_emoji} **{variant_name}** | [`{theme['filename']}`](themes/{theme['theme_folder']}/{theme['filename']}){autogen_note}

![{theme['name']}](themes/{theme['theme_folder']}/{theme['image']})

----

"""
        
        readme_content += "\n--------------\n\n"
    
    readme_content += f"""## 🛠️ Theme Development

### Creating Custom Themes

Each theme follows this standard theme format:

```json
{{
  "metadata": {{
    "name": "Your Theme Name",
    "author": "Your Name", 
    "version": "1.0",
    "description": "Theme description"
  }},
  "imgui": {{
    "ImGuiCol_WindowBg": {{ "r": 0.1, "g": 0.1, "b": 0.1, "a": 1.0 }}
  }}
}}
```

You can use either one of:
- [`/defaults/template/template.json`](defaults/template/template.json) 
- [`/defaults/template/template_light.json`](defaults/template/template_light.json)
as a base for your theme.
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
5. **Generate** a new README.md with [this script](generate_readme.py)
6. **Submit** a pull request with clear description

### Contribution Guidelines

- Follow the established folder structure: `/themes/themename/`
- Include both `.json` theme file and `.png` preview
- Provide both light and dark variants when possible
- Use descriptive theme names and clear descriptions
- Test themes extensively before submitting
- Generate an updated README using the provided script

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

- **[borgox](https://github.com/borgox) | [@borghettoo](https://discord.com/users/@borghettoo)** - Theme development and collection curation
- **bakkesmod.com** - Platform and default themes

---

*Made with ❤️ for the BakkesMod community*

**Total Themes:** {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))])} themes with variants
"""

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README.md generated successfully!")
    print(f"Found {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))])} themes")

if __name__ == "__main__":
    generate_readme()