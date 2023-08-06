import pytest
import own_blockchain_sdk.crypto

def test_encode_decode_base64():
    original_data = 'Chainium'
    expected = 'Q2hhaW5pdW0='
    actual = own_blockchain_sdk.crypto.encode64(original_data.encode())
    decoded = own_blockchain_sdk.crypto.decode64(actual).decode()
    assert expected == actual
    assert original_data == decoded

def test_encode_decode_base58():
    original_data = 'Chainium'
    expected = 'CGwVR5Wyya4'
    actual = own_blockchain_sdk.crypto.encode58(original_data.encode())
    decoded = own_blockchain_sdk.crypto.decode58(actual).decode()
    assert expected == actual
    assert original_data == decoded

def test_hash(): 
    original_data = 'Chainium'
    expected = 'Dp6vNLdUbRTc1Y3i9uSBritNqvqe4es9MjjGrVi1nQMu'
    actual = own_blockchain_sdk.crypto.hash(original_data.encode())
    assert expected == actual

def test_derive_hash():
    address = 'CHPJ6aVwpGBRf1dv6Ey1TuhJzt1VtCP5LYB'
    nonce = 32
    tx_action_number = 2
    expected = '5kHcMrwXUptjmbdR8XBW2yY3FkSFwnMdrVr22Yg39pTR'
    actual = own_blockchain_sdk.crypto.derive_hash(address, nonce, tx_action_number)
    assert expected == actual

def test_generate_wallet():
    private_key, address = own_blockchain_sdk.crypto.generate_wallet()
    expected = address   
    actual = own_blockchain_sdk.crypto.address_from_private_key(private_key)
    assert expected == actual
    
def test_address_from_private_key():
    private_key = '3rzY3EENhYrWXzUqNnMEbGUr3iEzzSZrjMwJ1CgQpJpq'
    expected = 'CHGmdQdHfLPcMHtzyDzxAkTAQiRvKJrkYv8'
    actual = own_blockchain_sdk.crypto.address_from_private_key(private_key)
    assert expected == actual
    
def test_sign_message():
    network_code = 'UNIT_TESTS'
    private_key = '3rzY3EENhYrWXzUqNnMEbGUr3iEzzSZrjMwJ1CgQpJpq'
    tx = 'Chainium'
    expected = 'EYzWMyZjqHkwsNFKcFEg4Q64m4jSUD7cAeKucyZ3a9MKeNmXTbRK3czqNVGj9RpkPGji9AtGiUxDtipqE3DtFPHxU'
    actual = own_blockchain_sdk.crypto.sign_message(network_code, private_key, tx)
    assert expected == actual
    
def test_sign_plain_text():
    private_key = '3rzY3EENhYrWXzUqNnMEbGUr3iEzzSZrjMwJ1CgQpJpq'
    text = 'Chainium'
    expected = 'EzCsWgPozyVT9o6TycYV6q1n4YK4QWixa6Lk4GFvwrj6RU3K1wHcwNPZJUMBYcsGp5oFhytHiThon5zqE8uLk8naB'
    actual = own_blockchain_sdk.crypto.sign_plain_text(private_key, text)
    assert expected == actual
    
def test_verify_plain_text_signature():
    private_key, address = own_blockchain_sdk.crypto.generate_wallet()
    expected = own_blockchain_sdk.crypto.address_from_private_key(private_key)
    text = 'Chainium'
    signature = own_blockchain_sdk.crypto.sign_plain_text(private_key, text)
    actual = own_blockchain_sdk.crypto.verify_plain_text_signature(signature, text)
    assert expected == actual
