//
//  PolynomialCalc.hpp
//  PolynomialCalc
//

#ifndef PolynomialCalc_hpp
#define PolynomialCalc_hpp

#include <math.h>
#include <thread>

#ifdef __cplusplus
   extern "C" {
#endif

namespace Polynomial{
    float polynomial_calc(float x, float a0, float a1, float a2, float a3, unsigned int sleep_time);
}

#ifdef __cplusplus
   }
#endif
       
#endif /* PolynomialCalc_hpp */
