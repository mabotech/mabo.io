package main

import (
	"fmt"
	//"net"
	//"strings"
	//"os"
)

func main() {

	fmt.Println("Server")
	
	fmt.Println("%d", 0x03)
	/*
	    ip := net.ParseIP("127.0.0.1")
	       addr := net.TCPAddr{ip,8888}


	     for {
	               client,err := listen.AcceptTCP()
	               if err!=nil {
	                   fmt.Println(err.Error())
	                   continue
	               }


	   			   data := make([]byte,1024)
	               c,err := client.Read(data)

	   			s := string(data[0:c])

	   			client.Write([]byte("echo!\r\n"))
	               client.Close()


	   }();

	*/

}
