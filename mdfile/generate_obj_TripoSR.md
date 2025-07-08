## 1. TripoSRインストール
```bash
cd C:\Users\任意のパス
.\.venv_tripo\Scripts\Activate
python.exe -m pip install --upgrade pip
pip install --upgrade pip wheel setuptools
git clone https://github.com/VAST-AI-Research/TripoSR.git
cd TripoSR
set DISTUTILS_USE_SDK=1
# requirements.txtの中でgradioのバージョンを4.0.0に、huggingface-hubを0.17.3に指定してから次を実行
pip install -r requirements.txt
pip install onnxruntime
pip install "pydantic<2.0.0"
```
GPUを使わないなら以下のコマンドを実行
```bash
cd C:\Users\任意のパス
.\.venv_tripo\Scripts\Activate
python.exe -m pip install --upgrade pip
pip install --upgrade pip wheel setuptools
git clone https://github.com/VAST-AI-Research/TripoSR.git
cd TripoSR
set DISTUTILS_USE_SDK=1
# requirements.txtの中でgradioのバージョンを4.0.0に、huggingface-hubを0.17.3に指定してから次を実行
pip install -r requirements.txt
pip install onnxruntime
pip install "pydantic<2.0.0"
```

必要なら先に仮想環境も構築する
```bash
# プロジェクトルートで
cd C:\Users\任意のパス
py -3.9 -m venv .venv_tripo
# 有効化
.\.venv_tripo\Scripts\activate
```

## 2. 実行
Web上でGUI操作したい場合は以下を実行（http://127.0.0.1:7860）
```bash
python gradio_app.py
```

コマンドライン上で実行する場合
```bash
python run.py ../assets/raw/test.png --output-dir ../assets/obj/ --bake-texture --texture-resolution 1024
```
各種オプションの説明
- examples/chair.png: 入力画像
- --bake-texture: テクスチャ付きメッシュ出力
- --texture-resolution: テクスチャ画像の解像度設定
- 成果物は ../assets/obj/ フォルダ内に .obj、.mtl、テクスチャPNGなどとともに保存されます
- --use_gpu: GPUを指定するオプション（必要なら追加する）

## その他の環境について：Visual C++ ビルド環境の導入
### Visual C++ ビルド環境の導入
① Visual Studio Build Tools のインストール（必須）
(公式サイト)[https://visualstudio.microsoft.com/ja/visual-cpp-build-tools/] から Visual Studio Build Tools をダウンロード
以下を選択してインストール：
「C++によるデスクトップ開発」
「Python開発」
「Windows 10 SDK or Windows 11 SDK」
CMake、MSBuild、C++ CMake tools、Ninja もチェック

### CUDAとGPU環境の構築
- python = 3.9.0（x86-64 installerを使用）
- PyTorch = 利用したいCUDAと同じバージョン（今回は12.6）
- CUDA ToolKit = PyTorchで利用したいCUDAと同じバージョン（今回は12.6）
#### それぞれ、以下のサイトでインストール
Pythonインストール用(サイト)[https://www.python.org/downloads/release/python-390/]
Pytorchインストール用(サイト)[https://pytorch.org/get-started/locally/]
CUDA ToolKitインストール用(サイト)[https://developer.nvidia.com/cuda-toolkit-archive]

### 「nvidia-smi」の実行結果が利用したいCUDA ToolKitバージョン未満だった場合、以下のサイトからドライバーをアップデートする必要がある。
GPUドライバーアップデート用(サイト)[https://www.nvidia.com/ja-jp/drivers/]

### CUDA Toolkit 11.0 以降では、nvToolsExt は 単体ライブラリとして提供されるようになり、本体には含まれない仕様になっているため、それが含まれる個別ライブラリを別途ダウンロードする必要がある。
NVIDIA Nsight Systemsダウンロード用(サイト)[https://developer.nvidia.com/nsight-systems/get-started]

## トラブルシューティング
torchmcubesのビルドでエラーが発生する -> nvtx関連のファイルが見つからないことが原因だと思われる。
この場合、[torchmcubesのGitHub](https://github.com/tatsy/torchmcubes.git)から直接torchmcubesをインストールする必要がある。
実行するコマンドは以下の通り。
```bash
cd C:\Users\任意のパス
git clone https://github.com/tatsy/torchmcubes.git
cd torchmcubes
# ここで、torchmcubes/CMakeLists.txt の先頭に「set(USE_NVTX OFF CACHE BOOL "Disable NVTX support" FORCE)」を追加
pip install .
```
これを実行したのち、TripoSR/requirements.txtのtorchmcubesをインストールするための一行をコメントアウトしてからTripoSRディレクトリに移動してインストールすればOK。

それでもうまくいかない場合、C++関連のライブラリやツールが原因だと思われる。
「コマンドプロンプト」ではなく「x64 Native Tools command prompt for VS 2022」を使用してtorchmcubesのインストールをしてみると改善する可能性がある。

## 参考文献
https://weel.co.jp/media/tech/triposr/
https://note.com/oyasai123/n/n08ac06ea2691