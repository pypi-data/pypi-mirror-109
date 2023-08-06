"""
indi game engine
"""

import os.path
import subprocess as sp
import pkg_resources

from igeEffekseer._igeEffekseer import *

textures = {}

def f_texture_loader(name, type):
    print('f_texture_loader - ' + name)
    tex = core.texture(name)
    textures[name] = tex
    return (tex.width, tex.height, tex.id, tex.numMips > 1)

try:
    dist = pkg_resources.get_distribution('igeCore')
    print('{} ({}) is installed'.format(dist.key, dist.version))
    import igeCore as core
    texture_loader(f_texture_loader)
except pkg_resources.DistributionNotFound:
    print('{} is NOT installed'.format('igeCore'))



def openEditor():
    dirname = os.path.dirname(__file__)
    exePath = os.path.join(dirname, "Tool/Effekseer.exe")
    sp.run(exePath)
