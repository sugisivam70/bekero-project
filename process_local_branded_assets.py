import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

BASE_DIR = r"c:\Users\Asus\Desktop\bakero-project"
REF_DIR = r"c:\Users\Asus\Desktop\prjetj1"
BRAIN_DIR = r"C:\Users\Asus\.gemini\antigravity\brain\30330708-f6ef-40eb-9360-d7d9fb8096da"
LOGO_PATH = os.path.join(BASE_DIR, "images", "bakero-logo.png")

logo = Image.open(LOGO_PATH).convert("RGBA")

def create_metallic_badge(target_width=140):
    """Generates a luxury brushed stainless steel nameplate with the authentic Bakero logo."""
    aspect = logo.height / logo.width
    logo_w = int(target_width * 0.78)
    logo_h = int(logo_w * aspect)
    resized_logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    
    badge_w = target_width
    badge_h = logo_h + 16
    
    badge = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
    
    # Outer drop shadow
    shadow = Image.new("RGBA", (badge_w + 12, badge_h + 12), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([4, 4, badge_w + 6, badge_h + 6], radius=5, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    
    # Brushed steel plate
    plate = Image.new("RGBA", (badge_w, badge_h), (244, 246, 249, 252))
    p_draw = ImageDraw.Draw(plate)
    # Metallic borders
    p_draw.rounded_rectangle([0, 0, badge_w - 1, badge_h - 1], radius=4, outline=(170, 175, 182, 255), width=1)
    p_draw.rounded_rectangle([1, 1, badge_w - 2, badge_h - 2], radius=3, outline=(255, 255, 255, 220), width=1)
    
    # Tiny copper screw rivets on top corners
    p_draw.ellipse([4, 4, 7, 7], fill=(182, 106, 53, 200), outline=(140, 80, 40, 255))
    p_draw.ellipse([badge_w - 8, 4, badge_w - 5, 7], fill=(182, 106, 53, 200), outline=(140, 80, 40, 255))
    
    # Center logo
    x_off = (badge_w - logo_w) // 2
    y_off = (badge_h - logo_h) // 2
    plate.paste(resized_logo, (x_off, y_off), resized_logo)
    
    final = Image.new("RGBA", (badge_w + 12, badge_h + 12), (0, 0, 0, 0))
    final.paste(shadow, (0, 0), shadow)
    final.paste(plate, (3, 2), plate)
    return final

def process_and_brand(src_path, dest_path, target_size=(1000, 1000), crop_box=None, badge_pos="top_left", badge_scale=140, dark_grade=False, contrast=1.1, color_mult=1.05):
    """Processes source image, crops, color-grades, and applies the Bakero metallic badge."""
    try:
        im = Image.open(src_path).convert("RGB")
        
        # Apply crop box if specified (left_pct, top_pct, right_pct, bottom_pct)
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
        if dark_grade:
            im = ImageEnhance.Brightness(im).enhance(0.72)
            im = ImageEnhance.Contrast(im).enhance(1.22)
        else:
            im = ImageEnhance.Contrast(im).enhance(contrast)
            im = ImageEnhance.Color(im).enhance(color_mult)
            
        # Add Bakero brand plate
        if badge_pos != "none":
            badge = create_metallic_badge(badge_scale)
            b_w, b_h = badge.size
            if badge_pos == "top_left":
                pos = (28, 28)
            elif badge_pos == "top_right":
                pos = (t_w - b_w - 28, 28)
            elif badge_pos == "bottom_right":
                pos = (t_w - b_w - 28, t_h - b_h - 28)
            elif badge_pos == "bottom_left":
                pos = (28, t_h - b_h - 28)
            else:
                pos = (28, 28)
                
            im_rgba = im.convert("RGBA")
            im_rgba.paste(badge, pos, badge)
            im = im_rgba.convert("RGB")
            
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        im.save(dest_path, "JPEG", quality=93, optimize=True)
        print("OK: " + os.path.basename(dest_path))
        return True
    except Exception as e:
        print("FAIL " + os.path.basename(dest_path) + ": " + str(e))
        return False

print("=== STARTING BAKERO BRANDED ASSET PROCESSING ===")

# 1. NEW CINEMATIC HERO BACKGROUND (Full-screen luxury commercial kitchen with dark cinematic grading)
hero_src = os.path.join(REF_DIR, "professional-stainless-steel-kitchen-design-photo-was-made-restouraunt.jpg")
process_and_brand(
    hero_src,
    os.path.join(BASE_DIR, "images", "hero", "hero-cinematic.jpg"),
    target_size=(2560, 1440),
    crop_box=(0.0, 0.15, 1.0, 0.95),
    badge_pos="none",  # Logo rendered in HTML navigation & headline
    dark_grade=True
)

# 2. BRAND INTRO IMAGE
process_and_brand(
    os.path.join(REF_DIR, "front-view-professional-kitchen.jpg"),
    os.path.join(BASE_DIR, "images", "hero", "kitchen-wide.jpg"),
    target_size=(1400, 950),
    crop_box=(0.05, 0.1, 0.95, 0.9),
    badge_pos="top_left",
    badge_scale=150
)

# 3. STOVE DETAIL (Cinematic dark story background)
process_and_brand(
    os.path.join(REF_DIR, "shiny-steel-stove-heats-fresh-food-inside-generated-by-ai.jpg"),
    os.path.join(BASE_DIR, "images", "hero", "stove-detail.jpg"),
    target_size=(1920, 1080),
    crop_box=(0.1, 0.1, 0.9, 0.9),
    badge_pos="top_left",
    badge_scale=150,
    dark_grade=True
)

# 4. KITCHEN WORKSTATION DETAIL
process_and_brand(
    os.path.join(REF_DIR, "photo-1535850452425-140ee4a8dbae.jpg"),
    os.path.join(BASE_DIR, "images", "hero", "kitchen-detail.jpg"),
    target_size=(1200, 800),
    badge_pos="top_left",
    badge_scale=130
)

# 5. PRODUCT CATEGORIES (6 Portrait Covers 900x1100)
process_and_brand(
    os.path.join(BRAIN_DIR, "beverage_equipment_category_1793889569554.jpg"),
    os.path.join(BASE_DIR, "images", "categories", "beverage-cat.png"),
    target_size=(900, 1100),
    badge_pos="top_left",
    badge_scale=140,
    dark_grade=True
)
process_and_brand(
    os.path.join(BRAIN_DIR, "deep_fryer_cat_1793888910536.jpg"),
    os.path.join(BASE_DIR, "images", "categories", "deep-fryer-cat.png"),
    target_size=(900, 1100),
    badge_pos="top_left",
    badge_scale=140,
    dark_grade=True
)
process_and_brand(
    os.path.join(BRAIN_DIR, "oven_cat_1793888970615.jpg"),
    os.path.join(BASE_DIR, "images", "categories", "oven-cat.png"),
    target_size=(900, 1100),
    badge_pos="top_left",
    badge_scale=140,
    dark_grade=True
)
process_and_brand(
    os.path.join(BRAIN_DIR, "cooking_range_category_1793889018913.jpg"),
    os.path.join(BASE_DIR, "images", "categories", "cooking-range-cat.png"),
    target_size=(900, 1100),
    badge_pos="top_left",
    badge_scale=140,
    dark_grade=True
)
process_and_brand(
    os.path.join(REF_DIR, "198660791_xl_normal_none.webp"),
    os.path.join(BASE_DIR, "images", "categories", "kitchen-equipment.webp"),
    target_size=(900, 1100),
    crop_box=(0.1, 0.05, 0.9, 0.95),
    badge_pos="top_left",
    badge_scale=140,
    dark_grade=True
)
process_and_brand(
    os.path.join(BRAIN_DIR, "pizza_oven_cat_1793889066053.jpg"),
    os.path.join(BASE_DIR, "images", "categories", "pizza-oven-cat.png"),
    target_size=(900, 1100),
    badge_pos="top_left",
    badge_scale=140,
    dark_grade=True
)

# 6. COOKING & EATING PRODUCTS (Popcorn, Waffle, Crepe, Sweetcorn, Range, Bain-Marie)
# Popcorn Machine
process_and_brand(
    os.path.join(REF_DIR, "images.jpg"),
    os.path.join(BASE_DIR, "images", "products", "popcorn-machine.jpg"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125,
    contrast=1.15
)
# Waffle Maker
process_and_brand(
    os.path.join(REF_DIR, "illustration-splash-ice-cream-scoop-waffle-cone-dark-background-generative-ai_843410-140.avif"),
    os.path.join(BASE_DIR, "images", "products", "waffle-maker.jpg"),
    target_size=(800, 800),
    crop_box=(0.0, 0.0, 1.0, 1.0),
    badge_pos="top_left",
    badge_scale=125,
    contrast=1.15
)
# Crepe Machine
process_and_brand(
    os.path.join(REF_DIR, "360_F_627853212_bIw6wBo8qXXZvrj7wVXNew9fovoVSEoJ.jpg"),
    os.path.join(BASE_DIR, "images", "products", "crepe-machine.jpg"),
    target_size=(800, 800),
    crop_box=(0.1, 0.0, 0.9, 1.0),
    badge_pos="top_left",
    badge_scale=125,
    contrast=1.15
)
# Sweetcorn Machine
process_and_brand(
    os.path.join(REF_DIR, "images (1).jpg"),
    os.path.join(BASE_DIR, "images", "products", "sweetcorn-machine.jpg"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125,
    contrast=1.15
)
# Cooking Range with static oven
process_and_brand(
    os.path.join(BRAIN_DIR, "cooking_range_category_1793889018913.jpg"),
    os.path.join(BASE_DIR, "images", "products", "cooking-range.jpg"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
# Bain Marie
process_and_brand(
    os.path.join(REF_DIR, "Restaurant-Commercial-Kitchen-Equipment-List-A-Comprehensive-Guide.png"),
    os.path.join(BASE_DIR, "images", "products", "bain-marie.jpg"),
    target_size=(800, 800),
    crop_box=(0.05, 0.45, 0.55, 0.95),
    badge_pos="top_left",
    badge_scale=125
)

# 7. FOOD MAKING TOOLS (Food cutter, Vegetable chopper, Potato slicer, Kneader, Mixer, Mincer)
process_and_brand(
    os.path.join(BRAIN_DIR, "commercial_blender_1793889172547.jpg"),
    os.path.join(BASE_DIR, "images", "products", "commercial-blender.png"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "Restaurant-Commercial-Kitchen-Equipment-List-A-Comprehensive-Guide.png"),
    os.path.join(BASE_DIR, "images", "products", "food-cutter.jpg"),
    target_size=(800, 800),
    crop_box=(0.45, 0.05, 0.95, 0.55),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "Restaurant-Commercial-Kitchen-Equipment-List-A-Comprehensive-Guide.png"),
    os.path.join(BASE_DIR, "images", "products", "vegetable-chopper.jpg"),
    target_size=(800, 800),
    crop_box=(0.05, 0.05, 0.55, 0.55),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "198660791_xl_normal_none.webp"),
    os.path.join(BASE_DIR, "images", "products", "potato-slicer.jpg"),
    target_size=(800, 800),
    crop_box=(0.05, 0.2, 0.55, 0.8),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "198660791_xl_normal_none.webp"),
    os.path.join(BASE_DIR, "images", "products", "dough-kneader.jpg"),
    target_size=(800, 800),
    crop_box=(0.45, 0.15, 0.95, 0.85),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "Restaurant-Commercial-Kitchen-Equipment-List-A-Comprehensive-Guide.png"),
    os.path.join(BASE_DIR, "images", "products", "meat-mincer.jpg"),
    target_size=(800, 800),
    crop_box=(0.5, 0.45, 0.98, 0.95),
    badge_pos="top_left",
    badge_scale=125
)

# 8. FRYING & GRILL
process_and_brand(
    os.path.join(BRAIN_DIR, "deep_fryer_cat_1793888910536.jpg"),
    os.path.join(BASE_DIR, "images", "products", "deep-fryer.jpg"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "pngtree-metal-fryer-with-fries-inside-in-front-of-it-image_2564585.jpg"),
    os.path.join(BASE_DIR, "images", "products", "dual-fryer.jpg"),
    target_size=(800, 800),
    crop_box=(0.05, 0.05, 0.95, 0.95),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "shiny-steel-stove-heats-fresh-food-inside-generated-by-ai.jpg"),
    os.path.join(BASE_DIR, "images", "products", "griddle-plancha.jpg"),
    target_size=(800, 800),
    crop_box=(0.2, 0.25, 0.75, 0.8),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "chef-restaurant-kitchen-stove-with-pan-doing-flambe-food_73899-6567.avif"),
    os.path.join(BASE_DIR, "images", "products", "char-grill.jpg"),
    target_size=(800, 800),
    crop_box=(0.1, 0.1, 0.9, 0.9),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "img-2.jpg"),
    os.path.join(BASE_DIR, "images", "products", "panini-grill.jpg"),
    target_size=(800, 800),
    crop_box=(0.15, 0.1, 0.85, 0.85),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "img-3.jpg"),
    os.path.join(BASE_DIR, "images", "products", "snack-fryer.jpg"),
    target_size=(800, 800),
    crop_box=(0.1, 0.1, 0.8, 0.85),
    badge_pos="top_left",
    badge_scale=125
)

