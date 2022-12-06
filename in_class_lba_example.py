import numpy as np

a1 = Matrix(ZZ, [[1,1,2], [0,1,3], [0,0,1]])
a2 = Matrix(ZZ, [[1,1,1], [0,1,1], [0,0,1]])
a3 = Matrix(ZZ, [[1,0,1], [0,1,1], [0,0,1]])
alice_public_key = np.array( [a1, a2, a3]); alice_public_key

A = a2 * a3**-1; A

b1 = Matrix(ZZ, [[1,2,3], [0,1,3], [0,0,1]])
b2 = Matrix(ZZ, [[1,6,3], [0,1,1], [0,0,1]])
bob_public_key = np.array([b1, b2]); bob_public_key

b1_prime = A**-1 * b1 * A; b1_prime
b2_prime = A**-1 * b2 * A; b2_prime

# attack
#fail
a1**-1 * b1_prime * a1
a1**-1 * b2_prime * a1
#correct
b1_temp_prime = a3**-1 * b1_prime * a3; b1_temp_prime
b2_temp_prime = a3**-1 * b2_prime * a3; b2_temp_prime
#fail
a1 * b1_temp_prime * a1**-1
a1 * b2_temp_prime * a1**-1
#correct
a2 * b1_temp_prime * a2**-1
a2 * b2_temp_prime * a2**-1

#conjugation factors and revert back to key:
A_lba -a2*a3**-1; A_lba



