import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

BASE_DIR = r"c:\Users\Asus\Desktop\bakero-project"
REF_DIR = r"c:\Users\Asus\Desktop\prjetj1"
BRAIN_DIR = r"C:\Users\Asus\.gemini\antigravity\brain\30330708-f6ef-40eb-9360-d7d9fb8096da"
GALLERY_DIR = os.path.join(BASE_DIR, "images", "gallery")
os.makedirs(GALLERY_DIR, exist_ok=True)

LOGO_PATH = os.path.join(BASE_DIR, "images", "bakero-logo.png")
logo = Image.open(LOGO_PATH).convert("RGBA")

def create_metallic_badge(target_width=180):
    """Generates a luxury brushed stainless steel nameplate with the authentic Bakero logo."""
    aspect = logo.height / logo.width
    logo_w = int(target_width * 0.78)
    logo_h = int(logo_w * aspect)
    resized_logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    
    badge_w = target_width
    badge_h = logo_h + 18
    
    # Outer drop shadow
    shadow = Image.new("RGBA", (badge_w + 14, badge_h + 14), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([4, 4, badge_w + 8, badge_h + 8], radius=6, fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    
    # Brushed steel plate
    plate = Image.new("RGBA", (badge_w, badge_h), (244, 246, 249, 252))
    p_draw = ImageDraw.Draw(plate)
    # Metallic borders
    p_draw.rounded_rectangle([0, 0, badge_w - 1, badge_h - 1], radius=5, outline=(160, 166, 175, 255), width=1)
    p_draw.rounded_rectangle([1, 1, badge_w - 2, badge_h - 2], radius=4, outline=(255, 255, 255, 230), width=1)
    
    # Bronze/copper screw rivets on top corners
    p_draw.ellipse([5, 5, 9, 9], fill=(182, 106, 53, 220), outline=(140, 80, 40, 255))
    p_draw.ellipse([badge_w - 10, 5, badge_w - 6, 9], fill=(182, 106, 53, 220), outline=(140, 80, 40, 255))
    
    # Center logo
    x_off = (badge_w - logo_w) // 2
    y_off = (badge_h - logo_h) // 2
    plate.paste(resized_logo, (x_off, y_off), resized_logo)
    
    final = Image.new("RGBA", (badge_w + 14, badge_h + 14), (0, 0, 0, 0))
    final.paste(shadow, (0, 0), shadow)
    final.paste(plate, (4, 3), plate)
    return final

def generate_image(src_path, dest_filename, target_size=(1600, 1000), crop_box=None, badge_pos="top_right", badge_width=180, brightness=1.0, contrast=1.15, color=1.08):
    dest_path = os.path.join(GALLERY_DIR, dest_filename)
    try:
        im = Image.open(src_path).convert("RGB")
        
        # Custom crop box (left_pct, top_pct, right_pct, bottom_pct)
        if crop_box:
            w, h = im.size
            im = im.crop((
                int(w * crop_box[0]),
                int(h * crop_box[1]),
                int(w * crop_box[2]),
                int(h * crop_box[3])
            ))
            
        # Target aspect ratio crop
        t_w, t_h = target_size
        aspect = im.width / im.height
        target_aspect = t_w / t_h
        
        if aspect > target_aspect:
            new_w = int(im.height * target_aspect)
            left = (im.width - new_w) // 2
            im = im.crop((left, 0, left + new_w, im.height))
        else:
            new_h = int(im.width / target_aspect)
            top = (im.height - new_h) // 2
            im = im.crop((0, top, im.width, top + new_h))
            
        im = im.resize((t_w, t_h), Image.Resampling.LANCZOS)
        
        # Color grading
        if brightness != 1.0:
            im = ImageEnhance.Brightness(im).enhance(brightness)
        if contrast != 1.0:
            im = ImageEnhance.Contrast(im).enhance(contrast)
        if color != 1.0:
            im = ImageEnhance.Color(im).enhance(color)
            
        # Add Bakero brand plate
        if badge_pos != "none":
            badge = create_metallic_badge(badge_width)
            b_w, b_h = badge.size
            if badge_pos == "top_left":
                pos = (40, 40)
            elif badge_pos == "top_right":
                pos = (t_w - b_w - 40, 40)
            elif badge_pos == "bottom_right":
                pos = (t_w - b_w - 40, t_h - b_h - 40)
            elif badge_pos == "bottom_left":
                pos = (40, t_h - b_h - 40)
            im.paste(badge, pos, badge)
            
        im.save(dest_path, quality=94, optimize=True)
        print(f"OK: Generated {dest_filename} ({t_w}x{t_h}) from {os.path.basename(src_path)}")
        return True
    except Exception as e:
        print(f"FAIL: {dest_filename} - {e}")
        return False

# Definition of the 10 showcase images
images_to_generate = [
    {
        "src": os.path.join(REF_DIR, "front-view-professional-kitchen.jpg"),
        "dest": "gallery-01-cooking-island.jpg",
        "crop": (0.05, 0.20, 0.95, 0.95),
        "badge": "top_right",
        "badge_w": 200,
        "brightness": 0.92,
        "contrast": 1.25,
        "color": 1.10
    },
    {
        "src": os.path.join(BRAIN_DIR, "pizza_oven_cat_1793889066053.jpg"),
        "dest": "gallery-02-artisan-pizza-oven.jpg",
        "crop": (0.0, 0.08, 1.0, 0.88),
        "badge": "top_left",
        "badge_w": 180,
        "brightness": 0.95,
        "contrast": 1.20,
        "color": 1.15
    },
    {
        "src": os.path.join(REF_DIR, "shiny-steel-stove-heats-fresh-food-inside-generated-by-ai.jpg"),
        "dest": "gallery-03-saute-flambe-station.jpg",
        "crop": (0.05, 0.10, 0.95, 0.92),
        "badge": "top_left",
        "badge_w": 190,
        "brightness": 0.88,
        "contrast": 1.28,
        "color": 1.12
    },
    {
        "src": os.path.join(BRAIN_DIR, "coffee_machine_1793889410416.jpg"),
        "dest": "gallery-04-specialty-espresso-bar.jpg",
        "crop": (0.05, 0.12, 0.95, 0.88),
        "badge": "top_right",
        "badge_w": 180,
        "brightness": 0.96,
        "contrast": 1.22,
        "color": 1.10
    },
    {
        "src": os.path.join(BRAIN_DIR, "deep_fryer_cat_1793888910536.jpg"),
        "dest": "gallery-05-qsr-frying-line.jpg",
        "crop": (0.0, 0.06, 1.0, 0.90),
        "badge": "top_left",
        "badge_w": 180,
        "brightness": 0.94,
        "contrast": 1.22,
        "color": 1.12
    },
    {
        "src": os.path.join(REF_DIR, "modern-kitchen-with-sleek-appliances-breakfast-bar.jpg"),
        "dest": "gallery-06-refrigerated-cold-line.jpg",
        "crop": (0.10, 0.22, 0.90, 0.92),
        "badge": "top_right",
        "badge_w": 200,
        "brightness": 0.90,
        "contrast": 1.24,
        "color": 1.08
    },
    {
        "src": os.path.join(BRAIN_DIR, "cooking_range_category_1793889018913.jpg"),
        "dest": "gallery-07-heavy-cooking-suite.jpg",
        "crop": (0.0, 0.05, 1.0, 0.88),
        "badge": "top_left",
        "badge_w": 180,
        "brightness": 0.93,
        "contrast": 1.22,
        "color": 1.10
    },
    {
        "src": os.path.join(REF_DIR, "198660791_xl_normal_none.webp"),
        "dest": "gallery-08-executive-plating-pass.jpg",
        "crop": (0.05, 0.15, 0.95, 0.95),
        "badge": "top_left",
        "badge_w": 190,
        "brightness": 0.90,
        "contrast": 1.26,
        "color": 1.12
    },
    {
        "src": os.path.join(BRAIN_DIR, "hotel_kitchen_project_1793888932609.jpg"),
        "dest": "gallery-09-hotel-banquet-production.jpg",
        "crop": (0.0, 0.02, 1.0, 0.95),
        "badge": "top_right",
        "badge_w": 190,
        "brightness": 0.92,
        "contrast": 1.22,
        "color": 1.10
    },
    {
        "src": os.path.join(BRAIN_DIR, "modular_kitchen_1793888877562.jpg"),
        "dest": "gallery-10-precision-fabrication.jpg",
        "crop": (0.0, 0.05, 1.0, 0.95),
        "badge": "top_left",
        "badge_w": 190,
        "brightness": 0.92,
        "contrast": 1.24,
        "color": 1.10
    }
]

print(f"Starting generation of {len(images_to_generate)} premium images...")
success = 0
for item in images_to_generate:
    if generate_image(
        src_path=item["src"],
        dest_filename=item["dest"],
        target_size=(1600, 1000),
        crop_box=item["crop"],
        badge_pos=item["badge"],
        badge_width=item["badge_w"],
        brightness=item["brightness"],
        contrast=item["contrast"],
        color=item["color"]
    ):
        success += 1

print(f"\nCompleted: {success}/{len(images_to_generate)} images generated into {GALLERY_DIR}")
