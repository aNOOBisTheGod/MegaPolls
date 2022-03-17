class UserException(Exception):
    def __init__(self, message='User not found! Create account or log in pls'):
        self.message = message
        super().__init__(self.message)