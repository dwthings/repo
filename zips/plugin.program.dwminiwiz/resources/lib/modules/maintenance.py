import os, shutil, sqlite3
import xbmc, xbmcgui
from xbmc import log
import addonvar
from addonvar import currSkin
from .skinSwitch import swapSkins
from .save_data import save_check, save_backup, save_restore

user_path = addonvar.user_path
db_path = addonvar.db_path
addon_name = addonvar.addon_name
addon_icon = addonvar.addon_icon
textures_db = addonvar.textures_db
advancedsettings_folder = addonvar.advancedsettings_folder
advancedsettings_xml = addonvar.advancedsettings_xml
dialog = addonvar.dialog
dp = addonvar.dp
xbmcPath = addonvar.xbmcPath
EXCLUDES = addonvar.EXCLUDES
packages = addonvar.packages
setting_set = addonvar.setting_set

def purge_db(db):
	if os.path.exists(db):
		try:
			conn = sqlite3.connect(db)
			cur = conn.cursor()
		except Exception as e:
			log("DB Connection Error: %s" % str(e), xbmc.LOGDEBUG)
			return False
	else: 
		log('%s not found.' % db, xbmc.LOGINFO)
		return False
	cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	for table in cur.fetchall():
		if table[0] == 'version': 
			log('Data from table `%s` skipped.' % table[0], xbmc.LOGDEBUG)
		else:
			try:
				cur.execute("DELETE FROM %s" % table[0])
				conn.commit()
				log('Data from table `%s` cleared.' % table[0], xbmc.LOGDEBUG)
			except Exception as e:
				log("DB Remove Table `%s` Error: %s" % (table[0], str(e)), xbmc.LOGERROR)
	conn.close()
	log('%s DB Purging Complete.' % db, xbmc.LOGINFO)

def clear_thumbnails():
	try:
		if os.path.exists(os.path.join(user_path, 'Thumbnails')):
			shutil.rmtree(os.path.join(user_path, 'Thumbnails'))
	except Exception as e:
    		log('Failed to delete %s. Reason: %s' % (os.path.join(user_path, 'Thumbnails'), e), xbmc.LOGINFO)
    		return
	try:
		if os.path.exists(os.path.join(db_path, 'Textures13.db')):
			os.unlink(os.path.join(db_path, 'Textures13.db'))
	except:
		purge_db(textures_db)
	xbmc.sleep(1000)
	xbmcgui.Dialog().ok(addon_name, 'Thumbnails have been deleted. Reboot Kodi to refresh thumbs.')
	return

def advanced_settings():
	selection = xbmcgui.Dialog().select('Select the Ram Size of your device.', ['1GB (1st - 3rd gen, Lite Firestick)','1GB to 1.5GB (4k Firestick)','1.5GB to 2GB (Firebox, Cube, Sheild Tube)','2GB to 3GB RAM','3GB or more (Nvidia Shield Pro)','Delete Advanced Settings'])
	if selection==0:
		xml = os.path.join(advancedsettings_folder, 'less1.xml')
	elif selection==1:
		xml = os.path.join(advancedsettings_folder, '1plus.xml')
	elif selection==2:
		xml = os.path.join(advancedsettings_folder, 'firetv.xml')
	elif selection==3:
		xml = os.path.join(advancedsettings_folder, '2plus.xml')
	elif selection==4:
		xml = os.path.join(advancedsettings_folder,'shield.xml')
	elif selection==5:
		if os.path.exists(advancedsettings_xml):
			os.unlink(advancedsettings_xml)
		xbmc.sleep(1000)
		dialog.ok(addon_name, 'Advanced Settings have been deleted. Kodi will now close to apply the settings.')
		os._exit(1)
	else:
		return
	if os.path.exists(advancedsettings_xml):
		os.unlink(advancedsettings_xml)
	shutil.copyfile(xml, advancedsettings_xml)
	xbmc.sleep(1000)
	dialog.ok(addon_name, 'Advanced Settings have been set. Kodi will now close to apply the settings.')
	os._exit(1)

def fresh_start():
	from .params import p
	mode = p.get_mode()
	yesFresh = dialog.yesno('Fresh Start', 'Are you sure you wish to clear all data?  This action cannot be undone.', nolabel='No', yeslabel='Fresh Start')
	if yesFresh:
		
		#Skin Switch
		if not currSkin() in ['skin.estuary']:
			swapSkins('skin.estuary')
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
			save_backup()
			
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
		if mode == 4:
			save_restore()
			setting_set('firstrun', 'true')
			setting_set('buildname', 'No Build Installed')
			setting_set('buildversion', '0')
			dialog.ok(addon_name, 'Fresh Start Complete. Click OK to Force Close Kodi.')
			os._exit(1)
	else:
		return

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
    xbmcgui.Dialog().notification(addon_name, str(file_count)+' packages cleared.', addon_icon, 5000, sound=False)