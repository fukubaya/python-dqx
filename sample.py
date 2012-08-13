#!/usr/bin/python
# -*- coding: utf-8 -*-

# 
# sample.py
# 
# Created by FUKUBAYASHI Yuichiro on 2012/08/11
# Copyright (c) 2012, FUKUBAYASHI Yuichiro
# 
# last update: <2012/08/11 01:30:22>
# 

import sys
from dqx import dqx

if __name__ == '__main__':
    argv = sys.argv
    uid = argv[1]

    u = dqx.User(uid)
    u.retrieve_and_update()

    print u

