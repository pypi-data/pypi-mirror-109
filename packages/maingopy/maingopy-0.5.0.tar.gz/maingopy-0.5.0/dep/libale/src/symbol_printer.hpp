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

#include "symbol.hpp"

#include <iostream>
#include <sstream>

namespace ale {



class symbol_printer {
public:
    void dispatch(base_symbol* sym) {
        return std::visit(*this, sym->get_base_variant());
    }

    template <typename TType>
    void operator()(value_symbol<TType>* sym) {
        return std::visit(*this, sym->get_value_variant());
    }

    template <unsigned IDim>
    void operator()(parameter_symbol<real<IDim>>* sym) {
        std::cout << "real[" << sym->m_value.shape(0);
        for (int i = 1; i < IDim; ++i) {
            std::cout << "," << sym->m_value.shape(i);
        }
        std::cout << "] symbol " << sym->m_name;
        std::cout << " with value " << tensor_string(sym->m_value);
        std::cout << '\n';
    }

    void operator()(parameter_symbol<real<0>>* sym) {
        std::cout << "real symbol " << sym->m_name;
        std::cout << " with value " << sym->m_value;
        std::cout << '\n';
    }

    template <unsigned IDim>
    void operator()(parameter_symbol<index<IDim>>* sym) {
        std::cout << "index["  << sym->m_value.shape(0);
        for (int i = 1; i < IDim; ++i) {
            std::cout << "," << sym->m_value.shape(i);
        }
        std::cout << "] symbol " << sym->m_name;
        std::cout << " with value " << tensor_string(sym->m_value);
        std::cout << '\n';
    }

    void operator()(parameter_symbol<index<0>>* sym) {
        std::cout << "index symbol " << sym->m_name;
        std::cout << " with value " << sym->m_value;
        std::cout << '\n';
    }

    template <unsigned IDim>
    void operator()(parameter_symbol<boolean<IDim>>* sym) {
        std::cout << "boolean[" << sym->m_value.shape(0);
        for (int i = 1; i < IDim; ++i) {
            std::cout << "," << sym->m_value.shape(i);
        }
        std::cout << "] symbol " << sym->m_name;
        std::cout << " with value " << tensor_string(sym->m_value);
        std::cout << '\n';
    }

    void operator()(parameter_symbol<boolean<0>>* sym) {
        std::cout << "boolean symbol " << sym->m_name;
        std::cout << " with value " << sym->m_value;
        std::cout << '\n';
    }

    template <typename TType, unsigned IDim>
    void operator()(parameter_symbol<set<TType, IDim>>* sym) {
        std::cout << "set symbol " << sym->m_name << '\n';
    }

    template <unsigned IDim>
    void operator()(variable_symbol<real<IDim>>* sym) {
        std::cout << "real[" << sym->shape(0);
        for (int i = 1; i < IDim; ++i) {
            std::cout << "," << sym->shape(i);
        }
        std::cout << "] symbol " << sym->m_name;
        std::cout << " in [" << tensor_string(sym->lower()) << ',';
        std::cout << tensor_string(sym->upper());
        std::cout << "] and init " << tensor_string(sym->init());
        std::cout << '\n';
    }

    void operator()(variable_symbol<real<0>>* sym) {
        std::cout << "real symbol " << sym->m_name;
        std::cout << " in [" << sym->lower() << ',';
        std::cout << sym->upper();
        std::cout << "] and init " << sym->init();
        std::cout << '\n';
    }

    void operator()(expression_symbol<real<0>>* sym) {
        std::cout << "real expression symbol " << sym->m_name << '\n';
    }

    void operator()(expression_symbol<boolean<0>>* sym) {
        std::cout << "boolean expression symbol " << sym->m_name << '\n';
    }

    void operator()(expression_symbol<index<0>>* sym) {
        std::cout << "index expression symbol " << sym->m_name << '\n';
    }

};



}
