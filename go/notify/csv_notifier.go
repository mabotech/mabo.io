package main

import (
	"github.com/BurntSushi/toml"
	"gopkg.in/fsnotify.v1"
	"log"
	//"github.com/howeyc/fsnotify"
)

type conf struct {
	App app
}

type app struct {
	Dir string

	Target string
}

func main() {

	var config conf
	_, err := toml.DecodeFile("config.toml", &config)

	dir := config.App.Dir

	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal(err)
	}

	done := make(chan bool)

	// Process events
	go func() {
		for {
			select {
			case ev := <-watcher.Events:
				log.Println("event:", ev)
			case err := <-watcher.Errors:
				log.Println("error:", err)
			}
		}
	}()

	log.Println(dir)
	target := config.App.Target

	log.Println(target)
	err = watcher.Add(dir)
	if err != nil {
		log.Fatal(err)
	}

	<-done

	/* ... do stuff ... */
	watcher.Close()
}
