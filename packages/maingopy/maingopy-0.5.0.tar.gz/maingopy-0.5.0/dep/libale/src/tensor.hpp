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

#include <cstddef>
#include <assert.h>
#include <exception>
#include <array>
#include <algorithm>
#include <sstream>
#include <iostream>

namespace ale {



template  <typename TType, unsigned IDim>
class tensor;

template <typename TType, unsigned IDim>
class tensor_ref {
public:
    tensor_ref<TType, IDim - 1> operator[](size_t index) {
        assert(index < m_shape[0]);
        return tensor_ref<TType, IDim - 1>(&m_data[index * m_subsizes[0]], m_shape + 1, m_subsizes + 1);
    }

    const tensor_ref<TType, IDim - 1> operator[](size_t index) const {
        assert(index < m_shape[0]);
        return tensor_ref<TType, IDim - 1>(&m_data[index * m_subsizes[0]], m_shape + 1, m_subsizes + 1);
    }

    TType& operator[](size_t indexes[IDim]) {
        assert(indexes[0] < m_shape[0]);
        return (*this)[indexes[0]][indexes + 1];
    }

    const TType& operator[](size_t indexes[IDim]) const {
        assert(indexes[0] < m_shape[0]);
        return (*this)[indexes[0]][indexes + 1];
    }

    template <typename UType>
    void assign(tensor_ref<UType, IDim> other) {
        assert(shape(0) == other.shape(0));
        for (size_t i = 0; i < shape(0); ++i) {
            (*this)[i].assign(other[i]);
        }
    }

    template <typename UType>
    void assign(const tensor<UType, IDim>& other) {
        assert(shape(0) == other.shape(0));
        for (size_t i = 0; i < shape(0); ++i) {
            (*this)[i].assign(other[i]);
        }
    }

    void initialize(TType init = TType()) {
        for (size_t i = 0; i < m_shape[0]; ++i) {
            (*this)[i].initialize(init);
        }
    }

    void copy_initialize(tensor_ref<TType, IDim> other, TType init = TType()) {
        for (size_t i = 0; i < std::min(m_shape[0], other.m_shape[0]); ++i) {
            (*this)[i].copy_initialize(other[i], init);
        }
        for (size_t i = std::min(m_shape[0], other.m_shape[0]); i < m_shape[0]; ++i) {
            (*this)[i].initialize(init);
        }
    }

    std::array<size_t, IDim> shape() const {
        std::array<size_t, IDim> result;
        for (int i = 0; i < IDim; ++i) {
            result[i] = m_shape[i];
        }
        return result;
    }

    size_t shape(unsigned dim) const {
        assert(dim < IDim);
        return m_shape[dim];
    }
private:
    friend class tensor_ref<TType, IDim + 1>;
    friend class tensor<TType, IDim>;
    friend class tensor<TType, IDim + 1>;

    tensor_ref(TType* data, const size_t* shape, const size_t* subsizes)
        : m_data(data), m_shape(shape), m_subsizes(subsizes) {}

    TType* m_data;
    const size_t* const m_shape;
    const size_t* const m_subsizes;
};

template <typename TType>
class tensor_ref<TType, 1> {
public:
    TType& operator[](size_t index) {
        assert(index < m_shape[0]);
        return m_data[index];
    }

    const TType& operator[](size_t index) const {
        assert(index < m_shape[0]);
        return m_data[index];
    }

    TType& operator[](size_t indexes[1]) {
        assert(indexes[0] < m_shape[0]);
        return (*this)[indexes[0]];
    }

    const TType& operator[](size_t indexes[1]) const {
        assert(indexes[0] < m_shape[0]);
        return (*this)[indexes[0]];
    }

    template <typename UType>
    void assign(tensor_ref<UType, 1> other) {
        assert(shape(0) == other.shape(0));
        for (size_t i = 0; i < shape(0); ++i) {
            (*this)[i] = other[i];
        }
    }

    template <typename UType>
    void assign(const tensor<UType, 1>& other) {
        assert(shape(0) == other.shape(0));
        for (size_t i = 0; i < shape(0); ++i) {
            (*this)[i] = other[i];
        }
    }

    void initialize(TType init = TType()) {
        for (size_t i = 0; i < m_shape[0]; ++i) {
            (*this)[i] = init;
        }
    }

    void copy_initialize(tensor_ref<TType, 1> other, TType init = TType()) {
        for (size_t i = 0; i < std::min(m_shape[0], other.m_shape[0]); ++i) {
            (*this)[i] = other[i];
        }
        for (size_t i = std::min(m_shape[0], other.m_shape[0]); i < m_shape[0]; ++i) {
            (*this)[i] = init;
        }
    }

