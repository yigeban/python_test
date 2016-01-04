import argparse
import socket
import threading

screenLock = threading.Semaphore(value=1)
def connScan(tgtHost,tgtPort):
	try:
		connSkt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		connSkt.connect((tgtHost,tgtPort))
		connSkt.send('HelloWorld!\r\n')
		result = connSkt.recv(100)
		screenLock.acquire()
		print('[+]%d/tcp open' % tgtPort)
		print('[+]'+str(result))
	except:
		screenLock.acquire()
		print('[-]%d tcp closed' % tgtPort)
	finally:
		screenLock.release()
		connSkt.close()

def portScan(tgtHost,tgtPorts):
	try:
		tgtIP = socket.gethostbyname(tgtHost)
	except:
		print("[-] Cannot resolve '%s':Unkonwn host" % tgtHost)
		return
	try:
		tgtName = socket.gethostbyaddr(tgtIP)
		print('\n[+] Scan Results for:'+ tgtHost[0])
	except:
		print('\n[+]Scan Results for:'+tgtIP)
	for tgtPort in tgtPorts:
		print('Scaning port:'+str(tgtPort))
		t=threading.Thread(target=connScan,args=(tgtHost,int(tgtPort)))
		t.start()

#portScan('google-public-dns-a.google.com',[80,443,3389,1433])
def main():
	parser = argparse.ArgumentParser('usage %prog -H <target> -p <port>')
	parser.add_argument('-H',dest='tgtHost',help='specify target host')
	parser.add_argument('-p',dest='tgtPort',type=int,nargs='+',help='specify target port')

	args = parser.parse_args()
	tgtHost = args.tgtHost
	tgtPort = args.tgtPort
	if (tgtHost == None) | (tgtPort == None):
	    print(parser.usage)    
	    exit(0) 
	else:
		portScan(tgtHost,tgtPort)
if __name__ == '__main__':
	main()
