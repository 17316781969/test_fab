#!/usr/bin/expect -f
set timeout 6
set mycmd [lindex $argv 0]
set fd [open "node_list" r]
while {[gets $fd line] >= 0} {
	spawn ssh c@$line
	expect "*apple*" {send "$mycmd \r"}
	expect "*assword*" {send "123321000.\r"}
	expect "*apple*" {send "exit \r"}
	expect eof
}
