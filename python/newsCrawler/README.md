# news from api bot
1. 此新聞爬蟲主要是以 newsapi.org 所提供的新聞為抓取的對像。
2. 目前的規劃是抓取後，直接寫入資料庫 neutralinfo 中。
3. 針對『新聞標題』以 ckiptagger 進行切詞，取得關鍵字。

# prepare
1. settings_sample.toml 檔案請修改DB主機位置及帳密後，改寫後的檔名為 settings.toml

# docker build
docker build -t newscrawler .

# docker run
docker run -v /var/log/newscrawler:/app --name newscrawler newscrawler
