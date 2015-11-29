package main

import (
	"fmt"
	"net"
	"time"
	"log"
)

/* 
TODO

- config, etcd?
- log

*/

func main() {

	//host := os.Args[1]
	
	
	
	var url string = "127.0.0.1:1337"
	
	log.Println(url)
	
	conn, err := net.Dial("tcp", url)
	
	checkError(err)

	ticker := time.NewTicker(1000 * time.Millisecond)
	quit := make(chan struct{})

	done := make(chan bool)
	t1 := time.Now().UnixNano()
	go func() {
		for {
			select {
			case <-ticker.C:
				// do stuff
				_, err = conn.Write([]byte("HEAD"))

				if err != nil {

					fmt.Println(err)
					// reconnect?

				}

				t2 := time.Now().UnixNano()
				fmt.Printf("> diff : %.6f\n", float64(t2-t1)/1000000)				
				fmt.Printf("%s, %d\n", time.Now().String(), t2%1000000000)
				
				log.Println(t2/1000000000)

				t1 = t2
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()

	<-done

	/*
				reader := bufio.NewReader(os.Stdin)
		        for {
		                line, err := reader.ReadString('\n')
		                fmt.Println(err)
		                line = strings.TrimRight(line, " \t\r\n")
		                if err != nil {
		                        conn.Close()
		                        break

		                }
		        }
	*/
}
func checkError(err error) {
	if err != nil {
		fmt.Println("Fatal error ", err.Error())
	}
}
