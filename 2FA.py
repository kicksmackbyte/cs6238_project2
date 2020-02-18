import cmd


#TODO
def _exists(username):
    return False


#TODO
def _update_shadow_file(username):
    pass


#TODO
def _update_password_file(username):
    pass


#TODO
def _create_home_directory(username):
    pass


def _create_user(username, password, salt, token):
    exists = _exists(username)

    if exists:
        message = 'FAILURE: user <%s> already exists' % username
        raise Exception(message)

    _update_shadow_file(username)
    _update_password_file(username)

    _create_home_directory(username)

    return 65534


def _check_username(username):
    exists = _exists(username)

    if not exists:
        message = 'FAILURE: user <%s> does not exist' % username
        raise Exception(message)


#TODO
def _login(username, password, current_token, next_token):
    pass


#TODO
def _update_user(username, password, new_password, new_salt, current_token, next_token):
    pass


#TODO
def _delete_user(username, password, current_token):
    pass


class TwoFactorAuthentication(cmd.Cmd):
    '''Two Factor Authentication'''


    def do_1(self, line):
        try:
            username = input('username: ')
            password = input('password: ')
            salt = input('salt: ')
            token = input('initial token: ')

            user_id = _create_user(username, password, salt, token)

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
            _check_username(username)

            password = input('password: ')
            current_token = input('current token: ')
            next_token = input('next token: ')

            _login(username, password, current_token, next_token)
        except Exception as e:
            print(str(e))
        else:
            print('SUCCESS: Login Successful')


    def help_2(self):
        print('Login')


    def do_3(self, line):
        try:
            username = input('username: ')
            _check_username(username)

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
            _check_username(username)

            password = input('password: ')
            current_token = input('current token: ')

            _delete_user(username, password, current_token)
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

    if len(sys.argv) > 1:
        TwoFactorAuthentication().onecmd(' ',join(sys.argv[1:]))
    else:
        TwoFactorAuthentication().cmdloop()


if __name__ == '__main__':
    main()
