#!/usr/bin/env python
# coding=utf-8

'''
Set up petuum
'''


import pexpect
from docopt import docopt


def copy_file(ip, src, dest):
    cmd = 'scp -r {src} {ip}:{dest}'.format(src=src, ip=ip,
                                            dest=dest)
    cpy = pexpect.spawn(cmd, timeout=10)
    cpy
    try:
        
    finally:
        cpy.close()








def main(args):
    pass


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0')
    main(args)
