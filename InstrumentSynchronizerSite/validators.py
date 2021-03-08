# checks if provided passwords matches each other
class PasswordsMatchValidator:
    def __init__(self, password1, password2, message=None):
        self.password1 = password1
        self.password2 = password2
        self.message = message if message else 'Provided passwords does not match'
        self.is_valid = self.__validate()

    def __validate(self):
        if self.password1 == self.password2:
            return True
        else:
            return False