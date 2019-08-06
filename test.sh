#!/bin/bash
m_pid=$(pgrep -f MyBrowser/v2.py)
if [ $m_pid ];then
	kill -9 $m_pid
fi
python3 ~/wuyi_client/MyBrowser/v2.py
