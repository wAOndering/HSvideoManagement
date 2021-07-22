import glob
import os 

mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
files = glob.glob(mainPath+'/**/*.mp4')

for i in files:
	os.remove(i)