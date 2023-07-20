from paramiko import SSHClient,AutoAddPolicy
from re import match
import csv
import yaml

with open('config.yml', 'r') as yaml_config_file:
    config = yaml.safe_load(yaml_config_file)

print(config["ssh"]["username"])

list_ip_file = open("ip.txt", "r")

with open('report.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    csv_header = ["IP", "Status"]
    writer.writerow(csv_header)

    for ip_with_enter in list_ip_file:
        ip = ip_with_enter.replace("\n", "")

        print (ip)

        try:
            client = SSHClient()
            #client.load_system_host_keys()
            #client.load_host_keys('~/.ssh/known_hosts')
            client.set_missing_host_key_policy(AutoAddPolicy())

            client.connect(ip, port = config["ssh"]["port"], username = config["ssh"]["username"], password = config["ssh"]["password"])

            stdin, stdout, stderr = client.exec_command('sudo -u root whoami')

            # print(f'STDOUT: {stdout.read().decode("utf8")}')
            output = stdout.read().decode("utf8").replace("\n", "")
            pattern = '^root$'
            if match(pattern, output):
                root_status = "Admin"
            else:
                root_status = ""

            csv_data = [ip, root_status]
            writer.writerow(csv_data)

            stdin.close()
            stdout.close()
            stderr.close()
            client.close()
        except:
            csv_data = [ip, ""]
            writer.writerow(csv_data)

    f.close()
