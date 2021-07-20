import glob
import os 

mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
files = glob.glob(mainPath+'/**/*.avi')

for i in files:
	os.remove(i)