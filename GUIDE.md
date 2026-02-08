# 🛸 YDLidar X2 Python Master Guide

Is guide mein maine YDLidar X2 ko Python (3.10) ke saath stable tarike se setup karne ka pura process documentation kiya hai.
---

##  1. System Requirements & Environment
Sabse pehle system ko dependencies ke saath tayyar karein. maine Ubuntu pe Python 3.10 use kiya hai kyunki SDK C++ wrappers ispe best chalti hain.



```bash
# 1. System toolkit install karna hoga

sudo apt-get update
sudo apt-get install -y git cmake build-essential python3.10-dev python3.10-tk

# 2. Virtual environment (System packages allow karna zaroori hai Tkinter ke liye)
# dekho virtual enviroment can be frustrating but uske bina orr bhi frustration hogi

python3.10 -m venv --system-site-packages ydlidar_py
source ydlidar_py/bin/activate

# 3. Required Python libraries
pip install matplotlib numpy



# 🛰️ YDLidar X2 Python SDK: Complete Developer's Guide

YDLidar X2 ek affordable triangle-based 2D LiDAR hai. Is guide mein humne SDK ke gaps ko fill kiya hai aur ek stable development environment banane ka tarika bataya hai.



---

## 🏗️ 1. Quick Installation (The Pro Way)

Naye system par in commands ko sequence mein chalana:

```bash
# System dependencies
sudo apt-get update
sudo apt-get install -y git cmake build-essential python3.10-dev python3.10-tk

# Build and Install SDK
git clone [https://github.com/YDLidar/YDLidar-SDK.git](https://github.com/YDLidar/YDLidar-SDK.git)
mkdir -p YDLidar-SDK/build && cd YDLidar-SDK/build
cmake .. && make && sudo make install
cd ../..

# Setup Virtual Environment
python3.10 -m venv --system-site-packages ydlidar_py
source ydlidar_py/bin/activate
pip install matplotlib numpy

# Fix Python Wrapper (Copying compiled binaries)
cp /usr/local/lib/python3.10/site-packages/ydlidar.py ./ydlidar_py/lib/python3.10/site-packages/
cp /usr/local/lib/python3.10/site-packages/_ydlidar.so ./ydlidar_py/lib/python3.10/site-packages/
```
