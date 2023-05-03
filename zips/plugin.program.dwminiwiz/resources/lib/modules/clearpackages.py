import os
from .addonvar import *
from xbmc import log
import shutil

def clear_packages():
    file_count = len([name for name in os.listdir(packages)])
    for filename in os.listdir(packages):
    	file_path = os.path.join(packages, filename)
    	try:
    	       if os.path.isfile(file_path) or os.path.islink(file_path):
    	       	os.unlink(file_path)
    	       elif os.path.isdir(file_path):
    	       	shutil.rmtree(file_path)
    	except Exception as e:
    		log('Failed to delete %s. Reason: %s' % (file_path, e), xbmc.LOGINFO)
    xbmcgui.Dialog().ok(addon_name, str(file_count)+' packages cleared.' )