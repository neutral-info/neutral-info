＃ botdata format
# 主要格式是JSON
# 搭配filebeat匯入的特性，所以每一筆資料必需在一行內
例子：
{"sys_id": "facebookgroup_2065219296931017_2745133162272957", "sys_type": "facebookgroup", "board_id": "2065219296931017", "post_id": "2745133162272957", "post_time": 1586477286, "post_person": "100009285067790", "post_message": "內容", "postComment": [{"comment_person": "100008336117291", "comment_message": "回文內容", "comment_time": "1586566959"}], "emoji": {"allEmoji": 20, "goodEmoji": 19, "haEmoji": 0, "waEmoji": 0, "heartEmoji": 0, "angryEmoji": 0, "cryEmoji": 0}},

# 以下格式化顯示，以便檢視規則
{
    "sys_id": "facebookgroup_2065219296931017_2748575538595386",
    "sys_type": "facebookgroup",
    "board_id": "2065219296931017",
    "post_id": "2748575538595386",
    "post_time": 1586615771,
    "post_person": "100000239611720",
    "post_message": "內容",
    "postComment": [
        {
            "comment_person": "100003358377261",
            "comment_message": "Sticker",
            "comment_time": "1586616194"
        },
        {
            "comment_person": "100005239331678",
            "comment_message": "回文內容",
            "comment_time": "1586618146"
        }
    ],
    "emoji": {
        "allEmoji": 0,
        "goodEmoji": 42,
        "haEmoji": 0,
        "waEmoji": 0,
        "heartEmoji": 0,
        "angryEmoji": 0,
        "cryEmoji": 0
    }
},


# 以下列出說明，每一行的底下就是對應的說明
{
    "sys_id": "facebookgroup_2065219296931017_2748575538595386",
    **說明：混合"sys_type"+"board_id"+"post_id"三欄而成，目的是給elasticsearch做為 document_id**
    "sys_type": "facebookgroup",
    **說明：用於標示這筆資料的來源**
    **清單：臉書社團->facebookgroup，PTT->ptt，IG->ig，Pixnet->pixnet，Dcard->dcard**
    "board_id": "2065219296931017",
    **說明：版面、社團在所在資料來源給予的識別碼**
    **例子：在臉書就是社團、粉絲團，IG就是頁面主人，PTT就是Gossiping、HatePolitics，Pixnet就是博主**
    "post_id": "2748575538595386",
    **說明：單篇文章系統給予的識別碼**
    "post_time": 1586615771,
    **說明：文章發表時間，以timestamp標示**
    "post_person": "100000239611720",
    **說明：文章發表者於系統給予的識別碼**
    "post_message": "內容",
    **說明：文章的內容**
    "postComment": [
    **說明：對於文章其它人的回應，回文以陣列儲存**
        {
            "comment_person": "100003358377261",
            **說明：回文發表者於系統給予的識別碼**
            "comment_message": "Sticker",
            **說明：回文的內容**
            "comment_time": "1586616194"
            **說明：回文的發表時間，以timestamp標示**
        },
        {
            "comment_person": "100005239331678",
            "comment_message": "回文內容",
            "comment_time": "1586618146"
        }
    ],
    "emoji": {
    **說明：用於存放情緒統計資料**
    **備註：目前臉書可應用的較多，是否其它系統都參考此？**
        "allEmoji": 0,
        **說明：全部情緒總計**
        "goodEmoji": 42,
        **說明：開心**
        "haEmoji": 0,
        **說明：哈**
        "waEmoji": 0,
        **說明：哇**
        "heartEmoji": 0,
        **說明：愛心**
        "angryEmoji": 0,
        **說明：生氣**
        "cryEmoji": 0
        **說明：哭**
    }
},