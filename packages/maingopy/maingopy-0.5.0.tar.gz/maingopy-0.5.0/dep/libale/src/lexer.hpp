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

#include "token.hpp"

#include <iostream>
#include <string>
#include <vector>

namespace ale {



class lexer {
public:
    lexer(std::istream&);
    token next_token();
    void reserve_keywords(std::initializer_list<std::string>);
private:
    char peek();
    void skip();
    void consume();
    bool check(char);
    bool match(char);

    void skip_space();
    void skip_comment();
    token match_number();
    token match_ident();
    token match_literal();

    token make_token(token::token_type);

    std::istream& input;

    std::vector<std::string> keywords;

    std::string lexeme;
    size_t line;
    size_t col;
};



}
