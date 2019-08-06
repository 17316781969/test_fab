#!/bin/bash
	
func()
{
	ip=$1 #接收IP的变量
	user=$2 #接收用户名的变量
	password=$3 #接收密码的变量
	filesource=$4
	filedestination=$5
expect <<EOF
set timeout 5 
spawn scp -r $filesource $user@$ip:$filedestination
expect "*(yes/no)*" {send "yes\r"}
expect "*100%*"
expect eof
EOF
}

for((i=1;i<=12;i++));
do
	IP=192.168.2.$((100+$i))
	USER="c"
	PAWD="123321000."
	func $IP $USER $PAWD $1 $2
done;
