"""
Interactive theme creator for BakkesMod themes.
Creates new theme folders and files from templates with user-provided metadata.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any


def load_template(template_path: str) -> Dict[str, Any]:
    """Load a template theme file."""
    try:
        with open(template_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ Template file not found: {template_path}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in template: {template_path}")
        return None


def save_theme(file_path: str, theme: Dict[str, Any]) -> bool:
    """Save a theme to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(theme, file, indent=4)
        return True
    except Exception as e:
        print(f"❌ Error saving theme: {e}")
        return False


def sanitize_folder_name(name: str) -> str:
    """Convert theme name to valid folder name."""
    # Remove/replace invalid characters
    folder_name = re.sub(r'[^\w\s-]', '', name.lower())
    # Replace spaces with underscores
    folder_name = re.sub(r'[\s_]+', '_', folder_name)
    # Remove leading/trailing underscores
    folder_name = folder_name.strip('_')
    return folder_name


def get_user_input(prompt: str, default: str = "", allow_empty: bool = False) -> str:
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input or allow_empty:
                return user_input
            print("❌ This field is required. Please enter a value.")


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    while True:
        response = input(f"{prompt} [{default_str}]: ").strip().lower()
        if not response:
            return default
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' for yes or 'n' for no.")


def check_folder_exists(theme_folder: Path) -> bool:
    """Check if theme folder already exists."""
    if theme_folder.exists():
        print(f"⚠️  Theme folder '{theme_folder.name}' already exists!")
        return get_yes_no("Do you want to overwrite it?", default=False)
    return True


def create_theme_metadata(folder_name: str) -> Dict[str, Any]:
    """Interactively create theme metadata."""
    print("\n🎨 Theme Metadata Setup")
    print("=" * 40)
    
    # Get theme information
    theme_name = get_user_input("Theme name", folder_name.replace('_', ' ').title())
    
    print("\n📝 Author Information:")
    author_name = get_user_input("Author name (Markdown Links Allowed)", "@borgox")
    
    print("\n📖 Theme Description:")
    print("💡 Tip: Describe the theme's color scheme, mood, or inspiration")
    description = get_user_input("Description")
    
    print("\n🏷️ Theme Classification:")
    print("Available categories:")
    print("  1. dark - Dark theme (low light, minimal eye strain)")
    print("  2. light - Light theme (bright environments)")
    print("  3. cyberpunk - Futuristic/sci-fi themes (neon, tech)")
    print("  4. nature - Earth tones, natural colors")
    print("  5. space - Cosmic, galaxy, astronomical themes")
    print("  6. retro - Vintage, 80s, vaporwave aesthetics")
    print("  7. anime - Anime-inspired, character themes")
    print("  8. pastel - Soft, gentle color palettes")
    print("  9. neon - High-contrast, glowing accents")
    print(" 10. monochrome - Single color variations")
    print(" 11. minimal - Clean, simple designs")
    print(" 12. gaming - Gaming-focused themes")
    print(" 13. fire - Warm colors (orange, yellow, red)")
    print(" 14. other - Custom/unique category")
    
    while True:
        category = get_user_input("Category (1-14)", "1").strip()
        category_map = {
            '1': 'dark', '2': 'light', '3': 'cyberpunk', '4': 'nature',
            '5': 'space', '6': 'retro', '7': 'anime', '8': 'pastel',
            '9': 'neon', '10': 'monochrome', '11': 'minimal', '12': 'gaming',
            '13': 'fire', '14': 'other'
        }
        if category in category_map:
            category = category_map[category]
            break
        print("❌ Please enter a number from 1-14")
    
    # Version
    version = get_user_input("Version", "1.0")
    
    return {
        'name': theme_name,
        'author': author_name,
        'description': description,
        'category': category,
        'version': version
    }


