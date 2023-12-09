from cryptography.fernet import Fernet
import base64
import sympy
from random import randint


def generate_prime():
    while True:
        prime = sympy.randprime(2**255, 2**256)
        if sympy.isprime(prime):
            return prime


p = generate_prime()
g = 5


def int_to_bytes(num):
    byte_array = num.to_bytes(32, "little")
    return byte_array


private_key_alice = randint(1, 10000)
private_key_bob = randint(1, 10000)

public_key_alice = pow(g, private_key_alice, p)
public_key_bob = pow(g, private_key_bob, p)

shared_key_alice = pow(public_key_bob, private_key_alice, p)
shared_key_bob = pow(public_key_alice, private_key_bob, p)

assert shared_key_alice == shared_key_bob
f = Fernet(base64.urlsafe_b64encode(int_to_bytes(shared_key_alice)))

message_from_alice = b"Hello Bob!"
encrypted_message_alice = f.encrypt(message_from_alice)

decrypted_message_bob = f.decrypt(encrypted_message_alice).decode()

print("Alice 的公钥:", public_key_alice)
print("Bob 的公钥:", public_key_bob)
print("\n共享密钥:", shared_key_alice)

print("\nAlice 发送加密消息给Bob:", encrypted_message_alice)

print("\nBob 解密消息:", decrypted_message_bob)
