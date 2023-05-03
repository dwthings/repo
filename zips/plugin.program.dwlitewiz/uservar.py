import xbmcaddon

addon_id = xbmcaddon.Addon().getAddonInfo('id')

'''#####-----Build File-----#####'''
buildfile = 'https://raw.githubusercontent.com/dwthings/dwnewwiz/master/builds.xml'

'''#####-----Notifications File-----#####'''
notify_url  = 'https://raw.githubusercontent.com/dwthings/dwnewwiz/master/notify19.txt'

'''#####-----Excludes-----#####'''
excludes  = [addon_id, 'packages', 'backups']
