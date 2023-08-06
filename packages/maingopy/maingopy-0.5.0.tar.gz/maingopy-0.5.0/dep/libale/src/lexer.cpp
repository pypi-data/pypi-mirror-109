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

#include "lexer.hpp"

#include <algorithm>

namespace ale {



lexer::lexer(std::istream& input) : input(input), line(1), col(1) {}

void lexer::reserve_keywords(std::initializer_list<std::string> keys) {
    keywords.insert(keywords.end(), keys);
}

char lexer::peek() {
    int next = input.peek();
    if (next == EOF) {
        return '\0';
    }
    return next;
}

void lexer::skip() {
    input.get();
    col++;
}

void lexer::consume() {
    lexeme += input.get();
}

bool lexer::check(char expect) {
    if (peek() != expect) {
        return false;
    }
    return true;
}

bool lexer::match(char expect) {
    if (check(expect)) {
        consume();
        return true;
    }
    return false;
}

token lexer::make_token(token::token_type type) {
    token tok(type, lexeme, line, col);
    col += lexeme.length();
    lexeme = "";
    return tok;
}

token lexer::next_token() {
    while (char next = peek()) {
        switch (next) {
            case ' ':
            case '\r':
            case '\t':
            case '\n': skip_space(); continue;
            case '#': skip(); skip_comment(); continue;
            case '\"': return match_literal(); continue;
            case '+': consume(); return make_token(token::PLUS);
            case '-': consume(); return make_token(token::MINUS);
            case '*': consume(); return make_token(token::STAR);
            case '/': consume(); return make_token(token::SLASH);
            case '^': consume(); return make_token(token::HAT);
            case '|': consume(); return make_token(token::PIPE);
            case '&': consume(); return make_token(token::AND);
            case '!': consume(); return make_token(token::BANG);
            case '=': consume(); return make_token(token::EQUAL);
            case '(': consume(); return make_token(token::LPAREN);
            case ')': consume(); return make_token(token::RPAREN);
            case '[': consume(); return make_token(token::LBRACK);
            case ']': consume(); return make_token(token::RBRACK);
            case '{': consume(); return make_token(token::LBRACE);
            case '}': consume(); return make_token(token::RBRACE);
            case ',': consume(); return make_token(token::COMMA);
            case ';': consume(); return make_token(token::SEMICOL);
            case '.': consume(); return make_token(match('.') ? token::DOTS : token::DOT);
            case ':': consume(); return make_token(match('=') ? token::DEFINE : token::COLON);
            case '<': consume();
                if (match('=')) {
                    return make_token(token::LEQUAL);
                }
                if (match('-')) {
                    return make_token(token::ASSIGN);
                }
                return make_token(token::LESS);
            case '>': consume(); return make_token(match('=') ? token::GEQUAL : token::GREATER);
            default:
                if (isdigit(next)) {
                    return match_number();
                }
                else if (isalpha(next)) {
                    return match_ident();
                }
                consume();
                return make_token(token::ERROR);
        }
    }
    return make_token(token::END);
}

void lexer::skip_space() {
    while (check(' ') || check('\r') || check('\t') || check('\n')) {
        if (check('\n')) {
            line++;
            col = 0;
        }
        skip();
    }
}

void lexer::skip_comment() {
    while (peek() && !check('\n')) {
        skip();
    }
}

token lexer::match_number() {
    while (isdigit(peek())) {
        consume();
    }
    if (!check('.') && !check('e') && !check('E')) {
        return make_token(token::INTEGER);
    }
    if (match('.')) {
        while (isdigit(peek())) {
            consume();
        }
    }
    if (match('e') || match('E')) {
        match('-') || match('+');
        if (isdigit(peek())) {
            consume();
        }
        else {
            return make_token(token::ERROR);
        }
        while (isdigit(peek())) {
            consume();
        }
    }
    return make_token(token::NUMBER);
}



token lexer::match_ident() {
    if (isalpha(peek())) {
        consume();
    }
    else {
        return make_token(token::ERROR);
    }
    while (isalpha(peek()) || isdigit(peek()) || peek() == '_') {
        consume();
    }
    // TODO: accept any capitalization
    if (std::find(keywords.begin(), keywords.end(), lexeme) != keywords.end()) {
        return make_token(token::KEYWORD);
    }
    else {
        return make_token(token::IDENT);
    }
}



token lexer::match_literal() {
    skip();
    while ((peek() != '\"') && (peek() != '\0')) {
        consume();
    }
    if (check('\"')) {
        auto tok = make_token(token::LITERAL);
        skip();
        return tok;
    }
    else {
        return make_token(token::ERROR);
    }
}



}
