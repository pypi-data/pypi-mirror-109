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

#include "MAiNGOdebug.h"
#include "returnCodes.h"
#include "settings.h"

#include <iostream>
#include <map>
#include <queue>
#include <vector>


namespace maingo {


/**
* @enum SETTING_NAMES
* @brief Enum for representing the setting names and making the tracking of set settings easier
*/
enum SETTING_NAMES {
    // The first name has to be 1 and the names have to be increasing (in numbering)
    EPSILONA = 1,                /*!< absolute optimality tolerance */
    EPSILONR,                    /*!< relative optimality tolerance */
    DELTAINEQ,                   /*!< absolute inequality tolerance */
    DELTAEQ,                     /*!< absolute equality tolerance */
    RELNODETOL,                  /*!< relative minimal node size tolerance */
    INFTY,                       /*!< infinity value */
    TARGETLOWERBOUND,            /*!< target value for LBD at which MAiNGO terminates */
    TARGETUPPERBOUND,            /*!< target value for UBD at which MAiNGO terminates */
    BAB_MAXNODES,                /*!< max number of nodes */
    BAB_MAXITERATIONS,           /*!< max number of iterations */
    MAXTIME,                     /*!< max time */
    CONFIRMTERMINATION,          /*!< whether to confirm termination */
    TERMINATEONFEASIBLEPOINT,    /*!< whether to terminate once a feasible point was found */
    PRE_MAXLOCALSEARCHES,        /*!< max local searches in pre-processing */
    PRE_OBBTMAXROUNDS,           /*!< max number of obbt rounds in pre-processing */
    PRE_PUREMULTISTART,          /*!< whether to do a pure multistart */
    BAB_NODESELECTION,           /*!< node selection heuristic */
    BAB_BRANCHVARIABLE,          /*!< branching variable heuristic */
    BAB_ALWAYSSOLVEOBBT,         /*!< whether to always solve obbt */
    BAB_PROBING,                 /*!< whether to do probing */
    BAB_DBBT,                    /*!< whether to do dbbt */
    BAB_CONSTRAINTPROPAGATION,   /*!< whether to do constraint propagation */
    LBP_SOLVER,                  /*!< lower bounding solver */
    LBP_LINPOINTS,               /*!< linearization point strategy */
    LBP_SUBGRADIENTINTERVALS,    /*!< whether to use subgradient intervals heuristic */
    LBP_OBBTMINIMPROVEMENT,      /*!< minimal obbt improvement */
    LBP_ACTIVATEMORESCALING,     /*!< number of consecutive iterations with no lbd imrovement needed to activate more aggressive scaling in LP solver (e.g., CPLEX) */
    LBP_ADDAUXILIARYVARS,        /*!< whether to add auxiliary variables for common factors in the lower bounding problem */
    LBP_MINFACTORSFORAUX,        /*!< minimum number of common factors to add an auxiliary variable */
    LBP_MAXNUMBEROFADDEDFACTORS, /*!< maximum number of added factor as auxiliaries */
    MC_MVCOMPUSE,                /*!< whether to use multivariate mccormick */
    MC_MVCOMPTOL,                /*!< mccormick computational tolerance */
    MC_ENVELTOL,                 /*!< mccormick envelope computation tolerance */
    UBP_SOLVERPRE,               /*!< upper bounding solver in pre-processing */
    UBP_MAXSTEPSPRE,             /*!< max steps for upper bounding solver in pre-processing */
    UBP_MAXTIMEPRE,              /*!< max time for upper bounding solver in pre-processing */
    UBP_SOLVERBAB,               /*!< upper bounding solver in B&B */
    UBP_MAXSTEPSBAB,             /*!< max steps for upper bounding solver in B&B */
    UBP_MAXTIMEBAB,              /*!< max time for upper bounding solver in B&B */
    UBP_IGNORENODEBOUNDS,        /*!< whether to ignore bounds in upper bounding */
    EC_NPOINTS,                  /*!< number of points on the Pareto front in epsilon-constraint method */
    LBP_VERBOSITY,               /*!< lower bounding verbosity */
    UBP_VERBOSITY,               /*!< upper bounding verbosity */
    BAB_VERBOSITY,               /*!< b&b verbosity */
    BAB_PRINTFREQ,               /*!< frequency of printed b&b iterations */
    BAB_LOGFREQ,                 /*!< frequency of written b&b iterations */
    OUTSTREAMVERBOSITY,          /*!< verbosity for outstream */
    WRITECSV,                    /*!< whether to write csv */
    WRITEJSON,                   /*!< whether to write json */
    writeResultFile,             /*!< whether to write an additional log file containing non-standard information about the problem */
    WRITETOLOGSEC,               /*!< write to log/csv every x seconds */
    PRE_PRINTEVERYLOCALSEARCH,   /*!< whether to print every local search */
    WRITETOOTHERLANGUAGE,        /*!< write a file in a different modeling language */
    UNKNOWN_SETTING = 500        /*!< unknown setting */
};

/**
* @class Logger
* @brief This class contains all logging and output information
*
* This class is used by the MAiNGO, BranchAndBound, LowerBoundingSolver and UpperBoundingSolver classes for a central and proper storing of output and logging information.
*/
class Logger {

