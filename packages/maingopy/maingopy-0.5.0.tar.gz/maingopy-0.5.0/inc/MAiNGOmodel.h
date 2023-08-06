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

#include "evaluationContainer.h"

#include "babOptVar.h"
#include "babUtils.h"

#include "ffunc.hpp"
#include "functionWrapper.h"


#include <vector>


// Using declarations of all additional functions defined in MC++ for a comfortable use of these functions in the model
using mc::acquisition_function;
using mc::arh;
using mc::bounding_func;
using mc::bstep;
using mc::cost_function;
using mc::covariance_function;
using mc::enthalpy_of_vaporization;
using mc::euclidean_norm_2d;
using mc::expx_times_y;
using mc::fabsx_times_x;
using mc::fstep;
using mc::gaussian_probability_density_function;
using mc::iapws;
using mc::ideal_gas_enthalpy;
using mc::lb_func;
using mc::lmtd;
using mc::mc_print;
using mc::neg;
using mc::nrtl_dGtau;
using mc::nrtl_dtau;
using mc::nrtl_G;
using mc::nrtl_Gdtau;
using mc::nrtl_Gtau;
using mc::nrtl_tau;
using mc::p_sat_ethanol_schroeder;
using mc::pos;
using mc::regnormal;
using mc::rho_liq_sat_ethanol_schroeder;
using mc::rho_vap_sat_ethanol_schroeder;
using mc::rlmtd;
using mc::saturation_temperature;
using mc::sqr;
using mc::squash_node;
using mc::sum_div;
using mc::ub_func;
using mc::vapor_pressure;
using mc::xexpax;
using mc::xlog;
using mc::xlog_sum;
using std::max;
using std::min;


/**
*	@namespace maingo
*	@brief namespace holding all essentials of MAiNGO
*/
namespace maingo {

using OptimizationVariable = babBase::OptimizationVariable; /*!< Redefine for easier usage */
using Bounds               = babBase::Bounds;               /*!< Redefine for easier usage */
using VT                   = babBase::enums::VT;            /*!< Redefine for easier usage */
constexpr VT VT_CONTINUOUS = babBase::enums::VT_CONTINUOUS; /*!< Redefine for easier usage */
constexpr VT VT_BINARY     = babBase::enums::VT_BINARY;     /*!< Redefine for easier usage */
constexpr VT VT_INTEGER    = babBase::enums::VT_INTEGER;    /*!< Redefine for easier usage */

/**
* @class MAiNGOmodel
* @brief This class is the base class for models to be solved by MAiNGO
*
* This class is used to derive a Model class in problem.h, where the user can implement their actual model.
*/
class MAiNGOmodel {

  public:
    using Var = mc::FFVar; /*!< Redefine for easier usage */

    /**
		* @brief Destructor
		*/
    virtual ~MAiNGOmodel() {}

    /**
		* @brief Virtual function which has to be implemented by the user in order to enable evaluation of the model
		*
		* @param[in] optVars is a vector holding the optimization variables
		*/
    virtual EvaluationContainer evaluate(const std::vector<Var> &optVars) = 0;

    /**
		* @brief Virtual function which has to be implemented by the user in order to enable getting data on optimization variables
		*/
    virtual std::vector<OptimizationVariable> get_variables() = 0;

    /**
		* @brief Virtual function which has to be implemented by the user in order to enable getting data on the initial point
		*/
    virtual std::vector<double> get_initial_point() { return std::vector<double>(); }

  private:
};


}    // namespace maingo