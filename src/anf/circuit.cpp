/**
 * Subject: Bachelor's thesis
 * Author: Adam Sedlacek | xsedla1e@vutbr.cz
 * Year: 2021
 * Description:
 *      Circuit is a class that is moreless wrapper that provides interconnection among formulas.
 *      Methods are writen with intetion for simple use, and easier access to desired functionality.
 * 
 */

#include <vector>
#include <iostream>
#include <set>
#include "parameters.hpp"
#include "formula.hpp"
#include "circuit.hpp"
#include "../reference_bits.hpp"
#include "../utils.hpp"
#include "../process_size.hpp"

#include "../cgp/cell.hpp"

/**
 * Circuit constructor which calls formula(s) constructor(s). Recommended to check out the formula class instead. 
 */
Circuit::Circuit(const Parameters &parameters, const ReferenceBits &reference_bits) {
    for (size_t i = 0; i < reference_bits.output.size(); i++) {
        Formula formula(parameters.term_count, parameters.arity, reference_bits);
        formulas.push_back(formula);
    }
}

/**
 * Mutates N times value in a formula that is chosen randomly.
 */
void Circuit::mutate_overall(const Parameters &parameters, const ReferenceBits &reference_bits) {
    for (int i = 0; i < parameters.mutation; i++) {
        int formula_idx = utils::randint(0, formulas.size());
        formulas[formula_idx].mutate(parameters, reference_bits);
    }
}

/**
 * Method returns tuple of used gates (xor, and, not). Those gates are count with optimization on mind.
 * The "not" gate(s) is actually count only once ("inverted out of a circuit beforehand").
 *
 * The "and" gate(s) reduction is provided as index-term pattern(s).
 * For each formula is checked the pattern of term (idx of input) and inserted in set, an instance:
 *      012, 01, 13, 134, ...
 *      if enconters same pattern (same indices) 01 and 01 the "and" gate is count only once.
 *      Subpatterns are not incount -> only of entire term's indices.
 * 
 * The "xor" gate(s) are count from "non-zeros" vector which hold current literals in vectors.
 *      This means if the vector has only 5 elements, there will be 4 XORs as the output.
 */ 
std::tuple<int, int, int> Circuit::used_gates_optimized(const int inputs_count) {
    std::set<std::vector<int>> used_elements;
    std::set<int> nots;
    int xor_count = 0;
    int and_count = 0;

    for (auto &f: formulas) {
        xor_count += f.non_zeros.size() - 1; // XORs in one formula
        for (auto &nz : f.non_zeros) {
            std::sort(nz.begin(), nz.end());
            if (nz.size() == 0) xor_count--;
            std::vector<int> pattern;
            
            for (auto &l : nz) {
                int idx = l % inputs_count;
                if (f.literals[l].state == State::Not) {
                    nots.insert(idx);
                }
                pattern.emplace_back(idx);
            }

            if (used_elements.find(pattern) == used_elements.end() && pattern.size() > 1) {  
                used_elements.insert(pattern);
                and_count += pattern.size() - 1;
            }
        }
    }
    return {xor_count, and_count, nots.size()};
}


/**
 * This method is very similar to optimized option beside it doesn't operate the optimization with pattern sets.
 * This was found as better for area optimization during EA run. Higher redundance seems to have a positive impact.
 */
std::tuple<int, int, int> Circuit::used_gates(const int inputs_count) {
    std::set<int> nots;
    int xor_count = 0;
    int and_count = 0;

    for (auto &f: formulas) {
        xor_count += f.non_zeros.size() - 1; // XORs in one formula
        for (auto &nz : f.non_zeros) {
            if (nz.size() == 0) xor_count--;
            
            for (auto &l : nz) {
                int idx = l % inputs_count;
                if (f.literals[l].state == State::Not) {
                    nots.insert(idx);
                }
            }
            
            if (nz.size() > 1) {
                and_count += nz.size() - 1;
            }
        }
    }
    return {xor_count, and_count, nots.size()};
}