    std::array<size_t, 1> shape() const {
        std::array<size_t, 1> result;
        result[0] = m_shape[0];
        return result;
    }

    size_t shape(unsigned dim) const {
        assert(dim < 1);
        return m_shape[dim];
    }
private:
    friend class tensor_ref<TType, 2>;
    friend class tensor<TType, 1>;
    friend class tensor<TType, 2>;

    tensor_ref(TType* data, const size_t* shape, const size_t* subsizes)
        : m_data(data), m_shape(shape) {}

    TType* m_data;
    const size_t* const m_shape;
};

template <typename TType>
class tensor_ref<TType, 0> {};


template <typename TType, unsigned IDim>
class tensor {
public:
    tensor() : m_data(nullptr), m_size(0) {
        for (int i = 0; i < IDim; ++i) {
            m_shape[i] = 0;
            m_subsizes[i] = 0;
        }
    }

    tensor(std::array<size_t, IDim> shape, TType init = TType()) {
        m_size = 1;
        for (int i = 0; i < IDim; ++i) {
            m_size *= shape[i];
            m_shape[i] = shape[i];
            m_subsizes[i] = 1;
            for (int j = i + 1; j < IDim; ++j) {
                m_subsizes[i] *= shape[j];
            }
        }
        m_data = new TType[m_size];
        if (!m_data) {
            throw std::exception();
        }
        ref().initialize(init);
    }

    tensor(size_t shape[IDim], TType init = TType()) {
        m_size = 1;
        for (int i = 0; i < IDim; ++i) {
            m_size *= shape[i];
            m_shape[i] = shape[i];
            m_subsizes[i] = 1;
            for (int j = i + 1; j < IDim; ++j) {
                m_subsizes[i] *= shape[j];
            }
        }
        m_data = new TType[m_size];
        if (!m_data) {
            throw std::exception();
        }
        ref().initialize(init);
    }

    tensor(const tensor<TType, IDim>& other) {
        m_size = other.m_size;
        for (int i = 0; i < IDim; ++i) {
            m_shape[i] = other.m_shape[i];
        }
        for (int i = 0; i < IDim; ++i) {
            m_subsizes[i] = other.m_subsizes[i];
        }
        m_data = new TType[m_size];
        if (!m_data) {
            throw std::exception();
        }
        for (int i = 0; i < m_size; ++i) {
            m_data[i] = other.m_data[i];
        }
    }

    tensor(const tensor_ref<TType, IDim>& other) {
        m_size = 1;
        for (int i = 0; i < IDim; ++i) {
            m_size *= other.shape(i);
            m_shape[i] = other.shape(i);
            m_subsizes[i] = 1;
            for (int j = i + 1; j < IDim; ++j) {
                m_subsizes[i] *= other.shape(j);
            }
        }

        m_data = new TType[m_size];
        if (!m_data) {
            throw std::exception();
        }
        ref().copy_initialize(other);
    }

    ~tensor() {
        delete[] m_data;
    }

    std::array<size_t, IDim> shape() const {
        std::array<size_t, IDim> result;
        for (int i = 0; i < IDim; ++i) {
            result[i] = m_shape[i];
        }
        return result;
    }

    size_t shape(unsigned dim) const {
        assert(dim < IDim);
        return m_shape[dim];
    }

    void resize(std::array<size_t, IDim> shape, TType init = TType()) {
        tensor<TType, IDim> temp(shape, init);
        temp.ref().copy_initialize(ref());
        swap(temp);
    }

    void resize(size_t shape[IDim], TType init = TType()) {
        tensor<TType, IDim> temp(shape, init);
        temp.ref().copy_initialize(ref());
        swap(temp);
    }

    void swap(tensor<TType, IDim>& other) {
        std::swap(m_data, other.m_data);
        std::swap(m_size, other.m_size);
        std::swap(m_shape, other.m_shape);
        std::swap(m_subsizes, other.m_subsizes);
    }

    operator tensor_ref<TType, IDim>() {
        return ref();
    }

    tensor_ref<TType, IDim> ref() {
        return tensor_ref<TType, IDim>(m_data, m_shape, m_subsizes);
    }

    const tensor_ref<TType, IDim> ref() const {
        return tensor_ref<TType, IDim>(m_data, m_shape, m_subsizes);
    }

    tensor_ref<TType, IDim - 1> operator[](size_t index) {
        assert(index < m_shape[0]);
        return tensor_ref<TType, IDim - 1>(&m_data[index * m_subsizes[0]], m_shape + 1, m_subsizes + 1);
    }

    const tensor_ref<TType, IDim - 1> operator[](size_t index) const {
        assert(index < m_shape[0]);
        return tensor_ref<TType, IDim - 1>(&m_data[index * m_subsizes[0]], m_shape + 1, m_subsizes + 1);
    }

