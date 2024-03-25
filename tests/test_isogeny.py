import unittest
from copy import deepcopy
# from random import randint

from sage.all import EllipticCurve, proof, GF, PolynomialRing, ZZ

from CTIDH import PrimeField, MontgomeryCurve, MontgomeryIsogeny

from CTIDH.utils import read_prime_info, batchmaxprime_of_Li, get_randint


p1024_info = read_prime_info("p1024_CTIDH")
p2048_info = read_prime_info("p2048_CTIDH")
p1024 = p1024_info["p"]
p2048 = p2048_info["p"]


sage_GFp1024 = GF(p1024)
sage_GFp2048 = GF(p2048)

MontCurve_p1024 = MontgomeryCurve("p1024_CTIDH")
MontCurve_p2048 = MontgomeryCurve("p2048_CTIDH")

Fp1024 = MontCurve_p1024.field
Fp2048 = MontCurve_p2048.field

isogeny_tvelu_p1024 = MontgomeryIsogeny("tvelu")(MontCurve_p1024)
isogeny_tvelu_p2048 = MontgomeryIsogeny("tvelu")(MontCurve_p2048)

# NOTE: To test velusqrt, Add hvelu in the future. Maybe also add svelu.


def get_sage_montgomery_curve(sage_Fp, a: int):
    return EllipticCurve(sage_Fp, [0, a, 0, 1, 0])


def get_affine_from_projective(A: list) -> int:
    """Given A = (Ax: Az), Az!= 0, compute a = Ax * Az^(-1).

    Args:
        A (list): [Ax, Az] that represents (Ax:Az), where Ax, Az are ZModPrime
    """
    Ax, Az = A[0], A[1]
    assert len(A) == 2
    assert Az != 0

    a = Ax * Az ** (-1)
    return int(a.get_int_value())


