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

#include "lexer.hpp"
#include "token_buffer.hpp"
#include "node.hpp"
#include "symbol_table.hpp"

#include <stack>
#include <queue>
#include <set>
#include <memory>

namespace ale {



class parser {
public:
    parser(std::istream&, symbol_table&);
    bool fail();
    void clear();
    void print_errors();
protected:
    symbol_table& symbols;

    // input handling
    token current();
    void consume();
    void discard();
    bool check(token::token_type);
    bool match(token::token_type);
    bool check_keyword(const std::string&);
    bool match_keyword(const std::string&);
    void recover();

    void init();
    bool accept();
    bool reject();

    // parser rules
    // helper rules
    template <typename... TRest> bool check_any(token::token_type, TRest...);
    template <typename... TTypes> bool match_any(TTypes...);
    template <typename... TRest> bool check_any_keyword(const std::string&, const TRest&...);
    template <typename TType> bool exists(std::string);
    bool available(std::string);

    // entry points
    template <typename TType> bool match_expression(std::unique_ptr<value_node<TType>>&);
    template <typename TType> bool match_expression(std::unique_ptr<value_node<TType>>&, std::string&);
    bool match_literal(std::string&);
    //  expression<T> = value<T> [LITERAL] SEMICOL

    // generic dispatch
    template <typename TType> bool match_value(std::unique_ptr<value_node<TType>>&);
    //  value<T> = primary<T>

    // generic primary tensor
    template <typename TType> bool match_primary(std::unique_ptr<value_node<TType>>&);
    //  primary<T> = constant<T>
    //             | parameter<T>

    // generic primary set
    template <typename TType> bool match_primary(std::unique_ptr<value_node<set<TType, 0>>>&);
    //  primary<set<T>> = constant<set<T>>
    //                  | parameter<set<T>>
    //                  | entry<set<T>>


    // generic primary alternatives
    template <typename TType> bool match_constant(std::unique_ptr<value_node<TType>>&);
    //  constant<T> = basic<T>
    template <typename TType> bool match_parameter(std::unique_ptr<value_node<TType>>&);
    //  parameter<T> = IDENT
    template <typename TType> bool match_grouping(std::unique_ptr<value_node<TType>>&);
    //  grouping<T> = LPAREN value<T> RPAREN
    template <typename TType> bool match_partial_entry(std::unique_ptr<value_node<TType>>&);
    template <typename TAtom> bool match_partial_entry(std::unique_ptr<value_node<tensor_type<TAtom, LIBALE_MAX_DIM - 1>>>&);
    template <typename TAtom> bool match_partial_entry(std::unique_ptr<value_node<set<TAtom, LIBALE_MAX_SET_DIM - 1>>>&);
    template <typename TType> bool match_entry(std::unique_ptr<value_node<TType>>&);
    template <typename TAtom> bool match_entry(std::unique_ptr<value_node<tensor_type<TAtom, LIBALE_MAX_DIM - 1>>>&);
    template <typename TAtom> bool match_entry(std::unique_ptr<value_node<set<TAtom, LIBALE_MAX_SET_DIM - 1>>>&);
    // LET n AND m BE DIMENSIONS WITH n < m
    //  entry<T<n>> = value<T<m>> LBRACK value<index<0>> ( COMMA value<index<0>> )*(m-n-1) RBRACK

    // generic basics
    template <typename TAtom, unsigned IDim> bool match_tensor(typename tensor_type<TAtom, IDim>::basic_type&);
    template <typename TAtom> bool match_vector(typename tensor_type<TAtom, 1>::basic_type&);
    template <typename TAtom> bool match_set(typename set<TAtom, 0>::basic_type&);
    template <typename TAtom> bool match_sequence(typename set<TAtom, 0>::basic_type&);

