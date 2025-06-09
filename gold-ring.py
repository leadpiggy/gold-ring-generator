#!/usr/bin/env python3
from pathlib import Path
import os
import cv2
from PIL import Image, ImageDraw

# --- CONFIGURATION ---
# (1) Path to your gold ring PNG (should be 800x800 with transparency)
RING_IMAGE = "/path-to/gold-ring.png"
# (2) Path to your test headshot image (can be any size)
TEST_IMAGE = "/path-to/test-headshot.jpg"

try:
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
except AttributeError:
    pkg_dir = os.path.dirname(cv2.__file__)
    cascade_path = os.path.join(pkg_dir, "data", "haarcascade_frontalface_default.xml")
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f"Haar cascade not found at {cascade_path}")

# --- IMAGE PROCESSING FUNCTIONS ---

def detect_face_crop_square(img_path: str) -> Image.Image:
    """
    Load with OpenCV, detect the largest face, 
    then return a PIL Image cropped to a square
    centered on the face. If no face is found,
    do a simple center-square crop.
    """
    # Load image via OpenCV
    cv_img = cv2.imread(img_path)
    gray  = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    h_img, w_img = gray.shape

    # Run face detection
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if len(faces) > 0:
        # Pick the largest face
        x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
        cx, cy = x + w // 2, y + h // 2
    else:
        # Fallback to image center
        cx, cy = w_img // 2, h_img // 2

    # Determine square side = min(img width, img height)
    side = min(w_img, h_img)
    half = side // 2

    # Compute square top-left corner
    left = max(0, min(w_img - side, cx - half))
    top  = max(0, min(h_img - side, cy - half))

    # Convert BGR→RGB and crop via PIL
    pil_img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
    return pil_img.crop((left, top, left + side, top + side))


def circular_mask(size: int) -> Image.Image:
    """Generate a white-on-black circular mask of given size."""
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    return mask


def compose_with_ring(headshot_path: str):
    # 1) Crop
    head_square = detect_face_crop_square(headshot_path)

    # 2) Load ring & define target size
    ring = Image.open(RING_IMAGE).convert("RGBA")
    target_size = ring.width  # should be 800

    # 3) Resize head & apply circular alpha
    head_resized = head_square.resize(
        (target_size, target_size),
        Image.Resampling.LANCZOS
    )
    mask = circular_mask(target_size)
    head_resized.putalpha(mask)

    # 4) Composite
    canvas = Image.new("RGBA", (target_size, target_size), (0,0,0,0))
    canvas.paste(head_resized, (0, 0), head_resized)
    canvas.paste(ring,         (0, 0), ring)

    # 5) Save
    stem = Path(headshot_path).stem
    output_file = f"{stem}_with-ring.png"
    canvas.save(output_file)
    print(f"✅ Saved: {output_file}")

# --- TEST FUNCTIONS ---
def argparse_test():
    """
    Simple argparse test to verify the function works.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Compose headshot with a gold ring overlay.")
    parser.add_argument("headshot", type=str, help="Path to the headshot image")
    args = parser.parse_args()
    
    compose_with_ring(args.headshot)

def test_image_test():
    """
    Simple console test to verify the function works.
    """
    print("Testing with hardcoded image path...")
    compose_with_ring(TEST_IMAGE)

# --- ENTRY POINT ---
if __name__ == "__main__":
    test_image_test()