# facebook group bot
1. 此Image包含chrome、chromedriver、python+selenium及圖片OCR。

# prepare
1. 其中圖片OCR中需要的中文字訓練集，需另外建一個『tessdata』目錄。
2. 在Home目錄下要先建一個botdata目錄
3. settings_sample.toml 檔案請修改帳密後，改寫檔名為 settings.toml

# docker build
docker build -t facebookgroupbot .

# docker run
docker run -v /var/log/facebookbookgroup:/app --name facebookgroupbot facebookgroupbot