    // tag dispatch overloads for match_basic
    template <typename TType> struct basic_tag {};
    template <typename TAtom, unsigned IDim>
    bool match_basic(typename tensor_type<TAtom, IDim>::basic_type&, basic_tag<tensor_type<TAtom, IDim>>);
    template <typename TAtom>
    bool match_basic(typename tensor_type<TAtom, 1>::basic_type&, basic_tag<tensor_type<TAtom, 1>>);
    template <typename TAtom>
    bool match_basic(typename set<TAtom, 0>::basic_type&, basic_tag<set<TAtom, 0>>);
    inline bool match_basic(typename real<0>::basic_type&, basic_tag<real<0>>);
    inline bool match_basic(typename index<0>::basic_type&, basic_tag<index<0>>);
    inline bool match_basic(typename boolean<0>::basic_type&, basic_tag<boolean<0>>);
    // template call to tag dispatch overloads
    template <typename TType> bool match_basic(typename TType::basic_type&);
    //  basic<T<n>> = LBRACK [ basic<T<n-1>> ( COMMA basic<T<n-1>> )* ] RBRACK
    //  basic<real<0>> = [MINUS] ( NUMBER | INTEGER )
    //  basic<index<0>> = INTEGER
    //  basic<boolean<0>> = "true" | "false"
    //  basic<set<T>> = LBRACE [ basic<T> ( COMMA basic<T> )* ] RBRACE
    //  basic<set<index<0>>> = LBRACE [ basic<index<0>> ( COMMA basic<index<0>> )* ] RBRACE
    //                       | LBRACE basic<index<0>> DOTS basic<index<0>> RBRACE

    // set operations
    template <unsigned IDim> bool match_any_sum(std::unique_ptr<value_node<real<0>>>&);
    // any_sum = sum<real<0>> | sum <index<0>>
    //         | ...
    //         | sum<real<LIBALE_MAX_DIM>> | sum<index<LIBALE_MAX_DIM>>
    template <typename TType> bool match_sum(std::unique_ptr<value_node<real<0>>>&);
    // sum<T> = "sum" LPAREN IDENT "in" COLON value<real<0>> RPAREN
    template <unsigned IDim> bool match_any_set_min(std::unique_ptr<value_node<real<0>>>&);
    // any_set_min = set_min<real<0>> | set_min <index<0>>
    //             | ...
    //             | set_min<real<LIBALE_MAX_DIM>> | set_min<index<LIBALE_MAX_DIM>>
    template <typename TType> bool match_set_min(std::unique_ptr<value_node<real<0>>>&);
    // set_min<T> = "min" LPAREN IDENT "in" COLON value<real<0>> RPAREN
    template <unsigned IDim> bool match_any_set_max(std::unique_ptr<value_node<real<0>>>&);
    // any_set_max = set_max<real<0>> | set_max<index<0>>
    //             | ...
    //             | set_max<real<LIBALE_MAX_DIM>> | set_max<index<LIBALE_MAX_DIM>>
    template <typename TType> bool match_set_max(std::unique_ptr<value_node<real<0>>>&);
    // set_max<T> = "max" LPAREN IDENT "in" COLON value<real<0>> RPAREN

    //comparisons
    template <typename TType> bool match_comparison(std::unique_ptr<value_node<boolean<0>>>&);
    //  comparison<T> = value<T> ( EQUAL | LESS | LEQUAL | GREATER | GEQUAL ) value<T>

    // sets
    template <typename TType> bool match_indicator_set(std::unique_ptr<value_node<set<TType, 0>>>&);
    //  indicator_set<T> = LBRACE IDENT "in" value<set<T>> COLON value<boolean<0>> RBRACE

    // quantifiers
    template <unsigned IDim> bool match_any_quantifier(std::unique_ptr<value_node<boolean<0>>>&);
    //  any_quantifier = forall<real<0>> | forall<index<0>>
    //                | ...
    //                | forall<real<LIBALE_MAX_DIM>> | forall<index<LIBALE_MAX_DIM>>
    template <typename TType> bool match_forall(std::unique_ptr<value_node<boolean<0>>>&);
    //  forall<T> = "forall" IDENT "in" value<set<T>> COLON value<boolean<0>>

