/**
 * Subject: Bachelor's thesis
 * Author: Adam Sedlacek | xsedla1e@vutbr.cz
 * Year: 2021
 * Description:
 *     Enum of logical functions. Also function to string function (used for gates count).
 * 
 */

#ifndef FUNCTION_H
#define FUNCTION_H
#include <string>

enum class Function {
    In,
    Not,
    And,
    Or,
    Xor,
    Nand,
    Nor,
    Xnor,
};

static inline std::string function_name(const Function f) {
    switch (f) {
        case Function::In: return "in";
        case Function::Not: return "not";
        case Function::And: return "and";
        case Function::Or: return "or";
        case Function::Xor: return "xor";
        case Function::Nand: return "nand";
        case Function::Nor: return "nor";
        case Function::Xnor: return "xnor";
        default:
            return "unknown gate name - shouldn't appear in any way";
    }
}

static inline Function index_to_function(const int idx) {
        switch (idx) {
        case 0: return Function::In;
        case 1: return Function::Not;
        case 2: return Function::And;
        case 3: return Function::Or;
        case 4: return Function::Xor;
        case 5: return Function::Nand;
        case 6: return Function::Nor;
        case 7: return Function::Xnor;
        default:
            throw "unknown function's index in CGP representation";
    }
}

#endif /* FUNCTION_H */