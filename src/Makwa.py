import secrets,KDF,ArytmetykaModularna

"""
Verifies the MAKWA hash of a message against an expected value.
* Compares expected value of hash with computed value for input
Parameters:
* message (str or bytes) - the input message to verify
* salt (bytes) - the salt used in hashing
* mcost (int) - the memory cost parameter
* postHashingLength (int) - length of the output after post-hashing KDF
* preHashing (bool) - whether to pre-hash the message
* modulus (int) - the modulus used in MAKWA
* expectedValue (str) - the expected hash value (hex string)
* p (int, optional) - first prime factor of modulus (default=1)
* q (int, optional) - second prime factor of modulus (default=1)
Output:
* (bool) - True if hash matches expectedValue, else False
"""
def makwa_verify(message, salt, mcost, postHashingLength, preHashing,modulus,expectedValue, p = 1,q=1):
    if p > 1 and q > 1:
        hash = makwa_hash(message, salt, mcost, postHashingLength, preHashing, modulus,p,q)
    else:
        hash = makwa_hash(message, salt, mcost, postHashingLength, preHashing, modulus)
    if hash.upper() == expectedValue.upper():
        return True
    else:
        return False
"""
Generates a cryptographically secure random 16-byte salt.
Output:
* (bytes) - 16 random bytes to be used as salt
"""
def generate_salt():
    return secrets.token_bytes(16)
"""
Computes the MAKWA hash of a message.

Parameters:
* message (str or bytes) - input message to hash
* salt (bytes) - salt used in hashing
* mcost (int) - memory cost parameter (number of iterations)
* postHashingLength (int) - output length after post-hashing KDF
* preHashing (bool) - whether to pre-hash the message before processing
* modulus (int) - modulus used in MAKWA calculations
* p (int, optional) - first prime factor of modulus (default=1)
* q (int, optional) - second prime factor of modulus (default=1)
Output:
* (str) - hex string of the resulting hash
Raises:
* ValueError if parameters are invalid or message too long
"""
def makwa_hash(message, salt, mcost, postHashingLength, preHashing,modulus, p=1,q=1):
    mcost += 1
    # Verify input types and constraints
    if not isinstance(message, bytes):
      message = message.encode('utf-8')
    if mcost < 0:
        raise ValueError('mcost is negative')
    modulusByteLength = (modulus.bit_length()+7)//8
    if modulusByteLength < 160:
        return ValueError('modulusByteLength is too small')
    u  = len(message)
    if u > 255 or u > (modulusByteLength - 32):
        raise ValueError('message is too long')
    # Pre-hash the message if enabled
    if preHashing:
        message = KDF.kdf(message,64)
        u = len(message)
    # Prepare input block for modular exponentiation
    x = salt + message + bytes([u])
    sb = KDF.kdf(salt + message + bytes([u]),modulusByteLength - 2 - u)
    xb = bytes([0x00]) + sb + message + bytes([u])
    x = int.from_bytes(xb, byteorder='big')

    # Perform main modular exponentiation using quick or normal path depends on knowledge about factorisation
    if p > 1 and q > 1 and modulus == p * q:
        x = ArytmetykaModularna.quickPath(x,p,q,mcost)
    else:
        x = ArytmetykaModularna.normalPath(x,modulus,mcost)

    out = x
    # Convert the result back to bytes
    out = out.to_bytes(modulusByteLength, byteorder='big')
    # Apply post-hashing if required
    if postHashingLength > 0:
        out = KDF.kdf(out,postHashingLength)

    return out.hex()
"""
Checks whether given p and q are Blum primes (both congruent to 3 mod 4).
Parameters:
* p (int) - first prime candidate
* q (int) - second prime candidate
Output:
* bool - True if both p and q are Blum primes, False otherwise
"""
def checkIsBlumNumber(p,q):
    if (p % 4 != 3) or (q % 4 != 3):
        return False
    return True

