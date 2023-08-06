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

#include "node.hpp"
#include "symbol_table.hpp"
#include "expression.hpp"

#include <cmath>
#include <exception>
#include <limits>

namespace ale::util {

class member_checker;

class evaluator {
public:
    evaluator(symbol_table& symbols) : symbols(symbols) {};

    // expression dispatch
    template <typename TType>
    typename TType::basic_type dispatch(expression<TType>& expr) {
        return dispatch(expr.get());
    }

    // value_node dispatch
    template <typename TType>
    typename TType::ref_type dispatch(value_node<TType>* node) {
        return std::visit(*this, node->get_variant());
    }

    template <typename TType>
    typename set<TType, 0>::basic_type dispatch(value_node<set<TType, 0>>* node) {
        return std::visit(*this, node->get_variant());
    }

    // symbol dispatch
    template <typename TType>
    typename TType::ref_type dispatch(value_symbol<TType>* sym) {
        return std::visit(*this, sym->get_value_variant());
    }

    template <typename TType>
    typename set<TType, 0>::basic_type dispatch(value_symbol<set<TType, 0>>* sym) {
        return std::visit(*this, sym->get_value_variant());
    }



    // terminal visits
    template <typename TType>
    typename TType::ref_type operator()(constant_node<TType>* node) {
        return node->value;
    }

    template <typename TType>
    typename TType::ref_type operator()(parameter_node<TType>* node) {
        auto sym = symbols.resolve<TType>(node->name);
        if (!sym) {
            throw std::invalid_argument("symbol " + node->name + " is ill-defined");
        }
        return dispatch(sym);
    }



    // symbol visits
    template <typename TType>
    typename TType::ref_type operator()(parameter_symbol<TType>* sym) {
        return sym->m_value;
    }

    template <typename TType>
    typename set<TType, 0>::basic_type operator()(parameter_symbol<set<TType, 0>>* sym) {
        return sym->m_value;
    }

    template <typename TType>
    typename TType::ref_type operator()(variable_symbol<TType>* sym) {
        throw std::invalid_argument("cannot evaluate variable_symbol");
    }

    template <typename TType>
    typename TType::ref_type operator() (expression_symbol<TType>* sym) {
        return dispatch(sym->m_value.get());
    }

    // non-terminal visits
    template <typename TType>
    typename TType::ref_type operator()(entry_node<TType>* node) {
        return dispatch(node->template get_child<0>())[dispatch(node->template get_child<1>())-1];
    }

    // non-terminal real node visits
    double operator()(minus_node* node) {
        return - dispatch(node->get_child<0>());
    }

    double operator()(inverse_node* node) {
        return 1 / dispatch(node->get_child<0>());
    }

    double operator()(addition_node* node) {
        double result = 0;
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            result += dispatch(it->get());
        }
        return result;
    }