  public:
    /**
        * @brief Default constructor.
        */
    Logger(){};

    /**
        * @brief Default copy constructor.
        */
    Logger(const Logger&) = default;

    /**
        * @brief Default copy assignment.
        */
    Logger& operator=(const Logger&) = default;

    /**
        * @brief Default destructor.
        */
    ~Logger() {}

    /**
        * @brief The main function used for printing a given message and storing it in log and/or csv
        *
        * @param[in] message is the message to be printed or written
        * @param[in] verbosityGiven is the verbosity given by, e.g., settings
        * @param[in] verbosityNeeded is the least verbosity needed for the message to be printed/written
        * @param[in] givenOutstreamVerbosity tells whether to print to _outStream and/or write files
        */
    void print_message(const std::string& message, const VERB verbosityGiven, const VERB verbosityNeeded, const LOGGING_DESTINATION givenOutstreamVerbosity);

    /**
        * @brief The main function used for printing a given message and storing it in log and/or csv
        *
        * @param[in] message is the message to be printed or written
        * @param[in] givenOutstreamVerbosity tells whether to print to _outStream and/or write files
        */
    void print_message_to_stream_only(const std::string& message, const LOGGING_DESTINATION givenOutstreamVerbosity);

    /**
        *  @brief Sets output stream.
        *
        *  @param[in] outputStream is the new output stream to be used by MAiNGO.
        */
    void set_output_stream(std::ostream* const outputStream);

    /**
        * @brief Function used for creating the log file
        *
        * @param[in] givenOutstreamVerbosity tells whether to print to _outStream and/or write files
        */
    void create_log_file(const LOGGING_DESTINATION givenOutstreamVerbosity);

    /**
        * @brief Function used for creating the csv file with information on the B&B iterations
        *
        * @param[in] writeCsv says whether to write the csv file
        */
    void create_iterations_csv_file(const bool writeCsv);

    /**
        * @brief Function used for writing all lines stored in queue babLine to log
        *
        * @param[in] errorMessage is a possible additional error message
        */
    void write_all_lines_to_log(const std::string& errorMessage = "");

    /**
        * @brief Function used for writing all iterations currently stored queue babLineCsv to csv
        */
    void write_all_iterations_to_csv();

    /**
        * @brief Function used for saving the names of setting files set by the user
        *
        * @param[in] fileName it the name of the file set by the user
        * @param[in] fileFound tells whether the wanted file has been found
        */
    void save_settings_file_name(const std::string& fileName, const bool fileFound);

    /**
        * @brief Function used for saving the user-set settings
        *
        * @param[in] settingName is the changed setting
        * @param[in] str is the corresponding string
        */
    void save_setting(const SETTING_NAMES settingName, const std::string& str);

    /**
        * @brief Function for printing and writing user-set settings
        *
        * @param[in] verbosityGiven is the verbosity given by, e.g., settings
        * @param[in] verbosityNeeded is the least verbosity needed for the message to be printed/written
        * @param[in] givenOutstreamVerbosity tells whether to print to _outStream and/or write files
        */
    void print_settings(const VERB verbosityGiven, const VERB verbosityNeeded, const LOGGING_DESTINATION givenOutstreamVerbosity);

    /**
        * @brief Clears all logging information
        */
    void clear();

    /**
        * @name Auxiliary public variables for storing output and logging information
        */
    /**@{*/
    std::queue<std::string> babLine{};                /*!< queue for storing lines of B&B output */
    std::queue<std::string> babLineCsv{};             /*!< queue for storing lines of B&B output for CSV file */
    std::string logFileName       = "maingo.log";     /*!< name of the txt file into which the log may be written */
    std::string csvIterationsName = "iterations.csv"; /*!< name of the csv file into which information on the individual B&B iterations may be written */
    bool reachedMinNodeSize;                          /*!< bool for saving information if minimum node size has been reached within B&B */
                                                      /**@}*/

  private:
    /**
        * @name Private variable storing the output
        */
    /**@{*/
    std::ostream* _outStream    = &std::cout;    /*!< default MAiNGO output stream is set to std::cout */
    unsigned int _nSettingFiles = 0;             /*!< number of setting files from which the user has read, default is set to 0 */
    std::map<int, std::string> _userSetSettings; /*!< map holding settings set by the user */
                                                 /**@}*/

};    // end of class Logger


}    // end namespace maingo