# 9. BAKING & ROASTING
process_and_brand(
    os.path.join(BRAIN_DIR, "pizza_oven_cat_1793889066053.jpg"),
    os.path.join(BASE_DIR, "images", "products", "pizza-oven.jpg"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(BRAIN_DIR, "oven_cat_1793888970615.jpg"),
    os.path.join(BASE_DIR, "images", "products", "deck-oven.jpg"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "198660791_xl_normal_none.webp"),
    os.path.join(BASE_DIR, "images", "products", "convection-oven.jpg"),
    target_size=(800, 800),
    crop_box=(0.3, 0.1, 0.8, 0.7),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "Restaurant-Commercial-Kitchen-Equipment-List-A-Comprehensive-Guide.png"),
    os.path.join(BASE_DIR, "images", "products", "rotary-oven.jpg"),
    target_size=(800, 800),
    crop_box=(0.15, 0.05, 0.75, 0.65),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "img-4.webp"),
    os.path.join(BASE_DIR, "images", "products", "dough-proofer.jpg"),
    target_size=(800, 800),
    crop_box=(0.1, 0.1, 0.9, 0.9),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "shiny-steel-stove-heats-fresh-food-inside-generated-by-ai.jpg"),
    os.path.join(BASE_DIR, "images", "products", "drum-roaster.jpg"),
    target_size=(800, 800),
    crop_box=(0.4, 0.1, 0.95, 0.85),
    badge_pos="top_left",
    badge_scale=125
)

