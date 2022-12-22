import xbmc
import os, shutil
import addonvar

EXCLUDES = addonvar.EXCLUDES
user_path = addonvar.user_path
data_path = addonvar.data_path
setting = addonvar.setting
addon_id = addonvar.addon_id
packages = addonvar.packages
db_path = addonvar.db_path

def backup(path, file):
	if os.path.exists(os.path.join(path, file)):
		shutil.move(os.path.join(path, file), os.path.join(packages, file))

def restore(path, file):
	if os.path.exists(os.path.join(packages, file)):
		if os.path.exists(os.path.join(path, file)):
			try:
				if os.path.isfile(os.path.join(path, file)) or os.path.islink(os.path.join(path, file)):
					os.unlink(os.path.join(path, file))
				elif os.path.isdir(os.path.join(path, file)):
					shutil.rmtree(os.path.join(path, file))
			except Exception as e:
				xbmc.log('Failed to delete %s. Reason: %s' % (os.path.join(path, file), e), xbmc.LOGINFO)
		shutil.move(os.path.join(packages, file), os.path.join(path, file))

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

def save_backup():
	backup(user_path, addon_id)
	if setting('savefavs')=='true':
		try:backup(user_path, 'favourites.xml')
		except: pass
	if setting('savesources')=='true':
		try: backup(user_path, 'sources.xml')
		except: pass
	if setting('savedebrid')=='true':
		try: backup(data_path, 'script.module.resolveurl')
		except: pass
	if setting('saveadvanced')=='true':
		try: backup(user_path, 'advancedsettings.xml')
		except: pass

def save_restore():
	restore(user_path, addon_id)
	if setting('savefavs')=='true':
		try: restore(user_path, 'favourites.xml')
		except: pass
	if setting('savesources')=='true':
		try: restore(user_path, 'sources.xml')
		except: pass
	if setting('savedebrid')=='true':
		try: restore(data_path, 'script.module.resolveurl')
		except: pass
	if setting('saveadvanced')=='true':
		try: restore(user_path, 'advancedsettings.xml')
		except: pass
	
	shutil.rmtree(packages)