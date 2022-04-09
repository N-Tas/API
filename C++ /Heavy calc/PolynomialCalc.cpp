//
//  PolynomialCalc.cpp
//  PolynomialCalc
//


#include "PolynomialCalc.hpp"

float Polynomial::polynomial_calc(float x, float a0, float a1, float a2, float a3, unsigned int sleep_time){
    //Cubical equation f(x) = a0 + a1x + a2x2 + a3x3
    float res = 0;
    res = a0 + a1*x + a2*pow(x,2) + a3*pow(x,3);
    //Sleep for the time passed from python.
    std::this_thread::sleep_for(std::chrono::seconds(sleep_time));
    return res;
    }