# 10. BEVERAGE & SPECIAL USE
process_and_brand(
    os.path.join(BRAIN_DIR, "coffee_machine_1793889410416.jpg"),
    os.path.join(BASE_DIR, "images", "products", "coffee-machine.png"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(BRAIN_DIR, "beverage_equipment_category_1793889569554.jpg"),
    os.path.join(BASE_DIR, "images", "products", "milk-boiler.jpg"),
    target_size=(800, 800),
    crop_box=(0.55, 0.2, 0.98, 0.9),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(BRAIN_DIR, "beverage_equipment_category_1793889569554.jpg"),
    os.path.join(BASE_DIR, "images", "products", "hot-dispenser.jpg"),
    target_size=(800, 800),
    crop_box=(0.25, 0.15, 0.75, 0.85),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "front-view-professional-kitchen.jpg"),
    os.path.join(BASE_DIR, "images", "products", "water-chiller.jpg"),
    target_size=(800, 800),
    crop_box=(0.6, 0.3, 0.98, 0.9),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "modern-kitchen-with-sleek-appliances-breakfast-bar.jpg"),
    os.path.join(BASE_DIR, "images", "products", "soda-system.jpg"),
    target_size=(800, 800),
    crop_box=(0.2, 0.3, 0.7, 0.85),
    badge_pos="top_left",
    badge_scale=125
)