    // definitions
    template <typename TAtom> bool match_declarator();
    template <unsigned IDim> bool match_any_definition();
    //  any_definition = real_definition<0>
    //                 | integer_definition<0>
    //                 | binary_definition<0>
    //                 | definition<index<0>>
    //                 | definition<boolean<0>>
    //                 | set_definition<real<0>>
    //                 | set_definition<index<0>>
    //                 | set_definition<boolean<0>>
    //                 | expr_definition<real<0>>
    //                 | expr_definition<index<0>>
    //                 | expr_definition<boolean<0>>
    //                 | real_definition<1>
    //                 | integer_definition<1>
    //                 | binary_definition<1>
    //                 | definition<index<1>>
    //                 | definition<boolean<1>>
    //                 | set_definition<real<1>>
    //                 | set_definition<index<1>>
    //                 | set_definition<boolean<1>>
    //                 | ...
    //                 | real_definition<LIBALE_MAX_DIM>
    //                 | integer_definition<LIBALE_MAX_DIM>
    //                 | binary_definition<LIBALE_MAX_DIM>
    //                 | definition<index<LIBALE_MAX_DIM>>
    //                 | definition<boolean<LIBALE_MAX_DIM>>
    //                 | set_definition<real<LIBALE_MAX_DIM>>
    //                 | set_definition<index<LIBALE_MAX_DIM>>
    //                 | set_definition<boolean<LIBALE_MAX_DIM>>
    template <typename TType> bool match_definition();
    //  definition<index<n>> = "index" LBRACK INTEGER ( COMMA INTEGER )*n RBRACK IDENT
    //                         DEFINE ( basic<index<0>> | basic<index<n>> ) SEMICOL
    //  definition<index<0>> = "index" IDENT DEFINE basic<index<0>> SEMICOL
    //  definition<boolean<n>> = "boolean" LBRACK INTEGER ( COMMA INTEGER )*n RBRACK IDENT
    //                           DEFINE ( basic<boolean<0>> | basic<boolean<n>> ) SEMICOL
    //  definition<boolean<0>> = "boolean" IDENT DEFINE basic<boolean<0>> SEMICOL
    template <unsigned IDim> bool match_real_definition();
    //  real_definition<n> = "real" LBRACK INTEGER ( COMMA INTEGER )*n RBRACK IDENT
    //                       ( SEMICOL
    //                       | DEFINE ( basic<real<0>> | basic<real<n>> ) SEMICOL
    //                       | "in" LBRACK basic<real<0>> COMMA basic<real<0>> RBRACK SEMICOL
    //                       | "in" LBRACK basic<real<0>> COMMA basic<real<n>> RBRACK SEMICOL
    //                       | "in" LBRACK basic<real<n>> COMMA basic<real<0>> RBRACK SEMICOL
    //                       | "in" LBRACK basic<real<n>> COMMA basic<real<n>> RBRACK SEMICOL
    //                       )
    //  real_definition<0> = "real" IDENT
    //                       ( SEMICOL
    //                       | DEFINE basic<real<0>> SEMICOL
    //                       | "in" LBRACK basic<real<0>> COMMA basic<real<0>> RBRACK SEMICOL
    //                       )
    template <unsigned IDim> bool match_integer_definition();
    //  integer_definition<n> = "integer" LBRACK INTEGER ( COMMA INTEGER )*n RBRACK IDENT
    //                          ( SEMICOL
    //                          | "in" LBRACK basic<real<0>> COMMA basic<real<0>> RBRACK SEMICOL
    //                          | "in" LBRACK basic<real<0>> COMMA basic<real<n>> RBRACK SEMICOL
    //                          | "in" LBRACK basic<real<n>> COMMA basic<real<0>> RBRACK SEMICOL
    //                          | "in" LBRACK basic<real<n>> COMMA basic<real<n>> RBRACK SEMICOL
    //                          )
    //  integer_definition<n> = "integer" IDENT
    //                          ( SEMICOL
    //                          | "in" LBRACK basic<real<0>> COMMA basic<real<0>> RBRACK SEMICOL
    //                          )
    template <unsigned IDim> bool match_binary_definition();
    //  binary_definition<n> = "binary" LBRACK INTEGER ( COMMA INTEGER )*n RBRACK IDENT SEMICOL
    //  binary_definition<0> = "binary" IDENT SEMICOL
    template <typename TType> bool match_set_definition();
    //  set_definition<T<n>> = "set" LBRACE T LBRACK COLON ( COMMA COLON )*n RBRACK RBRACE IDENT
    //                         ( SEMICOL
    //                         | DEFINE basic<set<T<n>>> SEMICOL
    //                         )
    //  set_definition<T<0>> = "set" IDENT
    //                         ( SEMICOL
    //                         | DEFINE basic<set<T<0>>> SEMICOL
    //                         )
    template <typename TType> bool match_expr_definition();
    //  expr_definition<real<0>> = "real" IDENT DEFINE value<real<0>> SEMICOL
    //  expr_definition<index<0>> = "index" IDENT DEFINE value<index<0>> SEMICOL
    //  expr_definition<boolean<0>> = "boolean" IDENT DEFINE value<boolean<0>> SEMICOL

