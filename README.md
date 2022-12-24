# Pixiv-Picture-Downloader
Three Download modes available
![image](https://user-images.githubusercontent.com/70998992/209436827-ec02c14e-5b19-46a0-b596-19d2bb413af4.png)
![image](https://user-images.githubusercontent.com/70998992/209436895-a1f09a0e-185c-4b17-b73d-b6d7879c45ee.png)

* Searching with rank: Search tags with ranking
* Daily trending mode: Pixiv daily trending rank(automatic creat the folder , will not overlap the pervious day's folder)
* Normal Search : Download all picture followed by user input. (serval modes)
* 

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

***Note: If you are in country which cannot access pixiv.net please use VPN as well as turn on the TUN Mode as well!!!!
