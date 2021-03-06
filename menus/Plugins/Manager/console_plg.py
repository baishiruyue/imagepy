# -*- coding: utf-8 -*-
import wx
from wx.py.shell import ShellFrame
import scipy.ndimage as ndimg
import numpy as np
from imagepy import IPy

from imagepy.core.engine import Free
from imagepy.core.manager import PluginsManager

from wx.lib.pubsub import pub

def showconsole(cmds): 
    print('here')
    frame = ShellFrame(IPy.curapp, locals=cmds)
    frame.shell.run('# numpy(np) and scipy.ndimage(ndimg) has been imported!\n')
    frame.shell.run('# plgs.run_name() to call a ImagePy plugin.\n')
    frame.shell.run('# IPy is avalible here, and curips() to get the current ImagePlus, update() to redraw.\n')
    print('here')
    frame.Show(True)

pub.subscribe(showconsole, 'showconsole')

## There is something wrong!
## To be fixed!

def get_ips():
    ips = IPy.get_ips()
    if ips is None:
        print('no image opened!')
    return ips

def update():
    ips = IPy.get_ips()
    if not ips is None : 
        ips.update='pix'

class Macros(dict):
    def __init__(self):
        for i in list(PluginsManager.plgs.keys()):
            if not isinstance(i, str) or i == 'Command Line':
                #print(PluginsManager.plgs[i])
                continue
            name = ''.join(list(filter(str.isalnum, i)))
            ### TODO:Fixme! 
            #exec('self.run_%s = lambda para=None, 
            #      plg=PluginsManager.plgs[i]:plg().start(para)'%name)
            #self['run_%s'%i] = lambda para=None, plg=PluginsManager.plgs[i]:plg().start(para)
            exec('self.run_%s = lambda para=None, plg=PluginsManager.plgs[i]:plg().start(para)'%name)
            #exec('self._%s = PluginsManager.plgs[i]().start'%name)
        print(self)

cmds = {'IPy':IPy, 'ndimg':ndimg, 'update':update, 'curips':get_ips}

class Plugin(Free):
    title = 'Command Line'

    def load(self):
        cmds['plgs'] = Macros()
        return True

    def run(self, para=None):
        wx.CallAfter(pub.sendMessage, 'showconsole', cmds = cmds)