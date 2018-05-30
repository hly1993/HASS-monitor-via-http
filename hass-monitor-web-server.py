#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

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
        if post_data[:8]=="command=":
            ticksprev = time.time()
            if post_data[8:]=="TV":
                os.system("irsend SEND_ONCE TVSET KEY_TV")
            elif post_data[8:]=="TV_SIG":
                os.system("irsend SEND_ONCE TVSET KEY_SIG")
            elif post_data[8:]=="TV_KEY_UP":
                os.system("irsend SEND_ONCE TVSET KEY_UP")
            elif post_data[8:]=="TV_KEY_DOWN":
                os.system("irsend SEND_ONCE TVSET KEY_DOWN")
            elif post_data[8:]=="TV_KEY_CF":
                os.system("irsend SEND_ONCE TVSET KEY_CF")
            elif post_data[8:]=="AC_KEY_OPEN":
                os.system("irsend SEND_ONCE AC KEY_OPEN")
            elif post_data[8:]=="AC_KEY_UPDN":
                os.system("irsend SEND_ONCE AC KEY_UPDN")
            elif post_data[8:]=="AC_KEY_PO":
                os.system("irsend SEND_ONCE AC KEY_PO")
            elif post_data[8:]=="AC_KEY_PN":
                os.system("irsend SEND_ONCE AC KEY_PN")
            elif post_data[8:]=="AC_KEY_CLOSE":
                os.system("irsend SEND_ONCE AC KEY_CLOSE")
            else:
                print 'bad command'
        elif post_data == "Survival Confirmation": 
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
        r = requests.get("https://sc.ftqq.com/SCU27229Tf67f8df6514dd6b63fb881e0516221795b0e0005e7d48.send?text=Hass Service failed, restarting.....%s" % time.ctime(time.time()))
        ssh = pexpect.spawn('ssh pi@192.168.1.148')
        try:
            i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=0.5)
            if i == 0 :
                ssh.sendline('hanliya')
            elif i == 1:
                ssh.sendline('yes\n')
                ssh.expect('password: ')
                ssh.sendline('hanliya')
            ssh.sendline("wall 'Death Confirmation'\n")
            ssh.sendline("hassctl restart\n")
            ssh.expect(pexpect.EOF, timeout=1.5)
            #r = ssh.read()
            #print r
            ssh.close()
            #exit()
        except pexpect.EOF:
            print "EOF"
            ssh.close()
        except pexpect.TIMEOUT:
            print "TIMEOUT"
            ssh.close()
def run_while_true(server_class=HTTPServer,
                   handler_class=S,port=80):
    """
    This assumes that keep_running() is a function of no arguments which
    is tested initially and after each request.  If its return value
    is true, the server continues.
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    while keep_running():
        print 'Starting httpd...'
        httpd.handle_request()        
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