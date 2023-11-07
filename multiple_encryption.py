from extended_function import extended_function


def double_encrypt(plaintext, key1, key2):
	return extended_function(extended_function(plaintext, key1), key2)


def double_decrypt(ciphertext, key1, key2):
	return extended_function(extended_function(ciphertext, key2, True), key1, True)


if __name__ == '__main__':
	# 第四关：多重加密
	input_text = "Hello world!"

	# 双重加密
	key1 = 0b1111010101110000
	key2 = 12345
	
	ciphertext = double_encrypt(input_text, key1, key2)
	print(ciphertext)
	
	text = double_decrypt(ciphertext, key1, key2)
	print(text)

	# 中间相遇攻击
	mid_texts = {}
	find_keys = []
	
	for key in range(pow(2, 16)):
		mid_texts[extended_function(input_text, key)] = key

	for key in range(pow(2, 16)):
		mid_text = extended_function(ciphertext, key, True)
		if mid_text in mid_texts:
			find_keys.append([mid_texts[mid_text], key])

	print(find_keys)
	
	# 三重加密
	key3 = 0x7F7F

	ciphertext = extended_function(double_encrypt(input_text, key1, key2), key3)
	print(ciphertext)

	text = double_decrypt(extended_function(ciphertext, key3, True), key1, key2)
	print(text)
	