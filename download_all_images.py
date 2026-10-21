#!/usr/bin/env python3
"""
Hot Wheels Image Harvester & Asset Localizer
===========================================
1. Resolves all 46 missing / placeholder images using base casting fallbacks and wiki pages.
2. Downloads all images via curl with proper Referer headers into ./images/.
3. Validates that every downloaded file is a genuine image (WebP/JPEG/PNG) and NOT an HTML challenge page.
4. Populates cases_2026_full.json with local relative image paths.
"""

import os
import re
import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

with open("cases_2026_full.json", "r", encoding="utf-8") as f:
    cases = json.load(f)

# Verified casting fallback images for models that lack 2026 photos
CASTING_FALLBACKS = {
    "089": "https://static.wikia.nocookie.net/hotwheels/images/0/05/1985_Honda_CR-X_-_2020_Muscle_Mania.jpg/revision/latest",
    "155": "https://static.wikia.nocookie.net/hotwheels/images/a/a2/Vairstrike_White.jpg/revision/latest",
    "211": "https://static.wikia.nocookie.net/hotwheels/images/c/c5/1972_Datsun_Sunny_Coupe_-_2022_Compact_Kings.jpg/revision/latest",
    "218": "https://static.wikia.nocookie.net/hotwheels/images/8/82/Alfa_Romeo_Giulia_Sprint_GTA.jpg/revision/latest",
    "222": "https://static.wikia.nocookie.net/hotwheels/images/0/0d/Tooned_Supra_Red.jpg/revision/latest",
    "225": "https://static.wikia.nocookie.net/hotwheels/images/a/a2/Nissan_Maxima_Drift_Car_-_2022_HW_Drift.jpg/revision/latest",
    "244": "https://static.wikia.nocookie.net/hotwheels/images/3/30/Skyline2000GTX.jpg/revision/latest",
    "245": "https://static.wikia.nocookie.net/hotwheels/images/c/c7/70_Plymouth_AAR_Cuda_-_2017_HW_Flames.jpg/revision/latest",
    "247": "https://static.wikia.nocookie.net/hotwheels/images/0/06/HW_Gazella-GT_Red_2016_01_sm_DSCF8063.jpg/revision/latest",
    "249": "https://static.wikia.nocookie.net/hotwheels/images/e/ea/67_Pontiac_Firebird_400_Black.jpg/revision/latest",
}

# 1st pass: collect primary valid images from the dataset
base_img_by_col = {}
base_img_by_name = {}

for code, data in cases.items():
    for car in data["cars"]:
        img = car.get("img", "")
        if img and "Image_Not_Available" not in img and not car.get("is_recolor"):
            base_img_by_col[car["col"]] = img
            clean_name = re.sub(r"\s*\([^)]*\)", "", car["name"]).strip().lower()
            base_img_by_name[clean_name] = img

print(f"Collected {len(base_img_by_col)} primary casting images.")

# 2nd pass: resolve fallbacks and map every car to local file
resolved_count = 0
for code, data in cases.items():
    for car in data["cars"]:
        img = car.get("img", "")
        if not img or "Image_Not_Available" in img:
            col = car["col"]
            clean_name = re.sub(r"\s*\([^)]*\)", "", car["name"]).strip().lower()
            if col in CASTING_FALLBACKS:
                car["img"] = CASTING_FALLBACKS[col]
                resolved_count += 1
            elif col in base_img_by_col:
                car["img"] = base_img_by_col[col]
                resolved_count += 1
            elif clean_name in base_img_by_name:
                car["img"] = base_img_by_name[clean_name]
                resolved_count += 1

        safe_toy = re.sub(r"[^a-zA-Z0-9_-]", "_", car["toy"])
        safe_col = car["col"]
        local_filename = f"car_{safe_col}_{safe_toy}.webp"
        car["local_img"] = f"images/{local_filename}"

print(f"Resolved {resolved_count} missing images with verified fallbacks.")

