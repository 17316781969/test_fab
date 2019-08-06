#!/usr/bin/expect

set timeout 3
spawn sudo /usr/bin/supervisord -c /etc/supervisord.conf
expect "*sudo*" {send "123321000.\r"}
expect eof