    // assignments
    template <unsigned IDim> bool match_any_assignment();
    //  any_assignment = assignment<real<0>>
    //                 | assignment<index<0>>
    //                 | assignment<boolean<0>>
    //                 | bound_assignment<0>
    //                 | init_assignment<0>
    //                 | ...
    //                 | assignment<real<LIBALE_MAX_DIM>>
    //                 | assignment<index<LIBALE_MAX_DIM>>
    //                 | assignment<boolean<LIBALE_MAX_DIM>>
    //                 | bound_assignment<LIBALE_MAX_DIM>
    //                 | init_assignment<LIBALE_MAX_DIM>
    template <typename TType> bool match_assignment();
    //  assignment<T<n>> = IDENT LBRACK ( INTEGER | COLON ) ( COMMA ( INTEGER | COLON ) )*n RBRACK
    //                     ASSIGN basic<T<0>> SEMICOL
    //  assignment<T<0>> = IDENT ASSIGN basic<T<0>> SEMICOL
    template <unsigned IDim> bool match_bound_assignment();
    //  bound_assignment<n> = IDENT DOT ( "ub" | "lb" )
    //                        LBRACK ( INTEGER | COLON ) ( COMMA ( INTEGER | COLON ) )*n RBRACK
    //                        ASSIGN basic<real<0>> SEMICOL
    //  bound_assignment<0> = IDENT DOT ( "ub" | "lb" ) ASSIGN basic<real<0>> SEMICOL
    template <unsigned IDim> bool match_init_assignment();
    //  init_assignment<n> = IDENT DOT "init"
    //                       LBRACK ( INTEGER | COLON ) ( COMMA ( INTEGER | COLON ) )*n RBRACK
    //                       ASSIGN basic<real<0>> SEMICOL
    //  init_assignment<0> = IDENT DOT "init" ASSIGN basic<real<0>> SEMICOL

    bool match_value(std::unique_ptr<value_node<real<0>>>&);
    //  value<real<0>> = addition<real<0>>
    bool match_addition(std::unique_ptr<value_node<real<0>>>&);
    //  addition<real<0>> = [MINUS] multiplication<real<0>> ( ( PLUS | MINUS ) multiplication<real<0>> )*
    bool match_multiplication(std::unique_ptr<value_node<real<0>>>&);
    //  multiplication<real<0>> = exponentiation ( ( STAR | SLASH ) exponentiation )*
    bool match_exponentiation(std::unique_ptr<value_node<real<0>>>&);
    //  exponentiation = unary<real<0>> ( HAT unary<real<0>> )*
    bool match_unary(std::unique_ptr<value_node<real<0>>>&);
    //  unary<real<0>> = primary<real<0>>
    bool match_primary(std::unique_ptr<value_node<real<0>>>&);
    //  primary<real<0>> = constant<real<0>>
    //                   | parameter<real<0>>
    //                   | unary_function
    //                   | binary_function
    //                   | ternary_function
    //                   | quaternary_function
    //                   | quinary_function
    //                   | senary_function
    //                   | septenary_function
    //                   | octonary_function
    //                   | novenary_function
    //                   | unodenary_function
    //                   | nary_function
    //                   | any_sum
    //                   | any_set_min
    //                   | any_set_max
    //                   | grouping<real<0>>
    //                   | entry<real<0>>
    bool match_unary_function(std::unique_ptr<value_node<real<0>>>&);
    //  unary_dunction = FUNCTION_NAME grouping<real<0>>
    bool match_binary_function(std::unique_ptr<value_node<real<0>>>&);
    bool match_ternary_function(std::unique_ptr<value_node<real<0>>>&);
    bool match_quaternary_function(std::unique_ptr<value_node<real<0>>>&);
    bool match_quinary_function(std::unique_ptr<value_node<real<0>>>&);
    bool match_senary_function(std::unique_ptr<value_node<real<0>>>&);
    bool match_septenary_function(std::unique_ptr<value_node<real<0>>>&);
    bool match_octonary_function(std::unique_ptr<value_node<real<0>>>&);
    bool match_novenary_function(std::unique_ptr<value_node<real<0>>>&);
    bool match_unodenary_function(std::unique_ptr<value_node<real<0>>>&);
    //  LET k BE THE NUMBER OF ARGUMENTS
    //  kary_function = FUNCTION_NAME LPAREN value<real<0>> ( COMMA value<real<0>> )*k RPAREN

