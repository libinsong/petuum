#!/usr/bin/env python
# coding=utf-8


import pexpect

from sync_config import FILE_INFO


def sync(files):
    files_str = ' '.join(dir for dir in FILE_INFO)
    print files_str



if __name__ == '__main__':
    sync(FILE_INFO)