    double operator()(sum_div_node* node) {
        if (node->children.size() % 2 == 0) {
            throw std::invalid_argument("called sum_div with even number of arguments");
        }
        if (node->children.size() < 3) {
            throw std::invalid_argument("called sum_div with less than 3 arguments");
        }
        std::vector<double> vars;
        std::vector<double> coeff;
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            if (!(dispatch(it->get()) > 0)) {
                throw std::invalid_argument("called sum_div with non-positive argument");
            }
            if (distance(node->children.begin(), it) < (int)(node->children.size() / 2)) {
                vars.emplace_back(dispatch(it->get()));
            }
            else {
                coeff.emplace_back(dispatch(it->get()));
            }
        }
        double partial = coeff[1] * vars[0];
        for (int i = 1; i < (int)(node->children.size() / 2); ++i) {
            partial += coeff[i + 1] * vars[i];
        }
        return (coeff[0] * vars[0]) / partial;
    }

    double operator()(xlog_sum_node* node) {
        if (!(node->children.size() % 2 == 0)) {
            throw std::invalid_argument("called xlog_sum with odd number of arguments");
        }
        if (node->children.size() < 2) {
            throw std::invalid_argument("called xlog_sum with less than 2 arguments");
        }
        std::vector<double> vars;
        std::vector<double> coeff;
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            if (!(dispatch(it->get()) > 0)) {
                throw std::invalid_argument("called xlog_sum with non-positive argument");
            }
            if (distance(node->children.begin(), it) < (int)(node->children.size() / 2)) {
                vars.emplace_back(dispatch(it->get()));
            }
            else {
                coeff.emplace_back(dispatch(it->get()));
            }
        }
        double partial = 0;
        for (int i = 0; i < (int)(node->children.size() / 2); ++i) {
            partial += coeff[i] * vars[i];
        }
        return vars[0] * log(partial);
    }

    double operator()(multiplication_node* node) {
        double result = 1;
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            result *= dispatch(it->get());
        }
        return result;
    }

    double operator()(exponentiation_node* node) {
        double result = 1;
        for (auto it = node->children.rbegin(); it != node->children.rend(); ++it) {
            result = pow(dispatch(it->get()), result);
        }
        return result;
    }

    double operator()(min_node* node) {
        double result = std::numeric_limits<double>::infinity();
        for (auto it = node->children.rbegin(); it != node->children.rend(); ++it) {
            result = std::min(result, dispatch(it->get()));
        }
        return result;
    }

    double operator()(max_node* node) {
        double result = - std::numeric_limits<double>::infinity();
        for (auto it = node->children.rbegin(); it != node->children.rend(); ++it) {
            result = std::max(result, dispatch(it->get()));
        }
        return result;
    }

    double operator()(exp_node* node) {
        return exp(dispatch(node->get_child<0>()));
    }

    double operator()(log_node* node) {
        return log(dispatch(node->get_child<0>()));
    }

    double operator()(sqrt_node* node) {
        return sqrt(dispatch(node->get_child<0>()));
    }

    double operator()(sin_node* node) {
        return sin(dispatch(node->get_child<0>()));
    }

    double operator()(asin_node* node) {
        return asin(dispatch(node->get_child<0>()));
    }
    double operator()(cos_node* node) {
        return cos(dispatch(node->get_child<0>()));
    }

    double operator()(acos_node* node) {
        return acos(dispatch(node->get_child<0>()));
    }

    double operator()(tan_node* node) {
        return tan(dispatch(node->get_child<0>()));
    }

    double operator()(atan_node* node) {
        return atan(dispatch(node->get_child<0>()));
    }

    double operator()(xlogx_node* node) {
        double x = dispatch(node->get_child<0>());
        return x*log(x);
    }

    double operator()(abs_node* node) {
        return abs(dispatch(node->get_child<0>()));
    }

    double operator()(xabsx_node* node) {
        return abs(dispatch(node->get_child<0>()))*dispatch(node->get_child<0>());
    }

    double operator()(cosh_node* node) {
        return cosh(dispatch(node->get_child<0>()));
    }

    double operator()(sinh_node* node) {
        return sinh(dispatch(node->get_child<0>()));
    }

    double operator()(tanh_node* node) {
        return tanh(dispatch(node->get_child<0>()));
    }

    double operator()(coth_node* node) {
        return cosh(dispatch(node->get_child<0>())) / sinh(dispatch(node->get_child<0>()));
    }

    double operator()(acosh_node* node) {
        return acosh(dispatch(node->get_child<0>()));
    }

    double operator()(asinh_node* node) {
        return asinh(dispatch(node->get_child<0>()));
    }

    double operator()(atanh_node* node) {
        return atanh(dispatch(node->get_child<0>()));
    }

    double operator()(acoth_node* node) {
        double x = dispatch(node->get_child<0>());
        return 0.5 * log((x+1)/(x-1));
    }

    double operator()(erf_node* node) {
        return erf(dispatch(node->get_child<0>()));
    }

    double operator()(erfc_node* node) {
        return erfc(dispatch(node->get_child<0>()));
    }

    double operator()(pos_node* node) {
        if (dispatch(node->get_child<0>()) <= 0) {
            throw std::invalid_argument("called pos_node with non-positive variable");
        }
        return dispatch(node->get_child<0>());
    }

    double operator()(neg_node* node) {
        if (dispatch(node->get_child<0>()) >= 0) {
            throw std::invalid_argument("called neg_node with positive variable");
        }
        return dispatch(node->get_child<0>());
    }

    double operator()(schroeder_ethanol_p_node* node) {
        double t = dispatch(node->get_child<0>());
        const double t_c_K = 514.71;
        const double n_Tsat_1 = -8.94161;
        const double n_Tsat_2 = 1.61761;
        const double n_Tsat_3 = -51.1428;
        const double n_Tsat_4 = 53.1360;
        const double k_Tsat_1 = 1.0;
        const double k_Tsat_2 = 1.5;
        const double k_Tsat_3 = 3.4;
        const double k_Tsat_4 = 3.7;
        const double p_c = 62.68;
        return p_c*(exp(t_c_K/t*(n_Tsat_1*pow((1-t/t_c_K),k_Tsat_1) + n_Tsat_2*pow((1-t/t_c_K),k_Tsat_2)
           + n_Tsat_3*pow((1-t/t_c_K),k_Tsat_3) + n_Tsat_4*pow((1-t/t_c_K),k_Tsat_4))));
    }

    double operator()(schroeder_ethanol_rhovap_node* node) {
        double t = dispatch(node->get_child<0>());
        const double t_c_K = 514.71;
        const double n_vap_1 = -1.75362;
        const double n_vap_2 = -10.5323;
        const double n_vap_3 = -37.6407;
        const double n_vap_4 = -129.762;
        const double k_vap_1 = 0.21;
        const double k_vap_2 = 1.1;
        const double k_vap_3 = 3.4;
        const double k_vap_4 = 10;
        const double rho_c = 273.195;
        return rho_c*(exp(n_vap_1*pow((1 - t/t_c_K),k_vap_1) + n_vap_2*pow((1 - t/t_c_K),k_vap_2)
            + n_vap_3*pow((1 - t/t_c_K),k_vap_3) + n_vap_4*pow((1 - t/t_c_K),k_vap_4)));
    }

    double operator()(schroeder_ethanol_rholiq_node* node) {
        double t = dispatch(node->get_child<0>());
        const double t_c_K = 514.71;
        const double n_liq_1 = 9.00921;
        const double n_liq_2 = -23.1668;
        const double n_liq_3 = 30.9092;
        const double n_liq_4 = -16.5459;
        const double n_liq_5 = 3.64294;
        const double k_liq_1 = 0.5;
        const double k_liq_2 = 0.8;
        const double k_liq_3 = 1.1;
        const double k_liq_4 = 1.5;
        const double k_liq_5 = 3.3;
        const double rho_c = 273.195;
        return rho_c*(1 + n_liq_1*pow((1 - t/t_c_K),k_liq_1) + n_liq_2*pow((1 - t/t_c_K),k_liq_2)
            + n_liq_3*pow((1 - t/t_c_K),k_liq_3) + n_liq_4*pow((1 - t/t_c_K),k_liq_4)
            + n_liq_5*pow((1 - t/t_c_K),k_liq_5));
    }

    double operator()(covar_matern_1_node* node) {
        double x = dispatch(node->get_child<0>());
        return exp(-sqrt(x));
    }

    double operator()(covar_matern_3_node* node) {
        double x = dispatch(node->get_child<0>());
        double tmp = sqrt(3)*sqrt(x);
        return exp(-tmp) + tmp*exp(-tmp);
    }

    double operator()(covar_matern_5_node* node) {
        double x = dispatch(node->get_child<0>());
        double tmp = sqrt(5)*sqrt(x);
        return exp(-tmp) + tmp*exp(-tmp) + 5./3.*x*exp(-tmp);
    }

    double operator()(covar_sqrexp_node* node) {
        double x = dispatch(node->get_child<0>());
        return exp(-0.5*x);
    }

    double operator()(gpdf_node* node) {
        double x = dispatch(node->get_child<0>());
        return 1./(sqrt(2*M_PI)) * exp(-pow(x,2)/2.);
    }

    double operator()(lmtd_node* node) {
        double dT1 = dispatch(node->get_child<0>());
        double dT2 = dispatch(node->get_child<1>());
        return (dT1-dT2) / log(dT1/dT2);
    }

    double operator()(rlmtd_node* node) {
        double dT1 = dispatch(node->get_child<0>());
        double dT2 = dispatch(node->get_child<1>());
        return log(dT1/dT2) / (dT1-dT2);
    }

    double operator()(xexpax_node* node) {
        double x = dispatch(node->get_child<0>());
        double a = dispatch(node->get_child<1>());
        return x * exp(a * x);
    }

    double operator()(arh_node* node) {
        return exp(-dispatch(node->get_child<1>())/dispatch(node->get_child<0>()));
    }

    double operator()(lb_func_node* node) {
        if (dispatch(node->get_child<0>()) < dispatch(node->get_child<1>())) {
            std::ostringstream errmsg;
            errmsg << "called Lb_func with values lower than " << dispatch(node->get_child<1>())
                << " in range.";
            throw std::invalid_argument(errmsg.str());
        }
        return dispatch(node->get_child<0>());
    }

    double operator()(ub_func_node* node) {
        if (dispatch(node->get_child<0>()) > dispatch(node->get_child<1>())) {
            std::ostringstream errmsg;
            errmsg << "called ub_func with values larger than " << dispatch(node->get_child<1>())
                << " in range.";
            throw std::invalid_argument(errmsg.str());
        }
        return dispatch(node->get_child<0>());
    }

    double operator()(xexpy_node* node) {
        return dispatch(node->get_child<0>())*exp(dispatch(node->get_child<1>()));
    }

    double operator()(mid_node* node) {
        double arg1 = dispatch(node->get_child<0>());
        double arg2 = dispatch(node->get_child<1>());
        double arg3 = dispatch(node->get_child<2>());
        return std::min(std::max(arg1, arg2), std::min(std::max(arg2, arg3), std::max(arg3, arg1)));
    }

    double operator()(nrtl_dtau_node* node) {
        double t = dispatch(node->get_child<0>());
        double e = dispatch(node->get_child<1>());
        double f = dispatch(node->get_child<2>());
        double b = dispatch(node->get_child<3>());
        return b - e / std::pow(t, 2) + f / t;
    }
    double operator()(squash_node* node) {
        double arg1 = dispatch(node->get_child<0>());
        double arg2 = dispatch(node->get_child<1>());
        double arg3 = dispatch(node->get_child<2>());
        return std::min(std::max(arg1, arg2), arg3);
    }
    double operator()(regnormal_node* node) {
        double x = dispatch(node->get_child<0>());
        double a = dispatch(node->get_child<1>());
        double b = dispatch(node->get_child<2>());
        return x / std::sqrt(a+b*std::pow(x,2));
    }
    double operator()(af_lcb_node* node) {
        double mu    = dispatch(node->get_child<0>());
        double sigma = dispatch(node->get_child<1>());
        double kappa = dispatch(node->get_child<2>());
        return mu - kappa*sigma;
    }
    double operator()(af_ei_node* node) {
        double mu    = dispatch(node->get_child<0>());
        double sigma = dispatch(node->get_child<1>());
        double fmin  = dispatch(node->get_child<2>());
        if(sigma == 0){
            return std::max(fmin-mu, 0.);
        }
        double x   = mu - fmin;
        double gcd = std::erf(1./std::sqrt(2)*(-x/sigma))/2.+0.5;
        double gpd = 1./(std::sqrt(2*M_PI)) * std::exp(-std::pow(-x/sigma,2)/2.);
        return (-x)*gcd + sigma*gpd;
    }
    double operator()(af_pi_node* node) {
        double mu    = dispatch(node->get_child<0>());
        double sigma = dispatch(node->get_child<1>());
        double fmin  = dispatch(node->get_child<2>());
        if(sigma == 0 && fmin <= mu){
            return 0;
        }
        if(sigma == 0 && fmin > mu){
            return 1;
        }
        double x   = mu - fmin;
        return std::erf(1./std::sqrt(2)*(-x/sigma))/2.+0.5;
    }

    double operator()(ext_antoine_psat_node* node) {
        double t  = dispatch(node->get_child<0>());
        double p1 = dispatch(node->get_child<1>());
        double p2 = dispatch(node->get_child<2>());
        double p3 = dispatch(node->get_child<3>());
        double p4 = dispatch(node->get_child<4>());
        double p5 = dispatch(node->get_child<5>());
        double p6 = dispatch(node->get_child<6>());
        double p7 = dispatch(node->get_child<7>());
        return std::exp(p1 + p2 / (t + p3) + t * p4 + p5 * std::log(t) + p6 * std::pow(t, p7));
    }

    double operator()(antoine_psat_node* node) {
        double t  = dispatch(node->get_child<0>());
        double p1 = dispatch(node->get_child<1>());
        double p2 = dispatch(node->get_child<2>());
        double p3 = dispatch(node->get_child<3>());
        return std::pow(10., p1 - p2 / (p3 + t));
    }

    double operator()(wagner_psat_node* node) {
        double t  = dispatch(node->get_child<0>());
        double p1 = dispatch(node->get_child<1>());
        double p2 = dispatch(node->get_child<2>());
        double p3 = dispatch(node->get_child<3>());
        double p4 = dispatch(node->get_child<4>());
        double p5 = dispatch(node->get_child<5>());
        double p6 = dispatch(node->get_child<6>());
        double Tr = t / p5;
        return p6 * std::exp((p1*(1 - Tr) + p2 * std::pow(1 - Tr, 1.5) + p3 * std::pow(1 - Tr, 2.5)
            + p4 * std::pow(1 - Tr, 5)) / Tr);
    }

    double operator()(ik_cape_psat_node* node) {
        double t  = dispatch(node->get_child<0>());
        double p1 = dispatch(node->get_child<1>());
        double p2 = dispatch(node->get_child<2>());
        double p3 = dispatch(node->get_child<3>());
        double p4 = dispatch(node->get_child<4>());
        double p5 = dispatch(node->get_child<5>());
        double p6 = dispatch(node->get_child<6>());
        double p7 = dispatch(node->get_child<7>());
        double p8 = dispatch(node->get_child<8>());
        double p9 = dispatch(node->get_child<9>());
        double p10 = dispatch(node->get_child<10>());
        return std::exp(p1 + p2 * t + p3 * std::pow(t, 2) + p4 * std::pow(t, 3) + p5 * std::pow(t, 4)
            + p6 * std::pow(t, 5) + p7 * std::pow(t, 6) + p8 * std::pow(t, 7) + p9 * std::pow(t, 8)
            + p10 * std::pow(t, 9));
    }

    double operator()(aspen_hig_node* node) {
        double t  = dispatch(node->get_child<0>());
        double t0 = dispatch(node->get_child<1>());
        double p1 = dispatch(node->get_child<2>());
        double p2 = dispatch(node->get_child<3>());
        double p3 = dispatch(node->get_child<4>());
        double p4 = dispatch(node->get_child<5>());
        double p5 = dispatch(node->get_child<6>());
        double p6 = dispatch(node->get_child<7>());
        return p1 * (t - t0) + p2 / 2 * (std::pow(t, 2) - std::pow(t0, 2)) + p3 / 3 * (std::pow(t, 3)
            - std::pow(t0, 3)) + p4 / 4 * (std::pow(t, 4) - std::pow(t0, 4)) + p5 / 5 * (std::pow(t, 5)
            - std::pow(t0, 5)) + p6 / 6 * (std::pow(t, 6) - std::pow(t0, 6));
    }

    double operator()(nasa9_hig_node* node) {
        double t  = dispatch(node->get_child<0>());
        double t0 = dispatch(node->get_child<1>());
        double p1 = dispatch(node->get_child<2>());
        double p2 = dispatch(node->get_child<3>());
        double p3 = dispatch(node->get_child<4>());
        double p4 = dispatch(node->get_child<5>());
        double p5 = dispatch(node->get_child<6>());
        double p6 = dispatch(node->get_child<7>());
        double p7 = dispatch(node->get_child<8>());
        return -p1 * (1 / t - 1 / t0) + p2 * std::log(t / t0) + p3 * (t - t0) + p4 / 2 * (std::pow(t, 2)
            - std::pow(t0, 2)) + p5 / 3 * (std::pow(t, 3) - std::pow(t0, 3)) + p6 / 4 * (std::pow(t, 4)
            - std::pow(t0, 4)) + p7 / 5 * (std::pow(t, 5) - std::pow(t0, 5));
    }

    double operator()(dippr107_hig_node* node) {
        double t  = dispatch(node->get_child<0>());
        double t0 = dispatch(node->get_child<1>());
        double p1 = dispatch(node->get_child<2>());
        double p2 = dispatch(node->get_child<3>());
        double p3 = dispatch(node->get_child<4>());
        double p4 = dispatch(node->get_child<5>());
        double p5 = dispatch(node->get_child<6>());
        return p1 * (t - t0) + p2 * p3*(1 / std::tanh(p3 / t) - 1 / std::tanh(p3 / t0))
            - p4 * p5*(std::tanh(p5 / t) - std::tanh(p5 / t0));
    }

    double operator()(dippr127_hig_node* node) {
        double t  = dispatch(node->get_child<0>());
        double t0 = dispatch(node->get_child<1>());
        double p1 = dispatch(node->get_child<2>());
        double p2 = dispatch(node->get_child<3>());
        double p3 = dispatch(node->get_child<4>());
        double p4 = dispatch(node->get_child<5>());
        double p5 = dispatch(node->get_child<6>());
        double p6 = dispatch(node->get_child<7>());
        double p7 = dispatch(node->get_child<8>());
        return p1 * (t - t0) + p2 * p3*(1 / (std::exp(p3 / t) - 1) - 1 / (std::exp(p3 / t0) - 1))
            + p4 * p5*(1 / (std::exp(p5 / t) - 1) - 1 / (std::exp(p5 / t0) - 1))
            + p6 * p7*(1 / (std::exp(p7 / t) - 1) - 1 / (std::exp(p7 / t0) - 1));
    }

    double operator()(antoine_tsat_node* node) {
        double t  = dispatch(node->get_child<0>());
        double p1 = dispatch(node->get_child<1>());
        double p2 = dispatch(node->get_child<2>());
        double p3 = dispatch(node->get_child<3>());
        return p2 / (p1 - std::log(t) / std::log(10.)) - p3;
    }

    double operator()(watson_dhvap_node* node) {
        double t  = dispatch(node->get_child<0>());
        double tc = dispatch(node->get_child<1>());
        double a = dispatch(node->get_child<2>());
        double b = dispatch(node->get_child<3>());
        double t1 = dispatch(node->get_child<4>());
        double dHT1 = dispatch(node->get_child<5>());
        double tr = 1 - t / tc;
        if (tr > 0) {
            return dHT1 * std::pow(tr / (1 - t1 / tc), a + b * tr);
        }
        else {
            return 0.;
        }
    }

    double operator()(dippr106_dhvap_node* node) {
        double t  = dispatch(node->get_child<0>());
        double tc = dispatch(node->get_child<1>());
        double p2 = dispatch(node->get_child<2>());
        double p3 = dispatch(node->get_child<3>());
        double p4 = dispatch(node->get_child<4>());
        double p5 = dispatch(node->get_child<5>());
        double p6 = dispatch(node->get_child<6>());
        double tr = t / tc;
        if (tr < 1) {
            return p2 * std::pow(1 - tr, p3 + p4 * tr + p5 * std::pow(tr, 2) + p6 * std::pow(tr, 3));
        }
        else {
            return 0.;
        }
    }

    double operator()(cost_turton_node* node) {
        double x  = dispatch(node->get_child<0>());
        double p1 = dispatch(node->get_child<1>());
        double p2 = dispatch(node->get_child<2>());
        double p3 = dispatch(node->get_child<3>());
        return std::pow(10., p1 + p2 * std::log(x) / std::log(10.) + p3 * std::pow(std::log(x)
            / std::log(10.), 2));
    }

    double operator()(nrtl_tau_node* node) {
        double t = dispatch(node->get_child<0>());
        double a = dispatch(node->get_child<1>());
        double b = dispatch(node->get_child<2>());
        double e = dispatch(node->get_child<3>());
        double f = dispatch(node->get_child<4>());
        return a + b / t + e * std::log(t) + f * t;
    }

    double operator()(nrtl_g_node* node) {
        double t = dispatch(node->get_child<0>());
        double a = dispatch(node->get_child<1>());
        double b = dispatch(node->get_child<2>());
        double e = dispatch(node->get_child<3>());
        double f = dispatch(node->get_child<4>());
        double alpha = dispatch(node->get_child<5>());
        if (alpha < 0) {
            throw std::invalid_argument("alpha in nrtl_g is negative");
        }
        //the parameters are a,b,e,f and alpha, for further info, see ASPEN help
        return std::exp(-alpha * (a + b / t + e * std::log(t) + f * t));
    }

    double operator()(nrtl_gtau_node* node) {
        double t = dispatch(node->get_child<0>());
        double a = dispatch(node->get_child<1>());
        double b = dispatch(node->get_child<2>());
        double e = dispatch(node->get_child<3>());
        double f = dispatch(node->get_child<4>());
        double alpha = dispatch(node->get_child<5>());
        if (alpha < 0) {
            throw std::invalid_argument("alpha in nrtl_gtau is negative");
        }
        //the parameters are a,b,e,f and alpha, for further info, see ASPEN help
        return std::exp(-alpha * (a + b / t + e * std::log(t) + f * t)) * (a + b / t + e * std::log(t) + f * t);
        }

    double operator()(nrtl_gdtau_node* node) {
        double t = dispatch(node->get_child<0>());
        double a = dispatch(node->get_child<1>());
        double b = dispatch(node->get_child<2>());
        double e = dispatch(node->get_child<3>());
        double f = dispatch(node->get_child<4>());
        double alpha = dispatch(node->get_child<5>());
        if (alpha < 0) {
            throw std::invalid_argument("alpha in nrtl_gdtau is negative");
        }
        //the parameters are a,b,e,f and alpha, for further info, see ASPEN help
        return std::exp(-alpha * (a + b / t + e * std::log(t) + f * t))*(f - b / std::pow(t, 2) + e / t);
        }

    double operator()(nrtl_dgtau_node* node) {
        double t = dispatch(node->get_child<0>());
        double a = dispatch(node->get_child<1>());
        double b = dispatch(node->get_child<2>());
        double e = dispatch(node->get_child<3>());
        double f = dispatch(node->get_child<4>());
        double alpha = dispatch(node->get_child<5>());
        if (alpha < 0) {
            throw std::invalid_argument("alpha in nrtl_dgtau is negative");
        }
        //the parameters are a,b,e,f and alpha, for further info, see ASPEN help
        return -alpha*
            //nrtl_Gtau(t,a,b,e,f,alpha)
            (std::exp(-alpha * (a + b / t + e * std::log(t) + f * t)) * (a + b / t + e * std::log(t) + f * t))*
             //nrtl_dtau(t,b,e,f)
            (b - e / std::pow(t, 2) + f / t);
        }

    double operator()(norm2_node* node) {
        return std::sqrt(pow(dispatch(node->get_child<0>()),2) + pow(dispatch(node->get_child<1>()),2));
        }

    double operator()(bounding_func_node* node) {
        double x = dispatch(node->get_child<0>());
        double lb = dispatch(node->get_child<1>());
        double ub = dispatch(node->get_child<2>());
        if (lb > ub) {
            throw std::invalid_argument("lb > ub in bounding_func");
        }
        if (lb > x) {
            throw std::invalid_argument("lb > x in bounding_func");
        }
        if (x > ub) {
            throw std::invalid_argument("x > ub in bounding_func");
        }
        return x;
    }

    template <typename TType>
    double operator()(sum_node<TType>* node) {
        auto elements = dispatch(node->template get_child<0>());
        symbols.push_scope();
        double result = 0;
        for (auto it = elements.begin(); it != elements.end(); ++it) {
            symbols.define(node->name, new parameter_symbol<TType>(node->name, *it));
            result += dispatch(node->template get_child<1>());
        }
        symbols.pop_scope();
        return result;
    }

    template <typename TType>
    double operator()(set_min_node<TType>* node) {
        auto elements = dispatch(node->template get_child<0>());
        if (elements.begin() == elements.end()) {
            throw std::invalid_argument("called set_min with emtpy set");
        }
        symbols.push_scope();
        double result = std::numeric_limits<double>::infinity();
        for (auto it = elements.begin(); it != elements.end(); ++it) {
            symbols.define(node->name, new parameter_symbol<TType>(node->name, *it));
            result = std::min(result, dispatch(node->template get_child<1>()));
        }
        symbols.pop_scope();
        return result;
    }

    template <typename TType>
    double operator()(set_max_node<TType>* node) {
        auto elements = dispatch(node->template get_child<0>());
        if (elements.begin() == elements.end()) {
            throw std::invalid_argument("called set_max with emtpy set");
        }
        symbols.push_scope();
        double result = - std::numeric_limits<double>::infinity();
        for (auto it = elements.begin(); it != elements.end(); ++it) {
            symbols.define(node->name, new parameter_symbol<TType>(node->name, *it));
            result = std::max(result, dispatch(node->template get_child<1>()));
        }
        symbols.pop_scope();
        return result;
    }

    // non-terminal index node visits
    int operator()(index_minus_node* node) {
        return - dispatch(node->get_child<0>());
    }

    int operator()(index_addition_node* node) {
        int result = 0;
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            result += dispatch(it->get());
        }
        return result;
    }

    int operator()(index_multiplication_node* node) {
        int result = 1;
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            result *= dispatch(it->get());
        }
        return result;
    }

    // non-terminal boolean node visits
    bool operator()(negation_node* node) {
        return ! dispatch(node->get_child<0>());
    }

    template <typename TType>
    bool operator()(equal_node<TType>* node) {
        return dispatch(node->template get_child<0>()) == dispatch(node->template get_child<1>());
    }

    template <typename TType>
    bool operator()(less_node<TType>* node) {
        return dispatch(node->template get_child<0>()) < dispatch(node->template get_child<1>());
    }

    template <typename TType>
    bool operator()(less_equal_node<TType>* node) {
        return dispatch(node->template get_child<0>()) <= dispatch(node->template get_child<1>());
    }

    template <typename TType>
    bool operator()(greater_node<TType>* node) {
        return dispatch(node->template get_child<0>()) > dispatch(node->template get_child<1>());
    }

    template <typename TType>
    bool operator()(greater_equal_node<TType>* node) {
        return dispatch(node->template get_child<0>()) >= dispatch(node->template get_child<1>());
    }

    bool operator()(disjunction_node* node) {
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            if (dispatch(it->get())) {
                return true;
            }
        }
        return false;
    }

    bool operator()(conjunction_node* node) {
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            if (!dispatch(it->get())) {
                return false;
            }
        }
        return true;
    }

    bool operator()(element_node*);

    template <typename TType>
    bool operator()(forall_node<TType>* node) {
        auto elements = dispatch(node->template get_child<0>());
        symbols.push_scope();
        for (auto it = elements.begin(); it != elements.end(); ++it) {
            symbols.define(node->name, new parameter_symbol<TType>(node->name, *it));
            if (!dispatch(node->template get_child<1>())) {
                symbols.pop_scope();
                return false;
            }
        }
        symbols.pop_scope();
        return true;
    }

    template <typename TType>
    typename set<TType, 0>::basic_type operator()(constant_node<set<TType, 0>>* node) {
        return node->value;
    }

    template <typename TType>
    typename set<TType, 0>::basic_type operator()(parameter_node<set<TType, 0>>* node) {
        auto sym = symbols.resolve<set<TType, 0>>(node->name);
        if (!sym) {
            throw std::invalid_argument("symbol " + node->name + " is ill-defined");
        }
        return dispatch(sym);
    }

    template <typename TType>
    typename set<TType, 0>::basic_type operator()(entry_node<set<TType, 0>>* node) {
        return dispatch(node->template get_child<0>())[dispatch(node->template get_child<1>())-1];
    }

    template <typename TType>
    typename set<TType, 0>::basic_type operator()(indicator_set_node<TType>* node) {
        auto elements = dispatch(node->template get_child<0>());
        symbols.push_scope();
        for (auto it = elements.begin(); it != elements.end();) {
            symbols.define(node->name, new parameter_symbol<TType>(node->name, *it));
            if (!dispatch(node->template get_child<1>())) {
                it = elements.erase(it);
            }
            else {
                ++it;
            }
        }
        symbols.pop_scope();
        return elements;
    }

    symbol_table& get_symbols() {
        return symbols;
    }