class TestMontgomeryIsogeny(unittest.TestCase):
    # def test_kps_t(self, num_curve=5, num_isogeny=5):
    #     for sage_Fp, field, MontCurve, MontIsogeny in [
    #         (GF(p1024), Fp1024, MontCurve_p1024, isogeny_tvelu_p1024),
    #         (GF(p2048), Fp2048, MontCurve_p2048, isogeny_tvelu_p2048)
    #     ]:
    #         def test_one_curve(a=field(0), num_isogeny=num_isogeny):
    #             A = (a, field(1))
    #             A24 = (a+2, field(4))

    #             sage_EC = get_sage_montgomery_curve(sage_Fp, a.get_int_value())
    #             for _ in range(num_isogeny):
    #                 P, _ = MontCurve.elligator(A)
    #                 d_fake = (MontCurve.L[get_randint(0, MontCurve.n - 1)] - 1) // 2
    #                 Xi_Zis = MontIsogeny.kps_t(d_fake, P, A24)
    #                 self.assertEqual(len(Xi_Zis), d_fake)
    #                 self.assertEqual(Xi_Zis[0], P)

    #                 k = get_randint(1, d_fake)

    #                 Px = get_affine_from_projective(P)
    #                 P_sage = sage_EC.lift_x(sage_Fp(Px))
    #                 kP_sage = k * P_sage
    #                 self.assertEqual(get_affine_from_projective(Xi_Zis[k-1]), kP_sage.xy()[0])

    #         test_one_curve(a=field(0), num_isogeny=2*num_isogeny)
    #         for _ in range(num_curve-1):
    #             test_one_curve(a=field.get_random())

    # def test_xisog_t(self, num_curve=5, num_isogeny=5):
    #     for sage_Fp, field, MontCurve, MontIsogeny in [
    #         (GF(p1024), Fp1024, MontCurve_p1024, isogeny_tvelu_p1024),
    #         (GF(p2048), Fp2048, MontCurve_p2048, isogeny_tvelu_p2048)
    #     ]:
    #         # test and return a new curve's coefficient, because we need to ensure the curve is supersingular
    #         def test_one_curve(a=field(0), num_isogeny=num_isogeny) -> int:
    #             A = (a, field(1))
    #             A24 = (a+2, field(4))

    #             sage_EC = get_sage_montgomery_curve(sage_Fp, a.get_int_value())
    #             A_new = 1
    #             for _ in range(num_isogeny):
    #                 ind = get_randint(0, MontCurve.n - 1)
    #                 l = MontCurve.L[ind]
    #                 # print(f'ind = {ind}')
    #                 l_fake = batchmaxprime_of_Li(ind, MontCurve.batch_start, MontCurve.batch_stop, MontCurve.L)
    #                 d = (l-1) // 2
    #                 d_fake = (l_fake - 1)//2

    #                 assert d_fake >= d

    #                 while True:
    #                     P, _ = MontCurve.elligator(A)
    #                     P = MontCurve.xdbl(P, A24); P = MontCurve.xdbl(P, A24) # clear cofactor
    #                     for j in range(ind):
    #                         P = MontCurve.xmul_public(P, A24, j)
    #                     for j in range(ind+1, MontCurve.n):
    #                         P = MontCurve.xmul_public(P, A24, j)
    #                     if not MontCurve.isinfinity(P):
    #                         break

    #                 Xi_Zis = MontIsogeny.kps_t(d_fake, P, A24)
    #                 Xi_Zi_hats = [(Xi+Zi, Xi-Zi) for (Xi, Zi) in Xi_Zis]

    #                 A_new = MontIsogeny.xisog_t(d, d_fake, Xi_Zi_hats, A)

    #                 Px = sage_Fp(get_affine_from_projective(P))
    #                 sage_P = sage_EC.lift_x(Px)
    #                 phi = sage_EC.isogeny(kernel=sage_P, model='montgomery')
    #                 # print(f'codomain is {phi.codomain()}')
    #                 sage_A_new = phi.codomain().a2()
    #                 self.assertEqual(sage_Fp(get_affine_from_projective(A_new)), sage_A_new)

    #             return int(get_affine_from_projective(A_new))

    #         a_new = test_one_curve()
    #         for _ in range(num_curve-1):
    #             a_new = test_one_curve(field(a_new))

    # def test_xeval_t(self, num_curve=5, num_isogeny=3):
    #     for sage_Fp, field, MontCurve, MontIsogeny in [
    #         (GF(p1024), Fp1024, MontCurve_p1024, isogeny_tvelu_p1024),
    #         (GF(p2048), Fp2048, MontCurve_p2048, isogeny_tvelu_p2048)
    #     ]:
    #         # test and return a new curve's coefficient, because we need to ensure the curve is supersingular
    #         def test_one_curve(a=field(0), num_isogeny=num_isogeny) -> int:
    #             A = (a, field(1))
    #             A24 = (a+2, field(4))

    #             sage_EC = get_sage_montgomery_curve(sage_Fp, a.get_int_value())
    #             A_new = 1
    #             for _ in range(num_isogeny):
    #                 ind = get_randint(0, MontCurve.n - 1)
    #                 l = MontCurve.L[ind]
    #                 # print(f'ind = {ind}')
    #                 l_fake = batchmaxprime_of_Li(ind, MontCurve.batch_start, MontCurve.batch_stop, MontCurve.L)
    #                 d = (l-1) // 2
    #                 d_fake = (l_fake - 1)//2

    #                 assert d_fake >= d

    #                 while True:
    #                     T, _ = MontCurve.elligator(A)
    #                     P = T
    #                     P = MontCurve.xdbl(P, A24); P = MontCurve.xdbl(P, A24) # clear cofactor
    #                     for j in range(ind):
    #                         P = MontCurve.xmul_public(P, A24, j)
    #                     for j in range(ind+1, MontCurve.n):
    #                         P = MontCurve.xmul_public(P, A24, j)
    #                     if not MontCurve.isinfinity(P):
    #                         break

    #                 Xi_Zis = MontIsogeny.kps_t(d_fake, P, A24)
    #                 Xi_Zi_hats = [(Xi+Zi, Xi-Zi) for (Xi, Zi) in Xi_Zis]

    #                 A_new = MontIsogeny.xisog_t(d, d_fake, Xi_Zi_hats, A)
    #                 phi_T = MontIsogeny.xeval_t(d, d_fake, Xi_Zi_hats, T)

    #                 Px = sage_Fp(get_affine_from_projective(P))
    #                 sage_P = sage_EC.lift_x(Px)
    #                 self.assertEqual(sage_P.order(), l)
    #                 sage_phi = sage_EC.isogeny(kernel=sage_P, model='montgomery')
    #                 Tx = get_affine_from_projective(T)
    #                 sage_T = sage_EC.lift_x(sage_Fp(Tx))
    #                 sage_phi_Tx = sage_phi(sage_T).xy()[0]

    #                 self.assertEqual(sage_phi_Tx, get_affine_from_projective(phi_T))

    #             return int(get_affine_from_projective(A_new))

    #         a_new = test_one_curve()
    #         for _ in range(num_curve-1):
    #             a_new = test_one_curve(field(a_new))

    def test_tvelu(self, num_curve=5, num_isogeny=5):
        for sage_Fp, field, MontCurve, MontIsogeny in [
            (GF(p1024), Fp1024, MontCurve_p1024, isogeny_tvelu_p1024),
            # (GF(p2048), Fp2048, MontCurve_p2048, isogeny_tvelu_p2048) # too slow for a routine test
        ]:
            # test and return a new curve's coefficient, because we need to ensure the curves we choose are all supersingular
            def test_one_curve(a=field(0), num_isogeny=num_isogeny) -> int:
                A = (a, field(1))
                A24 = (a + 2, field(4))

                sage_EC = get_sage_montgomery_curve(sage_Fp, a.get_int_value())
                A_new = 1
                for _ in range(num_isogeny):
                    ind = get_randint(0, MontCurve.n - 1)
                    # ind = get_randint(0, 15)
                    l = MontCurve.L[ind]
                    # print(f'ind = {ind}')
                    l_fake = batchmaxprime_of_Li(
                        ind, MontCurve.batch_start, MontCurve.batch_stop, MontCurve.L
                    )
                    d = (l - 1) // 2
                    d_fake = (l_fake - 1) // 2

                    assert d_fake >= d

                    while True:
                        T, _ = MontCurve.elligator(A)
                        P = T
                        P = MontCurve.xdbl(P, A24)
                        P = MontCurve.xdbl(P, A24)  # clear cofactor
                        for j in range(ind):
                            P = MontCurve.xmul_public(P, A24, j)
                        for j in range(ind + 1, MontCurve.n):
                            P = MontCurve.xmul_public(P, A24, j)
                        if not MontCurve.isinfinity(P):
                            break

                    # Do kps_t and test
                    Xi_Zis = MontIsogeny.kps_t(d_fake, P, A24)
                    Xi_Zi_hats = [(Xi + Zi, Xi - Zi) for (Xi, Zi) in Xi_Zis]

                    self.assertEqual(len(Xi_Zis), d_fake)
                    self.assertEqual(Xi_Zis[0], P)
                    bound = d_fake - 1 if d_fake <= l else l - 1
                    k = get_randint(1, bound)
                    Px = get_affine_from_projective(P)
                    P_sage = sage_EC.lift_x(sage_Fp(Px))
                    kP_sage = k * P_sage
                    self.assertEqual(
                        get_affine_from_projective(Xi_Zis[k - 1]), kP_sage.xy()[0]
                    )

                    # test the correctness of xisog_t, xeval_t
                    A_new = MontIsogeny.xisog_t(d, d_fake, Xi_Zi_hats, A)
                    phi_T = MontIsogeny.xeval_t(d, d_fake, Xi_Zi_hats, T)

                    Px = sage_Fp(get_affine_from_projective(P))
                    sage_P = sage_EC.lift_x(Px)
                    self.assertEqual(sage_P.order(), l)
                    sage_phi = sage_EC.isogeny(kernel=sage_P, model="montgomery")
                    Tx = get_affine_from_projective(T)
                    sage_T = sage_EC.lift_x(sage_Fp(Tx))
                    sage_phi_Tx = sage_phi(sage_T).xy()[0]

                    sage_A_new = sage_phi.codomain().a2()
                    a_new = get_affine_from_projective(A_new)
                    self.assertEqual(
                        sage_Fp(a_new), sage_A_new
                    )

                    self.assertEqual(sage_phi_Tx, get_affine_from_projective(phi_T))

                return a_new

            a_new = test_one_curve()
            for _ in range(num_curve - 1):
                a_new = test_one_curve(field(a_new))


    def test_matryoshka_isogeny_tvelu(self, num_curve=5, num_batch=2, num_primes_per_batch=3):
        for sage_Fp, field, MontCurve, MontIsogeny in [
            (GF(p1024), Fp1024, MontCurve_p1024, isogeny_tvelu_p1024),
            # (GF(p2048), Fp2048, MontCurve_p2048, isogeny_tvelu_p2048),  # tooo slow for a routine test
        ]:
            batch_start, batch_stop, L, L_len = MontCurve.batch_start, MontCurve.batch_stop, MontCurve.L, MontCurve.n
            # test and return a new curve's coefficient, because we need to ensure the curves we choose are all supersingular
            def test_one_curve(a=field(0), num_batch=num_batch) -> int:
                A = (a, field(1))
                A24 = (a + 2, field(4))
                sage_Ea = get_sage_montgomery_curve(sage_Fp, a.get_int_value())
                sage_E_minus_a = get_sage_montgomery_curve(sage_Fp, -a.get_int_value())
                # NOTE: Tnewlen must be chosen here, otherwise we are not able to verify the constant-time property in our following code. 
                Tnewlen = get_randint(0, 2**32-1) % 3
                assert 0 <= Tnewlen <= 2

                def test_one_batch(num_primes_per_batch=num_primes_per_batch):
                    # Things to check: 
                    # 1. Anew correct
                    # 2. Ts_new correct 
                    # 3. the numbers of Fp-operations are (exactly) the same with different l in the same batch
                    mul_counts = []
                    sqr_counts = []
                    add_counts = []
                    pow_counts = []
                    # invert_count should always be 0

                    # Choose a batch
                    # b = get_randint(0, len(MontCurve.batch_start) - 1) # tooo slow for traditinal velu..
                    b = get_randint(0, 8)
                    # print(f'Testing batch {b}, curve a = {a}\n')

                    for _ in range(num_primes_per_batch):
                        ind = get_randint(batch_start[b], batch_stop[b] - 1) # index of l in L
                        rand = get_randint(0, 2**32-1)
                        is_positive_action = True if rand % 2 == 0 else False # Decide which point (P+ or P-) is the kernel point
                        
                        # print(f'\nA = {A}')
                        # print(f'Testing prime l = {L[ind]}.')
                        # print(f'is_positive_action = {is_positive_action}')

                        P = (field(0), field(1))
                        while True:
                            T_plus, T_minus = MontCurve.elligator(A)                             
                            P_tmp = deepcopy(T_plus) if is_positive_action else deepcopy(T_minus)

                            P_tmp = MontCurve.xdbl(P_tmp, A24)
                            P_tmp = MontCurve.xdbl(P_tmp, A24)  # clear cofactor
                            for j in range(ind):
                                if MontCurve.isinfinity(P_tmp):
                                    break # will continue the while loop
                                P_tmp = MontCurve.xmul_public(P_tmp, A24, j)
                            for j in range(ind + 1, L_len):
                                if MontCurve.isinfinity(P_tmp):
                                    break # will continue the while loop
                                P_tmp = MontCurve.xmul_public(P_tmp, A24, j)
                            if MontCurve.isinfinity(P_tmp):
                                continue
                            else:
                                P = deepcopy(P_tmp)
                                break
                        
                        Ts = [T_plus, T_minus]
                        T0, T1 = deepcopy(T_plus), deepcopy(T_minus) # Save T0, T1 to check the correctness of pushing point

                        field.reset_runtime()
                        field.reset_power_invert_time()

                        Anew, Ts_new = MontIsogeny.matryoshka_isogeny(A, Ts, Tnewlen, P, ind)
                        phi_T0, phi_T1 = Ts_new
                        # Check Anew and Ts_new are correct
                        if Tnewlen <= 1:
                            self.assertEqual(Ts_new[1], Ts[1])
                        if Tnewlen == 0:
                            self.assertEqual(Ts_new[0], Ts[0])
                        
                        self.assertEqual(field.inv_count, 0)
                        # Save the numbers of other Fp-operations
                        mul_counts.append(field.mul_count)
                        sqr_counts.append(field.sqr_count)
                        add_counts.append(field.add_count)
                        pow_counts.append(field.pow_count)
                       
                        if is_positive_action:   
                            # Check Anew is correct                                
                            Px = sage_Fp(get_affine_from_projective(P))
                            sage_P = sage_Ea.lift_x(Px)
                            self.assertEqual((ZZ(L[ind]) * sage_P).is_zero(), True) # check sage_P's order == L[ind]
                            if L[ind] <= 200: # l <= 200 use traditional velu
                                sage_phi = sage_Ea.isogeny(kernel=sage_P, model="montgomery", check=False)
                            else:
                                sage_phi = sage_Ea.isogeny(kernel=sage_P, model="montgomery", algorithm='velusqrt', check=False)
                            sage_a_new = sage_phi.codomain().a2()
                            a_new = get_affine_from_projective(Anew)
                            self.assertEqual(a_new, sage_a_new)
                            # Check two points
                            if Tnewlen >= 1:
                                T0x = get_affine_from_projective(T0)
                                # TODO: Check which one is faster (x_rational_map or point pushing)
                                sage_T0 = sage_Ea.lift_x(sage_Fp(T0x))
                                sage_phi_T0x = sage_phi(sage_T0).xy()[0]
                                # sage_phi_T0x = sage_phi.x_rational_map()(T0x)
                                self.assertEqual(sage_phi_T0x, get_affine_from_projective(phi_T0))
                            if Tnewlen == 2:
                                T1x = get_affine_from_projective(T1)
                                sage_phi_T1x = sage_phi.x_rational_map()(T1x)
                                self.assertEqual(sage_phi_T1x, get_affine_from_projective(phi_T1))
                        else: # negative action
                            # Check Anew
                            Px = sage_Fp(get_affine_from_projective(P))
                            sage_P = sage_E_minus_a.lift_x(-Px) # (x,iy) -> (-x, y)
                            sage_P = sage_E_minus_a(sage_P)
                            self.assertEqual((ZZ(L[ind]) * sage_P).is_zero(), True) # check sage_P's order == L[ind]
                            # FIXME: invalid parameters to EllipticCurveIsogeny constructor
                            if L[ind] <= 200: # l <= 200 use traditional velu
                                sage_phi = sage_E_minus_a.isogeny(kernel=sage_P, model="montgomery", check=False)
                            else:
                                sage_phi = sage_E_minus_a.isogeny(kernel=sage_P, model="montgomery", algorithm='velusqrt', check=False)
                            sage_a_new = sage_phi.codomain().a2()
                            a_new = get_affine_from_projective(Anew)
                            self.assertEqual(a_new, -sage_a_new) # sage's codomain is E_{-a'}
                            # Check two points
                            if Tnewlen >= 1:
                                T0x = get_affine_from_projective(T0)
                                sage_phi_T0x = sage_phi.x_rational_map()(-T0x) # reason same as above
                                self.assertEqual(-sage_phi_T0x, get_affine_from_projective(phi_T0)) # reason same as above
                            if Tnewlen == 2:
                                T1x = get_affine_from_projective(T1)
                                # # TODO: Check which one is faster (x_rational_map or point pushing)
                                sage_T1 = sage_E_minus_a.lift_x(sage_Fp(-T1x))
                                sage_phi_T1x = sage_phi(sage_T1).xy()[0]
                                # sage_phi_T1x = sage_phi.x_rational_map()(-T1x) # reason same as above
                                self.assertEqual(-sage_phi_T1x, get_affine_from_projective(phi_T1)) # reason same as above
                            

                        # print(f'a = {a}')

                        # print(f'a_new = {a_new}')
                        # print(f'sage_Anew = {sage_Anew}')
                        # print(f'sage_Enew = {sage_phi.codomain()}')


                    # Check the numbers of Fp-operations are (exactly) the same with different l in the same batch
                    # print(f'add_count={add_counts[0]}, mul_count={mul_counts[0]}, sqr_count={sqr_counts[0]}')
                    for j in range(1, num_primes_per_batch):
                        self.assertEqual(add_counts[0], add_counts[j])
                        self.assertEqual(mul_counts[0], mul_counts[j])
                        self.assertEqual(sqr_counts[0], sqr_counts[j])
                        self.assertEqual(pow_counts[0], pow_counts[j])
                    return int(a_new)
                
                a_new = 0
                for _ in range(num_batch):
                    a_new = test_one_batch()
                return a_new

            a_new = test_one_curve()
            for _ in range(num_curve - 1):
                a_new = test_one_curve(field(a_new))
    

    def test_kps_s(self, num_curve=5, num_isogeny=3):
        pass

    def test_xisog_s(self, num_curve=5, num_isogeny=3):
        pass

    def test_xeval_s(self, num_curve=5, num_isogeny=3):
        pass

    def test_svelu(self, num_curve=5, num_isogeny=3):
        pass

    def test_matryoshka_isogeny_svelu(self, num_curve=5, num_isogeny=3):
        pass
