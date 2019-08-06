checkfile(){
	if [ ! -e /home/c/wuyi_client -o ! -e /home/c/wuyi_client/ads_platforms -o ! -e /home/c/wuyi_client/MyBrowser -o ! -e /home/c/wuyi_client/proxy_providers -o ! -e /home/c/wuyi_client/utils ];
	then
		rm -rf /home/c/wuyi_client;
		mkdir /home/c/wuyi_client &&
		cd /home/c/wuyi_client &&
		git clone git@bitbucket.org:wuyiads/ads_platforms.git &&
		git clone git@bitbucket.org:wuyiads/MyBrowser.git &&
		git clone git@bitbucket.org:wuyiads/proxy_providers.git &&
		git clone git@bitbucket.org:wuyiads/utils.git;
	else
		cd /home/c/wuyi_client/ads_platforms &&
		git pull &&
		cd /home/c/wuyi_client/MyBrowser &&
		git pull &&
		cd /home/c/wuyi_client/proxy_providers &&
		git pull &&
		cd /home/c/wuyi_client/utils &&
		git pull;
	fi
	mkdir -p /home/c/wuyi_client/files &&
	date | cat >> $1 &&
	date | cat >> $2;
}
a=0;
c=0;
fa="/home/c/wuyi_client/files/browser.log";
fb="/home/c/wuyi_client/files/mission_valid.log";
if [ -e $fa -a -e $fb ];
then 
	a=`stat -c %Y $fa`;
	c=`stat -c %Y $fb`;
fi
b=`date +%s`;
mission_diff=$(($b-$c))
diff=$(($b-$a))
if [ $diff -gt 180 ];
then
	if [ ! $(pgrep -f v2.py) ];
	then
		checkfile $fa $fb;
		supervisorctl restart awesome;
	else
		kill $(pgrep -f v2.py);
	fi
elif [ $mission_diff -gt 300 -a $diff -lt 180 ];
then
	supervisorctl stop awesome;
	kill $(pgrep -f v2.py);
	kill $(pgrep -f chrome);
	checkfile $fa $fb;
	sudo init 6;
fi;
