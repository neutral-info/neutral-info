package main

import (
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

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
			}
			return nil
		},
	}

	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}
