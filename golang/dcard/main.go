package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path"
	"public-opinion/dcard/models"

	"github.com/jasonlvhit/gocron"

	"github.com/gocolly/colly"
	"github.com/urfave/cli/v2"
)

const dataFolder = "./data"

func crawlAllForums() {
	c := colly.NewCollector()

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL)
	})

	c.OnResponse(func(r *colly.Response) {
		fmt.Println("Visited", r.Request.URL)
		forums := r.Body
		var forumData []models.Forum
		json.Unmarshal(forums, &forumData)
		f, err := os.OpenFile(path.Join(dataFolder, "forums.jsonl"), os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		defer f.Close()
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

func crawlLatestPosts() {
	c := colly.NewCollector()

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL)
	})

	c.OnResponse(func(r *colly.Response) {
		fmt.Println("Visited", r.Request.URL)
		posts := r.Body
		var postData []models.Post
		json.Unmarshal(posts, &postData)
		f, err := os.OpenFile(path.Join(dataFolder, "posts.jsonl"), os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

		defer f.Close()
		if err != nil {
			log.Fatal(err)
		}

		for _, line := range postData {
			jsonData, _ := json.Marshal(line)
			if _, err := f.Write(append(jsonData, '\n')); err != nil {
				log.Fatal(err)
			}
		}
		if err := f.Close(); err != nil {
			log.Fatal(err)
		}
	})

	c.Visit("https://www.dcard.tw/_api/posts?limit=100")
}

func crawl() {
	os.RemoveAll("data")
	os.MkdirAll("data", os.ModePerm)

	crawlAllForums()
	crawlLatestPosts()
}

func main() {
	app := &cli.App{
		Name:  "dcard-crawler",
		Usage: "crawl dcard latest articles",
		Flags: []cli.Flag{&cli.BoolFlag{
			Name:    "schedule",
			Usage:   "Run every 2 hours",
			Aliases: []string{"s"},
		}},
		Action: func(ctx *cli.Context) error {
			if ctx.Bool("schedule") {
				fmt.Println("Schedule every 2 hours")
				gocron.Every(2).Hours().From(gocron.NextTick()).Do(crawl)
				<-gocron.Start()
			} else {
				crawl()
			}
			return nil
		},
	}

	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}
