package main



import "net"

import "fmt"

import "bufio"



func handle (conn net.Conn) {



  // will listen for message to process ending in newline (\n)

  message, _ := bufio.NewReader(conn).ReadString('\n')

  // output message received

  if message == "74uekFFoluaAMyvANtwc3sKnnoloMV\n" {
    conn.Write([]byte("CTF{n0t-S0-s3CR3t-K3Y}\n"))
  }

  conn.Close()

}


func main () {



  fmt.Println("Launching server...")



  // listen on all interfaces

  ln, _ := net.Listen("tcp", "0.0.0.0:8000")



  // run loop forever (or until ctrl-c)

  for {


    // accept connection on port

    conn, err := ln.Accept()
    if err != nil {
      fmt.Println(err)
      continue
    }

    go handle(conn)

  }

}
