"""
Create a random theme shuffling every value from the template theme.
"""

import random
from typing import Any, Dict
from copy import deepcopy
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
import os


def load_theme(file_path: str) -> Dict[str, Any]:
    """Load a theme from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def save_theme(file_path: str, theme: Dict[str, Any]) -> None:
    """Save a theme to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(theme, file, indent=4)

def randomize_value(value, is_light: bool = False, component: str = "color", element_key: str = ""):
    """Randomize a JSON RGBA value based on variant"""
    if component == "alpha":
        # Special handling for window/background alpha - keep them mostly opaque
        if element_key in ["ImGuiCol_WindowBg", "ImGuiCol_ChildBg", "ImGuiCol_PopupBg", "ImGuiCol_MenuBarBg"]:
            # 95% chance of being mostly opaque (0.85-1.0)
            if random.random() < 0.95:
                return random.uniform(0.85, 1.0)
            else:
                # 5% chance of being semi-transparent (0.6-0.85)
                return random.uniform(0.6, 0.85)
        else:
            # Other alpha values can be more varied but still bias towards visibility
            # 80% chance of being mostly opaque (0.7-1.0), 20% chance of being transparent (0.0-0.7)
            if random.random() < 0.8:
                return random.uniform(0.7, 1.0)
            else:
                return random.uniform(0.0, 0.7)
    
    if is_light:
        # Light variant: favor brighter values (0.4-1.0) with 99% probability
        if random.random() < 0.99:
            return random.uniform(0.4, 1.0)
        else:
            # 1% chance for darker accent
            return random.uniform(0.0, 0.4)
    else:
        # Dark variant: favor darker values (0.0-0.6) with 99% probability
        if random.random() < 0.99:
            return random.uniform(0.0, 0.6)
        else:
            # 1% chance for brighter accent
            return random.uniform(0.6, 1.0)

def randomize_super_key(key: Dict[str, Any], is_light: bool = False, element_key: str = "") -> Dict[str, Any]:
    """Randomize a super key (RGBA values) based on variant."""
    result = {}
    for k, v in key.items():
        component_type = "alpha" if k == "a" else "color"
        result[k] = randomize_value(v, is_light, component_type, element_key)
    return result

def randomize_theme(theme: Dict[str, Any], is_light: bool = False, theme_id: int = None) -> Dict[str, Any]:
    """Randomize the theme by picking random values for each key based on variant."""
    randomized_theme = deepcopy(theme.get("imgui", {}))
    
    # Special handling for background colors - ensure they stay true to variant
    background_keys = ["ImGuiCol_WindowBg", "ImGuiCol_ChildBg", "ImGuiCol_PopupBg", "ImGuiCol_MenuBarBg"]
    
    for key, value in randomized_theme.items():
        if isinstance(value, dict):
            if key in background_keys:
                # Force backgrounds to be more consistent with variant AND opaque
                if is_light:
                    # Light backgrounds: very high chance of bright values (0.7-1.0)
                    if random.random() < 0.995:
                        randomized_theme[key] = {
                            "a": randomize_value(value.get("a", 1), is_light, "alpha", key),
                            "r": random.uniform(0.7, 1.0),
                            "g": random.uniform(0.7, 1.0),
                            "b": random.uniform(0.7, 1.0)
                        }
                    else:
                        randomized_theme[key] = randomize_super_key(value, is_light, key)
                else:
                    # Dark backgrounds: very high chance of dark values (0.0-0.3)
                    if random.random() < 0.995:
                        randomized_theme[key] = {
                            "a": randomize_value(value.get("a", 1), is_light, "alpha", key),
                            "r": random.uniform(0.0, 0.3),
                            "g": random.uniform(0.0, 0.3),
                            "b": random.uniform(0.0, 0.3)
                        }
                    else:
                        randomized_theme[key] = randomize_super_key(value, is_light, key)
            else:
                randomized_theme[key] = randomize_super_key(value, is_light, key)
        else:
            randomized_theme[key] = randomize_value(value, is_light, "color", key)
    
    # Create metadata for the randomized theme
    if theme_id is None:
        theme_id = random.randint(1000, 9999)
    variant = "light" if is_light else "dark"
    
    metadata = {
        "name": f"Random {theme_id}",
        "author": "[@borgox](https://github.com/borgox) | [@borghettoo](https://discord.gg/XrqsmAANkC)",
        "description": f"A randomly generated {variant} theme with unique color combinations",
        "variant": variant
    }
    
    return {"metadata": metadata, "imgui": randomized_theme}

def ensure_unique_theme_id(theme_folder: Path) -> int:
    """Ensure the generated theme ID is unique within the themes directory."""
    existing_ids = {int(p.name.split('_')[1]) for p in theme_folder.parent.glob('random_*/') if p.name.startswith('random_')}
    while True:
        theme_id = random.randint(1000, 9999)
        if theme_id not in existing_ids:
            return theme_id

