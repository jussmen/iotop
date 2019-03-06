#!/usr/bin/python
# coding: utf-8
import os, sys, argparse, time
from datetime import datetime

'''
# iotop

iotop command that can run on F5 BigIP. It lists the top 10 processes of Read and Write in the interval. The data sorce is, read_bytes and write_bytes in /proc/PID/io and /proc/PID/task/io.

See man PROC(5) 
http://man7.org/linux/man-pages/man5/proc.5.html

# Problem that this script solves

F5 BigIP does not have useful linux commands that make difficult to understand which process is writing/reading most

# Options
You do not need any argument or you can specify an interval

-i / --interval : Specify interval in seconds. Default is 2 seconds

# How to use
1. Copy iotop to your BigIP, such as /shared/
2. Give permission
chmod +x /shared/iotop
3. Run
/shared/iotop


Mar 06 2019
Kimihito Tanaka - Sr.Enterprise Network Engineer@F5 Networks
'''

ioFiles = []
ioFileContent = []
topSyscr = {}
topSyscw = {}
topReadBytes = {}
topWriteBytes = {}

def genIoFileList():
	for p in os.listdir('/proc/'):
		if p.isdigit():
			pidIO = '/'.join(['/proc', p, 'io'])
			if os.path.isfile(pidIO):
				ioFiles.append(pidIO)
			for pp in os.listdir('/proc/' + p):
				if pp == 'task':
					pidTaskIO = '/'.join(['/proc', p, 'task', 'io'])
					if os.path.isfile(pidTaskIO):
						ioFiles.append(pidTaskIO)

def readIoFile(ioFile):
	try:
		f = open(ioFile, 'r')
		tmp = f.readlines()[2:6]
		tmp2 = [float(x.strip('\n').split(':')[1].strip(' ')) for x in tmp]
		tmp3 = [ioFile]
		tmp3.extend(tmp2)	
		ioFileContent.append(tmp3)
	except:
		pass

def sortBySyscr():
	ioFileContent.sort(key=lambda x:x[1], reverse=True)

def sortBySyscw():
	ioFileContent.sort(key=lambda x:x[2], reverse=True)

def sortByReadBytes():
	ioFileContent.sort(key=lambda x:x[3], reverse=True)

def sortByWriteBytes():
	ioFileContent.sort(key=lambda x:x[4], reverse=True)

def sanitise(val):
	return float(val.strip('\n').split(':')[1].strip(' '))

def runMonitor(interval):
	readDelta = []
	writeDelta = []
	while True:
		genIoFileList()
		for ioFile in ioFiles:
			readIoFile(ioFile)
		#sortBySyscr()
		#for i in ioFileContent:
		#	topSyscr.update({ i[0] : i[1] })
		#sortBySyscw()
		#for i in ioFileContent:
		#	topSyscw.update({ i[0] : i[2] })
		sortByReadBytes()
		for i in ioFileContent:
			topReadBytes.update({ i[0] : i[3] })
		sortByWriteBytes()
		for i in ioFileContent:
			topWriteBytes.update({ i[0] : i[4] })
		
		time.sleep(interval)
		for k,v in topReadBytes.items():
			try:
				f = open(k, 'r')
				curVal = sanitise(f.readlines()[4])
				if v != curVal:
					l = [k, curVal - v]
					readDelta.append(l)
					#topReadBytes[k] = curVal
				f.close()
			except:
				pass
		readDelta.sort(key=lambda x:x[1], reverse=True)
		print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		print('')
		print('{0:<50}{1:<5}{2:>10}{3:<5}{4:<20}'.format('Readers', ' ', 'Delta Bytes', ' ', 'Source File'))
		for i in range(10):
			try:
				pid = readDelta[i][0].split('/')[2]
				f = open('/proc/' + pid + '/cmdline', 'r')
				cmdline = f.readlines()[0].split('\x00')[0]
				f.close()
				print('{0:<50}{1:<5}{2:>10}{3:<5}{4:<20}'.format(cmdline,  ' ', readDelta[i][1], ' ', readDelta[i][0]))
			except:
				pass
		readDelta = []

		for k,v in topWriteBytes.items():
			try:
				f = open(k, 'r')
				curVal = sanitise(f.readlines()[5])
				if v != curVal:
					l = [k, curVal - v]
					writeDelta.append(l)
					#topReadBytes[k] = curVal
				f.close()
			except:
				pass
		writeDelta.sort(key=lambda x:x[1], reverse=True)
		print('')
		print('{0:<50}{1:<5}{2:>10}{3:<5}{4:<20}'.format('Writers', ' ', 'Delta Bytes', ' ', 'Source File'))
		for i in range(10):
			try:
				pid = writeDelta[i][0].split('/')[2]
				f = open('/proc/' + pid + '/cmdline', 'r')
				cmdline = f.readlines()[0].split('\x00')[0]
				f.close()
				print('{0:<50}{1:<5}{2:>10}{3:<5}{4:<20}'.format(cmdline,  ' ', writeDelta[i][1], ' ', writeDelta[i][0]))
			except:
				pass
		writeDelta = []
		print('-' * 100)



if __name__ == '__main__':
	try:
		parser = argparse.ArgumentParser(description='Display Top Processes for Read and Write')
		parser.add_argument('-i', '--interval', nargs=1, type=float, help='Specify interval in seconds. Default is 2 seconds')
		args = parser.parse_args()
		if args.interval:
			interval = args.interval[0]
		else:
			interval = 2
		runMonitor(interval)

	except (KeyboardInterrupt, IOError): 
		sys.stderr.close()
		sys.exit()  