    TType& operator[](size_t indexes[IDim]) {
        return (*this)[indexes[0]][indexes + 1];
    }

    const TType& operator[](size_t indexes[IDim]) const {
        return (*this)[indexes[0]][indexes + 1];
    }
private:
    TType* m_data = nullptr;
    size_t m_size;
    size_t m_shape[IDim];
    size_t m_subsizes[IDim];
};

template <typename TType>
class tensor<TType, 1> {
public:
    tensor() : m_data(nullptr), m_size(0) {
        m_shape[0] = 0;
        m_subsizes[0] = 0;
    }

    tensor(std::array<size_t, 1> shape, TType init = TType()) {
        m_size = shape[0];
        m_shape[0] = shape[0];
        m_subsizes[0] = 1;

        m_data = new TType[m_size];
        if (!m_data) {
            throw std::exception();
        }
        ref().initialize(init);
    }

    tensor(size_t shape[1], TType init = TType()) {
        m_size = shape[0];
        m_shape[0] = shape[0];
        m_subsizes[0] = 1;

        m_data = new TType[m_size];
        if (!m_data) {
            throw std::exception();
        }
        ref().initialize(init);
    }

    tensor(const tensor<TType, 1>& other) {
        m_size = other.m_size;
        m_shape[0] = other.m_shape[0];
        m_subsizes[0] = other.m_subsizes[0];
        m_data = new TType[m_size];
        if (!m_data) {
            throw std::exception();
        }
        for (int i = 0; i < m_size; ++i) {
            m_data[i] = other.m_data[i];
        }
    }

    tensor(const tensor_ref<TType, 1>& other) {
        m_size = other.shape(0);
        m_shape[0] = other.shape(0);
        m_subsizes[0] = 1;

        m_data = new TType[m_size];
        if (!m_data) {
            throw std::exception();
        }
        ref().copy_initialize(other);
    }

    ~tensor() {
        delete[] m_data;
    }

    std::array<size_t, 1> shape() const {
        std::array<size_t, 1> result;
        result[0] = m_shape[0];
        return result;
    }

    size_t shape(unsigned dim) const {
        assert(dim < 1);
        return m_shape[dim];
    }

    void resize(std::array<size_t, 1> shape,  TType init = TType()) {
        tensor<TType, 1> temp(shape, init);
        temp.ref().copy_initialize(ref());
        swap(temp);
    }

    void resize(size_t shape[1],  TType init = TType()) {
        tensor<TType, 1> temp(shape, init);
        temp.ref().copy_initialize(ref());
        swap(temp);
    }

    void swap(tensor<TType, 1>& other) {
        std::swap(m_data, other.m_data);
        std::swap(m_size, other.m_size);
        std::swap(m_shape, other.m_shape);
        std::swap(m_subsizes, other.m_subsizes);
    }

    operator tensor_ref<TType, 1>() {
        return ref();
    }

    tensor_ref<TType, 1> ref() {
        return tensor_ref<TType, 1>(m_data, m_shape, m_subsizes);
    }

    const tensor_ref<TType, 1> ref() const {
        return tensor_ref<TType, 1>(m_data, m_shape, m_subsizes);
    }

    TType& operator[](size_t index) {
        assert(index < m_shape[0]);
        return m_data[index];
    }

    const TType& operator[](size_t index) const {
        assert(index < m_shape[0]);
        return m_data[index];
    }

    TType& operator[](size_t indexes[1]) {
        return m_data[indexes[0]];
    }

    const TType& operator[](size_t indexes[1]) const {
        return m_data[indexes[0]];
    }
private:
    TType* m_data = nullptr;
    size_t m_size;
    size_t m_shape[1];
    size_t m_subsizes[1];
};

template <typename TType>
std::string tensor_string(tensor_ref<TType, 1> ten) {
    std::stringstream stream;
    stream << '(';
    for (size_t i = 0; i < ten.shape(0); ++i) {
        if (i > 0) {
            stream << ',';
        }
        stream << ten[i];
    }
    stream << ')';
    return stream.str();
}

template <typename TType, unsigned IDim>
std::string tensor_string(tensor_ref<TType, IDim> ten) {
    std::stringstream stream;
    stream << '(';
    for (size_t i = 0; i < ten.shape(0); ++i) {
        if (i > 0) {
            stream << ',';
        }
        stream << tensor_string(ten[i]);
    }
    stream << ')';
    return stream.str();
}

template <typename TType, unsigned IDim>
std::string tensor_string(tensor<TType, IDim> ten) {
    return tensor_string(ten.ref());
}



}
