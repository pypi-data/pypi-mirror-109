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
#include "symbol_printer.hpp"

#include <memory>
#include <stack>
#include <set>
#include <unordered_map>
#include <list>

namespace ale {



class symbol_stack;

class symbol_scope {
public:
    ~symbol_scope();
    void push(symbol_stack* stk) {
        definitions.insert(stk);
    }
private:
    std::set<symbol_stack*> definitions;
};

class symbol_stack {
public:
    base_symbol* top() {
        return bindings.top().second.get();
    }

    void push(base_symbol* sym, symbol_scope* scope) {
        if (bindings.size() > 0) {
            auto& bind = bindings.top();
            if (bind.first == scope) {
                bind.second.reset(sym);
                return;
            }
        }
        bindings.emplace(scope, sym);
        scope->push(this);
    }

    void pop() {
        bindings.pop();
    }

    void print () {
        if (bindings.size() > 0) {
            symbol_printer vis;
            vis.dispatch(top());
            return;
        }
        std::cout << "no definition" << std::endl;
    }

    bool empty() {
        return bindings.empty();
    }
private:
    std::stack<std::pair<symbol_scope*, std::unique_ptr<base_symbol>>> bindings;
};

inline symbol_scope::~symbol_scope() {
    for (auto it = definitions.begin(); it != definitions.end(); ++it) {
        (*it)->pop();
    }
}

struct symbol_table {
public:
    symbol_table() {
        push_scope();
    }

    void push_scope() {
        scope_stack.emplace();
    }

    void pop_scope() {
        // cant pop global scope
        if (scope_stack.size() > 1) {
            scope_stack.pop();
        }
    }

    template <typename TType>
    void define(std::string name, value_symbol<TType>* sym) {
        auto it = symbol_store.find(name);
        if (it != symbol_store.end()) {
            it->second.push(sym, &scope_stack.top());
        }
        else {
            symbol_names.push_back(name);
            symbol_store[name].push(sym, &scope_stack.top());
        }
    }

    void define(std::string name, base_symbol* sym) {
        auto it = symbol_store.find(name);
        if (it != symbol_store.end()) {
            it->second.push(sym, &scope_stack.top());
        }
        else {
            symbol_names.push_back(name);
            symbol_store[name].push(sym, &scope_stack.top());
        }
    }

    template <typename TType>
    value_symbol<TType>* resolve(std::string name) {
        auto it = symbol_store.find(name);
        if (it == symbol_store.end()) {
            return nullptr;
        }
        if (it->second.empty()) {
            return nullptr;
        }
        symbol_caster<TType> vis;
        return vis.dispatch(it->second.top());
    }

    base_symbol* resolve(std::string name) {
        auto it = symbol_store.find(name);
        if (it == symbol_store.end()) {
            return nullptr;
        }
        if (it->second.empty()) {
            return nullptr;
        }
        return it->second.top();
    }

    void print_all() {
        for (auto it = symbol_store.begin(); it != symbol_store.end(); ++it)
        {
            std::cout << "symbol " << it->first << ": ";
            it->second.print();
        }
    }

    const std::list<std::string>& get_names() {
        return symbol_names;
    }
private:
    std::unordered_map<std::string, symbol_stack> symbol_store;
    std::stack<symbol_scope> scope_stack;
    std::list<std::string> symbol_names;
};



}
