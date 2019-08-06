#!/usr/bin/expect -f
set src_file [lindex $argv 0]
set dest_file [lindex $argv 1]
set timeout 3
for {set i 1} {$i<=12} {incr i} {
	spawn scp $src_file c@192.168.2.[expr {$i + 100}]:$dest_file
	expect { -re "*(yes/no)?*" {send "yes\r"}}
	expect {
	-re ".*assword*." {
        send "${password}\r"    ;# why do you use ``\r\r''?
        exp_continue
    } "100%" {
        puts "File Transfer successful\n"
        set success1 0.5
        exp_continue
    } -re {[0-9]{1,2}%} {
        exp_continue
    } timeout {
        set success2 0
        set success1 0
    } -re ".*closed by remote host" {
        set success2 0.5
    }
}
}
