
import hashlib

# One-way permutation function using SHA256
# Already Implemented. 
def OWP(x):
    h = hashlib.sha256()
    h.update(x)
    return h.digest()


# A PRG construction that generates one random bit at a time
# Using the Goldreich-Levin hardcore bit construction that we studied in the class 
class PRG:

    def __init__(self, seed):
        self.r = seed[32:]
        #print (self.r)
        self.x = seed[:32]
        self.f = OWP

    # TODO: Return the inner product between self.r and self.x, and update self.x using self.f
    # HINT: Convert the byte strings to int objects and then use Python's math operators.
    def getbit(self):
        innerprod = 0
        r = int.from_bytes(self.r, byteorder='little')
        intobit_r = [int(x) for x in '{:b}'.format(r)]
        #intobit_r = map(int, [x for x in '{:b}'.format(r)])
        x = int.from_bytes(self.x, byteorder='little')
        intobit_x = [int(x) for x in '{:b}'.format(x)] 
        
        rlen = len(intobit_r)
    
        xlen = len(intobit_x)
     
        difference = 0
        
        if (rlen != xlen):
            if (rlen > xlen):
                difference = rlen - xlen
                for i in range (difference):
                    intobit_x.insert(0,0)
               
            elif (xlen > rlen):
                difference = xlen - rlen
                for i in range (difference):
                    intobit_r.insert(0,0)
      
        for y in range (len(intobit_r)):
            innerprod = innerprod ^ (intobit_r[y] & intobit_x[y])
            
        self.x = self.f(self.x)       
        
        return innerprod



# A Length-doubling PRG construction that extends 512-bit seed to 1024-bit output
# TODO: Using the PRG class, generate 128 bytes from a 64 bytes seed
def double_length(seed):
    result = 0
    prg = PRG(seed)
    s = []
    for i in range (1024):
        s.append(prg.getbit())
   
    tostring = ''.join(map(str,s))
  
    result = int(tostring , 2)     
        
    return result.to_bytes(128, byteorder='little')

if __name__ == '__main__':
    with open("64bytes", "rb") as fp:
        seed = fp.read()
    with open("128bytes", "rb") as fp:
        result = fp.read()
    assert double_length(seed) == result
