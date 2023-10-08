from cryptography import fernet
import json


class Password(object):
    def __init__(self):
        with open('key.key', 'rb') as key_file:
            self.key = key_file.read()

        with open('passwords.json', 'rb') as passwords_file:
            accounts = passwords_file.read()
            frn = fernet.Fernet(self.key)
            self.accounts = json.loads(frn.decrypt(accounts).decode('utf-8'))

    def end(self):
        with open('passwords.json', 'wb') as passwords_file:
            frn = fernet.Fernet(self.key)
            accounts = frn.encrypt(json.dumps(self.accounts).encode('utf-8'))
            passwords_file.write(accounts)

    def read_passwords(self):
        self.end()
        return self.accounts

    def get_password(self, account):
        self.end()
        return self.accounts[account]

    def add_password(self, account, username, password):
        self.accounts[account] = [username, password]
        self.end()

    def remove_password(self, account):
        try:
            del self.accounts[account]
        except KeyError:
            raise KeyError
        finally:
            self.end()

    def edit_username(self, account, username):
        if account in self.accounts:
            self.accounts[account][0] = username
            self.end()
        else:
            self.end()
            raise KeyError

    def edit_password(self, account, password):
        if account in self.accounts:
            self.accounts[account][1] = password
            self.end()
        else:
            self.end()
            raise KeyError


class AccessCode(object):
    def __init__(self):
        with open('key.key', 'rb') as key_file:
            self.key = key_file.read()
        with open('access_code.json', 'rb') as code_file:
            code = code_file.read()
            frn = fernet.Fernet(self.key)
            self.code = json.loads(frn.decrypt(code).decode('utf-8'))

    def edit(self, new_access_code):
        self.code = new_access_code
        with open('access_code.json', 'wb') as passwords_file:
            frn = fernet.Fernet(self.key)
            passwords = frn.encrypt(json.dumps(self.code).encode('utf-8'))
            passwords_file.write(passwords)


print(
    '© 2021 GOOF                               \n'
    ' ________  _________  _________    ___   \n'
    '/         /  _______ /  _______   /  |   \n'
    '|  ______ |  |     | |  |     | __|_/    \n'
    '|  |__  | |  |___| | |  |___| |   | __   \n'
    '\\_______/ \\________/ \\________/   |/  \n'
    '                                 /\\     \n'
    '                                |  \\    \n'
    '                                \\___|    \n'
    '                                         \n'
    '_____________________  _______________  |\n'
    '                    |                   |\n'
    '|                   |                   |\n'
    '|         ________  |  ________         |\n'
    '|         |         |         |         |\n'
    '|         |         |         |         |\n'
    '|         |_______  |  _______|         |\n'
    '|                   |                   |\n'
    '|                   |                    \n'
    '|  _______________  |____________________\n'
)

login_screen = True
access_code = AccessCode().code

while login_screen:
    access = input('Access code:\t')
    if access == access_code:
        break
    elif access == 'x':
        quit()
    else:
        print('Incorrect access code. Please try again\n')

print('Access granted! Type "x" at anytime to exit\n')

[print(f'{account}\t\t\t\t{values[0]}\t\t\t\t*****\n') for account, values in Password().read_passwords().items()]

print('\nList of available commands :\n')
print('see <account>\t\t\t\t- Reveals username and password, replace <account> with account who\'s password you wish to'
      ' see')
print('add <account> <username> <password>\t- Adds a password, replace <account> with the account, <username> with the '
      'username and  <password> with the password')
print('remove <account>\t\t\t- Removes an account, replace <account> with the account you wish to remove')
print('edituser <account> <password>\t\t- Edits the username for an account, replace <account> with the account you '
      'wish to edit and <username> with the new password')
print('editpass <account> <password>\t\t- Edits the password for an account, replace <account> with the account you '
      'wish to edit and <password> with the new password\n')

script = True

while script:
    command = input('What would you like to do:\t').strip()

    if command == 'x':
        quit()

    command = command.split()

    if command[0] == 'see':
        try:
            acc = Password().get_password(command[1])
            print(f'\n\t{acc[0]}\t{acc[1]}\n')
        except IndexError:
            print('\nPlease specify an account\n')
        except KeyError:
            print('\nThat account does not exist\n')

    elif command[0] == 'add':
        try:
            Password().add_password(command[1], command[2], command[3])
            print(f'\n{command[1]}:\t{command[2]}, {command[3]}\tadded successfully\n')
        except IndexError:
            print('\nPlease specify an account, username, and password\n')

    elif command[0] == 'remove':
        try:
            sure = input(f'\nAre you sure you want to remove {command[1]}? (y/n):\t')
            if sure == 'y':
                try:
                    Password().remove_password(command[1])
                    print(f'\nSuccessfully removed {command[1]}\n')
                except KeyError:
                    print('\nThat account does not exist\n')
            else:
                print('\nDelete cancelled\n')
        except IndexError:
            print('\nPlease specify an account\n')

    elif command[0] == 'edituser':
        try:
            Password().edit_username(command[1], command[2])
            print(f'\nChanged {command[1]} username to {command[2]}\n')
        except IndexError:
            print('\nPlease specify an account & username\n')
        except KeyError:
            print('\nThat account does not exist\n')

    elif command[0] == 'editpass':
        try:
            Password().edit_password(command[1], command[2])
            print(f'\nChanged {command[1]} password to {command[2]}\n')
        except IndexError:
            print('\nPlease specify an account & password\n')
        except KeyError:
            print('\nThat account does not exist\n')

    elif command[0] == 'changecode':
        old_code = input('\nPlease type old code:\t\t')
        if old_code == access_code:
            new_code = input('\nPlease type new code:\t\t')
            confirm_new_code = input('\nPlease confirm new code:\t')
            if new_code == confirm_new_code:
                AccessCode().edit(new_code)
                print('\nAccess code changed\n')
            else:
                print('\nCodes do not match\n')
        else:
            print('\nIncorrect code\n')

    else:
        print('\nUnknown command\n')