def rgba_to_rgb(rgba_dict: Dict[str, float], background=(0, 0, 0)) -> tuple:
    """Convert RGBA dict to RGB tuple, applying alpha blending over background."""
    r, g, b, a = rgba_dict['r'], rgba_dict['g'], rgba_dict['b'], rgba_dict['a']
    
    # Alpha blending: result = foreground * alpha + background * (1 - alpha)
    final_r = int((r * a + background[0] / 255 * (1 - a)) * 255)
    final_g = int((g * a + background[1] / 255 * (1 - a)) * 255)
    final_b = int((b * a + background[2] / 255 * (1 - a)) * 255)
    
    return (min(255, max(0, final_r)), min(255, max(0, final_g)), min(255, max(0, final_b)))

def get_default_font():
    """Get a default font for text rendering."""
    try:
        # Try to use a system font
        if os.name == 'nt':  # Windows
            return ImageFont.truetype("arial.ttf", 12)
        else:  # Unix-like systems
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        # Fallback to default PIL font
        return ImageFont.load_default()

def generate_theme_preview(theme: Dict[str, Any], is_light: bool = False, output_path: str = None) -> None:
    """Generate a comprehensive preview image for the theme."""
    imgui_colors = theme.get('imgui', {})
    
    # Get background color for alpha blending
    window_bg = imgui_colors.get('ImGuiCol_WindowBg', {'r': 0.1, 'g': 0.1, 'b': 0.1, 'a': 1.0})
    bg_color = rgba_to_rgb(window_bg)
    
    # Create image (800x600 for detailed preview)
    width, height = 800, 600
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Get font
    font = get_default_font()
    title_font = get_default_font()
    
    try:
        if os.name == 'nt':
            title_font = ImageFont.truetype("arial.ttf", 16)
        else:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        title_font = font
    
    # Helper function to get color
    def get_color(key, fallback=(128, 128, 128)):
        color_data = imgui_colors.get(key, {'r': 0.5, 'g': 0.5, 'b': 0.5, 'a': 1.0})
        return rgba_to_rgb(color_data, bg_color)
    
    # Draw main window frame
    frame_color = get_color('ImGuiCol_Border')
    draw.rectangle([10, 10, width-10, height-10], outline=frame_color, width=2)
    
    # Draw title bar
    title_bg = get_color('ImGuiCol_TitleBg')
    draw.rectangle([12, 12, width-12, 40], fill=title_bg)
    
    # Title text
    title_text_color = get_color('ImGuiCol_Text')
    theme_name = theme.get('metadata', {}).get('name', 'Random Theme')
    variant = " (Light)" if is_light else " (Dark)"
    draw.text([20, 18], f"{theme_name}{variant} - BakkesMod Theme Preview", fill=title_text_color, font=title_font)
    
    # Draw menu bar
    menubar_bg = get_color('ImGuiCol_MenuBarBg')
    draw.rectangle([12, 42, width-12, 65], fill=menubar_bg)
    
    # Menu items
    menu_text_color = get_color('ImGuiCol_Text')
    menu_items = ["File", "Edit", "View", "Tools", "Help"]
    x_pos = 20
    for item in menu_items:
        draw.text([x_pos, 48], item, fill=menu_text_color, font=font)
        x_pos += len(item) * 8 + 15
    
    # Draw main content area with child windows
    content_y = 70
    
    # Left panel (tree/list)
    child_bg = get_color('ImGuiCol_ChildBg')
    draw.rectangle([20, content_y, 250, height-30], fill=child_bg, outline=frame_color, width=1)
    
    # Tree nodes
    tree_items = ["🗂️ Game Settings", "  🏎️ Car Physics", "  🎮 Controls", "  📊 Stats", "🗂️ Plugins", "  📈 Training", "  🎨 Themes"]
    y_pos = content_y + 10
    for item in tree_items:
        item_color = title_text_color if not item.startswith("  ") else menu_text_color
        draw.text([30, y_pos], item, fill=item_color, font=font)
        y_pos += 20
    
    # Main content panel
    draw.rectangle([260, content_y, width-20, height-120], fill=child_bg, outline=frame_color, width=1)
    
    # Buttons showcase
    button_y = content_y + 20
    button_colors = [
        ('ImGuiCol_Button', 'Normal Button'),
        ('ImGuiCol_ButtonHovered', 'Hovered Button'),
        ('ImGuiCol_ButtonActive', 'Active Button')
    ]
    
    for i, (color_key, label) in enumerate(button_colors):
        button_color = get_color(color_key)
        button_x = 280 + (i * 140)
        draw.rectangle([button_x, button_y, button_x + 120, button_y + 30], fill=button_color, outline=frame_color)
        
        # Button text
        text_bbox = draw.textbbox([0, 0], label, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        text_x = button_x + (120 - text_w) // 2
        text_y = button_y + (30 - text_h) // 2
        draw.text([text_x, text_y], label, fill=title_text_color, font=font)
    
    # Input fields
    input_y = button_y + 50
    input_bg = get_color('ImGuiCol_FrameBg')
    
    # Text input
    draw.rectangle([280, input_y, 500, input_y + 25], fill=input_bg, outline=frame_color)
    draw.text([285, input_y + 5], "Sample text input field...", fill=menu_text_color, font=font)
    
    # Slider
    slider_y = input_y + 40
    draw.rectangle([280, slider_y, 500, slider_y + 20], fill=input_bg, outline=frame_color)
    
    # Slider handle
    slider_handle_color = get_color('ImGuiCol_SliderGrab')
    handle_pos = 350  # Sample position
    draw.rectangle([handle_pos-5, slider_y-2, handle_pos+5, slider_y+22], fill=slider_handle_color)
    
    # Checkbox
    check_y = slider_y + 35
    checkbox_bg = get_color('ImGuiCol_CheckMark')
    draw.rectangle([280, check_y, 295, check_y + 15], fill=input_bg, outline=frame_color)
    draw.text([285, check_y + 2], "✓", fill=checkbox_bg, font=font)
    draw.text([305, check_y], "Enable advanced settings", fill=title_text_color, font=font)
    
    # Progress bar
    progress_y = check_y + 30
    draw.rectangle([280, progress_y, 500, progress_y + 15], fill=input_bg, outline=frame_color)
    
    # Progress fill
    progress_color = get_color('ImGuiCol_PlotHistogram')
    progress_width = int(220 * 0.65)  # 65% progress
    draw.rectangle([280, progress_y, 280 + progress_width, progress_y + 15], fill=progress_color)
    
    # Tabs
    tab_y = progress_y + 35
    tab_colors = [
        ('ImGuiCol_Tab', 'Settings'),
        ('ImGuiCol_TabActive', 'Active Tab'),
        ('ImGuiCol_TabHovered', 'Hover Tab')
    ]
    
    tab_x = 280
    for color_key, label in tab_colors:
        tab_color = get_color(color_key)
        tab_width = len(label) * 8 + 20
        draw.rectangle([tab_x, tab_y, tab_x + tab_width, tab_y + 25], fill=tab_color, outline=frame_color)
        
        text_bbox = draw.textbbox([0, 0], label, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        draw.text([tab_x + (tab_width - text_w) // 2, tab_y + 5], label, fill=title_text_color, font=font)
        tab_x += tab_width + 5
    
    # Status bar
    status_bg = get_color('ImGuiCol_MenuBarBg')
    draw.rectangle([12, height-25, width-12, height-12], fill=status_bg, outline=frame_color)
    draw.text([20, height-20], f"Ready | Theme: {theme_name} | FPS: 144", fill=menu_text_color, font=font)
    
    # Popup/tooltip simulation
    if random.random() < 0.3:  # 30% chance to show popup
        popup_bg = get_color('ImGuiCol_PopupBg')
        popup_x, popup_y = 400, 200
        popup_w, popup_h = 180, 80
        
        draw.rectangle([popup_x, popup_y, popup_x + popup_w, popup_y + popup_h], fill=popup_bg, outline=frame_color, width=2)
        draw.text([popup_x + 10, popup_y + 10], "Tooltip/Popup", fill=title_text_color, font=title_font)
        draw.text([popup_x + 10, popup_y + 30], "This shows how popups", fill=menu_text_color, font=font)
        draw.text([popup_x + 10, popup_y + 45], "and tooltips look in", fill=menu_text_color, font=font)
        draw.text([popup_x + 10, popup_y + 60], "this theme.", fill=menu_text_color, font=font)
    
    # Save the image
    if output_path:
        image.save(output_path)
        print(f"Theme preview saved to {output_path}")
    
    return image
def main(light_ver = True):
    # Generate a unique theme ID
    theme_id = ensure_unique_theme_id(theme_folder=Path("./themes"))
    theme_folder = Path("./themes") / f"random_{theme_id}"
    
    # Create theme folder if it doesn't exist
    theme_folder.mkdir(exist_ok=True)
    
    try:
        # Generate dark theme
        template_path = Path("./defaults/template/template.json")
        output_path = theme_folder / f"random_{theme_id}.json"
        theme = load_theme(template_path)
        randomized_theme = randomize_theme(theme, is_light=False, theme_id=theme_id)
        save_theme(output_path, randomized_theme)
        print(f"Randomized dark theme saved to {output_path}")
        
        # Generate dark theme preview
        preview_path = theme_folder / f"random_{theme_id}.png"
        generate_theme_preview(randomized_theme, is_light=False, output_path=str(preview_path))

        if light_ver:
            # Generate light theme
            template_path = Path("./defaults/template/template_light.json")
            output_path = theme_folder / f"random_{theme_id}_light.json"
            theme = load_theme(template_path)
            randomized_theme_light = randomize_theme(theme, is_light=True, theme_id=theme_id)
            save_theme(output_path, randomized_theme_light)
            print(f"Randomized light theme saved to {output_path}")
            
            # Generate light theme preview
            preview_path_light = theme_folder / f"random_{theme_id}_light.png"
            generate_theme_preview(randomized_theme_light, is_light=True, output_path=str(preview_path_light))
            
    except ImportError as e:
        print(f"Warning: Could not generate previews. PIL (Pillow) is not installed.")
        print(f"To enable preview generation, install Pillow: pip install Pillow")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"Warning: Could not generate previews due to error: {e}")
        print("Themes were still created successfully.")

if __name__ == "__main__":
    main(light_ver=True)