import glob
import os


mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
files = glob.glob(mainPath+'/**/*.mp4')

def filestoReDo(filesList, lowlim = 100*10**6):
	sizeAll = []
	for i in filesList:
	    size = os.path.getsize(i)
	    dat = pd.DataFrame({'fileName': [i], 'size': [size]})
	    # print(dat)
	    sizeAll.append(dat)

	sizeAll = pd.concat(sizeAll)
	deletelist = list(sizeAll.loc[sizeAll['size'] <= lowlim, 'fileName'])

	redolist= []
	for i in deletelist:
		tmp = i.split('.')[0]+'.avi'
		os.remove(i)
		redolist.append(tmp)


	return redolist, deletelist

redolist, deletelist = filestoReDo(files)

