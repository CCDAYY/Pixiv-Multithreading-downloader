# Pixiv-Picture-Downloader
Three Download modes available


![image](![2d232d951aa92e85ac68dc54e10e35e](https://user-images.githubusercontent.com/70998992/209436827-ec02c14e-5b19-46a0-b596-19d2bb413af4.png))

* Searching with rank: Search tags with ranking
* Daily trending mode: Pixiv daily trending rank(automatic creat the folder , will not overlap the pervious day's folder)
* Normal Search : Download all picture followed by user input. (serval modes)

### 🔧 Installation

Download the executable binary file from [release](https://github.com/CCDAYY/Pixiv-Picture-Downloader/releases/latest) or [pre-release](https://github.com/CCDAYY/Pixiv-Picture-Downloader/releases/dev) (NOT STABLE !)

### 🔧 Build

1. Clone this repo 

    ```bash
    git clone https://github.com/CCDAYY/Pixiv-Picture-Downloader
    cd Pixiv-Picture-Downloader
    ```

2. Install dependent packages
    ```bash
    pip install -r requirements.txt
    pip install pyinstaller
    ```

3. Build

    ```bash
    pyinstall -F ./pixivDownloader.py
    ```

4. Enjoy!
