import hashlib,hmac

"""
Key Derivation Function (KDF) 
* based on HMAC_DRBG and SHA-256
* use the Python libraries hashlib and hmac
Inputs:
* data (bytes) - the password that will be used in the mixing and hashing operations
* outLength (int) -  desired length of the output
Output:
* T (bytes) - pseudorandom hash of specified length (outLength)
"""
def kdf(data,outLength):
    # Length of the SHA-256 hash output in bytes
    r = hashlib.sha256().digest_size
    # Initialize vectors V and K with length specified in HMAC_DRBG
    V = b'\x01' * r
    K = b'\x00' * r
    # Update K and V with HMAC
    K = hmac.new(K,V + bytes([0x00]) + data, hashlib.sha256).digest()
    V = hmac.new(K,V, hashlib.sha256).digest()
    K = hmac.new(K,V + bytes([0x01]) + data,hashlib.sha256).digest()
    V = hmac.new(K,V,hashlib.sha256).digest()
    # Generate output bytes until desired length reached
    T = b''
    while len(T) < outLength:
        V = hmac.new(K, V, hashlib.sha256).digest()
        T += V
    return T[:outLength]
