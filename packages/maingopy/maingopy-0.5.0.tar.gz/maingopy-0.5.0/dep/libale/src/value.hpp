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

#include "config.hpp"
#include "helper.hpp"
#include "tensor.hpp"

#include <vector>
#include <list>

namespace ale {



struct base_real {
    using basic_type = double;
    using ref_type = basic_type;
};

struct base_index {
    using basic_type = int;
    using ref_type = basic_type;
};

struct base_boolean {
    using basic_type = bool;
    using ref_type = basic_type;
};

template <typename TElement>
struct base_set {
    template <typename UType>
    using container_type = std::list<UType>;
    using element_type = TElement;
    using basic_type = container_type<typename element_type::basic_type>;
    using ref_type = basic_type&;
};

template <typename TAtom, unsigned IDim>
struct tensor_type {
    using basic_type = tensor<typename TAtom::basic_type, IDim>;
    using ref_type = tensor_ref<typename TAtom::basic_type, IDim>;
    using atom_type = TAtom;
    static const unsigned dim = IDim;
};

template <typename TAtom>
struct tensor_type<TAtom, 0> {
    using basic_type = typename TAtom::basic_type;
    using ref_type = typename TAtom::ref_type;
    using atom_type = TAtom;
    static const unsigned dim = 0;
};

template <typename TType>
using vector_of = tensor_type<typename TType::atom_type, TType::dim + 1>;

template <typename TType>
using entry_of = tensor_type<typename TType::atom_type, TType::dim - 1>;

template <unsigned IDim>
using real = tensor_type<base_real, IDim>;

template <unsigned IDim>
using index = tensor_type<base_index, IDim>;

template <unsigned IDim>
using boolean = tensor_type<base_boolean, IDim>;

template <typename TAtom, unsigned IDim>
struct tensor_pack {
    using type =
    typename combined_pack<
        typename tensor_pack<TAtom, IDim - 1>::type,
        pack<tensor_type<TAtom, IDim>>
    >::type;
};

template <typename TAtom>
struct tensor_pack<TAtom, 0> {
    using type = pack<tensor_type<TAtom, 0>>;
};

using real_types = typename tensor_pack<base_real, LIBALE_MAX_DIM>::type;
using index_types = typename tensor_pack<base_index, LIBALE_MAX_DIM>::type;
using boolean_types = typename tensor_pack<base_boolean, LIBALE_MAX_DIM>::type;

template <typename TElement, unsigned IDim>
using set = tensor_type<base_set<TElement>, IDim>;

// IDim = (outer) set dimension
// JDim = (inner) element dimension
// Returns all tensors (IDim) of sets of tensors (0 .. JDim)
template <typename TAtom, unsigned IDim, unsigned JDim>
struct element_pack {
    using type =
    typename combined_pack<
        typename element_pack<TAtom, IDim, JDim - 1>::type,
        pack<set<tensor_type<TAtom, JDim>, IDim>>
    >::type;
};

template <typename TAtom, unsigned IDim>
struct element_pack<TAtom, IDim, 0> {
    using type = pack<set<tensor_type<TAtom, 0>, IDim>>;
};

template <typename TAtom, unsigned IDim, unsigned JDim>
struct set_pack {
    using type =
    typename combined_pack<
        typename set_pack<TAtom, IDim - 1, JDim>::type,
        typename element_pack<TAtom, IDim, JDim>::type
    >::type;
};

template <typename TAtom, unsigned JDim>
struct set_pack<TAtom, 0, JDim> {
    using type = typename element_pack<TAtom, 0, JDim>::type;
};

using real_set_types = typename set_pack<base_real, LIBALE_MAX_SET_DIM, LIBALE_MAX_DIM>::type;
using index_set_types = typename set_pack<base_index, LIBALE_MAX_SET_DIM, LIBALE_MAX_DIM>::type;
using boolean_set_types = typename set_pack<base_boolean, LIBALE_MAX_SET_DIM, LIBALE_MAX_DIM>::type;



}