/**
 * Output of this method is used gates. Depends on the parameter "optimized".
 * If the optimization is required it will print out used gates with optimized pattern matching,
 * otherwise it will print out redundant gates in terms/formulas.
 */
void Circuit::print_used_gates(const int inputs_count, bool optimized) {
    auto [xor_count, and_count, not_count] = (optimized ? used_gates_optimized(inputs_count) : used_gates(inputs_count));
    int sum = and_count + not_count + xor_count;
    std::cout << "used gates: " << sum << std::endl;
    std::cout << "and: " << and_count << std::endl;
    std::cout << "xor: " << xor_count << std::endl;
    std::cout << "not: " << not_count << std::endl;
}

/**
 * Method calculates used are on the chip in 45 nm process.
 */
void Circuit::calculate_used_area(const int inputs_count, bool optimized) {
    auto [xor_count, and_count, not_count] = (optimized ? used_gates_optimized(inputs_count) : used_gates(inputs_count));
    area = and_count * gate_size::And + xor_count * gate_size::Xor + not_count * gate_size::Not;
}

/**
 * Prints out found circuit, dependent on the optional parameter in case console does not support non-ascii characters.
 */
void Circuit::print_circuit(const int inputs_count, const bool print_ascii) {
    for (size_t i = 0; i < formulas.size(); i++) {
        if (print_ascii) {
            formulas[i].print_circuit_ascii_only();
        } else {
            formulas[i].print_circuit(inputs_count);
        }
    }
}

/**
 * Calls each formula with request of its fitness.
 */
void Circuit::calculate_fitness(const ReferenceBits &reference_bits) {
    uint tmp_fit = 0;
    for (size_t i = 0; i < formulas.size(); i++) {
        formulas[i].calculate_fitness(reference_bits, i);
        tmp_fit += formulas[i].fitness;
    }
    fitness = tmp_fit;
}

/**
 * Crossover for two formulas. Commented section is for one-point crossover for all formulas involved in a circuit.
 *     formula yn | term - term - term | term contains indices of active inputs.
 * 
 * parent 1 => y0 | 01  - 23 - 134 |
 *             y1 | 123 - 01 - 24  |
 * 
 * parent 2 => y0 | 02  - 13 - 134 |
 *             y1 | 024 - 01 - 34  |
 
 * (point first dash for y0 and y1)
 * offspring => y0 | 01  - 13 - 134 |
 *              y1 | 123 - 01 - 34  |
 * 
 * The uncommented section is for each formula within random generated point of crossover.
 * parent 1 => y0 | 01  - 23 - 134 |
 *             y1 | 123 - 01 - 24  |
 * 
 * parent 2 => y0 | 02  - 13 - 134 |
 *             y1 | 024 - 01 - 34  |
 *
 * (point first dash for y0)
 * (point second dash for y1)
 * offspring => y0 | 01  - 23 - 134 |
 *              y1 | 123 - 01 - 34  |
 */
Circuit Circuit::crossover(Circuit parent1, Circuit parent2) {
    Circuit offspring = parent1;

    // auto size = offspring.formulas[0].literals.size();
    // // std::cout << "literals: " << size << std::endl;
    // auto nonzerossize = offspring.formulas[0].non_zeros.size();
    // // std::cout << "non_zeros/terms: " << nonzerossize << std::endl;
    // int inputs_count = size / nonzerossize;
    // int cross_point = utils::randint(1, nonzerossize);
    // int shift = cross_point * inputs_count;

    for (size_t i = 0; i < offspring.formulas.size(); i++) {
        auto size = offspring.formulas[i].literals.size();
        auto nonzerossize = offspring.formulas[i].non_zeros.size();
        int inputs_count = size / nonzerossize;
        int cross_point = utils::randint(1, nonzerossize);
        int shift = cross_point * inputs_count;
        
        for (size_t lit = shift; lit < size; lit++) {
            offspring.formulas[i].literals[lit] = parent2.formulas[i].literals[lit];
        }
        for (size_t idx = cross_point; idx < nonzerossize; idx++) {
            offspring.formulas[i].non_zeros[idx] = parent2.formulas[i].non_zeros[idx];
        }
    }
    return offspring;
}



