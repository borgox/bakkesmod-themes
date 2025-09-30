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

A curated collection of custom themes for BakkesMod, featuring various color schemes from dark cyberpunk aesthetics to light pastel designs, plus a powerful random theme generator!

*Generated on {datetime.now().strftime('%B %d, %Y')}*

## 🎲 Random Theme Generator

**NEW!** Generate infinite unique themes with our advanced randomizer:

```bash
python theme_randomizer.py
```

### Features:
- 🎯 **Variant-aware randomization** - Dark themes stay dark, light themes stay light (99% accuracy)
- 🖼️ **Automatic preview generation** - See exactly how your theme looks before applying
- � **Optimized transparency** - Windows stay visible and usable (95% opaque guarantee)
- 🏗️ **Complete theme structure** - Full metadata, proper folder organization
- 🔄 **Unique IDs** - No duplicate theme names

Each generated theme includes:
- `random_XXXX.json` / `random_XXXX_light.json` - Theme files
- `random_XXXX.png` / `random_XXXX_light.png` - Preview images

<details>
<summary>�📦 Installation Instructions</summary>

### Quick Installation

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

### 🔄 Making Themes Persistent

To make your theme persist between BakkesMod reloads:

1. **Open** your BakkesMod config file:
   ```
   %APPDATA%\\bakkesmod\\bakkesmod\\cfg\\config.cfg
   ```
2. **Find** the line containing `bakkesmod_style_theme`
3. **Edit** the line to point to your desired theme:
   ```
   bakkesmod_style_theme "themes/solarflare/solarflare.json" //Theme to use
   ```
   Or for themes in the root themes directory:
   ```
   bakkesmod_style_theme "/solarflare.json" //Theme to use
   ```

**Note:** The path defaults from `%APPDATA%\\bakkesmod\\bakkesmod\\data\\themes\\` and a `.json` file path must be provided.

</details>

## 🎭 Available Themes

Each theme may include both light and dark variants. **Click to expand** any theme to see preview images and download links:

"""

    themes_path = "themes"
    
    # Separate regular themes from random themes
    regular_themes = []
    random_themes = []
    
    for theme_folder in sorted(os.listdir(themes_path)):
        folder_path = os.path.join(themes_path, theme_folder)
        if not os.path.isdir(folder_path):
            continue
        
        theme_info = get_theme_info(folder_path)
        if not theme_info:
            continue
        
        if theme_folder.startswith('random_'):
            random_themes.extend(theme_info)
        else:
            regular_themes.append((theme_folder, theme_info))
    
    # Regular Themes Section
    for theme_folder, theme_info in regular_themes:
        main_theme = next((t for t in theme_info if t['variant'] == 'dark'), theme_info[0])
        
        clean_name = main_theme['name'].replace(' Dark', '').replace(' Light', '')
        
        # Smart emoji selection based on theme name and category
        name_lower = clean_name.lower()
        category = main_theme.get('category', '').lower()
        
        if "cyber" in name_lower or category == 'cyberpunk':
            theme_emoji = "🤖"
        elif "space" in name_lower or "cosmic" in name_lower or category == 'space':
            theme_emoji = "�"
        elif "neon" in name_lower or "pulse" in name_lower or category == 'neon':
            theme_emoji = "⚡"
        elif "retro" in name_lower or "wave" in name_lower or category == 'retro':
            theme_emoji = "📼"
        elif "pastel" in name_lower or category == 'pastel':
            theme_emoji = "🌸"
        elif "natural" in name_lower or "nature" in name_lower or category == 'nature':
            theme_emoji = "🌿"
        elif "nyan" in name_lower or "kurumi" in name_lower or category == 'anime':
            theme_emoji = "�"
        elif "mono" in name_lower or "blue" in name_lower or category == 'monochrome':
            theme_emoji = "⚫"
        elif "solar" in name_lower or "fire" in name_lower or "flare" in name_lower or category == 'fire':
            theme_emoji = "🔥"
        elif "dark" in name_lower and "mode" in name_lower:
            theme_emoji = "🌑"
        elif "glitch" in name_lower:
            theme_emoji = "📺"
        elif "frost" in name_lower:
            theme_emoji = "❄️"
        else:
            theme_emoji = "🎨"
        
        readme_content += f"""<details>
