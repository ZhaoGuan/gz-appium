## 输入法应用自动化回归用例代码

### 若想在本地执行脚本，需要安装如下依赖
1. 安装`node.js`  
	`brew install node`  
2. 安装`appium`  
    `npm install -g appium@1.6.3`
3. tesseract-ocr

    Tesseract的OCR引擎目前已作为开源项目发布在Google Project，其项目主页在这里查看https://github.com/tesseract-ocr，
    它支持中文OCR，并提供了一个命令行工具。python中对应的包是pytesseract. 通过这个工具我们可以识别图片上的文字。

    安装：
    * WINDOWS: https://github.com/tesseract-ocr/tesseract/wiki/Downloads
    * Ubuntu: sudo apt-get install tesseract-ocr
    * MAC: brew install tesseract  安装python包 sudo pip install pytesseract  tesseract-ocr已经提供了多种语言训练文本，当识别中文时，
    * 我们需要下载训练文件“chi_sim.traineddata”从下面的链接（https://github.com/tesseract-ocr/tessdata), 然后拷贝到安装路径下的tessdata文件 夹下，
    比如Ubuntu"/usr/share/tesseract-ocr/tessdata"
4. 安装`python lib`
	* pillow
	* pyorc
	* Appium-Python-Client
	* pytesseract(安装后还需要去下载traineddata文件地址https://github.com/tesseract-ocr/tessdata，放入
    * PyYAML

    `pip3 install -g Pillow pyorc Appium-Python-Client pytesseract PyYAML`

5.安装`python mitmproxy`
    * pip install mitmproxy