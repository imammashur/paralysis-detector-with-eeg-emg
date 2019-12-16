Download http://www.learningaboutelectronics.com/Code/botbook_mcp3002.txt 
Save dengan nama botbook_mcp3002.py lalu satukan foldernya

import time 
import botbook_mcp3002 as mcp # Coba baca mcp

def readtegangan(): 
	global tegangan 
	tegangan = mcp.readAnalog() # Baca nilai tegangan

def main(): 
	while True:
	readtegangan() # 
	print("The current tegangan value is %i " % tegangan) # 
	time.sleep( 0.5) # Delay pembacaan 

if __name__ = = "__main__": 
	main()
