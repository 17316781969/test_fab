#!/usr/bin/expect -f
set mycmd [lindex $argv 0]
set timeout 3
spawn sudo docker system prune
expect "*assword*" {send "123321000.\r"}
expect "y/N" {send "y\r"}
expect eof
