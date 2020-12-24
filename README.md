# neutral-info

# 系統起動步驟
1. MySql的結構會在Docker起動時一併建立，系統運作所需的起始資料，則請手動匯入 mysql_init_data.sql
2. 請記得先修改 docker-compose.yml 中 db 區的帳密