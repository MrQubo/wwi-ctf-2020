package main

import "net"
import "fmt"
import "bufio"

func handle (conn net.Conn, finished chan bool) {
  conn.Write([]byte("74uekFFoluaAMyvANtwc3sKnnoloMV\n"))
  message, _ := bufio.NewReader(conn).ReadString('\n')
  if message == "" || message == "\n" {
    fmt.Print("Did not get any reply!\n")
  }
  finished <- true
}

func main () {
  finished := make(chan bool)
  conn, _ := net.Dial("tcp", "ctf.staszic.waw.pl:43958")
  go handle(conn, finished)
  <- finished
  fmt.Print("Wziuuuuu!\n")
}