def create_theme_variants(metadata: Dict[str, Any], folder_name: str, theme_folder: Path) -> None:
    """Create theme variants (dark/light) based on user choices."""
    
    print(f"\n🎭 Theme Variants for '{metadata['name']}'")
    print("=" * 50)
    
    # Determine which variants to create
    create_dark = get_yes_no("Create dark variant?", default=True)
    create_light = get_yes_no("Create light variant?", default=True)
    
    if not create_dark and not create_light:
        print("❌ At least one variant must be created!")
        return
    
    # Create theme folder
    theme_folder.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created theme folder: {theme_folder}")
    
    templates_base = Path("defaults/template")
    created_files = []
    
    # Create dark variant
    if create_dark:
        dark_template_path = templates_base / "template.json"
        dark_template = load_template(str(dark_template_path))
        
        if dark_template:
            # Update metadata
            dark_metadata = metadata.copy()
            dark_metadata['variant'] = 'dark'
            if not metadata['name'].lower().endswith(' dark'):
                dark_metadata['name'] = metadata['name']
            
            dark_theme = {
                'metadata': dark_metadata,
                'imgui': dark_template.get('imgui', {})
            }
            
            # Save dark theme
            dark_file = theme_folder / f"{folder_name}.json"
            if save_theme(str(dark_file), dark_theme):
                created_files.append(str(dark_file))
                print(f"✅ Created dark variant: {dark_file.name}")
        else:
            print("❌ Failed to load dark template")
    
    # Create light variant
    if create_light:
        light_template_path = templates_base / "template_light.json"
        light_template = load_template(str(light_template_path))
        
        if light_template:
            # Update metadata
            light_metadata = metadata.copy()
            light_metadata['variant'] = 'light'
            if not metadata['name'].lower().endswith(' light'):
                light_metadata['name'] = metadata['name'] + ' Light'
            
            light_theme = {
                'metadata': light_metadata,
                'imgui': light_template.get('imgui', {})
            }
            
            # Save light theme
            light_file = theme_folder / f"{folder_name}_light.json"
            if save_theme(str(light_file), light_theme):
                created_files.append(str(light_file))
                print(f"✅ Created light variant: {light_file.name}")
        else:
            print("❌ Failed to load light template")
    
    # Summary
    if created_files:
        print(f"\n🎉 Successfully created {len(created_files)} theme file(s):")
        for file in created_files:
            print(f"   📄 {file}")
        
        # Offer to create placeholder preview files
        if get_yes_no("\nCreate placeholder preview files (.png)?", default=False):
            try:
                # Create simple placeholder images if PIL is available
                from PIL import Image, ImageDraw, ImageFont
                
                for theme_file in created_files:
                    preview_file = theme_file.replace('.json', '.png')
                    
                    # Create a simple placeholder image
                    img = Image.new('RGB', (400, 300), color=(64, 64, 64))
                    draw = ImageDraw.Draw(img)
                    
                    # Add placeholder text
                    try:
                        font = ImageFont.load_default()
                        text = f"Preview for\n{Path(theme_file).stem}"
                        bbox = draw.textbbox((0, 0), text, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        x = (400 - text_width) // 2
                        y = (300 - text_height) // 2
                        draw.text((x, y), text, fill=(255, 255, 255), font=font, align='center')
                    except:
                        draw.text((150, 140), "Preview Placeholder", fill=(255, 255, 255))
                    
                    img.save(preview_file)
                    print(f"   🖼️  Created placeholder: {Path(preview_file).name}")
                    
            except ImportError:
                print("   ⚠️  Pillow not available for preview generation")
                print("   📝 Create .png files manually or install Pillow: pip install Pillow")
        
        print(f"\n📂 Theme location: {theme_folder}")
        print("\n🎨 Next steps:")
        print("   1. Edit the .json files to customize colors")
        print("   2. Test the theme in BakkesMod with: theme_load /themes/[theme_name]")
        print("   3. Create/update preview images (.png files)")
        print("   4. Run 'python generate_readme.py' to update documentation")
        print("   5. Consider using 'python theme_randomizer.py' for color inspiration")
        
        print(f"\n💡 Pro tips:")
        print(f"   • Use the template files as reference for color properties")
        print(f"   • Test both variants in different lighting conditions")
        print(f"   • Consider accessibility with high contrast ratios")
    else:
        print("❌ No theme files were created")


def list_existing_themes() -> None:
    """List existing themes for reference."""
    themes_path = Path("themes")
    if not themes_path.exists():
        return
    
    existing_themes = [d.name for d in themes_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if existing_themes:
        print("\n📋 Existing themes:")
        for i, theme in enumerate(sorted(existing_themes), 1):
            print(f"   {i:2}. {theme}")
    else:
        print("\n📋 No existing themes found")


def main():
    """Main theme creation workflow."""
    print("🎨 BakkesMod Theme Creator")
    print("=" * 40)
    print("This tool helps you create new themes from templates")
    print("\n💡 Quick Start Guide:")
    print("   1. Choose a descriptive theme name")
    print("   2. Select the appropriate category for your theme")
    print("   3. Create both dark and light variants when possible")
    print("   4. Edit the generated .json files to customize colors")
    print("   5. Use 'python theme_randomizer.py' for color inspiration")
    print()
    
    # Check if we're in the right directory
    if not Path("defaults/template").exists():
        print("❌ Error: Template directory not found!")
        print("   Make sure you're running this script from the repository root")
        print("   Expected: defaults/template/template.json and template_light.json")
        return
    
    # Show existing themes for reference
    list_existing_themes()
    
    print("\n🏗️  Create New Theme")
    print("=" * 25)
    
    # Get folder name
    while True:
        theme_input = get_user_input("Theme name (will be used for folder)")
        folder_name = sanitize_folder_name(theme_input)
        
        if not folder_name:
            print("❌ Invalid theme name. Please use letters, numbers, spaces, and dashes only.")
            continue
        
        theme_folder = Path("themes") / folder_name
        
        print(f"📁 Folder will be created as: themes/{folder_name}")
        
        if check_folder_exists(theme_folder):
            break
        else:
            continue  # User chose not to overwrite, ask for new name
    
    # Create metadata
    metadata = create_theme_metadata(folder_name)
    
    # Confirm creation
    print(f"\n📋 Theme Summary:")
    print(f"   Name: {metadata['name']}")
    print(f"   Author: {metadata['author']}")
    print(f"   Description: {metadata['description']}")
    print(f"   Category: {metadata['category']}")
    print(f"   Version: {metadata['version']}")
    print(f"   Folder: themes/{folder_name}")
    
    if get_yes_no("\nCreate this theme?", default=True):
        create_theme_variants(metadata, folder_name, theme_folder)
    else:
        print("❌ Theme creation cancelled")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Theme creation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue if it persists")