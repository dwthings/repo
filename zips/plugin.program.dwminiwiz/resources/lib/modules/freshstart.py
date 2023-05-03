from xbmcgui import dialog
from xbmc import log
from . import skinSwitch
from .addonvar import *
import sys, shutil
from urllib.parse import parse_qs

args   = parse_qs(sys.argv[2][1:])
mode   = args.get('mode', None)
if mode:
	mode = int(mode[0])

def save_check():
	if setting('savefavs')=='true':
		EXCLUDES.append('favourites.xml')
	if setting('savesources')=='true':
		EXCLUDES.append('sources.xml')
	if setting('savedebrid')=='true':
		EXCLUDES.append('script.module.resolveurl')
	if setting('saveadvanced')=='true':
		EXCLUDES.append('advancedsettings.xml')
	return EXCLUDES

def save_move1():
	if os.path.exists(os.path.join(user_path, addon_id)):
		shutil.move(os.path.join(user_path, addon_id), os.path.join(packages, addon_id))
	if os.path.exists(os.path.join(user_path,'favourites.xml')):
		shutil.move(os.path.join(user_path, 'favourites.xml'), os.path.join(packages, 'favourites.xml'))
	if os.path.exists(os.path.join(user_path,'sources.xml')):
		shutil.move(os.path.join(user_path, 'sources.xml'), os.path.join(packages, 'sources.xml'))
	if os.path.exists(os.path.join(data_path,'script.module.resolveurl')):
		shutil.move(os.path.join(data_path, 'script.module.resolveurl'), os.path.join(packages, 'script.module.resolveurl'))
	if os.path.exists(os.path.join(user_path,'advancedsettings.xml')):
		shutil.move(os.path.join(user_path, 'advancedsettings.xml'), os.path.join(packages, 'advancedsettings.xml'))

def save_move2():
	if os.path.exists(os.path.join(packages,addon_id)):
		if os.path.exists(os.path.join(user_path, addon_id)):
			os.remove(os.path.join(user_path, addon_id))
		shutil.move(os.path.join(packages, addon_id), os.path.join(user_path, addon_id))
	
	if os.path.exists(os.path.join(packages,'favourites.xml')):
		if os.path.exists(os.path.join(user_path, 'favourites.xml')):
			os.remove(os.path.join(user_path, 'favourites.xml'))
		shutil.move(os.path.join(packages, 'favourites.xml'), os.path.join(user_path, 'favourites.xml'))
		
	if os.path.exists(os.path.join(packages,'sources.xml')):
		if os.path.exists(os.path.join(user_path, 'sources.xml')):
			os.remove(os.path.join(user_path, 'sources.xml'))
		shutil.move(os.path.join(packages, 'sources.xml'), os.path.join(user_path, 'sources.xml'))
	
	if os.path.exists(os.path.join(packages,'script.module.resolveurl')):
		if os.path.exists(os.path.join(data_path, 'script.module.resolveurl')):
			shutil.rmtree(os.path.join(data_path, 'script.module.resolveurl'))
		shutil.move(os.path.join(packages, 'script.module.resolveurl'), os.path.join(data_path, 'script.module.resolveurl'))
	shutil.rmtree(packages)
	
	if os.path.exists(os.path.join(packages,'advancedsettings.xml')):
		if os.path.exists(os.path.join(user_path, 'advancedsettings.xml')):
			os.remove(os.path.join(user_path, 'advancedsettings.xml'))
		shutil.move(os.path.join(packages, 'advancedsettings.xml'), os.path.join(user_path, 'advancedsettings.xml'))

def freshStart():
	yesFresh = dialog.yesno('Fresh Start', 'Are you sure you wish to clear all data?  This action cannot be undone.', nolabel='No', yeslabel='Fresh Start')
	if yesFresh:
		
		#Skin Switch
		if not currSkin() in ['skin.estuary']:
			skinSwitch.swapSkins('skin.estuary')
			x = 0
			xbmc.sleep(1000)
			while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
				x += 1
				xbmc.sleep(200)
				xbmc.executebuiltin('SendAction(Select)')
			if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
				xbmc.executebuiltin('SendClick(11)')
			else: 
				log('Fresh Install: Skin Swap Timed Out!', xbmc.LOGINFO)
				return False
			xbmc.sleep(1000)
		if not currSkin() in ['skin.estuary']:
			log('Fresh Install: Skin Swap failed.', xbmc.LOGINFO)
			return
		
		if mode==4:
			save_check()
			save_move1()
			
		dp.create(addon_name, 'Deleting files and folders...')
		xbmc.sleep(1000)
		dp.update(30, 'Deleting files and folders...')
		xbmc.sleep(1000)
		for root, dirs, files in os.walk(xbmcPath, topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in files:
				if name not in EXCLUDES:
					try:
						os.remove(os.path.join(root, name))
					except:
						log('Unable to delete ' + name, xbmc.LOGINFO)
		dp.update(60, 'Deleting files and folders...')
		xbmc.sleep(1000)	
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in dirs:
				if name not in ["Database","userdata","temp","addons","packages","addon_data"]:
					try:
						shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
					except:
						log('Unable to delete ' + name, xbmc.LOGINFO)
		dp.update(60, 'Deleting files and folders...')
		xbmc.sleep(1000)
		if not os.path.exists(packages):
			os.mkdir(packages)
		dp.update(100, 'Deleting files and folders...done')
		xbmc.sleep(2000)
		'''
		if mode == 4:
			save_move2()
			addon.setSetting('firstrun', 'true')
			addon.setSetting('buildname', 'No Build Installed')
			addon.setSetting('buildversion', '0')
			dialog.ok(addon_name, 'Fresh Start Complete. Click OK to Force Close Kodi.')
			os._exit(1)
		'''
	else:
		return