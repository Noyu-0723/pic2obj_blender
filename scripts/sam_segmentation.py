# scripts/sam_segmentation.py
import os
from PIL import Image
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

# 設定
IMAGE_DIR    = "../assets/raw"
MASK_OUT_DIR = "../assets/masked"
CHECKPOINT   = "models/sam_vit_h_4b8939.pth"  # DLしておく

os.makedirs(MASK_OUT_DIR, exist_ok=True)

# モデル準備
sam = sam_model_registry["vit_h"](checkpoint=CHECKPOINT)
sam.to("cuda" if sam.device.type=="cuda" else "cpu")
mask_gen = SamAutomaticMaskGenerator(sam)

for fname in os.listdir(IMAGE_DIR):
    if not fname.lower().endswith((".png", ".jpg")):
        continue
    img_path = os.path.join(IMAGE_DIR, fname)
    image = Image.open(img_path).convert("RGB")
    image_np = np.array(image)
    masks = mask_gen.generate(image_np)

    # 最大エリアのマスクだけ保存
    largest = max(masks, key=lambda x: x["area"])
    mask = largest["segmentation"].astype(np.uint8) * 255
    mask_img = Image.fromarray(mask)
    mask_img.save(os.path.join(MASK_OUT_DIR, fname))
    print(f"Saved mask for {fname}")