import os
import cmd
import crypt
import shutil


def _check_your_privilege():
    if os.getuid() != 0:
        raise Exception("Please, run as root.")


def _exists(username):
    with open('/etc/shadow', 'r') as shadow_file:
        usernames = [entry.split(':')[0] for entry in shadow_file]
        return username in usernames


def _create_shadow_file_entry(username, password, token, user_id, group_id):
    hardened_password = password + token
    hash_ = crypt.crypt(hardened_password, '$6$' + salt)

    line = '%s:%s:%s' % (username, hash_, 'TODO') #TODO
    #TODO: Write into file


def _create_password_file_entry(username, user_id, group_id):
    user_id = 1234
    group_id = 1234

    home_directory_path = '/home/%s' % username
    bash_path = '/bin/bash'

    line = '%s:%s:%d:%d:%s:%s:%s' % (username, 'x', user_id, group_id, username + ',,,', home_directory_path, bash_path)
    #TODO: Write into file


def _create_home_directory(username):
    home_directory_path = '/home/%s' % username

    try:
        os.makedirs(home_directory_path)
    except:
        pass


#TODO
def _delete_shadow_file_entry(username):
    pass


#TODO
def _delete_password_file_entry(username):
    pass


def _delete_home_directory(username):
    home_directory_path = '/home/%s' % username

    try:
        shutil.rmtree(home_directory_path)
    except:
        pass


#TODO
def _update_shadow_file_entry(username, token, password=None, salt=None):
    pass


def _check_username_exists(username):
    exists = _exists(username)

    if not exists:
        message = 'FAILURE: user <%s> does not exist' % username
        raise Exception(message)


def _validate_credentials(username, password, token):
    with open('/etc/shadow', 'r') as shadow_file:
        for entry in shadow_file:
            split_entry = entry.split(':')
            entry_username = split_entry[0]

            if username == entry_username:
                credentials = split_entry[1]
                _1, _2, salt = credentials.split('$')

                hardened_password = password + token
                result = crypt.crypt(hardened_password, '$6$' + salt)
                return result == credentials


def _login(username, password, current_token, next_token):
    valid_credentials = _validate_credentials(username, password, current_token)

    if valid_credentials:
        _update_shadow_file_entry(username, next_token)
    else:
        message = 'FAILURE: <%s/%s> incorrect' % (password, current_token)
        raise Exception(message)


#TODO
def _generate_user_id():
    pass


#TODO
def _generate_group_id():
    pass


def _create_user(username, password, salt, token):
    exists = _exists(username)

    if exists:
        message = 'FAILURE: user <%s> already exists' % username
        raise Exception(message)

    user_id = _generate_user_id()
    group_id = _generate_group_id()

    _create_shadow_file_entry(username, password, token, user_id, group_id)
    _create_password_file_entry(username, password, token, user_id, group_id)

    return user_id


def _delete_user(username, password, token):
    valid_credentials = _validate_credentials(username, password, token)

    if valid_credentials:
        _delete_shadow_file_entry(username)
        _delete_password_file_entry(username)
    else:
        message = 'FAILURE: <%s/%s> incorrect' % (password, current_token)
        raise Exception(message)


def _update_user(username, password, new_password, new_salt, current_token, next_token):
    valid_credentials = _validate_credentials(username, password, current_token)

    if valid_credentials:
        _update_shadow_file_entry(username, next_token, password=new_password, salt=new_salt)
    else:
        message = 'FAILURE: <%s/%s> incorrect' % (password, current_token)
        raise Exception(message)


class TwoFactorAuthentication(cmd.Cmd):
    '''Two Factor Authentication'''


    def do_1(self, line):
        try:
            username = input('username: ')
            password = input('password: ')
            salt = input('salt: ')
            token = input('initial token: ')

            user_id = _create_user(username, password, salt, token)
            _create_home_directory(username)

        except Exception as e:
            print(str(e))
        else:
            message = 'SUCCESS: <%s> created' % user_id
            print(message)


    def help_1(self):
        print('Create a new user')


    def do_2(self, line):
        try:
            username = input('username: ')
            _check_username_exists(username)

            password = input('password: ')
            current_token = input('current token: ')
            next_token = input('next token: ')

            _login(username, password, current_token)
        except Exception as e:
            print(str(e))
        else:
            print('SUCCESS: Login Successful')


    def help_2(self):
        print('Login')


    def do_3(self, line):
        try:
            username = input('username: ')
            _check_username_exists(username)

            password = input('password: ')
            new_password = input('new_password: ')
            new_salt = input('new_salt: ')
            current_token = input('current token: ')
            next_token = input('next token: ')

            _update_user(username, password, new_password, new_salt, current_token, next_token)
        except Exception as e:
            print(str(e))
        else:
            message = 'SUCCESS: user <%s> updated' % username
            print(message)


    def help_3(self):
        print('Update password')


    def do_4(self, line):
        try:
            username = input('username: ')
            _check_username_exists(username)

            password = input('password: ')
            current_token = input('current token: ')

            _delete_user(username, password, current_token)
            _delete_home_directory(username)
        except Exception as e:
            print(str(e))
        else:
            message = 'SUCCESS: user <%s> Deleted' % username
            print(message)


    def help_4(self):
        print('Delete a user')


    def do_exit(self, line):
        return True


def main():
    import sys

    _check_your_privilege()

    if len(sys.argv) > 1:
        TwoFactorAuthentication().onecmd(' ',join(sys.argv[1:]))
    else:
        TwoFactorAuthentication().cmdloop()


if __name__ == '__main__':
    main()
