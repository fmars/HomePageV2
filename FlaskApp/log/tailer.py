#!/usr/bin/python
import time
import subprocess
import select

LOG_FILE = '/var/log/apache2/access.log'
OUTPUT_FILE = '/var/www/HomePageV2/FlaskApp/log/access.log'
POLL_TIMEOUT = 1000
f_in = subprocess.Popen(['tail','-F', LOG_FILE],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(f_in.stdout)


f_out = open(OUTPUT_FILE, 'a', 0)
while True:
    if p.poll(1000):
        line = f_in.stdout.readline()
        if 'GET' in line:
            pieces = line.split()
            ip_addr = pieces[0]
            f_out.write(ip_addr + '\n')
