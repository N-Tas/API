from pydantic import BaseModel
import ctypes
import pathlib
import random

# -------------------------------------------------------------------
# Model Cubic Equation/Polynomial used as model_ce
# Guarantees the types. Pass the how obj after POST
# Cubic Equation: f(x) = a0 + a1x + a2x2 + a3x3
# -------------------------------------------------------------------        
class CubicEQN(BaseModel):
    # Polynomial
    x: float  
    polynomial = [0.0, 0.0, 0.0, 0.0]

# -------------------------------------------------------------------
# Dictionary to return after GET
# -------------------------------------------------------------------   
class PolynomialDict(dict):
    # Construct
    def __init__(self):
        self = dict()
          
    # Add key:value
    def add(self, id, val):
        self[id] = val
        
    # Get the value with id
    def getVal(self,id):
        return self[id]

# -------------------------------------------------------------------
# Class to store Pairs of ID & Polynomial
# Get ID direct after POST to return null if polynomial not comp.
# -------------------------------------------------------------------
class Pair:
    # Construct 
    def __init__(self,id,model_ce):
        self.id = id
        self.model_ce = model_ce
            
# -------------------------------------------------------------------
# Ctypes load lib
# -------------------------------------------------------------------
class Bindigns():
    # Load the shared library into ctypes at construction
    # The shared library is in the same directory as the Python script
    def __init__(self,c_lib_name):
        libname = pathlib.Path().absolute() / c_lib_name
        self.c_lib = ctypes.CDLL(libname)
        self.c_lib.polynomial_calc.restype = ctypes.c_float
        self.SLEEP_TIME_MIN = 5
        self.SLEEP_TIME_MAX = 25
          
    # Calc the cubic polynomial with the c++ function
    # Compute random time added to simulate different process times
    def polynomial_calc(self, model_ce : CubicEQN):
        compute_time = random.randint(self.SLEEP_TIME_MIN, self.SLEEP_TIME_MAX)
        result = self.c_lib.polynomial_calc(ctypes.c_float(float(model_ce.x)),
                            ctypes.c_float(float(model_ce.polynomial[0])),
                            ctypes.c_float(float(model_ce.polynomial[1])),
                            ctypes.c_float(float(model_ce.polynomial[2])),
                            ctypes.c_float(float(model_ce.polynomial[3])),
                            abs(compute_time))
        return result,compute_time