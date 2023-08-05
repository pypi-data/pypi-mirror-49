[![CircleCI](https://circleci.com/gh/mmontagna/generic-encryptors/tree/master.svg?style=svg)](https://circleci.com/gh/mmontagna/generic-encryptors/tree/master) [![PyPI version](https://badge.fury.io/py/generic-encryptors.svg)](https://badge.fury.io/py/generic-encryptors)

# Generic encryptors

A set of encryptors which provide an interface compatible with https://github.com/mmontagna/generic-encoders currently only AES is supported. 

## Installation

```
$ pip install generic-encoders
```

## Usage 

### Basic Example
```
>>> import os
>>> from generic_encryptors import AesEncryptor
>>> 
>>> key = os.urandom(32)
>>> encryptor = AesEncryptor(key=key)
>>> encryptor.encode('My secret data')
"\x10\x00\x00\x00\xe98\xabw\xb0?Kg\x8d2\x97=j\xed\xcfM \x00\x00\x00'awM\x04)\x13\xaf\x8a\xa9\xd6\xf7A\xf8\xf0\xa9\x1e\x81yG\x95q\x14\n\xb7\x8b'\x94`\x7f;q8\xb4\xc4\x1e\xb3\xcf{\xea8\xfd\xe5\x95\xa2\xb8\xc9\x04"
>>> encryptor.decode(encryptor.encode('My secret data'))
'My secret data'
```

### Combining Encryptors with other Encoders

Encryptors and Encoders can be composed via the ComposedEncoder class see https://github.com/mmontagna/generic-encoders

```
>>> import os
>>> from generic_encoders import ComposedEncoder, MsgPackEncoder, Lz4Encoder, Base64Encoder, TextEncoder
>>> from generic_encryptors import AesEncryptor
>>> 
>>> encoder = ComposedEncoder(MsgPackEncoder(), Lz4Encoder(), AesEncryptor(key=os.urandom(32)), Base64Encoder())
>>> 
>>> encoder.encode("Secret")
'EAAAAPbD4YUBYQs2g4sS9R4Py0sgAAAAo0NjO5OyJHvELhGZ6Wj4WkISA6BuB/mjuw7GeSpjGqCj4E5A3UHmbmCfvaLKcx5i0jDc/Gi3yCpLQ3Wd5y9etg=='
>>> 
>>> encoder.decode(encoder.encode("Secret"))
'Secret'

```

If an encoder is not capable of accepting the output/input of a parent encoder an EncoderLinkError exception will be raised. 



## Supported Encoders

* [aes](#aes-encryptor)


### AES Encryptor

The AES encryptor encrypts data via the AES algorithm more info here: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard

It generates a new Initializatio Vector (IV) for every call to encrypt and prepends the IV to each encrypted output, subsequent calls to decrypt read the IV from the output.

This encryptor also generates a hmac on every call to encrypt and inserts the hmac into the output, calls to decrypt then verify the hmac signature is valid. See https://docs.python.org/2/library/hmac.html for more info.

The format of the output is:
int - length of IV
string - Initialization Vector
int - lenght of HMAC
string - HMAC
string - encrypted data.

Example:

```
>>> import os
>>> from generic_encryptors import AesEncryptor
>>> 
>>> key = os.urandom(32)
>>> encryptor = AesEncryptor(key=key)
>>> encryptor.encode('My secret data')
"\x10\x00\x00\x00\xe98\xabw\xb0?Kg\x8d2\x97=j\xed\xcfM \x00\x00\x00'awM\x04)\x13\xaf\x8a\xa9\xd6\xf7A\xf8\xf0\xa9\x1e\x81yG\x95q\x14\n\xb7\x8b'\x94`\x7f;q8\xb4\xc4\x1e\xb3\xcf{\xea8\xfd\xe5\x95\xa2\xb8\xc9\x04"
>>> encryptor.decode(encryptor.encode('My secret data'))
'My secret data'
```