/**********************************************************************************
 * Copyright (c) 2019 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 **********************************************************************************/

#pragma once

#include "MAiNGOException.h"

#include "mcop.hpp"

#include <vector>


namespace maingo {


namespace ubp {


/** @brief Operator- for a double vector */
inline std::vector<double>
operator-(const std::vector<double>& in)
{
    std::vector<double> out(in.size());
    for (size_t i = 0; i < in.size(); i++) {
        out[i] = -in[i];
    }
    return out;
}

/** @brief Operator- for a double matrix */
inline std::vector<std::vector<double>>
operator-(const std::vector<std::vector<double>>& in)
{
    std::vector<std::vector<double>> out(in.size());
    for (size_t i = 0; i < in.size(); i++) {
        out[i] = -in[i];
    }
    return out;
}

/** @brief Operator+ for addition of two double vectors */
inline std::vector<double>
operator+(const std::vector<double>& in1, const std::vector<double>& in2)
{
    if (in1.size() != in2.size())
        throw MAiNGOException("  Error: UbpQuadExpr -- inconsistent sizes in vector + operator.");
    std::vector<double> out(in1.size());
    for (size_t i = 0; i < in1.size(); i++) {
        out[i] = in1[i] + in2[i];
    }
    return out;
}

/** @brief Operator+ for addition of two double matrices */
inline std::vector<std::vector<double>>
operator+(const std::vector<std::vector<double>>& in1, const std::vector<std::vector<double>>& in2)
{
    if (in1.size() != in2.size())
        throw MAiNGOException("  Error: UbpQuadExpr -- inconsistent sizes in vector<vector> + operator.");
    std::vector<std::vector<double>> out(in1.size());
    for (size_t i = 0; i < in1.size(); i++) {
        if (in1[i].size() != in2[i].size())
            throw MAiNGOException("  Error: UbpQuadExpr -- inconsistent sizes in vector<vector> + operator.");
        out[i] = in1[i] + in2[i];
    }
    return out;
}

/** @brief Operator- for subtraction of two double vectors */
inline std::vector<double>
operator-(const std::vector<double>& in1, const std::vector<double>& in2)
{
    if (in1.size() != in2.size())
        throw MAiNGOException("  Error: UbpQuadExpr -- inconsistent sizes in vector - operator.");
    std::vector<double> out(in1.size());
    for (size_t i = 0; i < in1.size(); i++) {
        out[i] = in1[i] - in2[i];
    }
    return out;
}

/** @brief Operator- for subtraction of two double matrices */
inline std::vector<std::vector<double>>
operator-(const std::vector<std::vector<double>>& in1, const std::vector<std::vector<double>>& in2)
{
    if (in1.size() != in2.size())
        throw MAiNGOException("  Error: UbpQuadExpr -- inconsistent sizes in vector<vector> - operator.");
    std::vector<std::vector<double>> out(in1.size());
    for (size_t i = 0; i < in1.size(); i++) {
        if (in1[i].size() != in2[i].size())
            throw MAiNGOException("  Error: UbpQuadExpr -- inconsistent sizes in vector<vector> - operator.");
        out[i] = in1[i] - in2[i];
    }
    return out;
}

/** @brief Operator* for multiplication of a double vector with a double constant */
inline std::vector<double>
operator*(const std::vector<double>& in1, const double in2)
{
    std::vector<double> out(in1.size());
    for (size_t i = 0; i < in1.size(); i++) {
        out[i] = in1[i] * in2;
    }
    return out;
}

/** @brief Operator* for multiplication of a double matrix with a double constant */
inline std::vector<std::vector<double>>
operator*(const std::vector<std::vector<double>>& in1, const double in2)
{
    std::vector<std::vector<double>> out(in1.size());
    for (size_t i = 0; i < in1.size(); i++) {
        out[i] = in1[i] * in2;
    }
    return out;
}

/**
* @struct UbpQuadExpr
* @brief Struct used to compute coefficients of linear and quadratic/bilinear terms in (MIQ)Ps.
*        This struct is used to avoid the need of propagating the IloExpr object resulting in HUGE RAM usage.
*/
struct UbpQuadExpr {

  public:
    /**
        * @brief Default constructor
        */
    UbpQuadExpr(){};

    /**
        * @brief Constructor accepting a number of variables
		*
		* @param[in] nvarIn is the number of variables
        */
    UbpQuadExpr(const size_t nvarIn)
    {
        nvar = nvarIn;
        coeffsLin.resize(nvar, 0);
        coeffsQuad.resize(nvar, std::vector<double>(nvar, 0));
        constant = 0;
        hasQuad  = false;
    }

