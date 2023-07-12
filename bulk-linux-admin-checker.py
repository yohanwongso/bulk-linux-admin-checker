from paramiko import SSHClient,AutoAddPolicy
from re import match

uname = ""
pword = ""

list_ip_file = open("ip.txt", "r")

for ip_with_enter in list_ip_file:
    ip = ip_with_enter.replace("\n", "")

    client = SSHClient()
    #client.load_system_host_keys()
    #client.load_host_keys('~/.ssh/known_hosts')
    client.set_missing_host_key_policy(AutoAddPolicy())

    client.connect(ip, username = uname, password = pword)

    stdin, stdout, stderr = client.exec_command('sudo -u root whoami')

    # print(f'STDOUT: {stdout.read().decode("utf8")}')
    output = stdout.read().decode("utf8").replace("\n", "")
    pattern = '^root$'
    if match(pattern, output):
        print (ip, "\tRoot")
    else:
        print (ip, "\tNot Root")

    stdin.close()
    stdout.close()
    stderr.close()
    client.close()
