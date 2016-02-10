/*



 */

package main

import (
	"github.com/BurntSushi/toml"
	"github.com/go-fsnotify/fsnotify"
	"log"
	"time"
)

type conf struct {
	App app
}

type app struct {
	Dir    string
	Target string
	//Heartbeat int
}

func main() {

	var config conf
	_, err := toml.DecodeFile("config.toml", &config)

	dir := config.App.Dir
	//heartbeat := config.App.Heartbeat

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
