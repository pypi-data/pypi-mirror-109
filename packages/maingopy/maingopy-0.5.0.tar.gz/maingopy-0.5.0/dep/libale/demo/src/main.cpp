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

#include "main.hpp"
#include "util/evaluator.hpp"

#include <fstream>

int main() {
    std::cout << "initializing\n";
    std::cout << std::boolalpha;
    ale::symbol_table symbols;
    std::ifstream input("input.txt");
    ale::demo::batch_parser par(input, symbols);
    std::cout << '\n';

    std::cout << "parsing input\n";
    auto trees = par.parse();
    par.print_errors();
    std::cout << '\n';

    std::cout << "printing defined symbols\n";
    symbols.print_all();
    std::cout << '\n';

    std::cout << "evaluating expressions\n";
    ale::util::evaluator eval(symbols);
    for (auto it = trees.first.begin(); it != trees.first.end(); ++it) {
        std::cout << eval.dispatch(*it) << '\n';
    }
    for (auto it = trees.second.begin(); it != trees.second.end(); ++it) {
        std::cout << it->second << ": " << eval.dispatch(it->first) << '\n';
    }
    std::cout << '\n';

    std::cout << "finished execution\n";
    return 0;
}
