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

#include "value.hpp"

#include <limits>
#include <string>
#include <variant>

#include "expression.hpp"

namespace ale {



template <typename TType>
struct value_symbol;

using value_symbol_types = typename combined_pack<
    pointer_pack_from_pack<value_symbol, real_types>::type,
    pointer_pack_from_pack<value_symbol, index_types>::type,
    pointer_pack_from_pack<value_symbol, boolean_types>::type,
    pointer_pack_from_pack<value_symbol, real_set_types>::type,
    pointer_pack_from_pack<value_symbol, index_set_types>::type,
    pointer_pack_from_pack<value_symbol, boolean_set_types>::type
>::type;

struct base_symbol {
    using variant = typename from_pack<std::variant, value_symbol_types>::type;
    virtual ~base_symbol() {};
    virtual variant get_base_variant() = 0;
    virtual base_symbol* clone() = 0;
};

template <typename TType>
struct parameter_symbol;

template <typename TType>
class variable_symbol;

template <typename TType>
struct expression_symbol;

template <typename TType>
struct value_symbol : public base_symbol {
    base_symbol::variant get_base_variant() {
        return static_cast<value_symbol<TType>*>(this);
    }
    using variant = std::variant<parameter_symbol<TType>*>;
    virtual variant get_value_variant() = 0;
};

template <unsigned IDim>
struct value_symbol<real<IDim>> : public base_symbol {
    base_symbol::variant get_base_variant() {
        return static_cast<value_symbol<real<IDim>>*>(this);
    }
    using variant = std::variant<parameter_symbol<real<IDim>>*, variable_symbol<real<IDim>>*>;
    virtual variant get_value_variant() = 0;
};

template <>
struct value_symbol<real<0>> : public base_symbol {
    base_symbol::variant get_base_variant() {
        return static_cast<value_symbol<real<0>>*>(this);
    }
    using variant = std::variant<parameter_symbol<real<0>>*, variable_symbol<real<0>>*, expression_symbol<real<0>>*>;
    virtual variant get_value_variant() = 0;
};

template <>
struct value_symbol<index<0>> : public base_symbol {
    base_symbol::variant get_base_variant() {
        return static_cast<value_symbol<index<0>>*>(this);
    }
    using variant = std::variant<parameter_symbol<index<0>>*, expression_symbol<index<0>>*>;
    virtual variant get_value_variant() = 0;
};

template <>
struct value_symbol<boolean<0>> : public base_symbol {
    base_symbol::variant get_base_variant() {
        return static_cast<value_symbol<boolean<0>>*>(this);
    }
    using variant = std::variant<parameter_symbol<boolean<0>>*, expression_symbol<boolean<0>>*>;
    virtual variant get_value_variant() = 0;
};

template <template<typename> typename TSymbol, typename TType>
struct derived_value_symbol : value_symbol<TType> {
    typename value_symbol<TType>::variant get_value_variant() override {
        return static_cast<TSymbol<TType>*>(this);
    }
    base_symbol* clone() final {
        return new TSymbol<TType>(static_cast<TSymbol<TType>&>(*this));
    }
};

template <typename TType>
struct parameter_symbol : derived_value_symbol<parameter_symbol, TType> {
    using basic_type = typename TType::basic_type;
    parameter_symbol(std::string name) : m_name(name), m_value() {}
    parameter_symbol(std::string name, basic_type value) : m_name(name), m_value(value) {}

    std::string m_name;
    basic_type m_value;
};

template <typename TAtom, unsigned IDim>
struct parameter_symbol<tensor_type<TAtom, IDim>> : derived_value_symbol<parameter_symbol, tensor_type<TAtom, IDim>> {
    using basic_type = typename tensor_type<TAtom, IDim>::basic_type;
    parameter_symbol(std::string name) : m_name(name), m_value() {}
    parameter_symbol(std::string name, size_t shape[IDim]) : m_name(name), m_value(shape) {}
    parameter_symbol(std::string name, std::array<size_t, IDim> shape) : m_name(name), m_value(shape) {}
    explicit parameter_symbol(std::string name, basic_type value) : m_name(name), m_value(value) {}

