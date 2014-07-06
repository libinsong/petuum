#!/usr/bin/env python
# coding=utf-8


PC_GROUP = {
    'mytest_1': {
        'ip': '172.17.13.26',
        'out_ip': '211.147.15.105',
        'password': 'whywkl305'
    },
    'mytest_2': {
        'ip': '172.17.13.33',
        'out_ip': '118.244.224.8',
        'password': 'whywkl305'
    },
    'mytest': {
        'ip': '172.17.11.71',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytestgroup_1': {
        'ip': '172.17.10.149',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytestgroup_2': {
        'ip': '172.17.10.150',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytestgroup_3': {
        'ip': '172.17.10.172',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytestgroup_4': {
        'ip': '172.17.10.220',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytestgroup_5': {
        'ip': '172.17.10.231',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytestgroup_6': {
        'ip': '172.17.10.4',
        'out_ip': 'None',
        'password': 'whywkl305'
    }
}



SSH_INFO = [
    PC_GROUP['mytest'],
    PC_GROUP['mytestgroup_1'], PC_GROUP['mytestgroup_2'],
    PC_GROUP['mytestgroup_3'], PC_GROUP['mytestgroup_4'],
    PC_GROUP['mytestgroup_5'], PC_GROUP['mytestgroup_6']
]



FILE_COPY = {
    'petuum': {
        'from': '~/petuum/',
        'to': '~/'
    },
    'third_party_lib': {
        'from': '~/third_party_lib/',
        'to': '~/petuum/third_party/src/'
    }
}

FILE_INFO = [
    FILE_COPY['petuum'], FILE_COPY['third_party_lib']
]








