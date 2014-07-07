#!/usr/bin/env python
# coding=utf-8


PC_GROUP = {
    'mytest_1': {
        'ip': '172.17.13.26',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytest_2': {
        'ip': '172.17.13.33',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytest': {
        'ip': '172.17.11.71',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'newtest': {
        'ip': '172.17.11.223',
        'out_ip': '118.244.224.8',
        'password': 'whywkl305'
    },
    'newtest2': {
        'ip': '172.17.11.22',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'empty': {
        'ip': '172.17.11.61',
        'out_ip': 'None',
        'password': 'whywkl305'
    }
}



SSH_INFO = [
    PC_GROUP['mytest_1'], PC_GROUP['mytest_2'],
]



FILE_COPY = {
    'third_party_lib': {
        'from': '/root/petuum_files/src/',
        'to': '/root/petuum/third_party/'
    },
    'archives': {
        'from': '/home/root/petuum_files/archives/',
        'to': '/home/root/archives/'
    }
}


PETUUM_PROJECT = {
    'from': '/root/petuum/',
    'to': '/root/'
}









