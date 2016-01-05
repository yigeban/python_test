import pexpect
import argparse

PROMPT = ['#','>>>','>','\$']

def send_command(child,cmd):
	child.sendline(cmd)
	child.expect(PROMPT)
	print(child.before)

def connect(user,host,password):
	ssh_newkey = 'Are you sure you want to continue connecting'
	connStr = 'ssh '+user+'@'+host
	child = pexpect.spawn(connStr)
	ret = child.expect([pexpect.TIMEOUT,ssh_newkey,'[P|p]assword:'])
	if ret == 0:
		print('[-] Error Connecting')
		return
	if ret == 1:
		child.sendline('yes')
		ret = child.expect([pexpect.TIMEOUT,'[P|p]assword:'])
	if ret == 0:
		print('[-] Error Connecting')
		return
	child.sendline(password)
	child.expect(PROMPT)
	return child

def main():
	parser = argparse.ArgumentParser('usage -H <host> -u <user> -p <password> -c <command>')	
	parser.add_argument('-H',dest='host',type=str,help='target host')
	parser.add_argument('-u',dest='user',type=str,help='target user')
	parser.add_argument('-p',dest='password',type=str,help='target password')
	parser.add_argument('-c',dest='command')
	args = parser.parse_args()
	host = args.host
	user = args.user
	password = args.password
	cmd = args.command
	child = connect(user,host,password)
	send_command(child,cmd)

if __name__ == '__main__':
	main()
