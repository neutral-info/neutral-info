package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/gocolly/colly"
)

// Forum is the forum description forum Dcard
type Forum struct {
	Alias             string `json:"alias"`             // "midnightlab"
	Name              string `json:"name"`              // "午夜實驗室"
	Description       string `json:"description"`       // "午夜實驗室10/6、10/7即將在華山登場！這裏提供大家交流活動資訊與討論，請大家要遵守 Dcard 板規喔！"
	SubscriptionCount string `json:"subscriptionCount"` // 1842
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