<summary>{theme_emoji} <strong>{clean_name}</strong> - {main_theme['description']}</summary>

**Author:** {main_theme['author']}

"""
        
        for theme in sorted(theme_info, key=lambda x: x['variant']):
            variant_emoji = "🌙" if theme['variant'] == 'dark' else "☀️"
            variant_name = theme['variant'].title()
            
            autogen_note = ""
            if theme['auto_generated']:
                autogen_note = " *(Auto-generated - may need adjustments)*"
            
            readme_content += f"""#### {variant_emoji} **{variant_name} Variant** | [`{theme['filename']}`](themes/{theme['theme_folder']}/{theme['filename']}){autogen_note}

![{theme['name']}](themes/{theme['theme_folder']}/{theme['image']})

"""
        
        readme_content += "</details>\n\n"
    
    # Random Themes Section (if any exist)
    if random_themes:
        readme_content += f"""<details>
<summary>🎲 <strong>Generated Random Themes</strong> ({len(set(t['theme_folder'] for t in random_themes))} themes) - Click to expand</summary>

*These themes were generated using the random theme generator. Each offers unique color combinations!*

"""
        
        # Group random themes by folder
        random_by_folder = {}
        for theme in random_themes:
            folder = theme['theme_folder']
            if folder not in random_by_folder:
                random_by_folder[folder] = []
            random_by_folder[folder].append(theme)
        
        for folder, themes in sorted(random_by_folder.items()):
            theme_id = folder.replace('random_', '')
            main_theme = next((t for t in themes if t['variant'] == 'dark'), themes[0])
            
            readme_content += f"""### 🎲 Random Theme {theme_id}

**Author:** {main_theme['author']}  
**Generated:** Auto-generated theme with unique color combinations

"""
            
            for theme in sorted(themes, key=lambda x: x['variant']):
                variant_emoji = "🌙" if theme['variant'] == 'dark' else "☀️"
                variant_name = theme['variant'].title()
                
                readme_content += f"""#### {variant_emoji} **{variant_name}** | [`{theme['filename']}`](themes/{theme['theme_folder']}/{theme['filename']})

<img src="themes/{theme['theme_folder']}/{theme['image']}" width="400" alt="{theme['name']}">

"""
        
        readme_content += "</details>\n\n"
    
    readme_content += f"""<details>
<summary>🛠️ <strong>Theme Development Guide</strong> - Click to expand</summary>

## Quick Start - Create Your First Theme

### 🚀 Method 1: Interactive Theme Creator (Recommended)

```bash
python init_theme.py
```

The interactive creator will guide you through:
- **Theme naming** and folder setup
- **Metadata collection** (author, description, category)
- **Variant selection** (dark, light, or both)
- **Template integration** with proper JSON structure
- **Next steps guidance** for customization

### 🎲 Method 2: Random Theme Generator

```bash
python theme_randomizer.py
```

Generate unique themes instantly with:
- **Variant-aware randomization**: 99% accuracy in maintaining dark/light characteristics
- **Smart transparency**: Background windows stay 85-100% opaque
- **Automatic previews**: See exactly how your theme looks
- **Complete structure**: Full metadata and proper organization

### 🛠️ Method 3: Manual Creation

Each theme follows this standard format:

```json
{{
  "metadata": {{
    "name": "Your Theme Name",
    "author": "Your Name", 
    "version": "1.0",
    "description": "Theme description",
    "category": "dark"
  }},
  "imgui": {{
    "ImGuiCol_WindowBg": {{ "r": 0.1, "g": 0.1, "b": 0.1, "a": 1.0 }}
  }}
}}
```

### Templates Available:
- [`/defaults/template/template.json`](defaults/template/template.json) - Dark theme base
- [`/defaults/template/template_light.json`](defaults/template/template_light.json) - Light theme base

### Color Customization Tips:

- **RGBA Values**: Red, Green, Blue, Alpha (transparency) from 0.0 to 1.0
- **Dark Themes**: Keep backgrounds below 0.3 for comfort
- **Light Themes**: Keep backgrounds above 0.7 for visibility
- **Text Colors**: Ensure high contrast with backgrounds
- **Alpha Channel**: Keep windows mostly opaque (0.85-1.0) for usability