    /**
        * @brief Constructor for a specific variable participating linearly
		*
		* @param[in] nvarIn is the number of variables
		* @param[in] iLin is the number of the variable participating linearly
        */
    UbpQuadExpr(const size_t nvarIn, const size_t iLin)
    {
        if (iLin >= nvarIn) {
            throw MAiNGOException("  Error: UbpQuadExpr -- iLin >= nvarIn.");
        }
        nvar = nvarIn;
        coeffsLin.resize(nvar, 0);
        coeffsLin[iLin] = 1;
        coeffsQuad.resize(nvar, std::vector<double>(nvar, 0));
        constant = 0;
        hasQuad  = false;
    }

    /**
        * @brief Constructor for a constant
		*
		* @param[in] in is the value of the constant
        */
    UbpQuadExpr(const double in)
    {
        nvar = 0;
        coeffsLin.clear();
        coeffsQuad.clear();
        constant = in;
        hasQuad  = false;
    }

    /** @brief Operator= for a double constant */
    UbpQuadExpr& operator=(const double in)
    {
        nvar = 0;
        coeffsLin.clear(), coeffsQuad.clear();
        constant = in;
        hasQuad  = false;
        return *this;
    }

    /** @brief Operator= for an integer constant */
    UbpQuadExpr& operator=(const int in)
    {
        nvar = 0;
        coeffsLin.clear(), coeffsQuad.clear();
        constant = (double)in;
        hasQuad  = false;
        return *this;
    }

    /** @brief Operator+= for UbpQuadExpr */
    UbpQuadExpr& operator+=(const UbpQuadExpr& in)
    {
        if (nvar != in.nvar && (nvar != 0 && in.nvar != 0))
            throw MAiNGOException("  Error: UbpQuadExpr -- nvar does not fit in += operator.");

        if (nvar == 0) {
            coeffsLin  = in.coeffsLin;
            coeffsQuad = in.coeffsQuad;
            constant += in.constant;
        }
        else if (in.nvar == 0) {
            constant += in.constant;
        }
        else {
            coeffsLin  = coeffsLin + in.coeffsLin;
            coeffsQuad = coeffsQuad + in.coeffsQuad;
            constant += in.constant;
        }
        hasQuad = hasQuad || in.hasQuad;
        return *this;
    }

    /** @brief Operator+= for double */
    UbpQuadExpr& operator+=(const double in)
    {
        constant += in;
        return *this;
    }

    /** @brief Operator+= for int */
    UbpQuadExpr& operator+=(const int in)
    {
        constant += in;
        return *this;
    }

    /** @brief Operator-= for UbpQuadExpr */
    UbpQuadExpr& operator-=(const UbpQuadExpr& in)
    {
        if (nvar != in.nvar && (nvar != 0 && in.nvar != 0))
            throw MAiNGOException("  Error: UbpQuadExpr -- nvar does not fit in += operator.");

        if (nvar == 0) {
            coeffsLin  = -in.coeffsLin;
            coeffsQuad = -in.coeffsQuad;
            constant -= in.constant;
        }
        else if (in.nvar == 0) {
            constant -= in.constant;
        }
        else {
            coeffsLin  = coeffsLin - in.coeffsLin;
            coeffsQuad = coeffsQuad - in.coeffsQuad;
            constant -= in.constant;
        }
        hasQuad = hasQuad || in.hasQuad;
        return *this;
    }

    /** @brief Operator-= for double */
    UbpQuadExpr& operator-=(const double in)
    {
        constant -= in;
        return *this;
    }

    /** @brief Operator-= for int */
    UbpQuadExpr& operator-=(const int in)
    {
        constant -= in;
        return *this;
    }

    /** @brief Operator*= for UbpQuadExpr */
    UbpQuadExpr& operator*=(const UbpQuadExpr& in)
    {
        if (nvar != in.nvar && (nvar != 0 && in.nvar != 0))
            throw MAiNGOException("  Error: UbpQuadExpr -- nvar does not fit in * operator.");

        if (nvar == 0) {
            coeffsLin  = in.coeffsLin * constant;
            coeffsQuad = in.coeffsQuad * constant;
            constant   = in.constant * constant;
            hasQuad    = in.hasQuad;
        }
        else if (in.nvar == 0) {
            coeffsLin  = coeffsLin * in.constant;
            coeffsQuad = coeffsQuad * in.constant;
            constant   = constant * in.constant;
        }
        else {
            if (hasQuad || in.hasQuad)
                throw MAiNGOException("  Error: UbpQuadExpr -- multiplications higher than second order are not allowed in (MIQ)Ps.");

            for (size_t i = 0; i < nvar; i++) {
                for (size_t j = 0; j < in.nvar; j++) {
                    coeffsQuad[i][j] = coeffsLin[i] * in.coeffsLin[j];
                }
                coeffsLin[i] = coeffsLin[i] * in.constant + in.coeffsLin[i] * constant;
            }
            constant = in.constant * constant;
            hasQuad  = true;
        }
        return *this;
    }

