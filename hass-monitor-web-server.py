#!/usr/bin/env python
"""
Usage::
    ./hass-monitor-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import time
import thread
import pexpect
import requests
global ticksprev
class S(BaseHTTPRequestHandler):
    global ticksprev
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>Python Dummy Server for IR Control!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        global ticksprev
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print post_data
        if post_data == "Survival Confirmation": 
            ticksprev = time.time()
        print ticksprev
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
def print_time( threadName, delay):
   global ticksprev
   count = 0
   while 1:
      time.sleep(delay)
      ticksnow = time.time()
      if ticksnow - ticksprev > 180:
        print "Hass Service failed, restarting.....\n%s: %s" % ( threadName, time.ctime(time.time()) )
        ticksprev = time.time()
        r = requests.get("https://sc.ftqq.com/*********.send?text=Hass Service failed, restarting.....%s" % time.ctime(time.time()))
        ssh = pexpect.spawn('ssh pi@192.168.1.*')
        try:
            i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=0.5)
            if i == 0 :
                ssh.sendline('****')
            elif i == 1:
                ssh.sendline('yes\n')
                ssh.expect('password: ')
                ssh.sendline('****')
            ssh.sendline("wall 'Death Confirmation'\n")#向所有已登录用户通知
            ssh.sendline("hassctl restart\n")#重启hass，需要安装hassctl工具
            ssh.expect(pexpect.EOF, timeout=1.5)
            ssh.close()
        except pexpect.TIMEOUT:
            print "TIMEOUT"
            ssh.close()   
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...%s' % time.ctime(time.time()) 
    httpd.serve_forever()
if __name__ == "__main__":
    from sys import argv
    global ticksprev
    global ticksnow
    ticksnow = time.time()
    ticksprev = ticksnow
    try:
        thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    except:
        print "Error: unable to start thread"
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
