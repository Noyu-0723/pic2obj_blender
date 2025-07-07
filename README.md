# AI画像→3Dモデル(.obj)生成プロジェクト

このリポジトリは、Stable Diffusionで生成した2D画像から、ローカル環境（Windows）で無料ツールを用いて.obj形式の3Dモデルを作成する一連のワークフローを提供します。

## 目次
1. プロジェクト概要
2. フォルダ構造
3. 動作環境・前提条件
4. 環境構築手順
    - Python仮想環境の作成
    - 依存ライブラリのインストール
    - 各種モデルのダウンロード
5. 各ステップの実行方法
    1. 2D画像生成（Stable Diffusion Web UI）
    2. 背景除去・セグメンテーション（SAM）
    3. 深度推定（MiDaS）
    4. 3D復元①：TripoSRによる単一画像→メッシュ
    5. 3D復元②：Open3Dによる深度→メッシュ
    6. Blenderでの微調整（任意）
6. よくある質問 (FAQ)
7. ライセンス

## プロジェクト概要
#### 本プロジェクトでは以下を実現します：
- Stable Diffusionで建物、植物、地形などの2D画像を生成
- Segment Anything Model (SAM) で対象物のマスクを抽出
- MiDaSモデルでシーンの相対深度マップを推定
- TripoSRまたはOpen3Dを用いて3Dメッシュを復元
- 最終的に.obj/.mtl（テクスチャPNG）形式で出力
すべてWindows環境で完全ローカルかつ無料で実行できるよう設計しています。

## フォルダ構造
```bash
project_root/
├─ .venv/
├─ assets/
│   ├─ depth/                 # MiDaS深度マップ(.png/.npy)
│   ├─ raw/                   # SD等で生成した2D画像
│   └─ masked/                # SAM出力マスク(.png)
├─ mesh/
│   └─ from_depth/            # Open3D経由のメッシュ(.obj)
├─ scripts/
│   ├─ generate_image.md      # SD画像生成手順
│   ├─ sam_segmentation.py    # SAMマスク生成スクリプト
│   ├─ depth_estimation.py    # 深度推定スクリプト
│   ├─ run_triposr.sh         # TripoSR実行シェルスクリプト
│   └─ mesh_from_depth.py     # Open3Dメッシュ化スクリプト
├─ stable_diffusion-webui/
│   └─ outputs/               # 生成した画像
├─ TropoSR/
│   └─ outputs/               # TripoSR出力(.obj/.mtl/.png)
├─ README.md                  # 本ファイル
└─ requirements.txt           # Python依存ライブラリ一覧
```

## 動作環境・前提条件
- OS: Windows 10/11
- Python: 3.10.6
- CUDA（任意）: GPUを利用する場合はCUDA対応のNVIDIAドライバ＆Toolkit
- ディスク容量: モデルや中間データを含めて数GB以上
- メモリ: Pythonで依存ライブラリを動かすため 8GB以上推奨

## 環境構築手順
以下の手順でローカル環境を準備。

1. 2D画像生成（Stable Diffusion Web UI）
    1. mdfile/generate_image.md を参照し、Web UIを起動
    2. プロンプトを入力、生成画像を assets/raw/ に保存

2. 学習済みモデルのダウンロード
- (SAM)[https://huggingface.co/HCMUE-Research/SAM-vit-h/tree/main]: Meta公式ページから sam_vit_h_4b8939.pth を scripts/models/ に保存
- MiDaS: PyTorch Hubが自動ダウンロード

3. 背景除去・セグメンテーション
```bash
cd project_root/scripts
python sam_segmentation.py
```
assets/raw/*.png を読み込み、 segmentation/sam_masks/ にマスクを出力

4. 深度推定
```bash
cd project_root/scripts
python depth_estimation.py
```
assets/raw/*.png → depth/depth_maps/*.png + .npy

5. 3D復元①：TripoSR
scripts/generate_obj.mdを参照し、*.objを生成

6. 3D復元②：Open3D
```bash
cd project_root/scripts
python mesh_from_depth.py
```
depth/depth_maps/*.npy → mesh/from_depth/*.obj

7. Blenderでの微調整（任意）
    - Blenderを起動し、 .obj ファイルをインポート
    - スムーズシェーディング、スケール調整、不要頂点削除等を実施
    - 再度 .obj エクスポート

## よくある質問 (FAQ)
- Q: GPUがない場合は？→ CPUでも動作しますが、TripoSRなどは処理時間が大幅に増加します。
- Q: 複数角度からのモデル生成は？→ Stable Diffusionで視点違いの画像を複数生成し、Meshroomでフォトグラメトリを行うか、TripoSRで各角度ごとに生成→手動でマージします。

## ライセンス
本プロジェクトはMITライセンスのもと提供します。詳細は LICENSE ファイルを参照してください。