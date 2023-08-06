The RSA algorithm is an asymmetric cryptography algorithm, 
which means that it uses a public key and a private key 
(i.e two different, mathematically linked keys). 
As their names suggest, a public key is shared publicly 
while a private key is secret and must not be shared with anyone.

The RSA algorithm is named after Ron Rivest, Adi Shamir, and Leonard Adleman
who invented it in 1978.

In the code written, the key_Pairs() function returns the public as well as
private keys, which themselves contain 2 values. So, while calling the
function, make sure to use 2 variables, one for the public key and another
for the private key.

The actual parameters to the encrypt_data() function should be the plain text 
taken input by the user, and the public key. The function returns the 
cipher text.

The actual parameters to the decrypt_data() function should be the cipher 
text, and the private key. The function returns the decrypted text,
which is the original plain text.

Happy Cryptography !!