    bool match_nary_function(std::unique_ptr<value_node<real<0>>>&);
    //  nary_function = min
    //                | max
    //                | sum_div
    //                | xlog_sum
    bool match_min(std::unique_ptr<value_node<real<0>>>&);
    //  min = "min" LPAREN value<real<0>> ( COMMA value<real<0>> )* RPAREN
    bool match_max(std::unique_ptr<value_node<real<0>>>&);
    //  max = "max" LPAREN value<real<0>> ( COMMA value<real<0>> )* RPAREN
    bool match_sum_div(std::unique_ptr<value_node<real<0>>>&);
    //  sum_div = "sum_div" LPAREN value<real<0>> ( COMMA value<real<0>> )* RPAREN
    bool match_xlog_sum(std::unique_ptr<value_node<real<0>>>&);
    //  xlog_sum = "xlog_sum" LPAREN value<real<0>> ( COMMA value<real<0>> )* RPAREN

    bool match_value(std::unique_ptr<value_node<index<0>>>&);
    //  value<index<0>> = addition<index<0>>
    bool match_addition(std::unique_ptr<value_node<index<0>>>&);
    //  addition<index<0>> = [MINUS] multiplication<index<0>> ( ( PLUS | MINUS ) multiplication<index<0>> )*
    bool match_multiplication(std::unique_ptr<value_node<index<0>>>&);
    //  multiplication<index<0>> = unary<index<0>> ( STAR unary<index<0>> )*
    bool match_unary(std::unique_ptr<value_node<index<0>>>&);
    //  unary<index<0>> = primary<index<0>>
    bool match_primary(std::unique_ptr<value_node<index<0>>>&);
    //  primary<index<0>> = constant<index<0>>
    //                    | parameter<index<0>>
    //                    | grouping<index<0>>
    //                    | entry<index<0>>

    bool match_value(std::unique_ptr<value_node<boolean<0>>>&);
    //  value<boolean<0>> = disjunction
    bool match_disjunction(std::unique_ptr<value_node<boolean<0>>>&);
    //  disjunction = conjunction ( PIPE conjunction )*
    bool match_conjunction(std::unique_ptr<value_node<boolean<0>>>&);
    //  conjunction = unary<boolean<0>> ( AND unary<boolean<0>> )*
    bool match_unary(std::unique_ptr<value_node<boolean<0>>>&);
    //  unary<boolean<0>> = negation
    //                    | primary<boolean<0>>
    bool match_negation(std::unique_ptr<value_node<boolean<0>>>&);
    //  negation = BANG unary<boolean<0>>
    bool match_primary(std::unique_ptr<value_node<boolean<0>>>&);
    //  primary<boolean<0>> = constant<boolean<0>>
    //                      | parameter<boolean<0>>
    //                      | comparison<real<0>>
    //                      | comparison<index<0>>
    //                      | element
    //                      | any_quantifier
    //                      | grouping<boolean<0>>
    bool match_element(std::unique_ptr<value_node<boolean<0>>>&);
    //  element = value<real<0>> "in" value<set<real<0>>>

    bool match_primary(std::unique_ptr<value_node<set<real<0>, 0>>>&);
    //  primary<set<real<0>>> = constant<set<real<0>>>
    //                        | parameter<set<real<0>>>
    //                        | entry<set<real<0>>>
    //                        | indicator_set<set<real<0>>>

    bool match_primary(std::unique_ptr<value_node<set<index<0>, 0>>>&);
    //  primary<set<index<0>>> = constant<set<index<0>>>
    //                        | parameter<set<index<0>>>
    //                        | entry<set<index<0>>>
    //                        | indicator_set<set<index<0>>>

    // token handling
    lexer lex;
    token_buffer buf;

    // error reporting
    void set_expected_token(token::token_type);
    void set_expected_keyword(std::string);
    void set_expected_symbol();
    void set_semantic(std::string);
    void report_empty();
    void report_lexical(token);
    void report_syntactical();

    bool had_error = false;
    std::queue<std::string> errors;
    std::ostream& error_stream;
    // unexpected token
    std::set<std::string> expected;
    token unexpected_token;
    // unexpected symbol
    token unexpected_symbol;
    // semantic issue
    std::string semantic_issue;
    token semantic_token;
};



}

#include "parser.tpp"
