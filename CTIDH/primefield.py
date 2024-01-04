from sage.all import GF, proof, is_prime
from sage.rings.finite_rings.integer_mod import IntegerMod_gmp, IntegerMod_int

proof.arithmetic(False)


def PrimeField(p: int):
    if not is_prime(p):
        raise ArithmeticError('Cannot construct Fp: p is not a prime!')
    
    GFp = GF(p)

    # other can have type ZModPrime or int
    def get_value(other):
        if isinstance(other, ZModPrime):
            return other.x
        elif isinstance(other, int):
            return other
        else:
            raise TypeError('Cannot get the value of (type:{}) {}!'.format(type(other), other))

    # TODO: Maybe rewrite get_value and operators with this decorator. Just for touching fish and learning python ×
    # def check_other_type_and_return(f):
    #   def wrapper(x, other):
    #       if isinstance(other, ZModPrime):
    #           return f(x.x, other.x)
    #       elif isinstance(other, int):
    #           return f(x.x, other)
    #   return wrapper

    class ZModPrime:        
        add_count = 0
        sqr_count = 0
        mul_count = 0
        pow_count = 0
        inv_count = 0    

        # self.x always has the type IntegerMod_gmp when p is large or IntegerMod_int
        def __init__(self, x):
            if isinstance(x, IntegerMod_gmp) or isinstance(x, IntegerMod_int):
                self.x = x
            elif isinstance(x, int):
                self.x = GFp(x)
            else:
                raise TypeError('Cannot convert {} type {} to a ZModPrime!'.format(type(x), x))

        def __add__(self, other):
            ZModPrime.add_count += 1
            other = get_value(other)
            return ZModPrime(self.x + other)
            
        def __radd__(self, other):
            return self + other
        
        def __iadd__(self, other):
            ZModPrime.add_count += 1
            other = get_value(other)
            self.x = self.x + other
            return self

        def __sub__(self, other):
            ZModPrime.add_count += 1
            other = get_value(other)
            return ZModPrime(self.x - other)

        def __rsub__(self, other):
            return -self + other
        
        def __isub__(self, other):
            ZModPrime.add_count += 1
            other = get_value(other)
            self.x -= other
            return self
        
        def __mul__(self, other):
            ZModPrime.mul_count += 1
            other = get_value(other)
            return ZModPrime(self.x * other)
        
        def __rmul__(self, other):
            return self * other
        
        def __imul__(self, other):
            ZModPrime.mul_count += 1
            other = get_value(other)
            self.x = self.x * other
            return self
        
        # TODO: Maybe implment div rdiv and idiv?
        def __div__(self, other):
            raise NotImplementedError
        
        def __rdiv__(self, other):
            raise NotImplementedError
        
        def __idiv__(self, other):
            raise NotImplementedError


        def __pow__(self, other):
            # TODO: write a fast constant-time power if it is slow
            raise NotImplementedError

        def __invert__(self, other):
            # TODO: write a fast constant-time invert if it is slow
            raise NotImplementedError
        
        def __neg__(self): 
            return ZModPrime(-self.x)

        def __eq__(self, other):
            other = get_value(other)
            return self.x == other

        def copy(self):
            ret = object.__new__(ZModPrime)
            ret.x = self.x
            return ret
        
        @classmethod
        def reset_runtime(cls):
            cls.add_count = 0
            cls.sqr_count = 0
            cls.mul_count = 0

        @classmethod
        def show_runtime(cls, label:str):
            print(
                "| %s: %7dM + %7dS + %7da"
                % (label, cls.mul_count, cls.sqr_count, cls.add_count),
                end="\t",
            )
        @classmethod
        def show_sqr_pow(cls, label:str):
            print(
                "| %s: %2dP + %2dI"
                % (label, cls.pow_count, cls.inv_count),
                end="\t",
            )
            

    return ZModPrime

