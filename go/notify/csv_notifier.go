package main

import (
	"github.com/BurntSushi/toml"
	"gopkg.in/fsnotify.v1"
	"log"
	"time"
	
	
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
			//timeout := time.After(1)
			select {
			

			case event := <-watcher.Events:
				log.Println("event:", event)
				if event.Op&fsnotify.Write == fsnotify.Write {
					log.Println("modified file:", event.Name)
				}
			case err := <-watcher.Errors:
				log.Println("error:", err)
				
				
			case <-time.After(time.Second * 2):
				log.Println("heartbeat")				
				
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
