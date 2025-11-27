# utils.py
import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Simple banned words list for content filtering
BANNED_KEYWORDS = [
    "nude", "naked", "nsfw", "gore", "bloody", "violence", "sex"
]

def is_prompt_allowed(prompt: str) -> bool:
    lowered = prompt.lower()
    for word in BANNED_KEYWORDS:
        if word in lowered:
            return False
    return True

def add_watermark(image: Image.Image, text: str = "AI GENERATED"):
    img = image.copy()
    draw = ImageDraw.Draw(img)

    width, height = img.size
    font_size = int(width * 0.03)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # NEW: use textbbox instead of textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 10
    x = width - text_width - padding
    y = height - text_height - padding

    # Semi-transparent rectangle
    rect_x0 = x - 5
    rect_y0 = y - 5
    rect_x1 = x + text_width + 5
    rect_y1 = y + text_height + 5

    draw.rectangle((rect_x0, rect_y0, rect_x1, rect_y1), fill=(0, 0, 0, 128))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    return img


def save_image_with_metadata(
    image: Image.Image,
    base_dir: str,
    prompt: str,
    negative_prompt: str,
    params: dict,
    index: int = 0
):
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"img_{timestamp}_{index}"

    png_path = os.path.join(base_dir, filename_base + ".png")
    jpg_path = os.path.join(base_dir, filename_base + ".jpg")

    image.save(png_path, format="PNG")
    image.convert("RGB").save(jpg_path, format="JPEG", quality=95)

    metadata = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "timestamp": timestamp,
        "parameters": params,
        "files": {
            "png": png_path,
            "jpg": jpg_path
        }
    }

    metadata_path = os.path.join(base_dir, filename_base + ".json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    return png_path, jpg_path, metadata_path