</details>

<details>
<summary>🎯 <strong>Theme Categories</strong> - Click to expand</summary>

### 🌙 Dark Themes
Perfect for users who prefer darker interfaces with minimal eye strain during long gaming sessions.

### ☀️ Light Themes  
Bright, clean themes for users who prefer lighter color schemes and better visibility in bright environments.

### 🚀 Cyberpunk & Sci-Fi
Futuristic themes with neon accents, glowing elements, and tech-inspired aesthetics. Perfect for that cyberpunk gaming vibe.

### 🌿 Nature & Earth
Earth-toned themes inspired by natural colors - greens, browns, and organic palettes for a calming experience.

### 🌌 Space & Cosmic
Stellar themes with deep blues, purples, and cosmic colors. Bring the galaxy to your BakkesMod interface.

### 🌈 Retro & Vaporwave
80s-inspired aesthetics with pink, purple, and turquoise. Nostalgic vibes for retro gaming enthusiasts.

### 🎭 Anime & Character
Themes inspired by anime characters and series. Bold, dramatic color schemes with personality.

### 🌸 Pastel & Soft
Gentle, soft color palettes for a calm and soothing interface experience.

### ⚡ Neon & High-Contrast
Bold, glowing themes with strong contrasts and vibrant neon accents for maximum visibility.

### ⚫ Monochrome
Single-color variations and minimalist designs focusing on elegance and simplicity.

### 🔥 Fire & Warm
Themes with warm colors - oranges, yellows, and reds inspired by fire and solar energy.

### 🎲 Random Generated
Infinite unique themes with intelligent color distribution and guaranteed usability.

</details>

<details>
<summary>🤝 <strong>Contributing Guidelines</strong> - Click to expand</summary>

## How to Contribute

We welcome contributions! Here's how you can help:

1. **Fork** this repository
2. **Create** your theme following our format
3. **Test** thoroughly with BakkesMod
4. **Capture** a preview screenshot of your theme in action
5. **Generate** a new README.md with [this script](generate_readme.py)
6. **Submit** a pull request with clear description

### Submission Requirements

- Follow the established folder structure: `/themes/themename/`
- Include both `.json` theme file and `.png` preview
- Provide both light and dark variants when possible
- Use descriptive theme names and clear descriptions
- Test themes extensively before submitting
- Generate an updated README using the provided script

### Using the Random Generator for Inspiration

1. Run `python theme_randomizer.py` to generate unique themes
2. Use generated themes as starting points for manual refinement
3. Modify colors to match your vision while keeping the structure
4. Create custom previews if desired

</details>

<details>
<summary>📋 <strong>Requirements & Support</strong> - Click to expand</summary>

## Requirements

- **BakkesMod** (latest version recommended)
- **Rocket League** (Steam/Epic Games)
- **Python 3.6+** (for theme randomizer)
- **Pillow** library (for preview generation): `pip install Pillow`

## 🐛 Issues & Support

Having problems with a theme? 

1. Check that the theme file is in the correct directory
2. Ensure BakkesMod is updated to the latest version
3. Try restarting BakkesMod/Rocket League
4. Use console command: `theme_load [theme_name]`
5. Create an issue in this repository with details

### Random Theme Generator Issues

- **"PIL not found"**: Install Pillow with `pip install Pillow`
- **"Template not found"**: Ensure you're running from the repository root
- **Themes not appearing**: Check the generated `themes/random_XXXX/` folders

## 📄 License

This collection is open source. Individual themes may have different licenses - check each theme's metadata for specific author information.

</details>

## 🙏 Credits

- **[borgox](https://github.com/borgox) | [@borghettoo](https://discord.com/users/@borghettoo)** - Theme development and collection curation
- **bakkesmod.com** - Platform and default themes

---

*Made with ❤️ for the BakkesMod community*

- **Total Unique Themes:** {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))])} themes with variants
- **Total Theme Files:** {sum(len(get_theme_info(os.path.join(themes_path, d))) for d in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, d)))} `.json` files
- **Last Updated:** {datetime.now().strftime('%B %d, %Y')}
"""

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README.md generated successfully!")
    print(f"Found {len([f for f in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, f))])} themes")

if __name__ == "__main__":
    generate_readme()