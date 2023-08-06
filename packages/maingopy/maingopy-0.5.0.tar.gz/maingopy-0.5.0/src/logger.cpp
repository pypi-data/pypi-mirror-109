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

#include "logger.h"

#include <fstream>
#include <sstream>


using namespace maingo;


/////////////////////////////////////////////////////////////////////////
// writes a message to outstream and possibly bablog
void
Logger::print_message(const std::string& message, const VERB verbosityGiven, const VERB verbosityNeeded, const LOGGING_DESTINATION givenOutstreamVerbosity)
{

    switch (givenOutstreamVerbosity) {

        case LOGGING_OUTSTREAM:
            // Print to _outStream only
            if (verbosityGiven >= verbosityNeeded) {
                (*_outStream) << message << std::flush;
            }
            break;
        case LOGGING_FILE:
            // Save message in log queue to be written later
            if (verbosityGiven >= verbosityNeeded) {
                babLine.push(message);
            }
            break;
        case LOGGING_FILE_AND_STREAM:
            // Print and write
            if (verbosityGiven >= verbosityNeeded) {
                (*_outStream) << message << std::flush;
                babLine.push(message);
            }
            break;
        case LOGGING_NONE:
        default:
            // Don't print or write
            break;
    }
}


/////////////////////////////////////////////////////////////////////////
// writes a message to outstream only without asking for vorbosities
void
Logger::print_message_to_stream_only(const std::string& message, const LOGGING_DESTINATION givenOutstreamVerbosity)
{
    if ((givenOutstreamVerbosity == LOGGING_FILE_AND_STREAM) || (givenOutstreamVerbosity == LOGGING_OUTSTREAM)) {
        (*_outStream) << message << std::flush;
    }
}


/////////////////////////////////////////////////////////////////////////
// sets output stream
void
Logger::set_output_stream(std::ostream* const outputStream)
{
    _outStream = outputStream;
}


/////////////////////////////////////////////////////////////////////////
// creates the log file
void
Logger::create_log_file(const LOGGING_DESTINATION givenOutstreamVerbosity)
{
    if ((givenOutstreamVerbosity == LOGGING_FILE_AND_STREAM) || (givenOutstreamVerbosity == LOGGING_FILE)) {
        std::ofstream logFile;
        logFile.open(logFileName, std::ios::out);
        logFile.close();
    }
}


/////////////////////////////////////////////////////////////////////////
// creates the csv file
void
Logger::create_iterations_csv_file(const bool writeCsv)
{
    if (writeCsv) {
        std::ofstream iterationsFile(csvIterationsName, std::ios::out);

        iterationsFile << " Iters,"
#ifdef MAiNGO_DEBUG_MODE
                       << " NodeId,"
                       << " NodeLBD,"
#endif
                       << " LBD, "
                       << " UBD,"
                       << " NodesLeft,"
                       << " AbsGap,"
                       << " RelGap,"
                       << " CPU" << std::endl;

        iterationsFile.close();
    }
}


/////////////////////////////////////////////////////////////////////////
// writes all lines currently stored in babLine to logFile
void
Logger::write_all_lines_to_log(const std::string& errorMessage)
{
    std::ofstream logFile;
    logFile.open(logFileName, std::ios::app);
    while (babLine.size() > 0) {
        logFile << babLine.front();
        babLine.pop();
    }
    if (!errorMessage.empty()) {
        logFile << errorMessage << std::endl;
    }
    logFile.close();
}


/////////////////////////////////////////////////////////////////////////
// writes all lines currently stored in babLine to logFile
void
Logger::write_all_iterations_to_csv()
{
    std::ofstream iterationsFile(csvIterationsName, std::ios::app);

    while (babLineCsv.size() > 0) {
        iterationsFile << babLineCsv.front();
        babLineCsv.pop();
    }

    iterationsFile.close();
}


/////////////////////////////////////////////////////////////////////////
// saves a proper string when a user wants to read in a setting file
void
Logger::save_settings_file_name(const std::string& fileName, const bool fileFound)
{

    // User wants to read in a file
    _nSettingFiles++;
    const int mapNumber = -1 * _nSettingFiles;
    std::string str     = "";
    if (fileFound) {
        // If file has been found, generate string
        str = "\n  Read settings from file " + fileName + ".";
    }
    else {
        // If file has not been found generate a different string
        if (fileName == "MAiNGOSettings.txt") {
            str = "\n  Warning: Could not open settings file with default name " + fileName + ".\n";
        } else {
            str = "\n  Warning: Could not open settings file " + fileName + ".\n";
        }
        str += "           Proceeding with default settings.";
    }
    // Then insert this string at a proper position in the map
    _userSetSettings[mapNumber] = str;
}


/////////////////////////////////////////////////////////////////////////
// save a user-set setting in map
void
Logger::save_setting(const SETTING_NAMES settingName, const std::string& str)
{

    switch (settingName) {
        case UNKNOWN_SETTING: {
            int wrongSettings = static_cast<int>(settingName);
            while (_userSetSettings.find(wrongSettings) != _userSetSettings.end()) {
                wrongSettings++;
            }
            _userSetSettings[wrongSettings] = str;
        } break;
        default:
            // Replace/insert the new setting string
            _userSetSettings[static_cast<int>(settingName)] = str;
            break;
    }
}


/////////////////////////////////////////////////////////////////////////
// print and or write user-set settings
void
Logger::print_settings(const VERB verbosityGiven, const VERB verbosityNeeded, const LOGGING_DESTINATION givenOutstreamVerbosity)
{

    // First check if any setting was changed at all
    if (!_userSetSettings.empty()) {
        bool someSettingChanged = (_userSetSettings.rbegin()->first > 0);    // This checks if there is at least one entry with a positive key, since these belong to the actual settings


        // If so, we print two additional lines two frame the actual settings (otherwise, we only give output about potential read attempts to empty or non-existing settings files
        if (someSettingChanged) {
            _userSetSettings[0] = "Settings set by the user:";
        }
        std::string str = "";
        for (std::map<int, std::string>::iterator it = _userSetSettings.begin(); it != _userSetSettings.end(); ++it) {
            if (it->first > 0) {
                str += "    " + (it->second) + "\n";
            }
            else {
                str += "  " + (it->second) + "\n";
            }
        }
        if (someSettingChanged) {
            str += "  Done.\n";
        }
        print_message(str, verbosityGiven, verbosityNeeded, givenOutstreamVerbosity);
    }
}


/////////////////////////////////////////////////////////////////////////
// clear logging information
void
Logger::clear()
{
    babLine            = std::queue<std::string>();
    babLineCsv         = std::queue<std::string>();
    reachedMinNodeSize = false;
}