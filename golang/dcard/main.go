package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/gocolly/colly"
)

// Forum is the forum of Dcard
type Forum struct {
	Alias             string `json:"alias"`             // "midnightlab"
	Name              string `json:"name"`              // "午夜實驗室"
	Description       string `json:"description"`       // "午夜實驗室10/6、10/7即將在華山登場！這裏提供大家交流活動資訊與討論，請大家要遵守 Dcard 板規喔！"
	SubscriptionCount int    `json:"subscriptionCount"` // 1842
	CreatedAt         string `json:"createdAt"`         //"2016-05-14T19:15:15.698Z"
	UpdatedAt         string `json:"updatedAt"`         //"2018-11-05T03:24:32.914Z"
	Invisible         bool   `json:"invisible"`
	IsSchool          bool   `json:"isSchool"`
	FullyAnonymous    bool   `json:"fullyAnonymous"`
	CanUseNickname    bool   `json:"canUseNickname"`
	PostThumbnail     struct {
		Size string `json:"size"` // "small
	} `json:"postThumbnail"`
	ShouldCategorized    bool     `json:"shouldCategorized"`    // false
	TitlePlaceholder     string   `json:"titlePlaceholder"`     // ""
	PostTitlePlaceholder string   `json:"postTitlePlaceholder"` // ""
	Topics               []string `json:"topics"`               // 午夜實驗室
	Nsfw                 bool     `json:"nsfw"`                 //false
	PostCount            struct {
		Last30Days int `json:"last30Days"`
	} `json:"postCount"`
}

// Post is the post data structure of Dcard
type Post struct {
	ID                string `json:"id"`                // "63a0d93e-acc5-4664-b55a-81e6fe0a4d88",
	Alias             string `json:"alias"`             // "csu",
	Name              string `json:"name"`              // "正修科大",
	Description       string `json:"description"`       // "正修科大板，一個能讓你暢所欲言的地方。在這裡，卡友們可以盡情討論校園裡的大小事，舉凡課程資訊、教授教學評價，又或是學校活動，只要是你想要知道的資訊，都能在校板中迅速獲得解答！",
	SubscriptionCount int    `json:"subscriptionCount"` // 5256
	Subscribed        bool   `json:"subscribed"`
	Read              bool   `json:"read"`
	CreatedAt         string `json:"createdAt"` // "2016-06-29T02:36:10.703Z"
	UpdatedAt         string `json:"updatedAt"` // "2019-09-26T10:24:23.553Z"
	CanPost           bool   `json:"canPost"`
	IgnorePost        bool   `json:"ignorePost"`
	Invisible         bool   `json:"invisible"`
	IsSchool          bool   `json:"isSchool"`
	FullyAnonymous    bool   `json:"fullyAnonymous"`
	CanUseNickname    bool   `json:"canUseNickname"`
	PostThumbnail     struct {
		Size string `json:"size"` // "small"
	} `json:"postThumbnail"`
	ShouldCategorized    bool     `json:"shouldCategorized"`
	TitlePlaceholder     string   `json:"titlePlaceholder"`     // ""
	PostTitlePlaceholder string   `json:"postTitlePlaceholder"` // ""
	IPCountryCondition   struct{} `json:"ipCountryCondition"`
	Subcategories        []string `json:"subcategories"` // ["課程評價"]
	Topics               []string `json:"topics"`
	Nsfw                 bool     `json:"nsfw"`
	MediaThreshold       struct{} `json:"mediaThreshold"`
	LimitCountries       int      `json:"limitStage"`
	AvailableLayouts     []string `json:"availableLayouts"` // ["classic"]
	HeroImage            struct {
		URL    string `json:"url"`    // "https://megapx-assets.dcard.tw/images/26ca693f-e13f-4342-9dc4-ff0de3dd32d5/orig.jpeg"
		Type   string `json:"type"`   // "image/jpeg"
		Width  int    `json:"width"`  // 1800
		Height int    `json:"height"` // 600
	} `json:"heroImage"`
	Logo struct {
		URL    string `json:"url"`    // "https://megapx-assets.dcard.tw/images/0cc0d5ae-535f-4e65-bddb-aa4aed767f05/orig.jpeg",
		Type   string `json:"type"`   // "image/jpeg"
		Width  int    `json:"width"`  // 200
		Height int    `json:"height"` // 200
	} `json:"logo"`
	PostCount struct {
		Last30Days int `json:"last30Days"` // 168
	} `json:"postCount"`
	Favorite bool `json:"favorite"`
}

func main() {
	c := colly.NewCollector()

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL)
	})

	c.OnResponse(func(r *colly.Response) {
		fmt.Println("Visited", r.Request.URL)
		forums := r.Body
		var forumData []Forum
		json.Unmarshal(forums, &forumData)
		fmt.Println(forumData)
		f, err := os.OpenFile("forums.jsonl", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			log.Fatal(err)
		}
		for _, line := range forumData {
			jsonData, _ := json.Marshal(line)
			if _, err := f.Write(append(jsonData, '\n')); err != nil {
				log.Fatal(err)
			}
		}
		if err := f.Close(); err != nil {
			log.Fatal(err)
		}
	})

	c.Visit("https://www.dcard.tw/_api/forums")
}
