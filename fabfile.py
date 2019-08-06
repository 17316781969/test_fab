from fabric.api import *

env.user = 'c'
env.hosts = ['192.168.2.105']
env.password = '123321000.'
env.shell_env = {'DISPLAY': ':0'}


def test_reboot():
    run('sudo shutdown -r now')

def git_pull_ads_platforms():
    with cd('/home/c/wuyi_client/ads_platforms/'):
        run('git pull')


def git_pull_mybrowser():
    with cd('/home/c/wuyi_client/MyBrowser/'):
        run('git pull')


def kill_v2():
    run('kill -9 $(pgrep -f v2.py)')


def start_v2():
    run('mate-terminal -- /home/c/test_fab/test.sh -- &', pty=False)

def task():
    execute(git_pull_ads_platforms)
    execute(git_pull_mybrowser)
    execute(kill_v2)
    execute(start_v2)
