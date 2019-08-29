#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys, os
import github
import gitee

if __name__ == '__main__':
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and 'http' not in sys.argv[1]):
        print("usage:  ./%s [--path=/save_dir] url1 url2 ..." % (os.path.basename(__file__)))
    else:
        start_index = 1
        path = os.getcwd()
        if 'path' in sys.argv[1]:
            path = sys.argv[1].split('=')[1]
            if path[0] == '~':
                path += os.path.expanduser("~") + path[1:]
            elif path[0] == '.':
                path += os.getcwd() + path[1:]
            start_index = 2
        for url in [sys.argv[i] for i in range(start_index, len(sys.argv))]:
            # print(url.split('//'))
            if "github.com" in url:
                github.getSubDir(url, path)
            if "gitee.com" in url:
                gitee.getSubDir(url, path)