#ifndef ORCHESTRATOR_LOGGER
#define ORCHESTRATOR_LOGGER
#include <string>
#include <memory>
#include <fstream>
#include <mutex>
#include <chrono>
#include <ddscxx/dds/dds.hpp>
#include <data_types.hpp>
namespace dashcam {



/**
 * @brief simple thread-safe logging system for the dashcam orchestrator
 */
class Logger {
public:
    explicit Logger(const std::string& log_file = "", LogLevel log_level = LogLevel::Debug);
    ~Logger();

    // Initialization
    bool initialise();
    
    // Logging methods
    void debug(const std::string& message);
    void info(const std::string& message);
    void warning(const std::string& message);
    void error(const std::string& message);
    void critical(const std::string& message);
    
    // Configuration
    void set_log_level(LogLevel level);

    private:
    std::string log_file_;
    LogLevel log_level_;
    std::string logging_topic_;

    void log_callback(const std::string& message, LogMessage log_info);

};

} // namespace dashcam


#endif