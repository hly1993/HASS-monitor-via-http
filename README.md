# HASS-monitor-via-http
monitor the homeasssistant and restart if dead
看门狗程序，hass自动化定时发出post请求，超时未收到即判定hass假死，并进行重启
基于raspbian jessie和python开发
使用前请先安装pip

sudo apt-get install python-pip

pip install pexpect

pip install requests

使用方法：
sudo python ./hass-monitor-web-server.py 8080 #端口可替换，不填默认80
执行没有错误可以从localhost:8080 看到网页提示
homeassitant填写自动化，定时执行：
curl -d "Survival Confirmation" "serv.beardog.top:8080"
3分钟没有收到post请求则会重启hass

本代码默认运行在和hass不同的主机上，若在hass本地运行，则不需要pexpect，直接os.system("hassctl restart")即可


消息通知服务使用server酱：
http://sc.ftqq.com/3.version
请自行了解
