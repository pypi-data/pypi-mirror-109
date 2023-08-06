/**********************************************************************************
 * Copyright (c) 2019 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 * @file babNode.h
 *
 * @brief File defining the class for Branch-and-Bound nodes
 *
 **********************************************************************************/

#pragma once

#include "babOptVar.h"
#include "babUtils.h"

#include <limits>
#include <string>


namespace babBase {


/**
    * @class BabNode
    * @brief Class representing a node in the Branch-and-Bound tree
    *
    * A BabNode is characterized by a vector containing the configuration for optimization variables (bounds etc.) in this node, as well as an ID (both private members).
    * It also contains a pruning score and a flag that indicates whether it holds the incumbent. Once constructed, a BabNode cannot be modified.
    */
class BabNode {

  public:
    /**
        * @brief Constructor for initializing a BabNode using separate vectors containing the bounds.
        *
        * @param[in] pruningScoreIn is the score of the node with respect to its pruning rule, a pruning score higher than a certain threshold will lead to pruning of the node
        * @param[in] lbdsIn is a vector containing the lower bounds on the optimization variables for this node
        * @param[in] ubdsIn is a vector containing the upper bounds on the optimization variables for this node
        * @param[in] idIn is the ID to be associated with this node
        * @param[in] depthIn is the depth of the node in the tree
        * @param[in] holdsIncumbent tells whether the node holds the current incumbent
        */
    BabNode(double pruningScoreIn, const std::vector<double>& lbdsIn, const std::vector<double>& ubdsIn, const int idIn, const unsigned depthIn, const bool holdsIncumbent):
        _pruningScore(pruningScoreIn), _lowerBounds(lbdsIn), _upperBounds(ubdsIn), _idNumber(idIn), _depth(depthIn), _holdsIncumbent(holdsIncumbent) {}

    /**
        * @brief Constructor for initializing a BabNode using a vector of OptimizationVariable (each of which contains a Bounds object). Used to initialize the root node.
        *
        * @param[in] pruningScoreIn is the score of the node with respect to its pruning rule, a pruning score higher than a certain threshold will lead to pruning of the node
        * @param[in] variablesIn is a vector containing the optimization variables
        * @param[in] idIn is the ID to be associated with this node
        * @param[in] depthIn is the depth of the node in the tree
        * @param[in] holdsIncumbent tells whether the node holds the current incumbent
        */
    BabNode(double pruningScoreIn, const std::vector<OptimizationVariable>& variablesIn, const int idIn, const unsigned depthIn, const bool holdsIncumbent):
        _pruningScore(pruningScoreIn), _idNumber(idIn), _depth(depthIn), _holdsIncumbent(holdsIncumbent)
    {
        size_t nVar = variablesIn.size();
        _lowerBounds.resize(nVar);
        _upperBounds.resize(nVar);
        for (size_t iVar = 0; iVar < nVar; iVar++) {
            _lowerBounds[iVar] = variablesIn[iVar].get_lower_bound();
            _upperBounds[iVar] = variablesIn[iVar].get_upper_bound();
        }
    }

    /**
        * @brief Default constructor
        */
    BabNode():
        _pruningScore(std::numeric_limits<double>::infinity()), _holdsIncumbent(false), _depth(0), _idNumber(0) {}

    /**
        * @brief Function for querying the pruning score within this node
        */
    double get_pruning_score() const { return _pruningScore; }

    /**
        * @brief Function for setting the pruning score within this node
        */
    void set_pruning_score(double pruningScoreIn) { _pruningScore = pruningScoreIn; }

    /**
        * @brief Function for querying the lower bounds on the optimization variables within this node.
        */
    std::vector<double> get_lower_bounds() const { return _lowerBounds; }

    /**
        * @brief Function for querying the upper bounds on the optimization variables within this node.
        */
    std::vector<double> get_upper_bounds() const { return _upperBounds; }

    /**
        * @brief Function for querying the node ID.
        */
    int get_ID() const { return _idNumber; };

    /**
        * @brief Function for querying the node depth.
        */
    int get_depth() const { return _depth; };

    /**
        * @brief Function obtaining information whether the node holds the incumbent.
        */
    bool holds_incumbent() const { return _holdsIncumbent; }

    /**
        * @brief Function for setting the _holdsIncumbent variable.
        */
    void set_holds_incumbent(const bool holdsIncumbent) { _holdsIncumbent = holdsIncumbent; }

    /**
        * @brief Function for setting the whole upper bound vector
        */
    void set_upper_bound(const std::vector<double> upperBounds) { _upperBounds = upperBounds; }

    /**
        * @brief Function for setting the whole upper bound vector
        */
    void set_upper_bound(const unsigned iVar, const double value) { _upperBounds[iVar] = value; }

    /**
        * @brief Function for setting the whole upper bound vector
        */
    void set_lower_bound(const std::vector<double> lowerBounds) { _lowerBounds = lowerBounds; }

    /**
        * @brief Function for setting the whole upper bound vector
        */
    void set_lower_bound(const unsigned iVar, const double value) { _lowerBounds[iVar] = value; }

    /**
        * @brief Overloaded operator for easier output.
        *        Definition of this operator is in bab.cpp.
        */
    friend std::ostream& operator<<(std::ostream& out, const BabNode& node);

  private:
    /**
        * @name Internal variables of a B&B node
        */
    /**@{*/
    std::vector<double> _lowerBounds; /*!< Lower bounds on optimization variables within this node */
    std::vector<double> _upperBounds; /*!< Upper bounds on optimization variables within this node */
    int _idNumber;                    /*!< Node ID */
    unsigned _depth;                  /*!< Depth of this node in the B&B tree */
    double _pruningScore;             /*!< PruningScore: if PruningScore is higher than a PruningThreshold, the node will be fathomed by and from the BAB-Tree*/
    bool _holdsIncumbent;             /*!< Variable telling whether this nodes holds the current incumbent */
    /**@}*/
};

/**
    * @brief operator << overloaded for BabNode for easier output
    *
    * @param[out] out is the outstream to be written to
    * @param[in] node is the B&B node to be printed
    */
inline std::ostream&
operator<<(std::ostream& out, const BabNode& node)
{
    std::string str;
    if (node.holds_incumbent()) {
        str = "yes";
    }
    else {
        str = "no";
    }
    out << "BabNode id: " << node.get_ID() << ", pruning score: " << node.get_pruning_score() << ", hold incumbent: " << str << "\n";
    for (unsigned int i = 0; i < node.get_lower_bounds().size(); i++) {
        out << "lb[" << i << "]: " << std::setprecision(16) << node.get_lower_bounds()[i] << " .. " << node.get_upper_bounds()[i] << " :[" << i << "]ub\n";
    }
    return out;
}


}    // end namespace babBase