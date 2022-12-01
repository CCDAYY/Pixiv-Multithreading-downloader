# Pixiv-Picture-Downloader
Three Downloade modes available


![image](https://user-images.githubusercontent.com/70998992/199743393-9ae1f2b5-f953-4133-9224-55cbfd5f3884.png)

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