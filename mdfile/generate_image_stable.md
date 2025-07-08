## 必要なら先に仮想環境を構築する
```bash
# プロジェクトルートで
cd C:\Users\任意のパス
py -3.10 -m venv .venv_stable
# 有効化
.\.venv_stable\Scripts\activate
```

## 1. 依存ライブラリのインストール
```bash
python -m pip install --upgrade pip wheel setuptools
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
```

## 2. モデルのインストール
[Stable Diffusion](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/tree/main): SD1.5等の.ckptファイルを stable-diffusion-webui/models/Stable-diffusion/ に配置（.3実行後）

## 3. Web UIインストール
```bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui
```

## 4. 起動(必要なライブラリのインストールも自動的に実行される)
```bash
python launch.py
# CPUのみで動かす場合は下の方を実行
# python launch.py --skip-torch-cuda-test --no-half --precision full
```
webui-user.batをダブルクリックしても起動できる

## 5. プロンプト例
- 建物: `“現代的なガラス張りの高層ビル、夕暮れ時、リアルな質感”`
- 道具: `“鉄製の古いランプ、錆びたディテール、クローズアップ写真風”`
- 植物: `“森の中の苔むした古木、朝の霧、超高解像度”`
- 地形: `“山と道、空から見下ろした風景、リアルな航空写真風”`

## 6. 保存
出力されたPNGを `../assets/raw/` に移動（必要なら）

### トラブルシューティング
必要なら以下を実行して、デフォルトエンコーディング設定を変更する
```bash
set PYTHONIOENCODING=utf-8
```

GITの環境変数を設定していない場合はダウンロードして設定する
[gitの公式サイト](https://gitforwindows.org/)

gitのセキュリティ関連のエラーが発生した場合は、以下を実行してリポジトリを信用する設定に変更する
※安全なリポジトリであることを確認してから実行する
```bash
git config --global --add safe.directory "C:/Users/user/Desktop/t5422043/pic2obj_blender"
git config --global --add safe.directory "C:/Users/user/Desktop/t5422043/pic2obj_blender/stable-diffusion-webui"
git config --global --add safe.directory "C:/Users/user/Desktop/t5422043/pic2obj_blender/stable-diffusion-webui/repositories"
git config --global --add safe.directory "C:/Users/user/Desktop/t5422043/pic2obj_blender/stable-diffusion-webui/repositories/BLIP"
git config --global --add safe.directory "C:/Users/user/Desktop/t5422043/pic2obj_blender/stable-diffusion-webui/repositories/k-diffusion"
git config --global --add safe.directory "C:/Users/user/Desktop/t5422043/pic2obj_blender/stable-diffusion-webui/repositories/stable-diffusion-stability-ai"
git config --global --add safe.directory "C:/Users/user/Desktop/t5422043/pic2obj_blender/stable-diffusion-webui/repositories/stable-diffusion-webui-assets"
git config --global --add safe.directory "C:/Users/user/Desktop/t5422043/pic2obj_blender/stable-diffusion-webui/repositories/generative-models"
```