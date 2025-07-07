import os, cv2
import numpy as np
import torch

# 入出力フォルダ（プロジェクトルート基準）
IMAGE_DIR     = "../assets/masked"
DEPTH_OUT_DIR = "../assets/depth"
os.makedirs(DEPTH_OUT_DIR, exist_ok=True)

# MiDaSモデル読み込み
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
midas = torch.hub.load("intel-isl/MiDaS", "DPT_Hybrid").to(device).eval()

# 変換関数（直接 Tensor を返す）
transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform

for fname in os.listdir(IMAGE_DIR):
    if not fname.lower().endswith(".png"):
        continue

    # 1) 入力画像を NumPy(BGR→RGB) で読み込み
    img_path = os.path.join(IMAGE_DIR, fname)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 2) transform で [1,3,H,W] Tensor を取得し、デバイスへ
    inp = transform(img).to(device)

    # 3) 推論 → 出力は [1, H', W'] の Tensor になる
    with torch.no_grad():
        prediction = midas(inp)                 # shape: [1, H', W']
        # 元画像サイズに合わせて補間（予測は畳み込みネット部の出力）
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),            # → [1,1,H',W']
            size=img.shape[:2],                 # (H, W)
            mode="bicubic",
            align_corners=False
        ).squeeze()                             # → [H, W]

    # 4) NumPy 化 & 正規化（0–255）
    depth = prediction.cpu().numpy()
    d_norm = ((depth - depth.min()) / (depth.max() - depth.min()) * 255).astype(np.uint8)

    # 5) 保存
    cv2.imwrite(os.path.join(DEPTH_OUT_DIR, fname), d_norm)
    np.save(os.path.join(DEPTH_OUT_DIR, fname[:-4] + ".npy"), depth)
    print(f"[OK] Saved depth for {fname}")
