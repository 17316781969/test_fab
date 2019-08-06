#!/usr/bin/python3
import datetime
import sys, os, time, atexit
from signal import SIGTERM
import subprocess


class daemon():
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        # 第一次fork，生成子进程，脱离父进程
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork fist faild:%d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # 修改工作目录
        os.chdir('/')
        # 设置新的会话连接
        os.setsid()
        # 重新设置文件创建权限
        os.umask(0)

        # 第二次fork，禁止进程打开终端
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork second faild:%d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()

        # 重定向标准输入、输出
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # 注册退出函数
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            ms = "pidfile %s already exist,daemon already running\n"
            sys.stderr.write(ms % self.pidfile)
            sys.exit(1)

        self.daemonize()
        self.run()

    def stop(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            ms = "pidfile %s does not exit,daemon not running\n"
            sys.stderr.write(ms % self.pidfile)
            return

        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
                os.remove(self.pidfile)
        except OSError as err:
            err = str(err)
            if err.find('No sush process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print(str(err))
                    sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    # 该方法用于在子类中重新定义，用来运行你的程序
    def run(self):
        """ run your fun"""


###以上代码可以做成一个库文件，也可以放在一个文件中###
###以下代码可以引用上面的库文件#########
class mydaemon(daemon):
    # 重新定义run函数，以运行你的功能
    def run(self):
        start_lines = 0
        while True:
            browser_log_r = subprocess.getstatusoutput('cat /home/c/wuyi_client/files/browser.log | wc -l')
            end_lines = int(browser_log_r[1])
            file = open('/home/c/wuyi_client/files/daemon.log', 'a+')
            dt = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            if end_lines - start_lines == 0:
                terminal_sum_r = subprocess.getstatusoutput('pgrep -f mate-terminal | wc -l')
                if int(terminal_sum_r[1]) > 3:
                    os.system('kill -9 $(pgrep -f mate-terminal)')
                chrome_count_r = subprocess.getstatusoutput('pgrep -f chrome | wc -l')
                if int(chrome_count_r[1]) > 0:
                    os.system('kill -9 $(pgrep -f chrome)')
                chromedriver_count_r = subprocess.getstatusoutput('pgrep -f chromedriver | wc -l')
                if int(chromedriver_count_r[1]) > 0:
                    os.system('kill -9 $(pgrep -f chromedriver)')
                whoami_r = subprocess.getstatusoutput('whoami')
                # os.system('mate-terminal -e \"python3 /home/c/wuyi_client/MyBrowser/v2.py\"')
                os.system('mate-terminal -- \"/home/c/test_fab/test.sh\"')
                # subprocess.getstatusoutput('mate-terminal -- /home/c/test_fab/test.sh')
                file.write(f"{dt} I'm {whoami_r[1]},start_lines: {start_lines},restart python script !\n")
            else:
                file.write(f"{dt} end_lines: {end_lines}, python script is running !\n")
            start_lines = end_lines
            file.close()
            time.sleep(180)


if __name__ == '__main__':
    daemon = mydaemon('/tmp/pidfile', stdout='/tmp/result')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print('unkonow command')
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage:%s start/stop/restart" % sys.argv[0])
        sys.exit(2)
