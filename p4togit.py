#!/bin/env python3

import subprocess as p
import sys
import re

print(sys.version.split(" ")[0].split(".")[0:2])

class P4GIT(object):
    def __init__(self, config):
        self.config = config
        self.p4client = ""
        self.p4user = ""
        self.p4port = ""
        self.p4 = ""
        self.p4tickts = ""
        self.p4changes = []
        self.batchsize = 500

        with open(config) as c:
            for line in c:
                match =  re.match("P4USER=(.+)", line)
                if match:
                    self.p4user = match.group(1)

                match =  re.match("P4CLIENT=(.+)", line)
                if match:
                    self.p4client = match.group(1)

                match =  re.match("P4PORT=(.+)", line)
                if match:
                    self.p4port = match.group(1)

                match =  re.match("P4TICKETS=(.+)", line)
                if match:
                    self.p4tickets = match.group(1)

        assert(self.p4user, self.p4client, self.p4port)
        #assert(self.p4tickets)
        self.p4 = "p4 -u %s -c %s " %(self.p4user, self.p4client)
#########################################################################################

    def GetData(self, change):
        cmd = self.p4 + "describe -s %d" %(change)
        data = p.check_output(cmd, shell=True,bufsize=1)
        print(data)
#########################################################################################

    def GetChanges(self):
        i=1
        cmd = self.p4 + "changes -s submitted -m1 //%s/..." %(self.p4client)
        print(cmd)
        head = p.check_output(cmd, shell=True,bufsize=1)
        head = int(head.split()[1])
        while(i):
            cmd = self.p4 + "changes -s submitted //%s/...@%d,%d" %(self.p4client, i, i+self.batchsize)
            cls = p.check_output(cmd, shell=True, bufsize=1)
            for c in cls.splitlines():
                cl   = int(c.split()[1])
                self.p4changes.append(cl)
                print(self.p4changes)
            i = i + self.batchsize
            if i >= head:
                break
#########################################################################################

    def migrate(self):
        changes = self.GetChanges()
        for change in self.p4changes:
            self.GetData(change)

#########################################################################################

def main():
    print(sys.argv)
    p4git = P4GIT(sys.argv[1])
    p4git.migrate()
#########################################################################################

if __name__ == '__main__':
    main()
