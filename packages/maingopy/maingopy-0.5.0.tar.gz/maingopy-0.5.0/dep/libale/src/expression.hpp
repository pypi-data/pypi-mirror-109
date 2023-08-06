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
#include "node.hpp"

namespace ale {



template <typename TType>
class expression {
public:
    expression() : m_root(new constant_node<TType>()), m_note("") {}
    expression(value_node<TType>* root, std::string note = "") : m_root(root), m_note(note) {}
    value_node<TType>* get() {
        return m_root.get();
    }
    void set(value_node<TType>* root) {
        m_root.reset(root);
    }
    std::string m_note;
private:
    value_node_ptr<TType> m_root;
};



}
