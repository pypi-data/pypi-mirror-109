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

#include "parser.hpp"

#include <iostream>

using token_type = ale::token::token_type;

namespace ale {



parser::parser(std::istream& input, symbol_table& symbols)
    : lex(input), buf(lex), error_stream(std::cerr), symbols(symbols)
{
    lex.reserve_keywords(
        {
            // fundamentals
            "real", "integer", "binary", "index", "boolean", "set",
            "in", "lb", "ub", "init", "true", "false",
            // functions
            "sum", "min", "max", "mid", "forall",
            "exp", "log", "pow", "sqr", "sqrt", "abs", "inv",
            "sin", "asin", "cos", "acos", "tan", "atan",
            "sinh", "cosh", "tanh", "coth", "asinh", "acosh", "atanh", "acoth",
            // special functions
            "arh", "xexpy", "xexpax", "xlogx", "xabsx",
            "erf", "erfc", "norm2", "sum_div", "xlog_sum",
            "pos", "neg", "lb_func", "ub_func", "bounding_func", "squash", "regnormal",
            "lmtd", "rlmtd", "cost_turton",
            "covar_matern_1", "covar_matern_3", "covar_matern_5", "covar_sqrexp",
            "af_lcb", "af_ei", "af_pi", "gpdf",
            "nrtl_tau", "nrtl_dtau", "nrtl_g", "nrtl_gtau", "nrtl_gdtau", "nrtl_dgtau",
            "antoine_psat", "ext_antoine_psat", "wagner_psat", "ik_cape_psat",
            "antoine_tsat",
            "aspen_hig", "nasa9_hig", "dippr107_hig", "dippr127_hig",
            "watson_dhvap", "dippr106_dhvap",
            "schroeder_ethanol_p","schroeder_ethanol_rhovap","schroeder_ethanol_rholiq"
        }
    );
}



// input handling
token parser::current() {
    token tok = buf.current();
    while (tok.type == token::ERROR) {
        report_lexical(tok);
        discard();
        tok = buf.current();
    }
    return tok;
}

void parser::consume() {
    buf.consume();
}

void parser::discard() {
    buf.discard();
}

bool parser::check(token::token_type expect) {
    set_expected_token(expect);
    if (current().type != expect) {
        return false;
    }
    return true;
}

bool parser::match(token::token_type expect) {
    if (check(expect)) {
        buf.consume();
        return true;
    }
    return false;
}

bool parser::check_keyword(const std::string& expect) {
    set_expected_keyword(expect);
    if (current().type == token::KEYWORD) {
        if (current().lexeme == expect) {
            return true;
        }
    }
    return false;
}

bool parser::match_keyword(const std::string& expect) {
    if (check_keyword(expect)) {
        buf.consume();
        return true;
    }
    return false;
}

// TODO: implement check() without setting expected
void parser::recover() {
    while (current().type != token::SEMICOL && current().type != token::END) {
        consume();
    }
    consume();
    buf.clear();
}

void parser::init() {
    buf.mark();
}

bool parser::accept() {
    buf.unmark();
    return true;
}

bool parser::reject() {
    buf.backtrack();
    return false;
}



// parser rules
bool parser::match_value(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_addition(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_addition(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    std::unique_ptr<value_node<real<0>>> child;
    if (match(token::MINUS)) {
        std::unique_ptr<value_node<real<0>>> mult;
        if (!match_multiplication(mult)) {
            return reject();
        }
        child.reset(new minus_node(mult.release()));
    }
    else if (!match_multiplication(child)) {
        return reject();
    }
    if (!check_any(token::PLUS, token::MINUS)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<addition_node>();
    parent->add_child(child.release());
    while (check_any(token::PLUS, token::MINUS)) {
        if (match(token::PLUS)) {
            if (!match_multiplication(child)) {
                return reject();
            }
            parent->add_child(child.release());
        }
        else if (match(token::MINUS)) {
            if (!match_multiplication(child)) {
                return reject();
            }
            auto minus = std::make_unique<minus_node>(child.release());
            parent->add_child(minus.release());
        }
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_multiplication(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    std::unique_ptr<value_node<real<0>>> child;
    if (!match_exponentiation(child)) {
        return reject();
    }
    if (!check_any(token::STAR, token::SLASH)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<multiplication_node>();
    parent->add_child(child.release());
    while (check_any(token::STAR, token::SLASH)) {
        if (match(token::STAR)) {
            if (!match_exponentiation(child)) {
                return reject();
            }
            parent->add_child(child.release());
        }
        else if (match(token::SLASH)) {
            if (!match_exponentiation(child)) {
                return reject();
            }
            auto inverse = std::make_unique<inverse_node>(child.release());
            parent->add_child(inverse.release());
        }
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_exponentiation(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    std::unique_ptr<value_node<real<0>>> child;
    if (!match_unary(child)) {
        return reject();
    }
    if (!check(token::HAT)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<exponentiation_node>();
    parent->add_child(child.release());
    while (match(token::HAT)) {
        if (!match_unary(child)) {
            return reject();
        }
        parent->add_child(child.release());
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_unary(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_primary(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_primary(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_constant(result)) {
        return accept();
    }
    if (match_parameter(result)) {
        return accept();
    }
    if (match_unary_function(result)) {
        return accept();
    }
    if (match_binary_function(result)) {
        return accept();
    }
    if (match_ternary_function(result)) {
        return accept();
    }
    if (match_quaternary_function(result)) {
        return accept();
    }
    if (match_quinary_function(result)) {
        return accept();
    }
    if (match_senary_function(result)) {
        return accept();
    }
    if (match_septenary_function(result)) {
        return accept();
    }
    if (match_octonary_function(result)) {
        return accept();
    }
    if (match_novenary_function(result)) {
        return accept();
    }
    if (match_unodenary_function(result)) {
        return accept();
    }
    if (match_nary_function(result)) {
        return accept();
    }
    if (match_any_sum<LIBALE_MAX_DIM>(result)) {
        return accept();
    }
    if (match_any_set_min<LIBALE_MAX_DIM>(result)) {
        return accept();
    }
    if (match_any_set_max<LIBALE_MAX_DIM>(result)) {
        return accept();
    }
    if (match_grouping(result)) {
        return accept();
    }
    if (match_entry(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_unary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("exp", "log", "sqrt", "sin", "asin", "cos", "acos",
        "tan", "atan", "xlogx", "sqr", "abs", "xabsx", "cosh", "sinh",
        "tanh", "coth", "asinh", "acosh", "atanh", "acoth", "inv", "erf", "erfc",
        "pos", "neg", "schroeder_ethanol_p", "schroeder_ethanol_rhovap",
        "schroeder_ethanol_rholiq", "covar_matern_1", "covar_matern_3", "covar_matern_5", "covar_sqrexp", "gpdf"))
    {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    std::unique_ptr<value_node<real<0>>> child;
    if (!match_grouping(child)) {
        return reject();
    }
    if (type == "exp") {
        result.reset(new exp_node(child.release()));
        return accept();
    }
    if (type == "log") {
        result.reset(new log_node(child.release()));
        return accept();
    }
    if (type == "sqrt") {
        result.reset(new sqrt_node(child.release()));
        return accept();
    }
    if (type == "sin") {
        result.reset(new sin_node(child.release()));
        return accept();
    }
    if (type == "asin") {
        result.reset(new asin_node(child.release()));
        return accept();
    }
    if (type == "cos") {
        result.reset(new cos_node(child.release()));
        return accept();
    }
    if (type == "acos") {
        result.reset(new acos_node(child.release()));
        return accept();
    }
    if (type == "tan") {
        result.reset(new tan_node(child.release()));
        return accept();
    }
    if (type == "atan") {
        result.reset(new atan_node(child.release()));
        return accept();
    }
    if (type == "xlogx") {
        result.reset(new xlogx_node(child.release()));
        return accept();
    }
    if (type == "sqr") {
        auto parent = std::make_unique<exponentiation_node>();
        parent->add_child(child.release());
        parent->add_child(new constant_node<real<0>>(2));
        result.reset(parent.release());
        return accept();
    }
    if (type == "abs") {
        result.reset(new abs_node(child.release()));
        return accept();
    }
    if (type == "xabsx") {
        result.reset(new xabsx_node(child.release()));
        return accept();
    }
    if (type == "cosh") {
        result.reset(new cosh_node(child.release()));
        return accept();
    }
    if (type == "sinh") {
        result.reset(new sinh_node(child.release()));
        return accept();
    }
    if (type == "tanh") {
        result.reset(new tanh_node(child.release()));
        return accept();
    }
    if (type == "coth") {
        result.reset(new coth_node(child.release()));
        return accept();
    }
    if (type == "acosh") {
        result.reset(new acosh_node(child.release()));
        return accept();
    }
    if (type == "asinh") {
        result.reset(new asinh_node(child.release()));
        return accept();
    }
    if (type == "atanh") {
        result.reset(new atanh_node(child.release()));
        return accept();
    }
    if (type == "acoth") {
        result.reset(new acoth_node(child.release()));
        return accept();
    }
    if (type == "inv") {
        result.reset(new inverse_node(child.release()));
        return accept();
    }
    if (type == "erf") {
        result.reset(new erf_node(child.release()));
        return accept();
    }
    if (type == "erfc") {
        result.reset(new erfc_node(child.release()));
        return accept();
    }
    if (type == "pos") {
        result.reset(new pos_node(child.release()));
        return accept();
    }
    if (type == "neg") {
        result.reset(new neg_node(child.release()));
        return accept();
    }
    if (type == "schroeder_ethanol_p") {
        result.reset(new schroeder_ethanol_p_node(child.release()));
        return accept();
    }
    if (type == "schroeder_ethanol_rhovap") {
        result.reset(new schroeder_ethanol_rhovap_node(child.release()));
        return accept();
    }
    if (type == "schroeder_ethanol_rholiq") {
        result.reset(new schroeder_ethanol_rholiq_node(child.release()));
        return accept();
    }
    if (type == "covar_matern_1") {
        result.reset(new covar_matern_1_node(child.release()));
        return accept();
    }
    if (type == "covar_matern_3") {
        result.reset(new covar_matern_3_node(child.release()));
        return accept();
    }
    if (type == "covar_matern_5") {
        result.reset(new covar_matern_5_node(child.release()));
        return accept();
    }
    if (type == "covar_sqrexp") {
        result.reset(new covar_sqrexp_node(child.release()));
        return accept();
    }
    if (type == "gpdf") {
        result.reset(new gpdf_node(child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_binary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("pow", "lmtd", "rlmtd", "xexpax", "arh", "lb_func",
        "ub_func", "xexpy", "norm2"))
    {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "pow") {
        auto parent = std::make_unique<exponentiation_node>();
        parent->add_child(first_child.release());
        parent->add_child(second_child.release());
        result.reset(parent.release());
        return accept();
    }
    if (type == "lmtd") {
        result.reset(new lmtd_node(
            first_child.release(), second_child.release()));
        return accept();
    }
    if (type == "rlmtd") {
        result.reset(new rlmtd_node(
            first_child.release(), second_child.release()));
        return accept();
    }
    if (type == "xexpax") {
        result.reset(new xexpax_node(
            first_child.release(), second_child.release()));
        return accept();
    }
    if (type == "arh") {
        result.reset(new arh_node(
            first_child.release(), second_child.release()));
        return accept();
    }
    if (type == "lb_func") {
        result.reset(new lb_func_node(
            first_child.release(), second_child.release()));
        return accept();
    }
    if (type == "ub_func") {
        result.reset(new ub_func_node(
            first_child.release(), second_child.release()));
        return accept();
    }
    if (type == "xexpy") {
        result.reset(new xexpy_node(
            first_child.release(), second_child.release()));
        return accept();
    }
    if (type == "norm2") {
        result.reset(new norm2_node(
            first_child.release(), second_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_ternary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("mid", "bounding_func", "squash", "regnormal", "af_lcb", "af_ei", "af_pi")) {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> third_child;
    if (!match_value(third_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "mid") {
        result.reset(new mid_node(
            first_child.release(), second_child.release(),
            third_child.release()));
        return accept();
    }
    if (type == "bounding_func") {
        result.reset(new bounding_func_node(
            first_child.release(), second_child.release(),
            third_child.release()));
        return accept();
    }
    if (type == "squash") {
        result.reset(new squash_node(
            first_child.release(), second_child.release(),
            third_child.release()));
        return accept();
    }
    if (type == "regnormal") {
        result.reset(new regnormal_node(
            first_child.release(), second_child.release(),
            third_child.release()));
        return accept();
    }
    if (type == "af_lcb") {
        result.reset(new regnormal_node(
            first_child.release(), second_child.release(),
            third_child.release()));
        return accept();
    }
    if (type == "af_ei") {
        result.reset(new regnormal_node(
            first_child.release(), second_child.release(),
            third_child.release()));
        return accept();
    }
    if (type == "af_pi") {
        result.reset(new regnormal_node(
            first_child.release(), second_child.release(),
            third_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_quaternary_function(std::unique_ptr<value_node<real<0>>>& result){
    init();
    if (!check_any_keyword("nrtl_dtau", "antoine_psat",
        "antoine_tsat", "cost_turton")) {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> third_child;
    if (!match_value(third_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fourth_child;
    if (!match_value(fourth_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "nrtl_dtau") {
        result.reset(new nrtl_dtau_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release()));
        return accept();
    }
    if (type == "antoine_psat") {
        result.reset(new antoine_psat_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release()));
        return accept();
    }
    if (type == "antoine_tsat") {
        result.reset(new antoine_tsat_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release()));
        return accept();
    }
    if (type == "cost_turton") {
        result.reset(new cost_turton_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_quinary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("nrtl_tau")) {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> third_child;
    if (!match_value(third_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fourth_child;
    if (!match_value(fourth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fifth_child;
    if (!match_value(fifth_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "nrtl_tau") {
        result.reset(new nrtl_tau_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_senary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("nrtl_g", "nrtl_gtau", "nrtl_gdtau",
        "nrtl_dgtau", "watson_dhvap")) {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> third_child;
    if (!match_value(third_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fourth_child;
    if (!match_value(fourth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fifth_child;
    if (!match_value(fifth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> sixth_child;
    if (!match_value(sixth_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "nrtl_g") {
        result.reset(new nrtl_g_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release()));
        return accept();
    }
    if (type == "nrtl_gtau") {
        result.reset(new nrtl_gtau_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release()));
        return accept();
    }
    if (type == "nrtl_gdtau") {
        result.reset(new nrtl_gdtau_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release()));
        return accept();
    }
    if (type == "nrtl_dgtau") {
        result.reset(new nrtl_dgtau_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release()));
        return accept();
    }
    if (type == "watson_dhvap") {
        result.reset(new watson_dhvap_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_septenary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("dippr106_dhvap", "wagner_psat", "dippr107_hig")) {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> third_child;
    if (!match_value(third_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fourth_child;
    if (!match_value(fourth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fifth_child;
    if (!match_value(fifth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> sixth_child;
    if (!match_value(sixth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> seventh_child;
    if (!match_value(seventh_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "dippr106_dhvap") {
        result.reset(new dippr106_dhvap_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release(),
            seventh_child.release()));
        return accept();
    }
    if (type == "wagner_psat") {
        result.reset(new wagner_psat_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release(),
            seventh_child.release()));
        return accept();
    }
    if (type == "dippr107_hig") {
        result.reset(new dippr107_hig_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release(),
            seventh_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_octonary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("aspen_hig", "ext_antoine_psat")) {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> third_child;
    if (!match_value(third_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fourth_child;
    if (!match_value(fourth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fifth_child;
    if (!match_value(fifth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> sixth_child;
    if (!match_value(sixth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> seventh_child;
    if (!match_value(seventh_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> eighth_child;
    if (!match_value(eighth_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "aspen_hig") {
        result.reset(new aspen_hig_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release(),
            seventh_child.release(), eighth_child.release()));
        return accept();
    }
    if (type == "ext_antoine_psat") {
        result.reset(new ext_antoine_psat_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release(),
            seventh_child.release(), eighth_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_novenary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("nasa9_hig", "dippr127_hig")) {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> third_child;
    if (!match_value(third_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fourth_child;
    if (!match_value(fourth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fifth_child;
    if (!match_value(fifth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> sixth_child;
    if (!match_value(sixth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> seventh_child;
    if (!match_value(seventh_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> eighth_child;
    if (!match_value(eighth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> nineth_child;
    if (!match_value(nineth_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "nasa9_hig") {
        result.reset(new nasa9_hig_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release(),
            seventh_child.release(), eighth_child.release(),
            nineth_child.release()));
        return accept();
    }
    if (type == "dippr127_hig") {
        result.reset(new dippr127_hig_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release(),
            seventh_child.release(), eighth_child.release(),
            nineth_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_unodenary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!check_any_keyword("ik_cape_psat")) {
        return reject();
    }
    std::string type = current().lexeme;
    consume();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> third_child;
    if (!match_value(third_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fourth_child;
    if (!match_value(fourth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> fifth_child;
    if (!match_value(fifth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> sixth_child;
    if (!match_value(sixth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> seventh_child;
    if (!match_value(seventh_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> eighth_child;
    if (!match_value(eighth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> nineth_child;
    if (!match_value(nineth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> tenth_child;
    if (!match_value(tenth_child)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> eleventh_child;
    if (!match_value(eleventh_child)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    if (type == "ik_cape_psat") {
        result.reset(new ik_cape_psat_node(
            first_child.release(), second_child.release(),
            third_child.release(), fourth_child.release(),
            fifth_child.release(), sixth_child.release(),
            seventh_child.release(), eighth_child.release(),
            nineth_child.release(), tenth_child.release(),
            eleventh_child.release()));
        return accept();
    }
    return reject();
}

bool parser::match_nary_function(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_min(result)) {
        return accept();
    }
    if (match_max(result)) {
        return accept();
    }
    if (match_sum_div(result)) {
        return accept();
    }
    if (match_xlog_sum(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_min(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!match_keyword("min")) {
        return reject();
    }
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> child;
    if (!match_value(child)) {
        return reject();
    }
    if (match(token::RPAREN)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<min_node>();
    parent->add_child(child.release());
    while (match(token::COMMA)) {
        if (!match_value(child)) {
            return reject();
        }
        parent->add_child(child.release());
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_max(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!match_keyword("max")) {
        return reject();
    }
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> child;
    if (!match_value(child)) {
        return reject();
    }
    if (match(token::RPAREN)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<max_node>();
    parent->add_child(child.release());
    while (match(token::COMMA)) {
        if (!match_value(child)) {
            return reject();
        }
        parent->add_child(child.release());
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_sum_div(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!match_keyword("sum_div")) {
        return reject();
    }
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> child;
    if (!match_value(child)) {
        return reject();
    }
    if (match(token::RPAREN)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<sum_div_node>();
    parent->add_child(child.release());
    while (match(token::COMMA)) {
        if (!match_value(child)) {
            return reject();
        }
        parent->add_child(child.release());
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_xlog_sum(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!match_keyword("xlog_sum")) {
        return reject();
    }
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::unique_ptr<value_node<real<0>>> child;
    if (!match_value(child)) {
        return reject();
    }
    if (match(token::RPAREN)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<xlog_sum_node>();
    parent->add_child(child.release());
    while (match(token::COMMA)) {
        if (!match_value(child)) {
            return reject();
        }
        parent->add_child(child.release());
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    result.reset(parent.release());
    return accept();
}



bool parser::match_value(std::unique_ptr<value_node<index<0>>>& result) {
    init();
    if (match_addition(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_addition(std::unique_ptr<value_node<index<0>>>& result) {
    init();
    std::unique_ptr<value_node<index<0>>> child;
    if (match(token::MINUS)) {
        std::unique_ptr<value_node<index<0>>> mult;
        if (!match_multiplication(mult)) {
            return reject();
        }
        child.reset(new index_minus_node(mult.release()));
    }
    else if (!match_multiplication(child)) {
        return reject();
    }
    if (!check_any(token::PLUS, token::MINUS)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<index_addition_node>();
    parent->add_child(child.release());
    while (check_any(token::PLUS, token::MINUS)) {
        if (match(token::PLUS)) {
            if (!match_multiplication(child)) {
                return reject();
            }
            parent->add_child(child.release());
        }
        else if (match(token::MINUS)) {
            if (!match_multiplication(child)) {
                return reject();
            }
            auto minus = std::make_unique<index_minus_node>(child.release());
            parent->add_child(minus.release());
        }
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_multiplication(std::unique_ptr<value_node<index<0>>>& result) {
    init();
    std::unique_ptr<value_node<index<0>>> child;
    if (!match_unary(child)) {
        return reject();
    }
    if (!check(token::STAR)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<index_multiplication_node>();
    parent->add_child(child.release());
    while (match(token::STAR)) {
        if (!match_unary(child)) {
            return reject();
        }
        parent->add_child(child.release());
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_unary(std::unique_ptr<value_node<index<0>>>& result) {
    init();
    if (match_primary(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_primary(std::unique_ptr<value_node<index<0>>>& result) {
    init();
    if (match_constant(result)) {
        return accept();
    }
    if (match_parameter(result)) {
        return accept();
    }
    if (match_grouping(result)) {
        return accept();
    }
    if (match_entry(result)) {
        return accept();
    }
    return reject();
}



bool parser::match_value(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    if (match_disjunction(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_disjunction(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    std::unique_ptr<value_node<boolean<0>>> child;
    if (!match_conjunction(child)) {
        return reject();
    }
    if (!check(token::PIPE)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<disjunction_node>();
    parent->add_child(child.release());
    while (match(token::PIPE)) {
        if (!match_conjunction(child)) {
            return reject();
        }
        parent->add_child(child.release());
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_conjunction(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    std::unique_ptr<value_node<boolean<0>>> child;
    if (!match_unary(child)) {
        return reject();
    }
    if (!check(token::AND)) {
        result.reset(child.release());
        return accept();
    }
    auto parent = std::make_unique<conjunction_node>();
    parent->add_child(child.release());
    while (match(token::AND)) {
        if (!match_unary(child)) {
            return reject();
        }
        parent->add_child(child.release());
    }
    result.reset(parent.release());
    return accept();
}

bool parser::match_unary(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    if (match_negation(result)) {
        return accept();
    }
    if (match_primary(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_negation(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    if (!match(token::BANG)) {
        return reject();
    }
    std::unique_ptr<value_node<boolean<0>>> child;
    if (!match_unary(child)) {
        return reject();
    }
    result.reset(new negation_node(child.release()));
    return accept();
}

bool parser::match_primary(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    if (match_constant(result)) {
        return accept();
    }
    if (match_parameter(result)) {
        return accept();
    }
    if (match_comparison<real<0>>(result)) {
        return accept();
    }
    if (match_comparison<index<0>>(result)) {
        return accept();
    }
    if (match_element(result)) {
        return accept();
    }
    if (match_any_quantifier<LIBALE_MAX_DIM>(result)) {
        return accept();
    }
    if (match_grouping(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_element(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    std::unique_ptr<value_node<real<0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match_keyword("in")) {
        return reject();
    }
    std::unique_ptr<value_node<set<real<0>, 0>>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    result.reset(new element_node(first_child.release(), second_child.release()));
    return accept();
}

bool parser::match_primary(std::unique_ptr<value_node<set<real<0>, 0>>>& result) {
    init();
    if (match_constant(result)) {
        return accept();
    }
    if (match_parameter(result)) {
        return accept();
    }
    if (match_entry(result)) {
        return accept();
    }
    if (match_indicator_set(result)) {
        return accept();
    }
    return reject();
}


bool parser::match_primary(std::unique_ptr<value_node<set<index<0>, 0>>>& result) {
    init();
    if (match_constant(result)) {
        return accept();
    }
    if (match_parameter(result)) {
        return accept();
    }
    if (match_entry(result)) {
        return accept();
    }
    if (match_indicator_set(result)) {
        return accept();
    }
    return reject();
}

bool parser::match_literal(std::string& lit) {
    init();
    if (!check(token::LITERAL)) {
        return reject();
    }
    lit = current().lexeme;
    consume();
    return accept();
}



// error reporting
bool parser::fail() {
    return had_error;
}

void parser::clear() {
    had_error = false;
}

void parser::print_errors() {
    while (!errors.empty()) {
        error_stream << errors.front() << std::endl;
        errors.pop();
    }
}

void parser::set_expected_token(token::token_type type) {
    if (current().position < unexpected_token.position) {
        return;
    }
    if (current().position == unexpected_token.position) {
        expected.insert(token::string(type));
        return;
    }
    unexpected_token = current();
    expected.clear();
    expected.insert(token::string(type));
}

void parser::set_expected_keyword(std::string lexeme) {
    if (current().position < unexpected_token.position) {
        return;
    }
    if (current().position == unexpected_token.position) {
        expected.insert(lexeme);
        return;
    }
    unexpected_token = current();
    expected.clear();
    expected.insert(lexeme);
}

void parser::set_expected_symbol() {
    if (current().position > unexpected_symbol.position) {
        unexpected_symbol = current();
    }
}

void parser::set_semantic(std::string error) {
    if (current().position > semantic_token.position) {
        semantic_token = current();
        semantic_issue = error;
        semantic_issue += " on input ";
        semantic_issue += current().position_string();
    }
}

void parser::report_empty() {
    had_error = true;
    errors.push("ERROR: Empty input");
}

void parser::report_lexical(token tok) {
    had_error = true;
    std::string error = "ERROR: Unexpected character '";
    error += tok.lexeme;
    error += "' on input ";
    error += tok.position_string();
    errors.push(error);
}

void parser::report_syntactical() {
    had_error = true;
    auto furthest = semantic_token.position;
    if (furthest < unexpected_symbol.position) {
        furthest = unexpected_symbol.position;
    }
    if (furthest < unexpected_token.position) {
        furthest = unexpected_token.position;
    }
    if (semantic_token.position == furthest) {
        errors.push(semantic_issue);
    }
    else if (unexpected_symbol.position == furthest) {
        std::string error;
        error += "ERROR: Unexpected symbol '";
        error += unexpected_symbol.lexeme;
        error += "' on input ";
        error += unexpected_symbol.position_string();
        errors.push(error);
    }
    else  {
        std::string error;
        error += "ERROR: Unexpected token '";
        if (unexpected_token.type == token::KEYWORD) {
            error += unexpected_token.lexeme;
        }
        else {
            error += token::string(unexpected_token.type);
        }
        error += "' on input ";
        error += unexpected_token.position_string() + ", ";
        error += "expected ";
        for (auto it = expected.begin(); it != expected.end(); ++it) {
            error += "'" + *it + "'";
            if (next(it) != expected.end()) {
                error += ", ";
            }
        }
        errors.push(error);
    }
}



}