    /** @brief Operator*= for double */
    UbpQuadExpr& operator*=(const double in)
    {
        coeffsLin  = coeffsLin * in;
        coeffsQuad = coeffsQuad * in;
        constant   = constant * in;
        return *this;
    }

    /** @brief Operator*= for int */
    UbpQuadExpr& operator*=(const int in)
    {
        coeffsLin  = coeffsLin * (double)in;
        coeffsQuad = coeffsQuad * (double)in;
        constant   = constant * (double)in;
        return *this;
    }

    /** @brief Operator/= for UbpQuadExpr */
    UbpQuadExpr& operator/=(const UbpQuadExpr& in) { throw MAiNGOException("  Error: UbpQuadExpr -- function x/y not allowed in (MIQ)Ps."); }
    /** @brief Operator/= for double */
    UbpQuadExpr& operator/=(const double in)
    {
        *this *= (1. / in);
        return *this;
    }
    /** @brief Operator/= for int */
    UbpQuadExpr& operator/=(const int in)
    {
        *this *= (1. / (double)in);
        return *this;
    }

    /**
        * @name Internal CPLEX variables
        */
    /**@{*/
    size_t nvar;                                 /*!< number of variables */
    double constant;                             /*!< value of numeric constant */
    std::vector<double> coeffsLin;               /*!< vector holding linear coefficients */
    std::vector<std::vector<double>> coeffsQuad; /*!< matrix holding coefficient of quadratic/bilinear terms */
    bool hasQuad;                                /*!< flag indicating whether a quadratic/bilinear term is already present */
                                                 /**@}*/
};

/** @brief Operator+ for UbpQuadExpr */
inline UbpQuadExpr
operator+(const UbpQuadExpr& in)
{
    return in;
}

/** @brief Operator+ for two UbpQuadExpr objects */
inline UbpQuadExpr
operator+(const UbpQuadExpr& in1, const UbpQuadExpr& in2)
{
    if (in1.nvar != in2.nvar && (in1.nvar != 0 && in2.nvar != 0))
        throw MAiNGOException("  Error: UbpQuadExpr -- nvar does not fit in + operator.");

    UbpQuadExpr res(in1.nvar);
    if (in1.nvar == 0) {
        res.coeffsLin  = in2.coeffsLin;
        res.coeffsQuad = in2.coeffsQuad;
        res.constant   = in1.constant + in2.constant;
    }
    else if (in2.nvar == 0) {
        res.coeffsLin  = in1.coeffsLin;
        res.coeffsQuad = in1.coeffsQuad;
        res.constant   = in1.constant + in2.constant;
    }
    else {
        res.coeffsLin  = in1.coeffsLin + in2.coeffsLin;
        res.coeffsQuad = in1.coeffsQuad + in2.coeffsQuad;
        res.constant   = in1.constant + in2.constant;
    }
    res.hasQuad = in1.hasQuad || in2.hasQuad;
    return res;
}

/** @brief Operator+ for addition of an UbpQuadExpr and a double */
inline UbpQuadExpr
operator+(const UbpQuadExpr& in1, const double& in2)
{
    UbpQuadExpr res(in1.nvar);
    res.coeffsLin  = in1.coeffsLin;
    res.coeffsQuad = in1.coeffsQuad;
    res.constant   = in1.constant + in2;
    res.hasQuad    = in1.hasQuad;
    return res;
}

/** @brief Operator+ for addition of an UbpQuadExpr and an int */
inline UbpQuadExpr
operator+(const UbpQuadExpr& in1, const int& in2)
{
    UbpQuadExpr res(in1.nvar);
    res.coeffsLin  = in1.coeffsLin;
    res.coeffsQuad = in1.coeffsQuad;
    res.constant   = in1.constant + in2;
    res.hasQuad    = in1.hasQuad;
    return res;
}

/** @brief Operator+ for addition of an UbpQuadExpr and a double */
inline UbpQuadExpr
operator+(const double& in1, const UbpQuadExpr& in2)
{
    return in2 + in1;
}

/** @brief Operator+ for addition of an UbpQuadExpr and an int */
inline UbpQuadExpr
operator+(const int& in1, const UbpQuadExpr& in2)
{
    return in2 + in1;
}

/** @brief Operator- for UbpQuadExpr */
inline UbpQuadExpr
operator-(const UbpQuadExpr& in)
{
    UbpQuadExpr res(in.nvar);
    res.coeffsLin  = -in.coeffsLin;
    res.coeffsQuad = -in.coeffsQuad;
    res.constant   = -in.constant;
    res.hasQuad    = in.hasQuad;
    return res;
}

/** @brief Operator- for two UbpQuadExpr objects */
inline UbpQuadExpr
operator-(const UbpQuadExpr& in1, const UbpQuadExpr& in2)
{
    if (in1.nvar != in2.nvar && (in1.nvar != 0 && in2.nvar != 0))
        throw MAiNGOException("  Error: UbpQuadExpr -- nvar does not fit in - operator.");

    UbpQuadExpr res(in1.nvar);

    if (in1.nvar == 0) {
        res.coeffsLin  = -in2.coeffsLin;
        res.coeffsQuad = -in2.coeffsQuad;
        res.constant   = in1.constant - in2.constant;
    }
    else if (in2.nvar == 0) {
        res.coeffsLin  = in1.coeffsLin;
        res.coeffsQuad = in1.coeffsQuad;
        res.constant   = in1.constant - in2.constant;
    }
    else {
        res.coeffsLin  = in1.coeffsLin - in2.coeffsLin;
        res.coeffsQuad = in1.coeffsQuad - in2.coeffsQuad;
        res.constant   = in1.constant - in2.constant;
    }
    res.hasQuad = in1.hasQuad || in2.hasQuad;
    return res;
}

/** @brief Operator- for subtraction of an UbpQuadExpr and a double */
inline UbpQuadExpr
operator-(const UbpQuadExpr& in1, const double& in2)
{
    UbpQuadExpr res(in1.nvar);
    res.coeffsLin  = in1.coeffsLin;
    res.coeffsQuad = in1.coeffsQuad;
    res.constant   = in1.constant - in2;
    res.hasQuad    = in1.hasQuad;
    return res;
}

/** @brief Operator- for subtraction of an UbpQuadExpr and an int */
inline UbpQuadExpr
operator-(const UbpQuadExpr& in1, const int& in2)
{
    UbpQuadExpr res(in1.nvar);
    res.coeffsLin  = in1.coeffsLin;
    res.coeffsQuad = in1.coeffsQuad;
    res.constant   = in1.constant - in2;
    res.hasQuad    = in1.hasQuad;
    return res;
}

/** @brief Operator- for subtraction of an UbpQuadExpr and a double */
inline UbpQuadExpr
operator-(const double& in1, const UbpQuadExpr& in2)
{
    UbpQuadExpr res(in2.nvar);
    res.coeffsLin  = -in2.coeffsLin;
    res.coeffsQuad = -in2.coeffsQuad;
    res.constant   = in1 - in2.constant;
    res.hasQuad    = in2.hasQuad;
    return res;
}

/** @brief Operator- for subtraction of an UbpQuadExpr and an int */
inline UbpQuadExpr
operator-(const int& in1, const UbpQuadExpr& in2)
{
    UbpQuadExpr res(in2.nvar);
    res.coeffsLin  = -in2.coeffsLin;
    res.coeffsQuad = -in2.coeffsQuad;
    res.constant   = in1 - in2.constant;
    res.hasQuad    = in2.hasQuad;
    return res;
}

/** @brief Operator* for two UbpQuadExpr objects */
inline UbpQuadExpr
operator*(const UbpQuadExpr& in1, const UbpQuadExpr& in2)
{
    if (in1.nvar != in2.nvar && (in1.nvar != 0 && in2.nvar != 0))
        throw MAiNGOException("  Error: UbpQuadExpr -- nvar does not fit in * operator.");

    UbpQuadExpr res(in1.nvar);
    if (in1.nvar == 0) {
        res.coeffsLin  = in2.coeffsLin * in1.constant;
        res.coeffsQuad = in2.coeffsQuad * in1.constant;
        res.constant   = in2.constant * in1.constant;
        res.hasQuad    = in2.hasQuad;
    }
    else if (in2.nvar == 0) {
        res.coeffsLin  = in1.coeffsLin * in2.constant;
        res.coeffsQuad = in1.coeffsQuad * in2.constant;
        res.constant   = in1.constant * in2.constant;
        res.hasQuad    = in1.hasQuad;
    }
    else {
        if (in1.hasQuad || in2.hasQuad)
            throw MAiNGOException("  Error: UbpQuadExpr -- multiplications higher than second order are not allowed in (MIQ)Ps.");

        for (size_t i = 0; i < in1.nvar; i++) {
            for (size_t j = 0; j < in2.nvar; j++) {
                res.coeffsQuad[i][j] = in1.coeffsLin[i] * in2.coeffsLin[j];
            }
            res.coeffsLin[i] = in1.coeffsLin[i] * in2.constant + in2.coeffsLin[i] * in1.constant;
        }
        res.constant = in1.constant * in2.constant;
        res.hasQuad  = true;
    }
    return res;
}

/** @brief Operator* for multiplication of an UbpQuadExpr and a double */
inline UbpQuadExpr
operator*(const UbpQuadExpr& in1, const double in2)
{
    UbpQuadExpr res(in1.nvar);
    res.coeffsLin  = in1.coeffsLin * in2;
    res.coeffsQuad = in1.coeffsQuad * in2;
    res.constant   = in1.constant * in2;
    res.hasQuad    = in1.hasQuad;
    return res;
}

/** @brief Operator* for subtraction of an UbpQuadExpr and an int */
inline UbpQuadExpr
operator*(const UbpQuadExpr& in1, const int in2)
{
    return in1 * ((double)in2);
}

/** @brief Operator* for multiplication of an UbpQuadExpr and a double */
inline UbpQuadExpr
operator*(const double in1, const UbpQuadExpr& in2)
{
    return in2 * in1;
}

/** @brief Operator* for subtraction of an UbpQuadExpr and an int */
inline UbpQuadExpr
operator*(const int in1, const UbpQuadExpr& in2)
{
    return in2 * ((double)in1);
}

/** @brief Operator/ for two UbpQuadExpr*/
inline UbpQuadExpr
operator/(const UbpQuadExpr& in1, const UbpQuadExpr& in2)
{
    throw MAiNGOException("  Error: UbpQuadExpr -- function x/y not allowed in (MIQ)Ps.");
}

/** @brief Operator/ for division of an UbpQuadExpr by a double */
inline UbpQuadExpr
operator/(const UbpQuadExpr& in1, const double in2)
{
    return in1 * (1. / in2);
}

/** @brief Operator/ for division of an UbpQuadExpr by a double */
inline UbpQuadExpr
operator/(const UbpQuadExpr& in1, const int in2)
{
    return in1 * (1. / (double)in2);
}

/** @brief Operator/ for division of a double by an UbpQuadExpr */
inline UbpQuadExpr
operator/(const double in1, const UbpQuadExpr& in2)
{
    throw MAiNGOException("  Error: UbpQuadExpr -- function 1/x not allowed in (MIQ)Ps.");
}

/** @brief Operator/ for division of an int by an UbpQuadExpr */
inline UbpQuadExpr
operator/(const int in1, const UbpQuadExpr& in2)
{
    throw MAiNGOException("  Error: UbpQuadExpr -- function 1/x not allowed in (MIQ)Ps.");
}


}    // end namespace ubp


}    // end namespace maingo


