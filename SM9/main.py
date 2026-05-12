from bn256 import G1, G2, GT
from poly_utils import PrimeField
from polynomials import univariate_multiply_polynomials, gen_bivariate_polynomial_u_xy, phase_three, evaluate_univariate_polynomial_at_x, evaluate_bivariate_polynomial_at_x_y, mod_inverse
import random
import hashlib


modulus = 21888242871839275222246405745257275088548364400416034343698204186575808495617
f = PrimeField(modulus)



def Setup():
    alpha = random.randint(1, modulus)
    beta = random.randint(1, modulus)
    P_pub = G2.scalar_base_mult(alpha)
    B = G2.scalar_base_mult(beta)
    return P_pub,alpha,B


def FixKeyGen(alpha,ID):
    Q_ID = int(hashlib.sha256(ID).hexdigest(), 16)%modulus
    SK_ID = G1.scalar_base_mult(f.mul( alpha, mod_inverse(alpha + Q_ID,modulus)))
    return SK_ID


def TmpKeyGen(B,SK_ID,ID,i):
    rho = random.randint(1, modulus)

    S_ID_i = G1.scalar_base_mult(rho)
    S_ID_i_2 = G2.scalar_base_mult(rho)
    C_i = G2.scalar_mult(B,rho)
    t_ID_i = 1111
    T_ID_i = G1.scalar_mult(SK_ID,rho)
    J_i = G1.scalar_base_mult(f.mul(rho, mod_inverse(rho + t_ID_i,modulus)))
    TSK_i = (S_ID_i,S_ID_i_2,C_i,T_ID_i,J_i)
    return TSK_i

def Sign(P_pub,TSK_i,ID,i,M):
    S_ID_i,S_ID_i_2,C_i,T_ID_i,J_i = TSK_i
    # r = 45641521619521
    r = random.randint(1, modulus)
    w1 = GT.pair(G1.scalar_mult(S_ID_i,r),P_pub)
    w2 = GT.pair(G1.scalar_mult(S_ID_i,r),G2.scalar_base_mult(1))

    print("w1:",w1)
    print("w2:",w2)
    h = 232323
    l = (r-h)%modulus
    S_i = G1.scalar_mult(T_ID_i,l)
    V_i = G1.scalar_mult(J_i,l)
    sigma = (S_ID_i,S_ID_i_2,C_i,S_i,h,V_i)

    return sigma

def Verify(B,P_pub,ID,i,sigma,M):
    S_ID_i,S_ID_i_2,C_i,S_i,h,V_i = sigma
    assert GT.pair(G1.scalar_base_mult(1),C_i)==GT.pair(S_ID_i,B)
    print("pass")

    Q_ID =  int(hashlib.sha256(ID).hexdigest(), 16)%modulus
    t_ID_i = 1111
    w1pie = GT.add(
        GT.pair(S_i,G2.add(
            G2.scalar_base_mult(Q_ID),P_pub
        )),
        GT.pair(G1.scalar_mult(S_ID_i,h),P_pub)
    )
    print("w1pie:",w1pie)
    w2pie = GT.add(
        GT.pair(V_i,G2.add(
            G2.scalar_base_mult(t_ID_i),S_ID_i_2
        )),
        GT.pair(G1.scalar_mult(S_ID_i,h),G2.scalar_base_mult(1))
    )
    print("w2pie:",w2pie)
    b = 0
    return b

# k1, g1 = G1.random_g1()
# k2, g2 = G2.random_g2()

# gt = GT.pair(g1, g2)

# print(gt.marshal().hex())

def SM9_test(modulus):
    ID = b"1234564897654866456"
    P_pub,alpha,B = Setup()
    SK_ID = FixKeyGen(alpha,ID)
    i = 1
    TSK_i = TmpKeyGen(B,SK_ID,ID,i)
    M = b"Hello world"
    sigma = Sign(P_pub,TSK_i,ID,i,M)
    b = Verify(B,P_pub,ID,i,sigma,M)





if __name__ == "__main__":
    SM9_test(modulus)



















# #插值的最小的x坐标，即omega_{l}
# omega_x = f.exp(3, (modulus-1)//l)
# print("(modulus-1)//l",(modulus-1)//2)
# print("(modulus-1)%l",(modulus-1)%l)
# omega_y = f.exp(3, (modulus-1)//n)
# print("(modulus-1)%n",(modulus-1)%n)
# xs = get_power_cycle(omega_x, modulus) # x坐标集合, omega^0....omega^{l-1}
# print(omega_y)
# # ys = get_power_cycle(omega_y, modulus) # y坐标集合
# # print((modulus-1)%l)



