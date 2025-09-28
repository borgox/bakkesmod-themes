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
                    'theme_folder': os.path.basename(theme_folder_path)
                })
            except Exception as e:
                print(f"Error reading {file}: {e}")
    
    return themes

def generate_readme():
    """Generate README.md with theme information and downloads"""
    
    readme_content = f"""# 🎨 BakkesMod Theme Collection

A curated collection of custom themes for BakkesMod, featuring various color schemes from dark cyberpunk aesthetics to light pastel designs. Each theme comes in both light and dark variants for maximum customization.

*Generated on {datetime.now().strftime('%B %d, %Y')}*

## 📦 Quick Installation

1. **Download** your desired theme(s) from the links below
2. **Copy** the `.json` file to your BakkesMod themes directory:
   ```
   %APPDATA%\\bakkesmod\\bakkesmod\\data\\themes\\
   ```
3. **Restart** BakkesMod or reload themes
4. **Select** your theme from the BakkesMod interface

## 🎭 Available Themes

Each theme includes both **light** and **dark** variants. Click the download links below to get the `.json` files directly.

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
        
        readme_content += f"""### 🌟 {main_theme['name'].replace(' Dark', '').replace(' Light', '')}

**Author:** {main_theme['author']}  
**Description:** {main_theme['description']}

| Variant | Preview | Download |
|---------|---------|----------|
"""
        
        # Add each variant
        for theme in sorted(theme_info, key=lambda x: x['variant']):
            variant_emoji = "🌙" if theme['variant'] == 'dark' else "☀️"
            variant_name = theme['variant'].title()
            
            readme_content += f"""| {variant_emoji} **{variant_name}** | ![{theme['name']}](themes/{theme['theme_folder']}/{theme['image']}) | [`{theme['filename']}`](themes/{theme['theme_folder']}/{theme['filename']}) |
"""
        
        readme_content += "\n"
    
    # Add footer with additional information
    readme_content += f"""---

## 🛠️ Theme Development

### Creating Custom Themes

Each theme follows the standard BakkesMod theme format:

```json
{{
  "metadata": {{
    "name": "Your Theme Name",
    "author": "Your Name",
    "version": "1.0",
    "description": "Theme description"
  }},
  "imgui": {{
    "ImGuiCol_WindowBg": {{ "r": 0.1, "g": 0.1, "b": 0.1, "a": 1.0 }},
    // ... other color definitions
  }}
}}
```

### Generating Previews

Preview images are automatically generated using the `create_previews.py` script:

```bash
python create_previews.py
```

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
4. **Generate** preview images using our script
5. **Submit** a pull request with clear description

### Contribution Guidelines

- Follow the established folder structure: `/themes/themename/`
- Include both `.json` theme file and `.png` preview
- Provide both light and dark variants when possible
- Use descriptive theme names and clear descriptions
- Test themes extensively before submitting

## 📋 Requirements

- **BakkesMod** (latest version recommended)
- **Rocket League** (Steam/Epic Games)

## 🐛 Issues & Support

Having problems with a theme? 

1. Check that the theme file is in the correct directory
2. Ensure BakkesMod is updated to the latest version
3. Try restarting BakkesMod/Rocket League
4. Create an issue in this repository with details

## 📄 License

This collection is open source. Individual themes may have different licenses - check each theme's metadata for specific author information.

## 🙏 Credits

- **@borgox | @borghettoo** - Theme development and collection curation
- **bakkesmod.com** - Platform and default themes
- **Community contributors** - Additional themes and feedback

---

*Made with ❤️ for the BakkesMod community*

**Total Themes:** {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))])} themes × 2 variants = {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))]) * 2} total theme files
"""

    # Write README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README.md generated successfully!")
    print(f"Found {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))])} themes")

if __name__ == "__main__":
    generate_readme()