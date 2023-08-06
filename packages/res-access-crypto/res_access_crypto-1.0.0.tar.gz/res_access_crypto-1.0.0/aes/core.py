import os, codecs, io

import pyAesCrypt


def generate_aes_key(n=32):
	random_bytes = os.urandom(n)
	aes_key = codecs.encode(random_bytes, "hex")
	
	return aes_key.decode()


def decrypt_aes_key(encrypted_aes_key, private_key, public_params):
	from ibe.ibe_rsa import decrypt_using_rsa

	decrypted_aes_key = decrypt_using_rsa(encrypted_aes_key, private_key,
		public_params)

	return codecs.decode(decrypted_aes_key, "utf-8")


def decrypt_file_as_stream(encrypted_file, encrypted_aes_key, recipient_id,
	private_key, public_param):
	# Decrypt AES Key using IBE
	decrypted_aes_key = decrypt_aes_key(encrypted_aes_key, private_key,
		public_param)

	# Decrypt file using AES Key
	decrypted_file = decrypt_file_using_aes_as_stream(encrypted_file,
		decrypted_aes_key)

	return decrypted_file


def encrypt_file_using_aes_as_stream(plain_text_file_bytes, key):
	buffer_size = 64 * 1024

	plain_text_file_stream = io.BytesIO(plain_text_file_bytes)
	encrypted_file_stream = io.BytesIO()

	pyAesCrypt.encryptStream(plain_text_file_stream, encrypted_file_stream,
		key, buffer_size)

	encrypted_file_stream.seek(0)
	return encrypted_file_stream.read()


def decrypt_file_using_aes_as_stream(encrypted_file_bytes, decrypted_aes_key):
	buffer_size = 64 * 1024

	decrypted_file_stream = io.BytesIO()
	ctlen = len(encrypted_file_bytes)
	encrypted_file_stream = io.BytesIO(encrypted_file_bytes)
	
	pyAesCrypt.decryptStream(encrypted_file_stream, decrypted_file_stream,
		decrypted_aes_key, buffer_size, ctlen)

	decrypted_file_stream.seek(0)
	return decrypted_file_stream.read()
