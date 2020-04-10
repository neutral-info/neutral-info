# facebook group bot
此Image包含chrome、chromedriver、python+selenium及圖片OCR。

其中圖片OCR中需要的中文字訓練集，需另外建一個『tessdata』目錄。

# docker build
docker build -t facebookgroupbot .

# docker run
docker run -v /var/log:/app/output --name facebookgroupbot facebookgroupbot
