#!/usr/bin/expect -f
set user [lindex $argv 0]
set ip [lindex $argv 1]
set mycmd [lindex $argv 3]
set passwd [lindex $argv 2]
set timeout 6

spawn ssh $user@$ip
expect "*assword*" {send "$passwd\r"}
expect "*@*" {send "$mycmd \r"}
expect "*assword*" {send "$passwd\r"}
#  expect "*assword*" {send "$passwd\r"}
expect "*@*" {send "exit \r"}
expect eof

