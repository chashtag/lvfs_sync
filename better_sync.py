#!/usr/bin/env python3.11
import requests
import os
import hashlib
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor


class Connection(object):
    def __init__(self) -> None:
        self.sess = requests.session()
        self.tp = ThreadPoolExecutor(max_workers=10)
        self.base = 'https://cdn.fwupd.org/downloads'
        self.manifest = '/'.join((self.base,'PULP_MANIFEST'))
        self.dl_dir = './mirror'
        self.workers = []

    def get_listing(self):
        a = []
        ret = self.sess.get(self.manifest).text
        for line in ret.split('\n'):
            if line:
                a.append(tuple(line.split(",")))
        return a
    

    def do_hash(self,file):
        h = hashlib.sha256()
        with open(file,'rb') as f:
            while r := f.read(1024*32):
                h.update(r)
        return h.hexdigest()


    def download(self,item: tuple):
        print(f'Downloading {item[0]}')
        path = os.path.join(self.dl_dir,item[0])
        url = '/'.join((self.base,item[0]))

        stream = self.sess.get(url, stream=True)
        with open(path,'wb') as f:
            for data in stream.raw.stream(1024*32, decode_content=False):
                f.write(data)
        return 1


    def sync_file(self,item: tuple):
        try:
            path = os.path.join(self.dl_dir,item[0])
        
            if os.path.exists(path):
                if self.do_hash(path) == item[1]:
                    return 1
                else:
                    print(f'Error: Checksum error {item[0]}')
            self.download(item)
        except Exception as e:
            print(f'Error: {e}')
        return 1


    def do_sync(self):
        print('Fetching items')
        gl = self.get_listing()
        print(f'Got {len(gl)} items')
        for item in gl:
            try:
                self.workers.append(self.tp.submit(self.sync_file,item))
            except Exception as e:
                print(f'Error: {e}')


    def wait(self):
        while True:
            worker_complete = len(list(filter(lambda x:x.done(),self.workers)))
            worker_count = len(self.workers)
            if worker_complete == worker_count:
                return 1
            print(f'Workers complete: {worker_complete}/{worker_count}')
            time.sleep(10)
        return 1

c = Connection()

if not os.path.exists(c.dl_dir):
    print(f'Please mount up {c.dl_dir}')
    exit(1)

c.do_sync()
c.wait()
exit()
