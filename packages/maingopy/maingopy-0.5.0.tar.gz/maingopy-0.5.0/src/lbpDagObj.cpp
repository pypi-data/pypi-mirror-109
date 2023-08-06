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

#include "lbpDagObj.h"


namespace maingo {


namespace lbp {


///////////////////////////////////////////////////////////////
// constructor
DagObj::DagObj(mc::FFGraph &DAG, const std::vector<mc::FFVar> &DAGvars, const std::vector<mc::FFVar> &DAGfunctions,
               const std::vector<babBase::OptimizationVariable> &variables, const unsigned nineq, const unsigned neq, const unsigned nineqRelaxationOnly,
               const unsigned neqRelaxationOnly, const unsigned nineqSquash, std::shared_ptr<Settings> settings, std::shared_ptr<std::vector<Constraint>> constraintPropertiesIn):
    _constraintProperties(constraintPropertiesIn)
{
    const unsigned nvar = variables.size();

    // Copy DAG for LowerBoundingSolver
    for (unsigned int i = 0; i < nvar; i++) {
        mc::FFVar Y;                      // Create a new DAG variable
        this->vars.push_back(Y);          // Add the new DAG variable to the vars vector
        this->vars[i].set(&this->DAG);    // Add the new DAG variable to the DAG
    }
    this->resultVars.resize(DAGfunctions.size());
    DAG.eval(DAGfunctions.size(), DAGfunctions.data(), this->resultVars.data(), nvar, DAGvars.data(), this->vars.data());    // Get functions and write them to resultVars
    for (unsigned int i = 0; i < this->resultVars.size(); i++) {
        this->functions.push_back(this->resultVars[i]);    // Get functions
    }

    // Get the list of operations used in the DAG
    // It is needed for the call of proper DAG functions
    this->subgraph = this->DAG.subgraph(this->functions.size(), this->functions.data());

    // Get operations of each function in the DAG
    this->functionsObj.clear();
    this->functionsIneq.clear();
    this->functionsEq.clear();
    this->functionsIneqRelaxationOnly.clear();
    this->functionsEqRelaxationOnly.clear();
    this->functionsIneqSquash.resize(nineq);
    this->functionsObj.resize(1);
    this->functionsIneq.resize(nineq);
    this->functionsEq.resize(neq);
    this->functionsIneqRelaxationOnly.resize(nineqRelaxationOnly);
    this->functionsEqRelaxationOnly.resize(neqRelaxationOnly);
    this->functionsIneqSquash.resize(nineqSquash);
    // Get each function, let's do it in one loop
    for (unsigned int i = 0; i < this->functions.size(); i++) {
        unsigned indexType = (*_constraintProperties)[i].indexTypeNonconstant;
        switch ((*_constraintProperties)[i].type) {
            case OBJ:
                this->functionsObj[indexType].push_back(this->functions[i]);
                break;
            case INEQ:
                this->functionsIneq[indexType].push_back(this->functions[i]);
                break;
            case EQ:
                this->functionsEq[indexType].push_back(this->functions[i]);
                break;
            case INEQ_REL_ONLY:
                this->functionsIneqRelaxationOnly[indexType].push_back(this->functions[i]);
                break;
            case EQ_REL_ONLY:
            case AUX_EQ_REL_ONLY:
                this->functionsEqRelaxationOnly[indexType].push_back(this->functions[i]);
                break;    // Auxiliary relaxation only equalities are handled the same way as rel only eqs
            case INEQ_SQUASH:
                this->functionsIneqSquash[indexType].push_back(this->functions[i]);
                break;
            default:
                break;
        }
    }
    // Get subgraph of each function
    this->subgraphObj.clear();
    this->subgraphIneq.clear();
    this->subgraphEq.clear();
    this->subgraphIneqRelaxationOnly.clear();
    this->subgraphEqRelaxationOnly.clear();
    this->subgraphIneqSquash.clear();
    this->subgraphObj.resize(1);
    this->subgraphIneq.resize(nineq);
    this->subgraphEq.resize(neq);
    this->subgraphIneqRelaxationOnly.resize(nineqRelaxationOnly);
    this->subgraphEqRelaxationOnly.resize(neqRelaxationOnly);
    this->subgraphIneqSquash.resize(nineqSquash);
    for (unsigned int i = 0; i < this->functions.size(); i++) {
        unsigned indexType = (*_constraintProperties)[i].indexTypeNonconstant;
        switch ((*_constraintProperties)[i].type) {
            case OBJ:
                this->subgraphObj[indexType] = this->DAG.subgraph(this->functionsObj[indexType].size(), this->functionsObj[indexType].data());
                break;
            case INEQ:
                this->subgraphIneq[indexType] = this->DAG.subgraph(this->functionsIneq[indexType].size(), this->functionsIneq[indexType].data());
                break;
            case EQ:
                this->subgraphEq[indexType] = this->DAG.subgraph(this->functionsEq[indexType].size(), this->functionsEq[indexType].data());
                break;
            case INEQ_REL_ONLY:
                this->subgraphIneqRelaxationOnly[indexType] = this->DAG.subgraph(this->functionsIneqRelaxationOnly[indexType].size(), this->functionsIneqRelaxationOnly[indexType].data());
                break;
            case EQ_REL_ONLY:
            case AUX_EQ_REL_ONLY:
                this->subgraphEqRelaxationOnly[indexType] = this->DAG.subgraph(this->functionsEqRelaxationOnly[indexType].size(), this->functionsEqRelaxationOnly[indexType].data());
                break;
            case INEQ_SQUASH:
                this->subgraphIneqSquash[indexType] = this->DAG.subgraph(this->functionsIneqSquash[indexType].size(), this->functionsIneqSquash[indexType].data());
                break;
            default:
                break;
        }
    }
    // Allocate memory for the corresponding vectors (in dependence on LBP_linpoints) and also set settings
    // We use these always, e.g., for option check
    this->McPoint.resize(nvar);
    this->MCarray.resize(this->subgraph.l_op.size());
    this->resultRelaxation.resize(this->functions.size());

    // Objects needed for heuristics
    this->intervals_already_computed = false;
    this->intervalArray.resize(2 * this->subgraph.l_op.size());    // It is double the size, since it is used for forward and backward propagation
    this->constraintIntervals.resize(this->functions.size());
    this->currentIntervals.resize(nvar);

    // Compute a McCormick object with correct dimensions and everything is 0, this object is needed to properly reset the LP in Kelley's algorithm
    this->infinityMC = MC(I(0, 1), settings->infinity);
    this->infinityMC.sub(nvar);
    this->intervals_already_computed = false;
    validIntervalLowerBound          = -settings->infinity;
}


/////////////////////////////////////////////////////////////////////////
// function for initializing additional stuff needed when using vector-McCormick
void
DagObj::initialize_vMcCormick()
{

    this->functionsNonlinear.clear();
    this->functionsLinear.clear();
    this->vMcPoint.resize(this->vars.size());

    // Get linear and nonlinear functions
    for (size_t i = 0; i < _constraintProperties->size(); i++) {
        if ((*_constraintProperties)[i].dependency > LINEAR) {
            this->functionsNonlinear.push_back(this->functions[i]);
        }
        else {
            this->functionsLinear.push_back(this->functions[i]);
        }
    }
    this->subgraphNonlinear = this->DAG.subgraph(this->functionsNonlinear.size(), this->functionsNonlinear.data());
    this->subgraphLinear    = this->DAG.subgraph(this->functionsLinear.size(), this->functionsLinear.data());
    this->resultRelaxationVMCNonlinear.resize(this->functionsNonlinear.size());
    this->resultRelaxationNonlinear.resize(this->functionsNonlinear.size());
    this->resultRelaxationLinear.resize(this->functionsLinear.size());
    this->vMCarray.resize(this->subgraphNonlinear.l_op.size());
}


}    // end namespace lbp


}    // end namespace maingo