/*
    Method print out the CGP representation (chromosome), which is processed and visualised by cgp viewer.

    For easier workthrough is utilized CELL from CGP implementation. Thus literals are mapped onto
    2 in 1 out gates and then chained in "evaluation" through XORs (for each term). This is done for each formula.

    Gate depends on its inputs:
        1 input   - only connects within its index and returns gate IN.
        2 inputs  - connecting two inputs then returns gates with AND (negated inputs are forwarded in "negative column")
        3+ inputs - connecting firstly two inputs then it's paired with previous pair and one input
            1 2 3 4 -> (1, 2)(new 5th index) next pair is (5, 3)(6th) then (6, 4)
*/
void Circuit::print_cgp_viewer(const ReferenceBits &reference_bits) {
    std::vector<Cell> cells;
    std::vector<int> terms_indices;
    std::vector<int> output_indices;

    insert_input_gates(reference_bits, cells);
    insert_not_input_gates(reference_bits, cells);

    auto literal_index = [&](auto const &f, auto const idx) {
        int ref_size = reference_bits.input.size();
        int literal_idx = idx % ref_size;

        if (f.literals[idx].state == State::Is) {
            return literal_idx;
        } 
        if (f.literals[idx].state == State::Not) {
            return literal_idx + ref_size;
        }
        throw std::runtime_error("ERROR: unexpected literal value IsNot");
    };

    auto simple_and = [&](auto const &f, int const idx, int const idx2) {
        Cell c;
        c.input1 = literal_index(f, idx);
        c.input2 = literal_index(f, idx2);
        c.function = Function::And;
        cells.push_back(c);
        return cells.size();
    };

    int xor_shift = 0;
    for (auto &f : formulas) {
        for (auto &non_vec : f.non_zeros) {
            if (non_vec.size() == 1) {
                Cell c;
                c.input1 = literal_index(f, non_vec[0]);
                c.input2 = 0;
                c.function = Function::In;
                cells.push_back(c);
                terms_indices.push_back(cells.size() - 1);
            }

            if (non_vec.size() == 2) {
                int idx = simple_and(f, non_vec[0], non_vec[1]);
                terms_indices.push_back(idx - 1);
            }

            if (non_vec.size() > 2) {
                int idx = simple_and(f, non_vec[0], non_vec[1]);

                for (size_t i = 2; i < non_vec.size(); i++) {
                    Cell c;
                    c.input1 = idx - 1;
                    c.input2 = literal_index(f, non_vec[i]);
                    c.function = Function::And;
                    cells.push_back(c);
                    idx = cells.size();
                }

                terms_indices.push_back(idx - 1);
            }
        }

        // if (f.non_zeros.size() < 2) continue;
        // if there is only 1 term in each formula will cause undefined behavior
        // for evolutionary search it's meaningless to run with term = 1
        Cell c;
        c.input1 = terms_indices[0 + xor_shift];
        c.input2 = terms_indices[1 + xor_shift];
        c.function = Function::Xor;
        cells.push_back(c);
        int idx = cells.size() - 1;

        for (size_t i = 2 + xor_shift; i < terms_indices.size(); i++) {
            Cell c;
            c.input1 = idx;
            c.input2 = terms_indices[i];
            c.function = Function::Xor;
            cells.push_back(c);
            idx = cells.size() - 1;
        }
        xor_shift = terms_indices.size();
        output_indices.push_back(idx);
    }

    cgp_print(reference_bits, cells, output_indices);
 }