# 11. COLD PREPARATIONS
process_and_brand(
    os.path.join(BRAIN_DIR, "commercial_electric_juicer_1793889525939.jpg"),
    os.path.join(BASE_DIR, "images", "products", "juicer.png"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(BRAIN_DIR, "sugarcane_machine_1793889593019.jpg"),
    os.path.join(BASE_DIR, "images", "products", "sugarcane-machine.png"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(BRAIN_DIR, "commercial_juicer_1793889482323.jpg"),
    os.path.join(BASE_DIR, "images", "products", "citrus-press.png"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "illustration-splash-ice-cream-scoop-waffle-cone-dark-background-generative-ai_843410-140.avif"),
    os.path.join(BASE_DIR, "images", "products", "ice-cream.avif"),
    target_size=(800, 800),
    badge_pos="top_left",
    badge_scale=125
)
process_and_brand(
    os.path.join(REF_DIR, "front-view-professional-kitchen.jpg"),
    os.path.join(BASE_DIR, "images", "products", "cold-counter.jpg"),
    target_size=(800, 800),
    crop_box=(0.0, 0.4, 0.45, 0.95),
    badge_pos="top_left",
    badge_scale=125
)

# 12. SERVICES
process_and_brand(
    os.path.join(BRAIN_DIR, "modular_kitchen_1793888877562.jpg"),
    os.path.join(BASE_DIR, "images", "services", "modular-kitchen.png"),
    target_size=(1200, 800),
    badge_pos="top_left",
    badge_scale=140
)
process_and_brand(
    os.path.join(REF_DIR, "male-shop-assistant-helps-young-couple-choose-new-home-appliance.jpg"),
    os.path.join(BASE_DIR, "images", "services", "consultation.jpg"),
    target_size=(1200, 800),
    crop_box=(0.1, 0.1, 0.9, 0.9),
    badge_pos="top_left",
    badge_scale=140
)
process_and_brand(
    os.path.join(REF_DIR, "shop-assistant-hypermarket-shows-new-model-gas-stove-young-couple-all-wearing-medical-masks.jpg"),
    os.path.join(BASE_DIR, "images", "services", "showroom.jpg"),
    target_size=(1200, 800),
    crop_box=(0.05, 0.05, 0.95, 0.95),
    badge_pos="top_left",
    badge_scale=140
)

# 13. ABOUT PAGE
process_and_brand(
    os.path.join(REF_DIR, "img-2.jpg"),
    os.path.join(BASE_DIR, "images", "about", "about-1.jpg"),
    target_size=(1200, 800),
    badge_pos="top_left",
    badge_scale=140
)
process_and_brand(
    os.path.join(REF_DIR, "img-3.jpg"),
    os.path.join(BASE_DIR, "images", "about", "about-2.jpg"),
    target_size=(1200, 800),
    badge_pos="top_left",
    badge_scale=140
)
process_and_brand(
    os.path.join(REF_DIR, "img-4.webp"),
    os.path.join(BASE_DIR, "images", "about", "about-3.webp"),
    target_size=(1200, 800),
    badge_pos="top_left",
    badge_scale=140
)

# 14. PROJECTS / OUR WORK
process_and_brand(
    os.path.join(BRAIN_DIR, "hotel_kitchen_project_1793888932609.jpg"),
    os.path.join(BASE_DIR, "images", "projects", "hotel-kitchen.png"),
    target_size=(1200, 800),
    badge_pos="top_left",
    badge_scale=140,
    dark_grade=True
)
process_and_brand(
    os.path.join(REF_DIR, "backside-chef-cooking-modern-restaurant-kitchen-backside-chef-cooking-modern-restaurant-kitchen-279366945.webp"),
    os.path.join(BASE_DIR, "images", "projects", "restaurant-kitchen-1.webp"),
    target_size=(1200, 800),
    crop_box=(0.0, 0.0, 1.0, 1.0),
    badge_pos="top_left",
    badge_scale=140
)
process_and_brand(
    os.path.join(REF_DIR, "backside-chef-cooking-modern-restaurant-kitchen-backside-chef-cooking-modern-restaurant-kitchen-279367841.webp"),
    os.path.join(BASE_DIR, "images", "projects", "restaurant-kitchen-2.webp"),
    target_size=(1200, 800),
    crop_box=(0.0, 0.0, 1.0, 1.0),
    badge_pos="top_left",
    badge_scale=140
)
process_and_brand(
    os.path.join(REF_DIR, "modern-kitchen-with-sleek-appliances-breakfast-bar.jpg"),
    os.path.join(BASE_DIR, "images", "projects", "modern-kitchen.jpg"),
    target_size=(1200, 800),
    crop_box=(0.05, 0.1, 0.95, 0.9),
    badge_pos="top_left",
    badge_scale=140
)

print("\n=== ALL BAKERO BRANDED ASSETS GENERATED SUCCESSFULLY! ===")