namespace mc {


//! @brief Specialization of the structure mc::Op for use of the type UbpQuadExpr as a template parameter in other MC++ types
template <>
struct Op<maingo::ubp::UbpQuadExpr> {
    typedef maingo::ubp::UbpQuadExpr QE;         /*!< typedef for easier usage */
    static QE sqr(const QE& x) { return x * x; } /*!< x^2 */
    static QE pow(const QE& x, const int n)
    {
        if (n == 0) {
            return QE(1.0);
        }
        if (n == 1) {
            return x;
        }
        if (n == 2) {
            return x * x;
        }
        throw std::runtime_error("  Error: UbpQuadExpr -- function pow with n <> 0,1,2 not allowed in (MIQ)Ps.");
    } /*!< powers are allowed up to order 2 */
    static QE pow(const QE& x, const double a)
    {
        if (a == 0) {
            return QE(1.0);
        }
        if (a == 1) {
            return x;
        }
        if (a == 2) {
            return x * x;
        }
        throw std::runtime_error("  Error: UbpQuadExpr -- function pow with a <> 0,1,2 not allowed in (MIQ)Ps.");
    }                                                                                                                                                                     /*!< power are allowed up to order 2 */
    static QE pow(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function pow(x,y) not allowed in (MIQ)Ps."); }                            /*!< x^y is not allowed */
    static QE pow(const double x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function pow(a,y) not allowed in (MIQ)Ps."); }                         /*!< c^x is not allowed */
    static QE pow(const int x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function pow(n,y) not allowed in (MIQ)Ps."); }                            /*!< d^x is not allowed */
    static QE prod(const unsigned int n, const QE* x) { throw std::runtime_error("  Error: UbpQuadExpr -- function prod not allowed in (MIQ)Ps."); }                      /*!< prod could be allowed but is currently not implemented */
    static QE monom(const unsigned int n, const QE* x, const unsigned* k) { throw std::runtime_error("  Error: UbpQuadExpr -- function monom not allowed in (MIQ)Ps."); } /*!< monom could be allowed but is currently not implemented */
    static QE point(const double c) { throw std::runtime_error("  Error: UbpQuadExpr -- function point not allowed in (MIQ)Ps."); }                                       /*!< point is not needed at all */
    static QE zeroone() { throw std::runtime_error("  Error: UbpQuadExpr -- function zeroone not allowed in (MIQ)Ps."); }                                                 /*!< zeroone is not needed at all */
    static void I(QE& x, const QE& y) { x = y; }                                                                                                                          /*!< even thou I should be understood as interval, it is implemented here as assignment */
    static double l(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function l not allowed in (MIQ)Ps."); }                                              /*!< no lower bound given */
    static double u(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function u not allowed in (MIQ)Ps."); }                                              /*!< no upper bound given */
    static double abs(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function abs not allowed in (MIQ)Ps."); }                                          /*!< abs is not allowed */
    static double mid(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function mid not allowed in (MIQ)Ps."); }                                          /*!< mid not given */
    static double diam(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function diam not allowed in (MIQ)Ps."); }                                        /*!< diam not given */
    static QE inv(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function inv not allowed in (MIQ)Ps."); }                                              /*!< inv is not allowed */
    static QE sqrt(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function sqrt not allowed in (MIQ)Ps."); }                                            /*!< sqrt is not allowed */
    static QE exp(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function exp not allowed in (MIQ)Ps."); }                                              /*!< exp is not allowed */
    static QE log(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function log not allowed in (MIQ)Ps."); }                                              /*!< log is not allowed */
    static QE xlog(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function xlog not allowed in (MIQ)Ps."); }                                            /*!< xlog is not allowed */
    static QE fabsx_times_x(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function fabsx_times_x not allowed in (MIQ)Ps."); }                          /*!< x*|x| is not allowed */
    static QE xexpax(const QE& x, const double a) { throw std::runtime_error("  Error: UbpQuadExpr -- function xexpax not allowed in (MIQ)Ps."); }                        /*!< x*exp(a*x) is not allowed */
    static QE lmtd(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function lmtd not allowed in (MIQ)Ps."); }                               /*!< lmtd is not allowed */
    static QE rlmtd(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function rlmtd not allowed in (MIQ)Ps."); }                             /*!< rlmtd is not allowed */
    static QE euclidean_norm_2d(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function euclidean_norm_2d not allowed in (MIQ)Ps."); }     /*!< euclidean is not allowed */
    static QE expx_times_y(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function expx_times_y not allowed in (MIQ)Ps."); }               /*!< exp(x)*y is not allowed */
    static QE vapor_pressure(const QE& x, const double type, const double p1, const double p2, const double p3, const double p4 = 0, const double p5 = 0, const double p6 = 0,
                             const double p7 = 0, const double p8 = 0, const double p9 = 0, const double p10 = 0) { throw std::runtime_error("  Error: UbpQuadExpr -- function vapor_pressure not allowed in (MIQ)Ps."); } /*!< no thermodynamic function is not allowed */
    static QE ideal_gas_enthalpy(const QE& x, const double x0, const double type, const double p1, const double p2, const double p3, const double p4, const double p5, const double p6 = 0,
                                 const double p7 = 0) { throw std::runtime_error("  Error: UbpQuadExpr -- function ideal_gas_enthalpy not allowed in (MIQ)Ps."); } /*!< no thermodynamic function is not allowed */
    static QE saturation_temperature(const QE& x, const double type, const double p1, const double p2, const double p3, const double p4 = 0, const double p5 = 0, const double p6 = 0,
                                     const double p7 = 0, const double p8 = 0, const double p9 = 0, const double p10 = 0) { throw std::runtime_error("  Error: UbpQuadExpr -- function saturation_temperature not allowed in (MIQ)Ps."); }                                                          /*!< no thermodynamic function is not allowed */
    static QE enthalpy_of_vaporization(const QE& x, const double type, const double p1, const double p2, const double p3, const double p4, const double p5, const double p6 = 0) { throw std::runtime_error("  Error: UbpQuadExpr -- function enthalpy_of_vaporization not allowed in (MIQ)Ps."); } /*!< no thermodynamic function is not allowed */
    static QE cost_function(const QE& x, const double type, const double p1, const double p2, const double p3) { throw std::runtime_error("  Error: UbpQuadExpr -- function cost_function not allowed in (MIQ)Ps."); }                                                                              /*!< no cost function function is not allowed */
    static QE nrtl_tau(const QE& x, const double a, const double b, const double e, const double f) { throw std::runtime_error("  Error: UbpQuadExpr -- function nrtl_tau not allowed in (MIQ)Ps."); }                                                                                              /*!< no thermodynamic function is not allowed */
    static QE nrtl_dtau(const QE& x, const double b, const double e, const double f) { throw std::runtime_error("  Error: UbpQuadExpr -- function nrtl_dtau not allowed in (MIQ)Ps."); }                                                                                                            /*!< no thermodynamic function is not allowed */
    static QE nrtl_G(const QE& x, const double a, const double b, const double e, const double f, const double alpha) { throw std::runtime_error("  Error: UbpQuadExpr -- function nrtl_G not allowed in (MIQ)Ps."); }                                                                              /*!< no thermodynamic function is not allowed */
    static QE nrtl_Gtau(const QE& x, const double a, const double b, const double e, const double f, const double alpha) { throw std::runtime_error("  Error: UbpQuadExpr -- function nrtl_Gtau not allowed in (MIQ)Ps."); }                                                                        /*!< no thermodynamic function is not allowed */
    static QE nrtl_Gdtau(const QE& x, const double a, const double b, const double e, const double f, const double alpha) { throw std::runtime_error("  Error: UbpQuadExpr -- function nrtl_Gdtau not allowed in (MIQ)Ps."); }                                                                      /*!< no thermodynamic function is not allowed */
    static QE nrtl_dGtau(const QE& x, const double a, const double b, const double e, const double f, const double alpha) { throw std::runtime_error("  Error: UbpQuadExpr -- function nrtl_dGtau not allowed in (MIQ)Ps."); }                                                                      /*!< no thermodynamic function is not allowed */
    static QE iapws(const QE& x, const double type) { throw std::runtime_error("  Error: UbpQuadExpr -- function iapws not allowed in (MIQ)Ps."); }                                                                                                                                                 /*!< no thermodynamic function is not allowed */
    static QE iapws(const QE& x, const QE& y, const double type) { throw std::runtime_error("  Error: UbpQuadExpr -- function iapws not allowed in (MIQ)Ps."); }                                                                                                                                    /*!< no thermodynamic function is not allowed */
    static QE p_sat_ethanol_schroeder(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function p_sat_ethanol_schroeder not allowed in (MIQ)Ps."); }                                                                                                                                /*!< no thermodynamic function is not allowed */
    static QE rho_vap_sat_ethanol_schroeder(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function rho_vap_sat_ethanol_schroeder not allowed in (MIQ)Ps."); }                                                                                                                    /*!< no thermodynamic function is not allowed */
    static QE rho_liq_sat_ethanol_schroeder(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function rho_liq_sat_ethanol_schroeder not allowed in (MIQ)Ps."); }                                                                                                                    /*!< no thermodynamic function is not allowed */
    static QE covariance_function(const QE& x, const double type) { throw std::runtime_error("  Error: UbpQuadExpr -- function covariance_function not allowed in (MIQ)Ps."); }                                                                                                                     /*!< no thermodynamic function is not allowed */
    static QE acquisition_function(const QE& x, const QE& y, const double type, const double fmin) { throw std::runtime_error("  Error: UbpQuadExpr -- function acquisition_function not allowed in (MIQ)Ps."); }                                                                                   /*!< no thermodynamic function is not allowed */
    static QE gaussian_probability_density_function(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function gaussian_probability_density_function not allowed in (MIQ)Ps."); }                                                                                                    /*!< no thermodynamic function is not allowed */
    static QE regnormal(const QE& x, const double a, const double b) { throw std::runtime_error("  Error: UbpQuadExpr -- function regnormal not allowed in (MIQ)Ps."); }                                                                                                                            /*!< no thermodynamic function is not allowed */
    static QE fabs(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function fabs not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< fabs function is not allowed */
    static QE sin(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function sin not allowed in (MIQ)Ps."); }                                                                                                                                                                        /*!< trigonometric function is not allowed */
    static QE cos(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function cos not allowed in (MIQ)Ps."); }                                                                                                                                                                        /*!< trigonometric function is not allowed */
    static QE tan(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function tan not allowed in (MIQ)Ps."); }                                                                                                                                                                        /*!< trigonometric function is not allowed */
    static QE asin(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function asin not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< trigonometric function is not allowed */
    static QE acos(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function acos not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< trigonometric function is not allowed */
    static QE atan(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function atan not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< trigonometric function is not allowed */
    static QE sinh(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function sinh not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< trigonometric function is not allowed */
    static QE cosh(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function cosh not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< trigonometric function is not allowed */
    static QE tanh(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function tanh not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< trigonometric function is not allowed */
    static QE coth(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function coth not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< trigonometric function is not allowed */
    static QE asinh(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function asinh not allowed in (MIQ)Ps."); }                                                                                                                                                                    /*!< trigonometric function is not allowed */
    static QE acosh(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function acosh not allowed in (MIQ)Ps."); }                                                                                                                                                                    /*!< trigonometric function is not allowed */
    static QE atanh(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function atanh not allowed in (MIQ)Ps."); }                                                                                                                                                                    /*!< trigonometric function is not allowed */
    static QE acoth(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function acoth not allowed in (MIQ)Ps."); }                                                                                                                                                                    /*!< trigonometric function is not allowed */
    static QE erf(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function erf not allowed in (MIQ)Ps."); }                                                                                                                                                                        /*!< erf function is not allowed */
    static QE erfc(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function erfc not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< erfc function is not allowed */
    static QE fstep(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function fstep not allowed in (MIQ)Ps."); }                                                                                                                                                                    /*!< discontinuous function is not allowed */
    static QE bstep(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function bstep not allowed in (MIQ)Ps."); }                                                                                                                                                                    /*!< discontinuous function is not allowed */
    static QE hull(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function hull not allowed in (MIQ)Ps."); }                                                                                                                                                         /*!< hull is not given */
    static QE min(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function min not allowed in (MIQ)Ps."); }                                                                                                                                                           /*!< min function is not allowed */
    static QE max(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function max not allowed in (MIQ)Ps."); }                                                                                                                                                           /*!< max function is not allowed */
    static QE pos(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function pos not allowed in (MIQ)Ps."); }                                                                                                                                                                        /*!< pos function is not allowed */
    static QE neg(const QE& x) { throw std::runtime_error("  Error: UbpQuadExpr -- function neg not allowed in (MIQ)Ps."); }                                                                                                                                                                        /*!< neg function is not allowed */
    static QE lb_func(const QE& x, const double lb) { throw std::runtime_error("  Error: UbpQuadExpr -- function lb_func not allowed in (MIQ)Ps."); }                                                                                                                                               /*!< lb_func function is not allowed */
    static QE ub_func(const QE& x, const double ub) { throw std::runtime_error("  Error: UbpQuadExpr -- function ub_func not allowed in (MIQ)Ps."); }                                                                                                                                               /*!< ub_func function is not allowed */
    static QE bounding_func(const QE& x, const double lb, const double ub) { throw std::runtime_error("  Error: UbpQuadExpr -- function bounding_func not allowed in (MIQ)Ps."); }                                                                                                                  /*!< bounding_func function is not allowed */
    static QE squash_node(const QE& x, const double lb, const double ub) { throw std::runtime_error("  Error: UbpQuadExpr -- function squash_node not allowed in (MIQ)Ps."); }                                                                                                                      /*!< squash_node function is not allowed */
    static QE sum_div(const std::vector<QE>& x, const std::vector<double>& coeff) { throw std::runtime_error("  Error: UbpQuadExpr -- function sum_div not allowed in (MIQ)Ps."); }                                                                                                                 /*!< sum_div function is not allowed */
    static QE xlog_sum(const std::vector<QE>& x, const std::vector<double>& coeff) { throw std::runtime_error("  Error: UbpQuadExpr -- function xlog_sum not allowed in (MIQ)Ps."); }                                                                                                               /*!< xlog_sum function is not allowed */
    static QE mc_print(const QE& x, const int number) { throw std::runtime_error("  Error: UbpQuadExpr -- function mc_print not allowed in (MIQ)Ps."); }                                                                                                                                            /*!< printing function is not allowed */
    static QE arh(const QE& x, const double k) { throw std::runtime_error("  Error: UbpQuadExpr -- function arh not allowed in (MIQ)Ps."); }                                                                                                                                                        /*!< arh function is not allowed */
    static QE cheb(const QE& x, const unsigned n) { throw std::runtime_error("  Error: UbpQuadExpr -- function cheb not allowed in (MIQ)Ps."); }                                                                                                                                                    /*!< cheb function is not allowed */
    static bool inter(QE& xIy, const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function inter not allowed in (MIQ)Ps."); }                                                                                                                                            /*!< interior is not given */
    static bool eq(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function eq not allowed in (MIQ)Ps."); }                                                                                                                                                           /*!< compare function is not allowed */
    static bool ne(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function ne not allowed in (MIQ)Ps."); }                                                                                                                                                           /*!< compare function is not allowed */
    static bool lt(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function lt not allowed in (MIQ)Ps."); }                                                                                                                                                           /*!< compare function is not allowed */
    static bool le(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function le not allowed in (MIQ)Ps."); }                                                                                                                                                           /*!< compare function is not allowed */
    static bool gt(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function gt not allowed in (MIQ)Ps."); }                                                                                                                                                           /*!< compare function is not allowed */
    static bool ge(const QE& x, const QE& y) { throw std::runtime_error("  Error: UbpQuadExpr -- function ge not allowed in (MIQ)Ps."); }                                                                                                                                                                      /*!< discontinuous function is not allowed */
    static QE centerline_deficit(const QE& x, const double xLim, const double type) { throw std::runtime_error("  Error: UbpQuadExpr -- function centerline_deficit not allowed in (MIQ)Ps."); }                                                                                                                /*!< discontinuous function is not allowed */
    static QE wake_profile(const QE& x, const double type) { throw std::runtime_error("  Error: UbpQuadExpr -- function wake_profile not allowed in (MIQ)Ps."); }                                                                                                               /*!< discontinuous function is not allowed */
    static QE wake_deficit(const QE& x, const QE& r, const double a, const double alpha, const double rr, const double type1, const double type2) { throw std::runtime_error("  Error: UbpQuadExpr -- function wake_deficit not allowed in (MIQ)Ps."); }                                                                                                               /*!< discontinuous function is not allowed */
    static QE power_curve(const QE& x, const double type) { throw std::runtime_error("  Error: UbpQuadExpr -- function power_curve not allowed in (MIQ)Ps."); }                                                                                                                                                       /*!< compare function is not allowed */
};


}    // end namespace mc