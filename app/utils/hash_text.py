from argon2 import PasswordHasher, exceptions as argon2_exceptions

password_hasher = PasswordHasher()

# Hash Password
def password_hash(password: str):
    return password_hasher.hash(password=password)

# Validate password hash
def verify_password(simple_text: str, hash_text: str):
    try:
        return password_hasher.verify(hash_text, simple_text)
    except argon2_exceptions.VerifyMismatchError:
        return False
    except Exception:
        return False



