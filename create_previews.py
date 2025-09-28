import os
from PIL import Image, ImageDraw, ImageFont
import json

def create_theme_preview(theme_name, theme_path, output_path, is_light=False):
    """Create a preview image for a theme"""
    try:
        # Read theme data
        with open(theme_path, 'r') as f:
            theme_data = json.load(f)
        
        # Get key colors from theme
        window_bg = theme_data['imgui'].get('ImGuiCol_WindowBg', {'r': 0.1, 'g': 0.1, 'b': 0.1})
        text_color = theme_data['imgui'].get('ImGuiCol_Text', {'r': 0.9, 'g': 0.9, 'b': 0.9})
        button_color = theme_data['imgui'].get('ImGuiCol_Button', {'r': 0.5, 'g': 0.5, 'b': 0.5})
        header_color = theme_data['imgui'].get('ImGuiCol_Header', {'r': 0.4, 'g': 0.4, 'b': 0.4})
        
        # Convert to RGB values (0-255)
        bg_rgb = (int(window_bg['r'] * 255), int(window_bg['g'] * 255), int(window_bg['b'] * 255))
        text_rgb = (int(text_color['r'] * 255), int(text_color['g'] * 255), int(text_color['b'] * 255))
        button_rgb = (int(button_color['r'] * 255), int(button_color['g'] * 255), int(button_color['b'] * 255))
        header_rgb = (int(header_color['r'] * 255), int(header_color['g'] * 255), int(header_color['b'] * 255))
        
        # Create image (400x300)
        img = Image.new('RGB', (400, 300), bg_rgb)
        draw = ImageDraw.Draw(img)
        
        # Draw mock UI elements
        # Title bar
        draw.rectangle([10, 10, 390, 40], fill=header_rgb)
        
        # Buttons
        draw.rectangle([20, 60, 120, 90], fill=button_rgb)
        draw.rectangle([140, 60, 240, 90], fill=button_rgb)
        draw.rectangle([260, 60, 360, 90], fill=button_rgb)
        
        # Mock content area
        draw.rectangle([20, 110, 380, 280], fill=tuple(max(0, min(255, c + (20 if is_light else -20))) for c in bg_rgb))
        
        # Try to add text (basic fallback if no font available)
        try:
            # Use default PIL font
            draw.text((25, 20), theme_data['metadata']['name'], fill=text_rgb)
            draw.text((25, 115), "Theme Preview", fill=text_rgb)
            draw.text((25, 140), f"by {theme_data['metadata']['author']}", fill=text_rgb)
        except:
            # If text rendering fails, just draw some shapes
            draw.ellipse([200, 150, 250, 200], fill=button_rgb)
        
        # Save image
        img.save(output_path)
        print(f"Created preview: {output_path}")
        
    except Exception as e:
        print(f"Error creating preview for {theme_name}: {e}")
        # Create a simple colored rectangle as fallback
        img = Image.new('RGB', (400, 300), (100, 100, 100))
        img.save(output_path)

def create_all_previews():
    """Create preview images for all themes"""
    themes_path = "themes"
    
    if not os.path.exists(themes_path):
        print("Themes directory not found!")
        return
    
    for theme_folder in os.listdir(themes_path):
        folder_path = os.path.join(themes_path, theme_folder)
        if not os.path.isdir(folder_path):
            continue
            
        print(f"Processing {theme_folder}...")
        
        for theme_file in os.listdir(folder_path):
            if theme_file.endswith('.json'):
                # Determine output filename
                theme_path = os.path.join(folder_path, theme_file)
                image_name = theme_file.replace('.json', '.png')
                image_path = os.path.join(folder_path, image_name)
                
                is_light = 'light' in theme_file.lower()
                create_theme_preview(theme_folder, theme_path, image_path, is_light)

if __name__ == "__main__":
    create_all_previews()
    print("Preview generation complete!")