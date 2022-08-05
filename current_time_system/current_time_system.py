#!/usr/bin/env python

import subprocess

def get_output(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.communicate()[0].strip().decode('ascii')

utc = get_output([ "date", "-u", "+%l:%M %p" ])
print(f"UTC = {utc}")
sweden =  get_output([ "date", "+%l:%M %p" ])
print(f" SE = {sweden}")
