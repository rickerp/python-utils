from passlib.context import CryptContext


class PasswordController(CryptContext):
    def __init__(self):
        super().__init__(schemes=["bcrypt"], deprecated="auto")
