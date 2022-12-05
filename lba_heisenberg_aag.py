### Imports v###
from sage.all import *
from sage.algebras.lie_algebras import *
from sage.rings.integer_ring import ZZ

import numpy as np
from numpy.random import default_rng

### Definitions ###

def generate_random_element(ring, x, y, z):
    """
    Generate a random element elt = x**xc * y**yc *z**zc
    Where xc, yc, and zc are randomly picked inside the Ring ring provided
    (Heisenberg H_3 specific procedure)
    """
    min_bound = -100000
    max_bound = 100000
    xc = ring.random_element(min_bound, max_bound)
    yc = ring.random_element(min_bound, max_bound)
    zc = ring.random_element(min_bound, max_bound)
    return x**xc * y**yc *z**zc

def generate_aag_public_key(x, y, z, size_public_key):
    """
    Generation of the AAG public key of the size specificed picking up random
    element in the Heisenberg group whose generators are x, y, z
    (Heisenberg H_3 specific procedure)
    """
    ring = ZZ #Ring of integers
    public_key = [generate_random_element(ring,x,y,z) for i in range(size_public_key)]
    return np.array(public_key)

def generate_aag_private_key(N, public_key, size_private_key):
    """
    Generation of the AAG private key which is a NxN matrix using
    size_private_key distinct elements from the public_key provided
    """
    assert size_private_key <= len(public_key)
    rng = default_rng() # https://numpy.org/doc/stable/reference/random/index.html
    indices = rng.permutation(np.arange(len(public_key))) # permute indices
    drawn_indices = indices[0:size_private_key] # extract indices
    exponents = rng.choice(a=[-1, 1], size=size_private_key) # exponents

    private_key = sage.all.identity_matrix(N) #init with identity and multiply from there
    for i in range(size_private_key):
        private_key *= public_key[drawn_indices[i]]**exponents[i]
    return private_key, drawn_indices, exponents

def conjugate_public_by_private(private_key, public_key):
    """
    This is the step in AAG where Alice conjugates every individual element of
    Bob's public key with its private key and communicate the result to Bob
    publicly
    """
    inv_private_key = private_key**-1
    conjugated_public_key = np.copy(public_key)
    for i in range(len(public_key)):
        conjugated_public_key[i] = inv_private_key * conjugated_public_key[i] * private_key
    return conjugated_public_key

def compute_shared_secret(private_key, drawn_indices, exponents, conjugated_public_key):
    """
    AAG computation of the shared secret
    """
    secret = private_key**-1
    for i in range(len(drawn_indices)):
        secret *= conjugated_public_key[drawn_indices[i]]**exponents[i]
    return secret

def aag_heisenberg(alice_sizes, bob_sizes, r=0, printvar = False):
    """
    Implementation of the AAG Key Exchange on the usual Heisenberg Group H_3
    (3x3 upper triangular matrices with ones on the diagonal)

    Input:
        - alice_size=[size_alice_public_key, size_alice_private_key]
        - bob_size=[size_bob_public_key, size_bob_private_key]alice_sizes, bob_sizes, r=0, printvar = False)
        - r= modulo involved in the computation for the Ring base
        - printvar= turn to True to print the different keys and material used
          in the computaiton of the derivation of the AAG protocol
    Output:
        - Return if Alice and Bob were able to derive the same shared secret
          (which should always be the case as this is the result of the AAG
          protocol)
    """
    # Ring base Z/RZ - ZZ.quo(R*ZZ) = Ring of integers modulo R
    R = ZZ.quo(r*ZZ)
    # Rank of the Heisenberg Algebra: H^(2n+1)
    # https://doc.sagemath.org/html/en/reference/algebras/sage/algebras/lie_algebras/heisenberg.html
    n = sage.all.Integer(1)
    # Heisenberg Group
    # https://doc.sagemath.org/html/en/reference/groups/sage/groups/matrix_gps/heisenberg.html
    H = sage.all.groups.matrix.Heisenberg(n, R)
    X, Y, Z = H.gens()
    ## Size of public and private keys for AAG
    La_size_public = Integer(alice_sizes[0]) # length of Alice's public key
    La_size_private = Integer(alice_sizes[1]) # length of Alice's private key
    Lb_size_public = Integer(bob_sizes[0]) # length of Bob's public key
    Lb_size_private = Integer(bob_sizes[1]) # length of Bob's private key

    a_public_key = generate_aag_public_key(X, Y, Z, La_size_public)
    b_public_key = generate_aag_public_key(X, Y, Z, Lb_size_public)

    a_private_key, a_drawn_indices, a_exponents = generate_aag_private_key(2*n+1, a_public_key, La_size_private)
    b_private_key, b_drawn_indices, b_exponents =  generate_aag_private_key(2*n+1, b_public_key, Lb_size_private)

    b_conjugated_public_key = conjugate_public_by_private(a_private_key, b_public_key)
    a_conjugated_public_key = conjugate_public_by_private(b_private_key, a_public_key)

    a_shared_secret = compute_shared_secret(a_private_key, a_drawn_indices, a_exponents, a_conjugated_public_key)
    b_shared_secret = compute_shared_secret(b_private_key, b_drawn_indices, b_exponents, b_conjugated_public_key)

    if (printvar):
        print("Alice")
        print("public_key: ", a_public_key)
        print("---")
        print("private_key:", a_private_key)
        print("---")
        print("drawn_indices:", a_drawn_indices)
        print("---")
        print("exponents:", a_exponents)
        print("---")
        print("conjugated", b_conjugated_public_key)
        print("---")
        print("shared secret:", a_shared_secret)
        print("---")
        print("Bob")
        print("public_key: ", b_public_key)
        print("---")
        print("private_key:", b_private_key)
        print("---")
        print("drawn_indices:", b_drawn_indices)
        print("---")
        print("exponents:", b_exponents)
        print("---")
        print("conjugated", a_conjugated_public_key)
        print("---")
        print("shared secret:", b_shared_secret)
        print("---")
        print("inv shared secret:", b_shared_secret**-1)
        print("---")
    # let's check that the shared secrets are identical and that there are equal
    # to what is expected
    return (a_shared_secret == b_shared_secret**-1) and (a_shared_secret == a_private_key**-1 * b_private_key**-1 * a_private_key * b_private_key)

def lba_heisenberg(alice_sizes, bob_sizes, r=0, printvar = False):
    """
    """
    return

##################
# Main
##################
# Random seed
set_random_seed()
print(aag_heisenberg(alice_sizes=[10,2], bob_sizes=[10,4]))



