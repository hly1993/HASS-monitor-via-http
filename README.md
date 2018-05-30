# HASS-monitor-via-http
monitor the homeasssistant and restart if dead
看门狗程序，hass自动化定时发出post请求，超时未收到即判定hass假死，并进行重启
基于raspbian jessie和python开发
使用前请先安装pip

sudo apt-get install python-pip

pip install pexpect

pip install requests

消息通知服务使用server酱：
http://sc.ftqq.com/3.version
请自行了解
