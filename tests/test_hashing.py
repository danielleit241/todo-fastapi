from app.utils.hashing import Hash
import pytest

@pytest.mark.parametrize("password", [
    "simplepassword",
    "P@ssw0rd!",
    "1234567890",
    "complex_password_with_$ymbols_and_NUM83RS"
])
def test_hashing_and_verify_password_success(password):
    hashed_password = Hash.argon2(password)
    assert Hash.verify_argon2(password, hashed_password)

@pytest.mark.parametrize("password", [
    "short",
    "anotherwrongpassword",
    "different_password_123"
])
def test_verify_password_failure(password):
    hashed_password = Hash.argon2(password)
    wrong_password = password + "_wrong"
    assert not Hash.verify_argon2(wrong_password, hashed_password)


@pytest.mark.parametrize("password1, password2", [
    ("unique_password_1", "unique_password_2"),
    ("anotherPassword!", "anotherPassword!Different"),
    ("12345abcde", "12345ABCDE"),
    ("Complex$Pass1", "Complex$Pass2")
])
def test_hashing_different_passwords_produce_different_hashes(password1, password2):
    hashed_password1 = Hash.argon2(password1)
    hashed_password2 = Hash.argon2(password2)
    assert hashed_password1 != hashed_password2
    assert Hash.verify_argon2(password1, hashed_password1)
    assert Hash.verify_argon2(password2, hashed_password2)
    assert not Hash.verify_argon2(password1, hashed_password2)
    assert not Hash.verify_argon2(password2, hashed_password1)
    