from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class Hash:
    @staticmethod
    def argon2(password: str) -> str:
        return password_hash.hash(password)

    @staticmethod
    def verify_argon2(password: str, hashed: str) -> bool:
        return password_hash.verify(password, hashed)