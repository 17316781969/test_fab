#!/usr/bin/expect -f
set timeout 6
set ip [lindex $argv 0]
set mycmd [lindex $argv 1]

spawn su c -c "ssh c@$ip"
expect "*assword*" {send "123321000.\r"}
expect "*c@*" {send "$mycmd \r"}
expect "*assword*" {send "123321000.\r"}
expect "*c@*" {send "exit \r"}
expect eof

