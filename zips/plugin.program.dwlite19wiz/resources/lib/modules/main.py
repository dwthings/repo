from xbmcgui import dialog
from .tools import save_check, save_move1

def main(NAME, NAME2, VERSION, URL, ICON, FANART, DESCRIPTION):
	
	yesInstall = dialog.yesno(NAME, 'The wizard is ready to install your build.', nolabel='Cancel', yeslabel='Continue')
	if yesInstall:
	    save_check()
	    save_move1()
	    yesFresh = dialog.yesno('Fresh Start', 'Do you wish to clear all data before installing?', nolabel='No', yeslabel='Fresh Start')
	    if yesFresh:
	    	from .freshstart import freshStart
	    	freshStart()
	    from .buildinstall import buildInstall
	    buildInstall(NAME, NAME2, VERSION, URL)
	else:
		return