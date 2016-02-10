package main

import (
	"net"
	"fmt"
	"os"
	  "encoding/binary"
    "bytes"
	
)

type Cmd struct {
	a1  int
	a2  int
	cmd [4]byte
	b1  int
	b2  int
	b3  int
	b4  int
	b5  int
}

func main() {
	strEcho := "Halo"
	servAddr := "127.0.0.1:23800"
	
	var cmd Cmd
	
	
	  s := "ASTZ"
    var a [4]byte
    copy(a[:], s)
	
	fmt.Println("s:", []byte(s), "a:", a)
	
	cmd.a1 = 0x02
	cmd.a2 = 0x20
	cmd.cmd =a
	cmd.b1 = 0x20
	cmd.b2 = 0x75
	cmd.b3 = 0x00
	cmd.b4 = 0x20
	cmd.b5 = 0x03
	
	tcpAddr, err := net.ResolveTCPAddr("tcp", servAddr)
	if err != nil {
		println("ResolveTCPAddr failed:", err.Error())
		os.Exit(1)
	}

	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		println("Dial failed:", err.Error())
		os.Exit(1)
	}

var bin_buf bytes.Buffer

binary.Write(&bin_buf, binary.BigEndian, &cmd)

fmt.Println("b:", bin_buf.Bytes())

	_, err = conn.Write(bin_buf.Bytes()) // strEcho
	if err != nil {
		println("Write to server failed:", err.Error())
		os.Exit(1)
	}

	println("write to server = ", strEcho)

	reply := make([]byte, 1024)

	_, err = conn.Read(reply)
	if err != nil {
		println("Write to server failed:", err.Error())
		os.Exit(1)
	}

	println("reply from server=", string(reply))

	conn.Close()
}
