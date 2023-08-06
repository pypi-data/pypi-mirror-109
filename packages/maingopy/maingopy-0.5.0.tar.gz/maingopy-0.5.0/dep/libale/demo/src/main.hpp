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

#include "parser.hpp"
#include "node.hpp"
#include "expression.hpp"

#include <vector>
#include <utility>

namespace ale::demo {



using namespace ale;

class batch_parser : public parser {
public:
    using parser::parser;
    using parse_result = std::pair<std::vector<expression<real<0>>>, std::vector<std::pair<expression<boolean<0>>, std::string>>>;

    parse_result parse() {
        std::queue<std::string>().swap(errors);
        std::vector<expression<real<0>>> reals;
        std::vector<std::pair<expression<boolean<0>>,std::string>> booleans;
        match(token::END);
        if (match(token::END)) {
            report_empty();
            recover();
        }
        while (!check(token::END)) {
            if (match_any_definition<LIBALE_MAX_DIM>()) {
                continue;
            }
            if (match_any_assignment<LIBALE_MAX_DIM>()) {
                continue;
            }
            {
                std::unique_ptr<value_node<real<0>>> expr;
                std::string note;
                if (match_expression(expr, note))
                {
                    reals.emplace_back(expr.release(), note);
                    continue;
                }
            }
            {
                std::unique_ptr<value_node<boolean<0>>> expr;
                std::string note;
                if (match_expression(expr, note))
                {
                    booleans.emplace_back(expr.release(), note);
                    continue;
                }
            }

            report_syntactical();
            recover();
        }
        print_errors();
        return std::make_pair(reals, booleans);
    }
};



}
