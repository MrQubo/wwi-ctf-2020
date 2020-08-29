package main

import "net"
import "fmt"
import "bufio"

func main() {

  // connect to server
  conn, _ := net.Dial("tcp", "ctf.staszic.waw.pl:43958")
  for {
    conn.Write([]byte("74uekFFoluaAMyvANtwc3sKnnoloMV\n"))
    message, _ := bufio.NewReader(conn).ReadString('\n')
    if message != "" {
      fmt.Print("Did not get any reply!\n")
    }
  }
}
