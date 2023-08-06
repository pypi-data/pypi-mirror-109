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

namespace ale {



// parser rules
// helper rules
template <typename... TRest>
bool parser::check_any(token::token_type expect, TRest... rest) {
    if (check(expect)) {
        return true;
    }
    return check_any(rest...);
}

template <>
inline bool parser::check_any(token::token_type expect) {
    return check(expect);
}

template <typename... TTypes>
bool parser::match_any(TTypes... types) {
    if (check_any(types...)) {
        buf.consume();
        return true;
    }
    return false;
}

template <typename... TRest>
bool parser::check_any_keyword(const std::string& expect, const TRest&... rest) {
    if (check_keyword(expect)) {
        return true;
    }
    return check_any_keyword(rest...);
}

template <>
inline bool parser::check_any_keyword(const std::string& expect) {
    return check_keyword(expect);
}

template <typename TType>
bool parser::exists(std::string name) {
    if (symbols.resolve<TType>(name)) {
        return true;
    }
    set_expected_symbol();
    return false;
}

inline bool parser::available(std::string name) {
    if (symbols.resolve(name)) {
        return false;
    }
    return true;
}



// entry points
template <typename TType>
bool parser::match_expression(std::unique_ptr<value_node<TType>>& result) {
    init();
    if (!match_value(result)) {
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    return accept();
}

template <typename TType>
bool parser::match_expression(std::unique_ptr<value_node<TType>>& result, std::string& lit) {
    init();
    if (!match_value(result)) {
        return reject();
    }
    if (!match_literal(lit)) {
        lit = "";
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    return accept();
}


// generic dispatch
template <typename TType>
bool parser::match_value(std::unique_ptr<value_node<TType>>& result){
    init();
    if (match_primary(result)) {
        return accept();
    }
    return reject();
}



// generic primary tensor
template <typename TType>
bool parser::match_primary(std::unique_ptr<value_node<TType>>& result) {
    init();
    if (match_constant(result)) {
        return accept();
    }
    if (match_parameter(result)) {
        return accept();
    }
    return reject();
}



// generic primary set
template <typename TType>
bool parser::match_primary(std::unique_ptr<value_node<set<TType, 0>>>& result) {
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
    return reject();
}



// generic primary alternatives
template <typename TType>
bool parser::match_constant(std::unique_ptr<value_node<TType>>& result) {
    init();
    typename value_node<TType>::basic_type value;
    if (match_basic<TType>(value)) {
        result.reset(new constant_node<TType>(value));
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_parameter(std::unique_ptr<value_node<TType>>& result) {
    init();
    std::string name;
    if (check(token::IDENT)) {
        name = current().lexeme;
        std::string name = current().lexeme;
        if (exists<TType>(name)) {
            consume();
            result.reset(new parameter_node<TType>(name));
            return accept();
        }
    }
    return reject();
}


template <typename TType>
bool parser::match_partial_entry(std::unique_ptr<value_node<TType>>& result) {
    init();
    std::unique_ptr<value_node<vector_of<TType>>> first_child;
    if (match_partial_entry(first_child)) {
        std::unique_ptr<value_node<index<0>>> second_child;
        if (!match_value(second_child)) {
            return reject();
        }
        if (!match(token::COMMA)) {
            return reject();
        }
        result.reset(new entry_node<TType>(first_child.release(), second_child.release()));
        return accept();
    }
    if (match_value(first_child)) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        std::unique_ptr<value_node<index<0>>> second_child;
        if (!match_value(second_child)) {
            return reject();
        }
        if (!match(token::COMMA)) {
            return reject();
        }
        result.reset(new entry_node<TType>(first_child.release(), second_child.release()));
        return accept();
    }
    return reject();
}

template <typename TAtom>
bool parser::match_partial_entry(std::unique_ptr<value_node<tensor_type<TAtom, LIBALE_MAX_DIM - 1>>>& result) {
    using TType = tensor_type<TAtom, LIBALE_MAX_DIM - 1>;
    init();
    std::unique_ptr<value_node<vector_of<TType>>> first_child;
    if (match_value(first_child)) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        std::unique_ptr<value_node<index<0>>> second_child;
        if (!match_value(second_child)) {
            return reject();
        }
        if (!match(token::COMMA)) {
            return reject();
        }
        result.reset(new entry_node<TType>(first_child.release(), second_child.release()));
        return accept();
    }
    return reject();
}

template <typename TAtom>
bool parser::match_partial_entry(std::unique_ptr<value_node<set<TAtom, LIBALE_MAX_SET_DIM - 1>>>& result) {
    using TType = set<TAtom, LIBALE_MAX_SET_DIM - 1>;
    init();
    std::unique_ptr<value_node<vector_of<TType>>> first_child;
    if (match_value(first_child)) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        std::unique_ptr<value_node<index<0>>> second_child;
        if (!match_value(second_child)) {
            return reject();
        }
        if (!match(token::COMMA)) {
            return reject();
        }
        result.reset(new entry_node<TType>(first_child.release(), second_child.release()));
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_entry(std::unique_ptr<value_node<TType>>& result) {
    init();
    std::unique_ptr<value_node<vector_of<TType>>> first_child;
    if (match_partial_entry(first_child)) {
        std::unique_ptr<value_node<index<0>>> second_child;
        if (!match_value(second_child)) {
            return reject();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
        result.reset(new entry_node<TType>(first_child.release(), second_child.release()));
        return accept();
    }
    if (match_value(first_child)) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        std::unique_ptr<value_node<index<0>>> second_child;
        if (!match_value(second_child)) {
            return reject();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
        result.reset(new entry_node<TType>(first_child.release(), second_child.release()));
        return accept();
    }
    return reject();
}

template <typename TAtom>
bool parser::match_entry(std::unique_ptr<value_node<tensor_type<TAtom, LIBALE_MAX_DIM - 1>>>& result) {
    using TType = tensor_type<TAtom, LIBALE_MAX_DIM - 1>;
    init();
    std::unique_ptr<value_node<vector_of<TType>>> first_child;
    if (match_value(first_child)) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        std::unique_ptr<value_node<index<0>>> second_child;
        if (!match_value(second_child)) {
            return reject();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
        result.reset(new entry_node<TType>(first_child.release(), second_child.release()));
        return accept();
    }
    return reject();
}

template <typename TAtom>
bool parser::match_entry(std::unique_ptr<value_node<set<TAtom, LIBALE_MAX_SET_DIM - 1>>>& result) {
    using TType = set<TAtom, LIBALE_MAX_SET_DIM - 1>;
    init();
    std::unique_ptr<value_node<vector_of<TType>>> first_child;
    if (match_value(first_child)) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        std::unique_ptr<value_node<index<0>>> second_child;
        if (!match_value(second_child)) {
            return reject();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
        result.reset(new entry_node<TType>(first_child.release(), second_child.release()));
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_grouping(std::unique_ptr<value_node<TType>>& result) {
    init();
    if (!match(token::LPAREN)) {
        return reject();
    }
    if (!match_value(result)) {
        return reject();
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    return accept();
}



// generic basics
template <typename TAtom, unsigned IDim>
bool parser::match_tensor(typename tensor_type<TAtom, IDim>::basic_type& value) {
    using TType = tensor_type<TAtom, IDim>;
    init();
    if (!match(token::LPAREN)) {
        return reject();
    }
    size_t shape[IDim];
    for (int i = 0; i < IDim; ++i) {
        shape[i] = 0;
    }
    std::vector<typename entry_of<TType>::basic_type> entries;
    typename entry_of<TType>::basic_type ent;
    if (match_basic<tensor_type<TAtom, IDim - 1>>(ent)) {
        entries.push_back(ent);
        for (int i = 1; i < IDim; ++i) {
            shape[i] = ent.shape(i - 1);
        }
        while (match(token::COMMA)) {
            if (!match_basic<tensor_type<TAtom, IDim - 1>>(ent)) {
                return reject();
            }
            for (int i = 1; i < IDim; ++i) {
                if (shape[i] != ent.shape(i - 1)) {
                    return reject();
                }
            }
            entries.push_back(ent);
        }
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    shape[0] = entries.size();
    value.resize(shape);
    for (int i = 0; i < entries.size(); ++i) {
        value[i].assign(entries[i]);
    }
    return accept();
}

template <typename TAtom>
bool parser::match_vector(typename tensor_type<TAtom, 1>::basic_type& value) {
    using TType = tensor_type<TAtom, 1>;
    init();
    if (!match(token::LPAREN)) {
        return reject();
    }
    std::vector<typename entry_of<TType>::basic_type> entries;
    typename entry_of<TType>::basic_type ent;
    if (match_basic<tensor_type<TAtom, 0>>(ent)) {
        entries.push_back(ent);
        while (match(token::COMMA)) {
            if (!match_basic<tensor_type<TAtom, 0>>(ent)) {
                return reject();
            }
            entries.push_back(ent);
        }
    }
    if (!match(token::RPAREN)) {
        return reject();
    }
    value.resize({entries.size()});
    for (int i = 0; i < entries.size(); ++i) {
        value[i] = entries[i];
    }
    return accept();
}

template <typename TAtom>
bool parser::match_set(typename set<TAtom, 0>::basic_type& value) {
    init();
    if (!match(token::LBRACE)) {
        return reject();
    }
    typename TAtom::basic_type elem;
    typename set<TAtom, 0>::basic_type elements;
    if (match_basic<TAtom>(elem)) {
        elements.push_back(elem);
        while(match(token::COMMA)) {
            if (!match_basic<TAtom>(elem)) {
                return reject();
            }
            elements.push_back(elem);
        }
    }
    if (!match(token::RBRACE)) {
        return reject();
    }
    value = elements;
    return accept();
}


template <typename TAtom>
bool parser::match_sequence(typename set<TAtom, 0>::basic_type&) {
    return false;
}

template <>
inline bool parser::match_sequence<index<0>>(typename set<index<0>, 0>::basic_type& value) {
    init();
    if (!match(token::LBRACE)) {
        return reject();
    }
    typename index<0>::basic_type first;
    if (!match_basic<index<0>>(first)) {
        return reject();
    }
    if (!match(token::DOTS)) {
        return reject();
    }
    typename index<0>::basic_type last;
    if (!match_basic<index<0>>(last)) {
        return reject();
    }
    if (first > last) {
        set_semantic("ERROR: Index sequence with negative increment");
        return reject();
    }
    if (!match(token::RBRACE)) {
        return reject();
    }
    value.clear();
    for (int i = first; i <= last; ++i) {
        value.push_back(i);
    }
    return accept();
}

// tag dispatch overloads for match_basic
template <typename TAtom, unsigned IDim>
bool parser::match_basic(typename tensor_type<TAtom, IDim>::basic_type& value, basic_tag<tensor_type<TAtom, IDim>>) {
    return match_tensor<TAtom, IDim>(value);
}

template <typename TAtom>
bool parser::match_basic(typename tensor_type<TAtom, 1>::basic_type& value, basic_tag<tensor_type<TAtom, 1>>) {
    return match_vector<TAtom>(value);
}

template <typename TAtom>
bool parser::match_basic(typename set<TAtom, 0>::basic_type& value, basic_tag<set<TAtom, 0>>) {
    return match_set<TAtom>(value);
}

template <>
inline bool parser::match_basic<index<0>>(typename set<index<0>, 0>::basic_type& value, basic_tag<set<index<0>, 0>>) {
    init();
    if (match_set<index<0>>(value)) {
        return accept();
    }
    if (match_sequence<index<0>>(value)) {
        return accept();
    }
    return reject();
}

inline bool parser::match_basic(typename real<0>::basic_type& value, basic_tag<real<0>>) {
    init();
    bool negative = false;
    if (match(token::MINUS)) {
        negative = true;
    }
    if (check_any(token::NUMBER, token::INTEGER)) {
        value = std::stod(current().lexeme);
        consume();
        if (negative) {
            value = - value;
        }
        return accept();
    }
    return reject();
}

inline bool parser::match_basic(typename index<0>::basic_type& value, basic_tag<index<0>>) {
    init();
    if (check_any(token::INTEGER)) {
        value = std::stoi(current().lexeme);
        consume();
        return accept();
    }
    return reject();
}

inline bool parser::match_basic(typename boolean<0>::basic_type& value, basic_tag<boolean<0>>) {
    init();
    if (match_keyword("true")) {
        value = true;
        return accept();
    }
    if (match_keyword("false")) {
        value = false;
        return accept();
    }
    return reject();
}

// template call to tag dispatch overloads
template <typename TType>
bool parser::match_basic(typename TType::basic_type& value) {
    return match_basic(value, basic_tag<TType>{});
}



template <unsigned IDim>
bool parser::match_any_sum(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_any_sum<IDim - 1>(result)) {
        return accept();
    }
    if (match_sum<index<IDim>>(result)) {
        return accept();
    }
    if (match_sum<real<IDim>>(result)) {
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_any_sum<0>(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_sum<index<0>>(result)) {
        return accept();
    }
    if (match_sum<real<0>>(result)) {
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_sum(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!match_keyword("sum")) {
        return reject();
    }
    if (!match(token::LPAREN)) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match_keyword("in")) {
        return reject();
    }
    std::unique_ptr<value_node<set<TType, 0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COLON)) {
        return reject();
    }
    symbols.push_scope();
    symbols.define(name, new parameter_symbol<TType>(name));
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        symbols.pop_scope();
        return reject();
    }
    if (!match(token::RPAREN)) {
        symbols.pop_scope();
        return reject();
    }
    result.reset(new sum_node<TType>(name, first_child.release(), second_child.release()));
    symbols.pop_scope();
    return accept();
}

template <unsigned IDim>
bool parser::match_any_set_min(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_any_set_min<IDim - 1>(result)) {
        return accept();
    }
    if (match_set_min<index<IDim>>(result)) {
        return accept();
    }
    if (match_set_min<real<IDim>>(result)) {
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_any_set_min<0>(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_set_min<index<0>>(result)) {
        return accept();
    }
    if (match_set_min<real<0>>(result)) {
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_set_min(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!match_keyword("min")) {
        return reject();
    }
    if (!match(token::LPAREN)) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match_keyword("in")) {
        return reject();
    }
    std::unique_ptr<value_node<set<TType, 0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COLON)) {
        return reject();
    }
    symbols.push_scope();
    symbols.define(name, new parameter_symbol<TType>(name));
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        symbols.pop_scope();
        return reject();
    }
    if (!match(token::RPAREN)) {
        symbols.pop_scope();
        return reject();
    }
    result.reset(new set_min_node<TType>(name, first_child.release(), second_child.release()));
    symbols.pop_scope();
    return accept();
}

template <unsigned IDim>
bool parser::match_any_set_max(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_any_set_max<IDim - 1>(result)) {
        return accept();
    }
    if (match_set_max<index<IDim>>(result)) {
        return accept();
    }
    if (match_set_max<real<IDim>>(result)) {
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_any_set_max<0>(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (match_set_max<index<0>>(result)) {
        return accept();
    }
    if (match_set_max<real<0>>(result)) {
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_set_max(std::unique_ptr<value_node<real<0>>>& result) {
    init();
    if (!match_keyword("max")) {
        return reject();
    }
    if (!match(token::LPAREN)) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match_keyword("in")) {
        return reject();
    }
    std::unique_ptr<value_node<set<TType, 0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COLON)) {
        return reject();
    }
    symbols.push_scope();
    symbols.define(name, new parameter_symbol<TType>(name));
    std::unique_ptr<value_node<real<0>>> second_child;
    if (!match_value(second_child)) {
        symbols.pop_scope();
        return reject();
    }
    if (!match(token::RPAREN)) {
        symbols.pop_scope();
        return reject();
    }
    result.reset(new set_max_node<TType>(name, first_child.release(), second_child.release()));
    symbols.pop_scope();
    return accept();
}

template <typename TType>
bool parser::match_comparison(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    std::unique_ptr<value_node<TType>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!check_any(token::EQUAL, token::LESS, token::LEQUAL, token::GREATER, token::GEQUAL)) {
        return reject();
    }
    token::token_type type = current().type;
    consume();
    std::unique_ptr<value_node<TType>> second_child;
    if (!match_value(second_child)) {
        return reject();
    }
    switch (type) {
        case token::EQUAL:
            result.reset(new equal_node<TType>(first_child.release(), second_child.release()));
            return accept();
        case token::LESS:
            result.reset(new less_node<TType>(first_child.release(), second_child.release()));
            return accept();
        case token::LEQUAL:
            result.reset(new less_equal_node<TType>(first_child.release(), second_child.release()));
            return accept();
        case token::GREATER:
            result.reset(new greater_node<TType>(first_child.release(), second_child.release()));
            return accept();
        case token::GEQUAL:
            result.reset(new greater_equal_node<TType>(first_child.release(), second_child.release()));
            return accept();
        default:
            return reject();
    }
}

template <unsigned IDim>
bool parser::match_any_quantifier(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    if (match_any_quantifier<IDim - 1>(result)) {
        return accept();
    }
    if (match_forall<index<IDim>>(result)) {
        return accept();
    }
    if (match_forall<real<IDim>>(result)) {
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_any_quantifier<0>(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    if (match_forall<index<0>>(result)) {
        return accept();
    }
    if (match_forall<real<0>>(result)) {
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_forall(std::unique_ptr<value_node<boolean<0>>>& result) {
    init();
    if (!match_keyword("forall")) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match_keyword("in")) {
        return reject();
    }
    std::unique_ptr<value_node<set<TType, 0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COLON)) {
        return reject();
    }
    symbols.push_scope();
    symbols.define(name, new parameter_symbol<TType>(name));
    std::unique_ptr<value_node<boolean<0>>> second_child;
    if (!match_value(second_child)) {
        symbols.pop_scope();
        return reject();
    }
    result.reset(new forall_node<TType>(name, first_child.release(), second_child.release()));
    symbols.pop_scope();
    return accept();
}

template <typename TType>
bool parser::match_indicator_set(std::unique_ptr<value_node<set<TType, 0>>>& result) {
    init();
    if (!match(token::LBRACE)) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match_keyword("in")) {
        return reject();
    }
    std::unique_ptr<value_node<set<TType, 0>>> first_child;
    if (!match_value(first_child)) {
        return reject();
    }
    if (!match(token::COLON)) {
        return reject();
    }
    symbols.push_scope();
    symbols.define(name, new parameter_symbol<TType>(name));
    std::unique_ptr<value_node<boolean<0>>> second_child;
    if (!match_value(second_child)) {
        symbols.pop_scope();
        return reject();
    }
    if (!match(token::RBRACE)) {
        symbols.pop_scope();
        return reject();
    }
    result.reset(new indicator_set_node<TType>(name, first_child.release(), second_child.release()));
    symbols.pop_scope();
    return accept();
}

template <>
inline bool parser::match_declarator<base_real>() {
    init();
    if (match_keyword("real")) {
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_declarator<base_index>() {
    init();
    if (match_keyword("index")) {
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_declarator<base_boolean>() {
    init();
    if (match_keyword("boolean")) {
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_definition() {
    init();
    if (!match_declarator<typename TType::atom_type>()) {
        return reject();
    }
    size_t shape[TType::dim];
    if (TType::dim > 0) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        for (int i = 0; i < TType::dim; ++i) {
            if (i > 0 && !match(token::COMMA)) {
                return reject();
            }
            if (!check(token::INTEGER)) {
                return reject();
            }
            shape[i] = std::stoi(current().lexeme);
            consume();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match(token::DEFINE)) {
        return reject();
    }
    typename TType::atom_type::basic_type scalar_init;
    if (TType::dim > 0 && match_basic<tensor_type<typename TType::atom_type, 0>>(scalar_init)) {
        typename TType::basic_type value(shape, scalar_init);
        if (!match_any(token::SEMICOL, token::END)) {
            return reject();
        }
        symbols.define(name, new parameter_symbol<TType>(name, value));
        return accept();
    }
    typename TType::basic_type value;
    if (!match_basic<TType>(value)) {
        return reject();
    }
    for (int i = 0; i < TType::dim; ++i) {
        if (shape[i] != value.shape(i)) {
            set_semantic("ERROR: Symbol defined with different shape than declared");
            return reject();
        }
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    symbols.define(name, new parameter_symbol<TType>(name, value));
    return accept();
}

template <>
inline bool parser::match_definition<index<0>>() {
    init();
    if (!match_declarator<typename index<0>::atom_type>()) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match(token::DEFINE)) {
        return reject();
    }
    typename index<0>::basic_type value;
    if (!match_basic<index<0>>(value)) {
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    symbols.define(name, new parameter_symbol<index<0>>(name, value));
    return accept();
}

template <>
inline bool parser::match_definition<boolean<0>>() {
    init();
    if (!match_declarator<typename boolean<0>::atom_type>()) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match(token::DEFINE)) {
        return reject();
    }
    typename boolean<0>::basic_type value;
    if (!match_basic<boolean<0>>(value)) {
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    symbols.define(name, new parameter_symbol<boolean<0>>(name, value));
    return accept();
}

template <unsigned IDim>
bool parser::match_real_definition() {
    init();
    if (!match_keyword("real")) {
        return reject();
    }
    size_t shape[IDim];
    if (IDim > 0) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        for (int i = 0; i < IDim; ++i) {
            if (i > 0 && !match(token::COMMA)) {
                return reject();
            }
            if (!check(token::INTEGER)) {
                return reject();
            }
            shape[i] = std::stoi(current().lexeme);
            consume();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (match_any(token::SEMICOL, token::END)) {
        symbols.define(name, new variable_symbol<real<IDim>>(name, shape));
        return accept();
    }
    if (match(token::DEFINE)) {
        typename real<0>::basic_type scalar_init;
        if (IDim > 0 && match_basic<real<0>>(scalar_init)) {
            using basic_type = typename real<0>::basic_type;
            tensor<basic_type, IDim> value(shape, scalar_init);
            if (!match_any(token::SEMICOL, token::END)) {
                return reject();
            }
            symbols.define(name, new parameter_symbol<real<IDim>>(name, value));
            return accept();
        }
        typename real<IDim>::basic_type value;
        if (!match_basic<real<IDim>>(value)) {
            return reject();
        }
        for (int i = 0; i < IDim; ++i) {
            if (shape[i] != value.shape(i)) {
                set_semantic("ERROR: Symbol defined with different shape than declared");
                return reject();
            }
        }
        if (!match_any(token::SEMICOL, token::END)) {
            return reject();
        }
        symbols.define(name, new parameter_symbol<real<IDim>>(name, value));
        return accept();
    }
    if (match_keyword("in")) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        typename real<IDim>::basic_type lower(shape);
        typename real<0>::basic_type scalar_lower;
        if (IDim > 0 && match_basic<real<0>>(scalar_lower)) {
            using basic_type = typename real<0>::basic_type;
            lower.ref().initialize(scalar_lower);
        }
        else {
            if (!match_basic<real<IDim>>(lower)) {
                return reject();
            }
            for (int i = 0; i < IDim; ++i) {
                if (shape[i] != lower.shape(i)) {
                    set_semantic("ERROR: Symbol defined with different shape than declared");
                    return reject();
                }
            }
        }
        if (!match(token::COMMA)) {
            return reject();
        }
        typename real<IDim>::basic_type upper(shape);
        typename real<0>::basic_type scalar_upper;
        if (IDim > 0 && match_basic<real<0>>(scalar_upper)) {
            using basic_type = typename real<0>::basic_type;
            upper.ref().initialize(scalar_upper);
        }
        else {
            if (!match_basic<real<IDim>>(upper)) {
                return reject();
            }
            for (int i = 0; i < IDim; ++i) {
                if (shape[i] != upper.shape(i)) {
                    set_semantic("ERROR: Symbol defined with different shape than declared");
                    return reject();
                }
            }
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
        if (!match_any(token::SEMICOL, token::END)) {
            return reject();
        }
        symbols.define(name, new variable_symbol<real<IDim>>(name, lower, upper));
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_real_definition<0>() {
    init();
    if (!match_declarator<typename real<0>::atom_type>()) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (match_any(token::SEMICOL, token::END)) {
        symbols.define(name, new variable_symbol<real<0>>(name));
        return accept();
    }
    if (match(token::DEFINE)) {
        typename real<0>::basic_type value;
        if (!match_basic<real<0>>(value)) {
            return reject();
        }
        if (!match_any(token::SEMICOL, token::END)) {
            return reject();
        }
        symbols.define(name, new parameter_symbol<real<0>>(name, value));
        return accept();
    }
    if (match_keyword("in")) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        typename real<0>::basic_type lower;
        if (!match_basic<real<0>>(lower)) {
            return reject();
        }
        if (!match(token::COMMA)) {
            return reject();
        }
        typename real<0>::basic_type upper;
        if (!match_basic<real<0>>(upper)) {
            return reject();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
        if (!match_any(token::SEMICOL, token::END)) {
            return reject();
        }
        symbols.define(name, new variable_symbol<real<0>>(name, lower, upper));
        return accept();
    }
    return reject();
}

template <unsigned IDim>
bool parser::match_integer_definition() {
    init();
    if (!match_keyword("integer")) {
        return reject();
    }
    size_t shape[IDim];
    if (IDim > 0) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        for (int i = 0; i < IDim; ++i) {
            if (i > 0 && !match(token::COMMA)) {
                return reject();
            }
            if (!check(token::INTEGER)) {
                return reject();
            }
            shape[i] = std::stoi(current().lexeme);
            consume();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (match_any(token::SEMICOL, token::END)) {
        symbols.define(name, new variable_symbol<real<IDim>>(name, shape, true));
        return accept();
    }
    if (!match_keyword("in")) {
        return reject();
    }
    if (!match(token::LBRACK)) {
        return reject();
    }
    typename real<IDim>::basic_type lower(shape);
    typename real<0>::basic_type scalar_lower;
    if (IDim > 0 && match_basic<real<0>>(scalar_lower)) {
        using basic_type = typename real<0>::basic_type;
        lower.ref().initialize(scalar_lower);
    }
    else {
        if (!match_basic<real<IDim>>(lower)) {
            return reject();
        }
        for (int i = 0; i < IDim; ++i) {
            if (shape[i] != lower.shape(i)) {
                set_semantic("ERROR: Symbol defined with different shape than declared");
                return reject();
            }
        }
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    typename real<IDim>::basic_type upper(shape);
    typename real<0>::basic_type scalar_upper;
    if (IDim > 0 && match_basic<real<0>>(scalar_upper)) {
        using basic_type = typename real<0>::basic_type;
        upper.ref().initialize(scalar_upper);
    }
    else {
        if (!match_basic<real<IDim>>(upper)) {
            return reject();
        }
        for (int i = 0; i < IDim; ++i) {
            if (shape[i] != upper.shape(i)) {
                set_semantic("ERROR: Symbol defined with different shape than declared");
                return reject();
            }
        }
    }
    if (!match(token::RBRACK)) {
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    symbols.define(name, new variable_symbol<real<IDim>>(name, lower, upper, true));
    return accept();
}

template <>
inline bool parser::match_integer_definition<0>() {
    init();
    if (!match_keyword("integer")) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (match_any(token::SEMICOL, token::END)) {
        symbols.define(name, new variable_symbol<real<0>>(name, true));
        return accept();
    }
    if (!match_keyword("in")) {
        return reject();
    }
    if (!match(token::LBRACK)) {
        return reject();
    }
    typename real<0>::basic_type lower;
    if (!match_basic<real<0>>(lower)) {
        return reject();
    }
    if (!match(token::COMMA)) {
        return reject();
    }
    typename real<0>::basic_type upper;
    if (!match_basic<real<0>>(upper)) {
        return reject();
    }
    if (!match(token::RBRACK)) {
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    symbols.define(name, new variable_symbol<real<0>>(name, lower, upper, true));
    return accept();
}

template <unsigned IDim>
bool parser::match_binary_definition() {
    init();
    if (!match_keyword("binary")) {
        return reject();
    }
    size_t shape[IDim];
    if (IDim > 0) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        for (int i = 0; i < IDim; ++i) {
            if (i > 0 && !match(token::COMMA)) {
                return reject();
            }
            if (!check(token::INTEGER)) {
                return reject();
            }
            shape[i] = std::stoi(current().lexeme);
            consume();
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    typename real<IDim>::basic_type lower(shape, 0);
    typename real<IDim>::basic_type upper(shape, 1);
    symbols.define(name, new variable_symbol<real<IDim>>(name, lower, upper, true));
    return accept();
}

template <>
inline bool parser::match_binary_definition<0>() {
    init();
    if (!match_keyword("binary")) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    symbols.define(name, new variable_symbol<real<0>>(name, 0, 1, true));
    return accept();
}

template <typename TType>
bool parser::match_set_definition() {
    init();
    if (!match_keyword("set")) {
        return reject();
    }
    if (!match(token::LBRACE)) {
        return reject();
    }
    if (!match_declarator<typename TType::atom_type>()) {
        return reject();
    }
    if (TType::dim > 0) {
        if (!match(token::LBRACK)) {
            return reject();
        }
        for (int i = 0; i < TType::dim; ++i) {
            if (i > 0 && !match(token::COMMA)) {
                return reject();
            }
            if (!match(token::COLON)) {
                return reject();
            }
        }
        if (!match(token::RBRACK)) {
            return reject();
        }
    }
    if (!match(token::RBRACE)) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (match_any(token::SEMICOL, token::END)) {
        symbols.define(name, new parameter_symbol<set<TType, 0>>(name));
        return accept();
    }
    if (!match(token::DEFINE)) {
        return reject();
    }
    typename set<TType, 0>::basic_type value;
    if (!match_basic<set<TType, 0>>(value)) {
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    symbols.define(name, new parameter_symbol<set<TType, 0>>(name, value));
    return accept();
}

template <typename TType>
bool parser::match_expr_definition() {
    init();
    if (!match_declarator<typename TType::atom_type>()) {
        return reject();
    }
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    if (!available(name)) {
        set_semantic("ERROR: Symbol declared under occupied name");
        return reject();
    }
    if (!match(token::DEFINE)) {
        return reject();
    }
    std::unique_ptr<value_node<TType>> expr;
    if(!match_value(expr)){
        return reject();
    }
    if (!match_any(token::SEMICOL, token::END)) {
        return reject();
    }
    symbols.define(name, new expression_symbol<TType>(name, expr.release()));
    return accept();
}

template <unsigned IDim>
bool parser::match_any_definition() {
    init();
    if (match_any_definition<IDim - 1>()) {
        return accept();
    }
    if (match_real_definition<IDim>()) {
        return accept();
    }
    if (match_integer_definition<IDim>()) {
        return accept();
    }
    if (match_binary_definition<IDim>()) {
        return accept();
    }
    if (match_definition<index<IDim>>()) {
        return accept();
    }
    if (match_definition<boolean<IDim>>()) {
        return accept();
    }
    if (match_set_definition<real<IDim>>()) {
        return accept();
    }
    if (match_set_definition<index<IDim>>()) {
        return accept();
    }
    if (match_set_definition<boolean<IDim>>()) {
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_any_definition<0>() {
    init();
    if (match_real_definition<0>()) {
        return accept();
    }
    if (match_integer_definition<0>()) {
        return accept();
    }
    if (match_binary_definition<0>()) {
        return accept();
    }
    if (match_definition<index<0>>()) {
        return accept();
    }
    if (match_definition<boolean<0>>()) {
        return accept();
    }
    if (match_set_definition<real<0>>()) {
        return accept();
    }
    if (match_set_definition<index<0>>()) {
        return accept();
    }
    if (match_set_definition<boolean<0>>()) {
        return accept();
    }
    if (match_expr_definition<real<0>>()) {
        return accept();
    }
    if (match_expr_definition<index<0>>()) {
        return accept();
    }
    if (match_expr_definition<boolean<0>>()) {
        return accept();
    }
    return reject();
}

template <typename TType>
bool parser::match_assignment() {
    init();
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    parameter_symbol<TType>* sym = cast_parameter_symbol<TType>(symbols.resolve(name));
    if (!sym) {
        set_semantic("ERROR: Symbol of unexpected type");
        return reject();
    }
    size_t indexes[TType::dim];
    std::vector<size_t> wildcards;
    if (!match(token::LBRACK)) {
        return reject();
    }
    for (int i = 0; i < TType::dim; ++i) {
        if (i > 0 && !match(token::COMMA)) {
            return reject();
        }
        if (check(token::INTEGER)) {
            indexes[i] = std::stoi(current().lexeme) - 1;
            consume();
        }
        else {
            if (!match(token::COLON)) {
                return reject();
            }
            wildcards.push_back(i);
            indexes[i] = 0;
        }
    }
    if (!match(token::RBRACK)) {
        return reject();
    }
    if (!match(token::ASSIGN)) {
        return reject();
    }
    typename TType::atom_type::basic_type value;
    if (!match_basic<tensor_type<typename TType::atom_type, 0>>(value)) {
        return reject();
    }
    if (!match_any(token::END, token::SEMICOL)) {
        return reject();
    }
    for (int i = 0; i < TType::dim; ++i) {
        if (indexes[i] < 0 || indexes[i] >= sym->m_value.shape(i)) {
            set_semantic("ERROR: Assignment with index out of bounds");
            return reject();
        }
    }
    if (wildcards.size() != 0) {
        size_t n = wildcards.size()-1;
        while (indexes[wildcards[n]] < sym->m_value.shape(wildcards[n])) {
            sym->m_value[indexes] = value;
            for (int i = 0; i <= n; ++i) {
                if (++indexes[wildcards[i]] < sym->m_value.shape(wildcards[i])) {
                    break;
                }
                else if (i != n) {
                    indexes[wildcards[i]] = 0;
                }
            }
        }
    }
    else {
        sym->m_value[indexes] = value;
    }
    return accept();
}

template <>
inline bool parser::match_assignment<real<0>>() {
    init();
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    parameter_symbol<real<0>>* sym = cast_parameter_symbol<real<0>>(symbols.resolve(name));
    if (!sym) {
        set_semantic("ERROR: Symbol of unexpected type");
        return reject();
    }
    if (!match(token::ASSIGN) ) {
        return reject();
    }
    real<0>::basic_type value;
    if (!match_basic<real<0>>(value)) {
        return reject();
    }
    if (!match_any(token::END, token::SEMICOL)) {
        return reject();
    }
    sym->m_value = value;
    return accept();
}

template <>
inline bool parser::match_assignment<index<0>>() {
    init();
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    parameter_symbol<index<0>>* sym = cast_parameter_symbol<index<0>>(symbols.resolve(name));
    if (!sym) {
        set_semantic("ERROR: Symbol of unexpected type");
        return reject();
    }
    if (!match(token::ASSIGN) ) {
        return reject();
    }
    index<0>::basic_type value;
    if (!match_basic<index<0>>(value)) {
        return reject();
    }
    if (!match_any(token::END, token::SEMICOL)) {
        return reject();
    }
    sym->m_value = value;
    return accept();
}

template <>
inline bool parser::match_assignment<boolean<0>>() {
    init();
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    parameter_symbol<boolean<0>>* sym = cast_parameter_symbol<boolean<0>>(symbols.resolve(name));
    if (!sym) {
        set_semantic("ERROR: Symbol of unexpected type");
        return reject();
    }
    if (!match(token::ASSIGN) ) {
        return reject();
    }
    boolean<0>::basic_type value;
    if (!match_basic<boolean<0>>(value)) {
        return reject();
    }
    if (!match_any(token::END, token::SEMICOL)) {
        return reject();
    }
    sym->m_value = value;
    return accept();
}

template <unsigned IDim>
bool parser::match_bound_assignment() {
    init();
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    variable_symbol<real<IDim>>* sym = cast_variable_symbol<real<IDim>>(symbols.resolve(name));
    if (!sym) {
        set_semantic("ERROR: Symbol of unexpected type");
        return reject();
    }
    if (!match(token::DOT) ) {
        return reject();
    }
    bool upper = false;
    if (match_keyword("ub")) {
        upper = true;
    }
    else if (!match_keyword("lb")) {
        return reject();
    }
    size_t indexes[IDim];
    std::vector<size_t> wildcards;
    if (!match(token::LBRACK)) {
        return reject();
    }
    for (int i = 0; i < IDim; ++i) {
        if (i > 0 && !match(token::COMMA)) {
            return reject();
        }
        if (check(token::INTEGER)) {
            indexes[i] = std::stoi(current().lexeme) - 1;
            consume();
        }
        else {
            if (!match(token::COLON)) {
                return reject();
            }
            wildcards.push_back(i);
            indexes[i] = 0;
        }
    }
    if (!match(token::RBRACK)) {
        return reject();
    }
    if (!match(token::ASSIGN) ) {
        return reject();
    }
    real<0>::basic_type value;
    if (!match_basic<real<0>>(value)) {
        return reject();
    }
    if (!match_any(token::END, token::SEMICOL)) {
        return reject();
    }
    for (int i = 0; i < IDim; ++i) {
        if (indexes[i] < 0 || indexes[i] >= sym->shape(i)) {
            set_semantic("ERROR: Assignment with index out of bounds");
            return reject();
        }
    }
    if (wildcards.size() != 0) {
        size_t n = wildcards.size()-1;
        while (indexes[wildcards[n]] < sym->shape(wildcards[n])) {
            if (upper) {
                sym->upper()[indexes] = value;
            }
            else {
                sym->lower()[indexes] = value;
            }
            for (int i = 0; i <= n; ++i) {
                if (++indexes[wildcards[i]] < sym->shape(wildcards[i])) {
                    break;
                }
                else if (i != n) {
                    indexes[wildcards[i]] = 0;
                }
            }
        }
    }
    else {
        if (upper) {
            sym->upper()[indexes] = value;
        }
        else {
            sym->lower()[indexes] = value;
        }
    }
    return accept();
}

template <>
inline bool parser::match_bound_assignment<0>() {
    init();
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    variable_symbol<real<0>>* sym = cast_variable_symbol<real<0>>(symbols.resolve(name));
    if (!sym) {
        set_semantic("ERROR: Symbol of unexpected type");
        return reject();
    }
    if (!match(token::DOT) ) {
        return reject();
    }
    bool upper = false;
    if (match_keyword("ub")) {
        upper = true;
    }
    else if (!match_keyword("lb")) {
        return reject();
    }
    if (!match(token::ASSIGN) ) {
        return reject();
    }
    real<0>::basic_type value;
    if (!match_basic<real<0>>(value)) {
        return reject();
    }
    if (!match_any(token::END, token::SEMICOL)) {
        return reject();
    }
    if (upper) {
        sym->upper() = value;
    }
    else {
        sym->lower() = value;
    }
    return accept();
}

template <unsigned IDim>
bool parser::match_init_assignment() {
    init();
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    variable_symbol<real<IDim>>* sym = cast_variable_symbol<real<IDim>>(symbols.resolve(name));
    if (!sym) {
        set_semantic("ERROR: Symbol of unexpected type");
        return reject();
    }
    if (!match(token::DOT) ) {
        return reject();
    }
    if (!match_keyword("init")) {
        return reject();
    }
    size_t indexes[IDim];
    std::vector<size_t> wildcards;
    if (!match(token::LBRACK)) {
        return reject();
    }
    for (int i = 0; i < IDim; ++i) {
        if (i > 0 && !match(token::COMMA)) {
            return reject();
        }
        if (check(token::INTEGER)) {
            indexes[i] = std::stoi(current().lexeme) - 1;
            consume();
        }
        else {
            if (!match(token::COLON)) {
                return reject();
            }
            wildcards.push_back(i);
            indexes[i] = 0;
        }
    }
    if (!match(token::RBRACK)) {
        return reject();
    }
    if (!match(token::ASSIGN) ) {
        return reject();
    }
    real<0>::basic_type value;
    if (!match_basic<real<0>>(value)) {
        return reject();
    }
    if (!match_any(token::END, token::SEMICOL)) {
        return reject();
    }
    for (int i = 0; i < IDim; ++i) {
        if (indexes[i] < 0 || indexes[i] >= sym->shape(i)) {
            set_semantic("ERROR: Assignment with index out of bounds");
            return reject();
        }
    }
    if (wildcards.size() != 0) {
        size_t n = wildcards.size()-1;
        while (indexes[wildcards[n]] < sym->shape(wildcards[n])) {
            sym->init()[indexes] = value;
            for (int i = 0; i <= n; ++i) {
                if (++indexes[wildcards[i]] < sym->shape(wildcards[i])) {
                    break;
                }
                else if (i != n) {
                    indexes[wildcards[i]] = 0;
                }
            }
        }
    }
    else {
        sym->init()[indexes] = value;
    }
    return accept();
}

template <>
inline bool parser::match_init_assignment<0>() {
    init();
    if (!check(token::IDENT)) {
        return reject();
    }
    std::string name = current().lexeme;
    consume();
    variable_symbol<real<0>>* sym = cast_variable_symbol<real<0>>(symbols.resolve(name));
    if (!sym) {
        set_semantic("ERROR: Symbol of unexpected type");
        return reject();
    }
    if (!match(token::DOT) ) {
        return reject();
    }
    if (!match_keyword("init")) {
        return reject();
    }
    if (!match(token::ASSIGN) ) {
        return reject();
    }
    real<0>::basic_type value;
    if (!match_basic<real<0>>(value)) {
        return reject();
    }
    if (!match_any(token::END, token::SEMICOL)) {
        return reject();
    }
    sym->init() = value;
    return accept();
}

template <unsigned IDim>
bool parser::match_any_assignment() {
    init();
    if (match_any_assignment<IDim - 1>()) {
        return accept();
    }
    if (match_assignment<real<IDim>>()) {
        return accept();
    }
    if (match_assignment<index<IDim>>()) {
        return accept();
    }
    if (match_assignment<boolean<IDim>>()) {
        return accept();
    }
    if (match_bound_assignment<IDim>()) {
        return accept();
    }
    if (match_init_assignment<IDim>()) {
        return accept();
    }
    return reject();
}

template <>
inline bool parser::match_any_assignment<0>() {
    init();
    if (match_assignment<real<0>>()) {
        return accept();
    }
    if (match_assignment<index<0>>()) {
        return accept();
    }
    if (match_assignment<boolean<0>>()) {
        return accept();
    }
    if (match_bound_assignment<0>()) {
        return accept();
    }
    if (match_init_assignment<0>()) {
        return accept();
    }
    return reject();
}



}
