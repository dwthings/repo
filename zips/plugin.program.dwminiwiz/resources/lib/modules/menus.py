import json
import addonvar
from .utils import addDir
from .parser import Parser

addon_icon = addonvar.addon_icon
addon_fanart = addonvar.addon_fanart
local_string = addonvar.local_string
buildfile = addonvar.buildfile
headers = addonvar.headers

def main_menu():
    addDir('Build Menu','',1,addon_icon,addon_fanart,local_string(30001),isFolder=True)
    addDir('Maintenance','',5,addon_icon,addon_fanart,local_string(30002),isFolder=True)
    addDir('Fresh Start','',4,addon_icon,addon_fanart,local_string(30003),isFolder=False)
    addDir('Notification','',100,addon_icon,addon_fanart,'Bring up the notifications dialog',isFolder=False)
    addDir('Settings','',9,addon_icon,addon_fanart,local_string(30001),isFolder=False)

def build_menu():
    if not buildfile.endswith('.xml') and not buildfile.endswith('.json'):
        addDir('Invalid build URL. Please contact the build creator.','','','','','',isFolder=False)
        return
    p = Parser(buildfile)
    builds = json.loads(p.get_list())['builds']
    
    for build in builds:
        name = (build.get('name', 'Unknown'))
        version = (build.get('version', '0'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        description = (build.get('description', 'No Description Available.'))
        preview = (build.get('preview',None))
        tweak = (build.get('tweak',None))
        extra = (build.get('extra',None))
        
        if url.endswith('.xml') or url.endswith('.json'):
            addDir(name,url,1,icon,fanart,description,name2=name,version=version,isFolder=True)
        addDir(name + ' Version ' + version,url,3,icon,fanart,description,name2=name,version=version,isFolder=False)
        if preview:
            addDir('***Build Video SneakPeak*** ' + name + ' Version ' + version,preview,10,icon,fanart,description,name2=name,version=version,isFolder=False)
        if tweak:
            addDir('***Video Tweaks*** ' + name + ' Version ' + version,tweak,10,icon,fanart,description,name2=name,version=version,isFolder=False)
        if extra:
            addDir('***Video Extra*** ' + name + ' Version ' + version,extra,10,icon,fanart,description,name2=name,version=version,isFolder=False)    

def submenu_maintenance():
    addDir('Clear Packages','',6,addon_icon,addon_fanart,local_string(30005),isFolder=False)
    addDir('Clear Thumbnails','',7,addon_icon,addon_fanart,local_string(30008),isFolder=False)
    addDir('Advanced Settings','',8,addon_icon,addon_fanart,local_string(30009),isFolder=False)