void Circuit::print_cgp_viewer_optimized(const ReferenceBits &reference_bits) {
    std::map<std::string, int> terms = find_term_patterns(reference_bits.input.size());
    std::vector<Cell> cells;
    insert_input_gates(reference_bits, cells);
    insert_not_input_gates(reference_bits, cells);

    for (const auto &[pattern, idx] : terms) {
        std::vector<int> inputs;
        for (size_t i = 0; i < pattern.size(); i++) {
            if (pattern[i] == '1') inputs.push_back(i);
            if (pattern[i] == 'N') inputs.push_back(i + reference_bits.input.size());
        }

        if (inputs.size() == 1) {
            Cell c;
            c.input1 = inputs[0];
            c.input2 = 0;
            c.function = Function::In;
            cells.push_back(c);
        }

        auto simple_and = [&](int const idx, int const idx2) {
            Cell c;
            c.input1 = idx;
            c.input2 = idx2;
            c.function = Function::And;
            cells.push_back(c);
            return cells.size();
        };

        if (inputs.size() >= 2) {
            int idx = simple_and(inputs[0], inputs[1]);
            for (size_t i = 2; i < inputs.size(); i++) {
                Cell c;
                c.input1 = idx - 1;
                c.input2 = inputs[i];
                c.function = Function::And;
                cells.push_back(c);
                idx = cells.size();
            }
        }
        terms[pattern] = cells.size() - 1;
    }

    int input_size = reference_bits.input.size();
    std::vector<int> output_indices;

    for (const auto &f : formulas) {
        std::string pattern = get_pattern(f, 0, 0 + input_size);
        int idx = terms[pattern];
        for (size_t i = input_size; i < f.literals.size(); i += input_size) {
            std::string pattern2 = get_pattern(f, i, i + input_size);
            Cell c;
            c.input1 = idx;
            c.input2 = terms[pattern2];
            c.function = Function::Xor;
            cells.push_back(c);
            idx = cells.size() - 1;
        }
        output_indices.push_back(cells.size() - 1);
    }

    cgp_print(reference_bits, cells, output_indices);
}

// "copy paste" from CGP implementation, very slight changes were done
void Circuit::cgp_print(const ReferenceBits &reference_bits, const std::vector<Cell> &cells, const std::vector<int> &output_indices) const {
    printf("{%ld,%ld,%ld,%d,2,1,%d}", // two inputs, one output (basic logic gate)
        reference_bits.input.size(),
        reference_bits.output.size(),
        cells.size() - reference_bits.input.size(), 1, 8 // one row, 8 logical functions
    );

    for (unsigned int i = reference_bits.input.size(); i < cells.size(); i++) {
        printf("([%d]%d,%d,%d)", i, cells[i].input1, cells[i].input2, static_cast<int>(cells[i].function));
    }

    std::cout << "(" << output_indices[0]; // there should be always at least one output
    for (unsigned int i = 1; i < output_indices.size(); i++) {
        if (i != output_indices.size()) {
            std::cout << "," << output_indices[i];
        } else {
            std::cout << output_indices[i];
        }
    }
    std::cout << ")" << std::endl;
}

std::string Circuit::get_pattern(const Formula &f, const int start, const int end) {
    std::string pattern = "";

    for (int i = start; i < end; i++) {
        auto l = f.literals[i];
        if (l.state == State::Is) {
            pattern += "1"; // in
        } else if (l.state == State::Not) {
            pattern += "N"; // not
        } else {
            pattern += "0"; // none
        }
    }

    return pattern;
}

std::map<std::string, int> Circuit::find_term_patterns(const int input_size) {
    std::map<std::string, int> terms;

    for (const auto &f : formulas) {
        for (size_t i = 0; i < f.literals.size(); i += input_size) {
            std::string pattern = get_pattern(f, i, i + input_size);
            terms.insert(std::pair(pattern, -1)); // -1 indicates not generated sub-circuit
        }
    }

    return terms;
}

void Circuit::insert_input_gates(const ReferenceBits &reference_bits, std::vector<Cell> &cells) {
    for (auto input : reference_bits.input) {
        Cell c;
        c.function = Function::In;
        cells.push_back(c);
    }
}

void Circuit::insert_not_input_gates(const ReferenceBits &reference_bits, std::vector<Cell> &cells) {
    for (size_t i = 0; i < reference_bits.input.size(); i++) {
        Cell c;
        c.function = Function::Not;
        c.input1 = i;
        c.input2 = 0;
        cells.push_back(c);
    }
}