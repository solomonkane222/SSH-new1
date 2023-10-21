import sys
import pexpect

ip_address = input('Enter IP address: ')
username = input('Enter username: ')
password = input('Enter password: ')
password_enable = input('Enter enable password: ')

session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    sys.exit(1)  # Exit the script with an error code

session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('--- FAILURE! entering password: ', password)
    sys.exit(1)  # Exit the script with an error code

session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('--- Failure! entering enable mode')
    sys.exit(1)  # Exit the script with an error code

session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('--- Failure! entering enable mode after sending password')
    sys.exit(1)  # Exit the script with an error code

session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('--- Failure! entering config mode')
    sys.exit(1)  # Exit the script with an error code

hostname = input('Enter new hostname: ')
session.sendline('hostname ' + hostname)
result = session.expect([r'{}\(config\)#'.format(hostname), pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('--- Failure! setting hostname')
    sys.exit(1)  # Exit the script with an error code

session.sendline('exit')

print('------------------------------------------------------')
print('')
print('--- Success! connecting to: ', ip_address)
print('---              Username: ', username)
print('---              Password: ', password)
print('---              New Hostname: ', hostname)
print('')
print('------------------------------------------------------')

session.close()
