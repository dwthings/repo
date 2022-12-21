import xbmc, xbmcgui
import json, base64
import xml.etree.ElementTree as ET
import addonvar
from .maintenance import clear_packages

setting = addonvar.setting
buildfile = addonvar.buildfile
addon_name = addonvar.addon_name
headers = addonvar.headers
notify_url = addonvar.notify_url
setting_set = addonvar.setting_set

current_build = setting('buildname')
try:
	current_version = float(setting('buildversion')) 
except:
	current_version = 0.0

class startup:
	
	def check_updates(self):
	   	if current_build == 'No Build Installed':
	   		return
	   	response = self.get_page(buildfile)
	   	version = 0.0
	   	try:
	   		builds = json.loads(response)['builds']
	   		for build in builds:
	   				if build.get('name') == current_build:
	   					version = float(build.get('version'))
	   					break
	   	except:
	   		builds = ET.fromstring(response)
	   		for tag in builds.findall('build'):
	   				if tag.find('name').text == current_build:
	   					version = float(tag.find('version').text)
	   					break
	   	if version > current_version:
	   		xbmcgui.Dialog().ok(addon_name, 'A new version of ' + current_build +' is available.' + '\n' + 'Installed Version: ' + str(current_version) + '\n' + 'New Version: ' + str(version) + '\n' + 'You can update from the Build Menu in ' + addon_name + '.')
	   	else:
	   		return

	def file_check(self, bfile):
		if addonvar.isBase64(bfile):
			return base64.b64decode(bfile).decode('utf8')
		else:
			return bfile
			
	def get_page(self, url):
	   	from urllib.request import Request,urlopen
	   	req = Request(self.file_check(url), headers = headers)
	   	return urlopen(req).read()
    	
	def save_menu(self):
		save_items = []
		choices = ["Favourites", "Sources", "Debrid - Resolve URL", "Advanced Settings"]
		save_select = addonvar.dialog.multiselect(addon_name + " - Select items to keep during a build install.",choices, preselect=[])
		if save_select == None:
			return
		else:
			for index in save_select:
				save_items.append(choices[index])
		if 'Favourites' in save_items:
			setting_set('savefavs','true')
		else:
			setting_set('savefavs','false')
		if 'Sources' in save_items:
			setting_set('savesources', 'true')
		else:
			setting_set('savesources', 'false')
		if 'Debrid - Resolve URL' in save_items:
			setting_set('savedebrid','true')
		else:
			setting_set('savedebrid','false')
		if 'Advanced Settings' in save_items:
			setting_set('saveadvanced','true')
		else:
			setting_set('saveadvanced','false')
	
		setting_set('firstrunSave', 'true')

	def notify_check(self):
		notify_version = self.get_notifyversion()	
		if not setting('firstrunNotify')=='true' or notify_version > int(setting('notifyversion')):
			self.notification()
			
	def notification(self):
		from resources.lib.GUIcontrol import notify
		d=notify.notify()
		d.doModal()
		del d
		setting_set('firstrunNotify', 'true')
		setting_set('notifyversion', str(self.get_notifyversion()))
	
	def get_notifyversion(self):
		response = self.get_page(notify_url).decode('utf-8')
		try:
			split_response = response.split('|||')
			return int(split_response[0])	
		except:
			return False
	
	def no_buildfile(self):
		xbmcgui.Dialog().ok('No Buildfile', 'Please add a valid buildfile\nto the addonvar.py')

	def run_startup(self):
		if setting('autoclearpackages')=='true':
			clear_packages()
		if 'CHANGEME' in buildfile:
			self.no_buildfile()
		if not setting('firstrunSave')=='true':
			self.save_menu()
		try: self.check_updates()
		except: pass
		try: self.notify_check()
		except: pass
		if setting('firstrun') == 'true':
			from resources.lib.modules import addonsEnable
			addonsEnable.enable_addons()
			xbmc.executebuiltin('UpdateLocalAddons')
			xbmc.executebuiltin('UpdateAddonRepos')
		setting_set('firstrun', 'false')