private:
    symbol_table& symbols;
};

class member_checker {
public:
    member_checker(double value, evaluator& eval) : value(value), eval(eval), symbols(eval.get_symbols()) {};

    bool dispatch(value_node<set<real<0>, 0>>* node) {
        return std::visit(*this, node->get_variant());
    }

    bool dispatch(value_symbol<set<real<0>, 0>>* sym) {
        return std::visit(*this, sym->get_value_variant());
    }

    bool operator()(parameter_symbol<set<real<0>, 0>>* sym) {
        for (auto it = sym->m_value.begin(); it != sym->m_value.end(); ++it) {
            if (*it == value) {
                return true;
            }
        }
        return false;
    }

    bool operator()(constant_node<set<real<0>, 0>>* node) {
        for (auto it = node->value.begin(); it != node->value.end(); ++it) {
            if (*it == value) {
                return true;
            }
        }
        return false;
    }

    bool operator()(parameter_node<set<real<0>, 0>>* node) {
        auto sym = symbols.resolve<set<real<0>, 0>>(node->name);
        if (!sym) {
            throw std::invalid_argument("symbol " + node->name + " is ill-defined");
        }
        return dispatch(sym);
    }

    bool operator()(entry_node<set<real<0>, 0>>* node) {
        auto temp = eval.dispatch(node);
        for (auto it = temp.begin(); it != temp.end(); ++it) {
            if (*it == value) {
                return true;
            }
        }
        return false;
    }

    bool operator()(indicator_set_node<real<0>>* node) {
        symbols.push_scope();
        symbols.define(node->name, new parameter_symbol<real<0>>(node->name, value));
        bool result = dispatch(node->get_child<0>()) && eval.dispatch(node->get_child<1>());
        symbols.pop_scope();
        return result;
    }
private:
    double value;
    evaluator& eval;
    symbol_table& symbols;
};

inline bool evaluator::operator()(element_node* node) {
    member_checker mem(dispatch(node->get_child<0>()), *this);
    return mem.dispatch(node->get_child<1>());
}



}
