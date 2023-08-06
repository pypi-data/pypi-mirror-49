#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import subprocess
import threading
import time

from .Trigger import Trigger


def loadSingleMulti(data, n):
    if n in data:
        if not isinstance(data[n], list):
            return([data[n]])
        else:
            return(data[n])
    return([])


class Rule:
    def __init__(self, tree, name, data, configdir, statusfile, jobmanager):
        self.tree = tree
        self.name = name
        self.cmd = loadSingleMulti(data, 'cmd')
        self.callBefore = loadSingleMulti(data, 'callBefore')
        self.callAfter = loadSingleMulti(data, 'callAfter')
        self.call = loadSingleMulti(data, 'call')
        if len(self.call) != 0:
            print('The usage of \'call\' is deprecated! Rule '
                  + self.name + ' should be updated!')
        self.migrateCmd()
        self.configdir = configdir
        self.statusfile = statusfile
        self.jobmanager = jobmanager
        self.trigger = [
            Trigger(t, self.configdir, self.statusfile) for
            t in loadSingleMulti(data, 'trigger')
        ]

    def show(self):
        print('name:', self.name)
        print('cmd:', self.cmd)
        print('callBefore:', self.callBefore)
        print('callAfter:', self.callAfter)
        print('call:', self.call)
        print('trigger:', self.trigger)
        print('-----')

    def run(self, juuid=None):
        run = False
        self.jobmanager.avail(self.name)
        self.execCallBefore()
        if self.statusfile.checkRuleCallBefore(self.name, self.callBefore):
            run = True
        if not run:
            if self.checkTriggers():
                run = True
        if run:
            print(self.name)
            self.executeCmds()
            self.saveStatus()
            self.saveRunBeforeStatus()
        self.execCallAfter()
        self.saveTriggers()
        self.jobmanager.unavail(self.name)
        if juuid is not None:
            self.jobmanager.unregister(juuid)
        return(run)

    def runThread(self):
        juuid = self.jobmanager.register()
        run = threading.Thread(target=self.run, kwargs={'juuid': juuid})
        run.start()
        return(juuid)

    def executeCmds(self):
        jobs = []
        for c in self.cmd:
            if c['type'] == 'cmd':
                self.jobmanager.resume(self.name)
                subprocess.call('cd ' + self.configdir + '; ' + c['cmd'],
                                shell=True, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL
                                )
                self.jobmanager.pause(self.name)
            elif c['type'] == 'rule':
                if c['dedicated']:
                    jobs.append(self.tree[c['rule']].runThread())
                else:
                    self.tree[c['rule']].run()
            elif c['type'] == 'AwesomeBuild':
                if c['cmd'] == 'reset-status':
                    self.statusfile.initialize()
        while True in [self.jobmanager.isRegistered(j) for j in jobs]:
            time.sleep(0.1)

    def execCallBefore(self):
        jobs = []
        for cb in self.callBefore:
            jobs.append(self.tree[cb].runThread())
        while True in [self.jobmanager.isRegistered(j) for j in jobs]:
            time.sleep(0.1)

    def execCallAfter(self):
        for ca in self.callAfter:
            self.tree[ca].run()

    def checkTriggers(self):
        run = False
        if len(self.trigger) == 0:
            run = True
        for t in self.trigger:
            self.jobmanager.resume(self.name)
            if t.eval():
                run = True
            self.jobmanager.pause(self.name)
        return(run)

    def saveTriggers(self):
        for t in self.trigger:
            self.jobmanager.resume(self.name)
            t.save()
            self.jobmanager.pause(self.name)

    def migrateCmd(self):
        cmds = []
        for c in self.cmd:
            if isinstance(c, dict):
                if 'dedicated' not in c:
                    c['dedicated'] = False
                cmds.append(c)
            elif isinstance(c, str):
                cmds.append(
                    {
                        'type': 'cmd',
                        'cmd': c
                    }
                )
        for c in self.call:
            cmds.append(
                {
                    'type': 'rule',
                    'rule': c
                }
            )
        self.cmd = cmds

    def saveStatus(self):
        self.statusfile.setRule(self.name, time.time())

    def saveRunBeforeStatus(self):
        self.statusfile.saveRuleCallBefore(self.name, self.callBefore)