def make_fandom_url(url, width=400):
    if "/scale-to-width-down/" in url:
        return re.sub(r"/scale-to-width-down/\d+", f"/scale-to-width-down/{width}", url)
    elif "?cb=" in url:
        parts = url.split("?cb=")
        return f"{parts[0]}/scale-to-width-down/{width}?cb={parts[1]}"
    elif "/revision/latest" in url:
        parts = url.split("/revision/latest")
        return f"{parts[0]}/revision/latest/scale-to-width-down/{width}{parts[1]}"
    return url

def is_valid_image(filepath):
    if not os.path.exists(filepath) or os.path.getsize(filepath) < 100:
        return False
    try:
        with open(filepath, "rb") as f:
            header = f.read(16)
        if header.startswith(b"RIFF") and b"WEBP" in header:
            return True
        if header.startswith(b"\xff\xd8\xff"):
            return True
        if header.startswith(b"\x89PNG"):
            return True
    except Exception:
        pass
    return False

# Clean out any invalid / HTML files currently in images/
removed_bad = 0
for fname in os.listdir(IMAGES_DIR):
    fpath = os.path.join(IMAGES_DIR, fname)
    if os.path.isfile(fpath) and not is_valid_image(fpath):
        os.remove(fpath)
        removed_bad += 1
if removed_bad:
    print(f"Cleaned up {removed_bad} corrupt / HTML placeholder files from ./{IMAGES_DIR}/")

# Unique URLs download mapping
# Map URL -> list of target filenames
url_to_targets = {}
for code, data in cases.items():
    for car in data["cars"]:
        img = car["img"]
        fname = os.path.basename(car["local_img"])
        if img not in url_to_targets:
            url_to_targets[img] = []
        url_to_targets[img].append(fname)

print(f"Total unique images to fetch from Fandom: {len(url_to_targets)}")

def download_and_distribute(item):
    url, targets = item
    primary_target = os.path.join(IMAGES_DIR, targets[0])
    
    # If primary already exists and is valid, just distribute
    if not is_valid_image(primary_target):
        scaled_url = make_fandom_url(url, width=400)
        cmd = [
            "curl", "-s", "-L",
            "-H", "Referer: https://hotwheels.fandom.com/",
            "--max-time", "15",
            scaled_url,
            "-o", primary_target
        ]
        try:
            subprocess.run(cmd, check=True)
        except Exception:
            pass
        
        # If scaled failed, try raw url
        if not is_valid_image(primary_target):
            cmd[-2] = url
            try:
                subprocess.run(cmd, check=True)
            except Exception:
                pass

    if not is_valid_image(primary_target):
        if os.path.exists(primary_target):
            os.remove(primary_target)
        return False, url, targets

    # Copy to any other targets that share this image
    for extra in targets[1:]:
        extra_path = os.path.join(IMAGES_DIR, extra)
        if not is_valid_image(extra_path):
            shutil.copyfile(primary_target, extra_path)
            
    return True, url, targets

print("Starting parallel download with 8 workers...")
with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(download_and_distribute, url_to_targets.items()))

success_count = sum(1 for r in results if r[0])
failed = [r for r in results if not r[0]]

print(f"✅ Successfully downloaded {success_count} / {len(url_to_targets)} unique images.")
if failed:
    print(f"⚠️ {len(failed)} images failed to download:")
    for f in failed:
        print("  -", f[1], f[2])

# Verify total images in images/
valid_images_on_disk = [
    f for f in os.listdir(IMAGES_DIR)
    if is_valid_image(os.path.join(IMAGES_DIR, f))
]
print(f"📦 Total verified valid images in ./{IMAGES_DIR}/: {len(valid_images_on_disk)} / 366")

# Save updated dataset
with open("cases_2026_full.json", "w", encoding="utf-8") as f:
    json.dump(cases, f, indent=2)

print("✅ Saved cases_2026_full.json with complete local image paths!")