    std::string m_name;
    basic_type m_value;
};

template <typename TType>
class variable_symbol : public derived_value_symbol<variable_symbol, TType> {
};

template <unsigned IDim>
class variable_symbol<real<IDim>> : public derived_value_symbol<variable_symbol, real<IDim>> {
    using basic_type = typename real<IDim>::basic_type;
    using ref_type = typename real<IDim>::ref_type;
    using scalar_type = typename real<IDim>::atom_type::basic_type;
public:
    variable_symbol(std::string name, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(),
        m_lower(),
        m_upper()
    {}

    variable_symbol(std::string name, size_t shape[IDim], bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(shape, std::numeric_limits<scalar_type>::quiet_NaN()),
        m_lower(shape, - std::numeric_limits<scalar_type>::infinity()),
        m_upper(shape, std::numeric_limits<scalar_type>::infinity())
    {}
    variable_symbol(std::string name, std::array<size_t, IDim> shape, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(shape, std::numeric_limits<scalar_type>::quiet_NaN()),
        m_lower(shape, - std::numeric_limits<scalar_type>::infinity()),
        m_upper(shape, std::numeric_limits<scalar_type>::infinity())
    {}

    variable_symbol(std::string name, size_t shape[IDim], scalar_type init, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(shape, init),
        m_lower(shape, - std::numeric_limits<scalar_type>::infinity()),
        m_upper(shape, std::numeric_limits<scalar_type>::infinity())
    {}
    variable_symbol(std::string name, std::array<size_t, IDim> shape, scalar_type init, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(shape, init),
        m_lower(shape, - std::numeric_limits<scalar_type>::infinity()),
        m_upper(shape, std::numeric_limits<scalar_type>::infinity())
    {}
    variable_symbol(std::string name, size_t shape[IDim], scalar_type lower, scalar_type upper, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(shape, std::numeric_limits<scalar_type>::quiet_NaN()),
        m_lower(shape, lower),
        m_upper(shape, upper)
    {}
    variable_symbol(std::string name, std::array<size_t, IDim> shape, scalar_type lower, scalar_type upper, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(shape, std::numeric_limits<scalar_type>::quiet_NaN()),
        m_lower(shape, lower),
        m_upper(shape, upper)
    {}

    variable_symbol(std::string name, basic_type init, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(init),
        m_lower(init.shape(), - std::numeric_limits<scalar_type>::infinity()),
        m_upper(init.shape(), std::numeric_limits<scalar_type>::infinity())
    {}
    variable_symbol(std::string name, basic_type lower, basic_type upper, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(lower.shape(), std::numeric_limits<scalar_type>::quiet_NaN()),
        m_lower(lower),
        m_upper(upper)
    {
        for (int i = 0; i < IDim; ++i) {
            if (m_lower.shape(i) != m_upper.shape(i)) {
                throw std::invalid_argument("Attempted to construct variable_symbol with differently shaped bounds");
            }
        }
    }

    bool integral() {
        return m_integral;
    }

    ref_type init() {
        return m_init.ref();
    }

    ref_type lower() {
        return m_lower.ref();
    }

    ref_type upper() {
        return m_upper.ref();
    }

    const std::array<size_t, IDim> shape() const {
        return m_init.shape();
    }

    const size_t shape(unsigned dim) const {
        return m_init.shape(dim);
    }

    void resize(std::array<size_t, IDim> shape) {
        m_init.resize(shape, std::numeric_limits<scalar_type>::quiet_NaN());
        m_lower.resize(shape, - std::numeric_limits<scalar_type>::infinity());
        m_upper.resize(shape, std::numeric_limits<scalar_type>::infinity());
    }

    void resize(size_t shape[IDim]) {
        m_init.resize(shape, std::numeric_limits<scalar_type>::quiet_NaN());
        m_lower.resize(shape, - std::numeric_limits<scalar_type>::infinity());
        m_upper.resize(shape, std::numeric_limits<scalar_type>::infinity());
    }

    std::string m_name;
private:
    bool m_integral;

    basic_type m_init;
    basic_type m_lower;
    basic_type m_upper;
};

template <>
class variable_symbol<real<0>> : public derived_value_symbol<variable_symbol, real<0>> {
    using basic_type = typename real<0>::basic_type;
public:
    variable_symbol(std::string name, bool integral = false) :
        m_name(name),
        m_init(std::numeric_limits<basic_type>::quiet_NaN()),
        m_lower(- std::numeric_limits<basic_type>::infinity()),
        m_upper(std::numeric_limits<basic_type>::infinity()),
        m_integral(integral) {}
    variable_symbol(std::string name, size_t shape[0], bool integral = false) :
        variable_symbol(name, integral)
    {}
    variable_symbol(std::string name, std::array<size_t, 0> shape, bool integral = false) :
        variable_symbol(name, integral)
    {}
    variable_symbol(std::string name, basic_type init, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(init),
        m_lower(- std::numeric_limits<basic_type>::infinity()),
        m_upper(std::numeric_limits<basic_type>::infinity())
    {}
    variable_symbol(std::string name, basic_type lower, basic_type upper, bool integral = false) :
        m_name(name),
        m_integral(integral),
        m_init(std::numeric_limits<basic_type>::quiet_NaN()),
        m_lower(lower),
        m_upper(upper)
    {}

    bool integral() {
        return m_integral;
    }

    basic_type& init() {
        return m_init;
    }

    basic_type& lower() {
        return m_lower;
    }

    basic_type& upper() {
        return m_upper;
    }

    std::string m_name;
private:
    bool m_integral;

    basic_type m_init;
    basic_type m_lower;
    basic_type m_upper;
};


template <typename TType>
struct expression_symbol : derived_value_symbol<expression_symbol, TType> {
    using basic_type = typename TType::basic_type;
    expression_symbol(std::string name, value_node<TType>* value) : m_name(name), m_value(value) {}
    std::string m_name;
    value_node_ptr<TType> m_value;
};

template <typename TType>
class symbol_caster {
public:
    value_symbol<TType>* dispatch(base_symbol* sym) {
        if (!sym) {
            return nullptr;
        }
        return std::visit(*this, sym->get_base_variant());
    }

    template <typename UType>
    value_symbol<TType>* operator()(value_symbol<UType>* sym) {
        return nullptr;
    }

    value_symbol<TType>* operator()(value_symbol<TType>* sym) {
        return sym;
    }
};

template <typename TType>
value_symbol<TType>* cast_value_symbol(base_symbol* sym) {
    symbol_caster<TType> cast;
    return cast.dispatch(sym);
}

template <typename TType>
class parameter_symbol_caster {
public:
    parameter_symbol<TType>* dispatch(base_symbol* sym) {
        if (!sym) {
            return nullptr;
        }
        return std::visit(*this, sym->get_base_variant());
    }

    template <typename UType>
    parameter_symbol<TType>* operator()(value_symbol<UType>* sym) {
        // unexpected value type
        return nullptr;
    }

    parameter_symbol<TType>* operator()(value_symbol<TType>* sym) {
        return std::visit(*this, sym->get_value_variant());
    }

    template <template<typename> typename TTemplate>
    parameter_symbol<TType>* operator()(TTemplate<TType>* sym) {
        // not a parameter symbol
        return nullptr;
    }

    parameter_symbol<TType>* operator()(parameter_symbol<TType>* sym) {
        return sym;
    }
};

template <typename TType>
parameter_symbol<TType>* cast_parameter_symbol(base_symbol* sym) {
    parameter_symbol_caster<TType> cast;
    return cast.dispatch(sym);
}

template <typename TType>
class variable_symbol_caster {
public:
    variable_symbol<TType>* dispatch(base_symbol* sym) {
        if (!sym) {
            return nullptr;
        }
        return std::visit(*this, sym->get_base_variant());
    }

    template <typename UType>
    variable_symbol<TType>* operator()(value_symbol<UType>* sym) {
        // unexpected value type
        return nullptr;
    }

    variable_symbol<TType>* operator()(value_symbol<TType>* sym) {
        return std::visit(*this, sym->get_value_variant());
    }

    template <template<typename> typename TTemplate>
    variable_symbol<TType>* operator()(TTemplate<TType>* sym) {
        // not a variable symbol
        return nullptr;
    }

    variable_symbol<TType>* operator()(variable_symbol<TType>* sym) {
        return sym;
    }
};

template <typename TType>
variable_symbol<TType>* cast_variable_symbol(base_symbol* sym) {
    variable_symbol_caster<TType> cast;
    return cast.dispatch(sym);
}



}
