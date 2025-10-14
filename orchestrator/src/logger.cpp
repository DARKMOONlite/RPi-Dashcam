#include <logger.hpp>
#include <ddscxx/dds/dds.hpp>

using namespace dashcam;


Logger::Logger(std::string const& log_file, LogLevel log_level) : log_file_(log_file), log_level_(log_level) {

}
Logger::~Logger(){

}
bool Logger::initialise(){
    return true;
}
void Logger::debug(const std::string& message){
    LogMessage log;
    log.logging_level = LogLevel::Debug;
    log.name = "logger";
    log_callback(message,log);

}
void Logger::info(const std::string& message){
    LogMessage log;
    log.logging_level = LogLevel::Info;
    log.name = "logger" ;
    log_callback(message,log);
}
void Logger::warning(const std::string& message){
    LogMessage log;
    log.logging_level = LogLevel::Warning;
    log.name = "logger" ;
    log_callback(message,log);
}
void Logger::error(const std::string& message){
    LogMessage log;
    log.logging_level = LogLevel::Error;
    log.name = "logger" ;
    log_callback(message,log);
}
void Logger::critical(const std::string& message){
    LogMessage log;
    log.logging_level = LogLevel::Critical;
    log.name = "logger" ;
    log_callback(message,log);
}
void Logger::set_log_level(LogLevel level){
    log_level_ = level;
}



void Logger::log_callback(const std::string& message, LogMessage log_info){
    // Get current time
    if (log_info.logging_level < log_level_){
        return;
    }
    char time_str[100];
    std::strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", std::localtime(&log_info.timestamp));

    // Convert log level to string
    std::string level_str;
    switch (log_info.logging_level) {
        case LogLevel::Debug: level_str = "DEBUG"; break;
        case LogLevel::Info: level_str = "INFO"; break;
        case LogLevel::Warning: level_str = "WARNING"; break;
        case LogLevel::Error: level_str = "ERROR"; break;
        case LogLevel::Critical: level_str = "CRITICAL"; break;
        default: level_str = "UNKNOWN"; break;
    }

    // Format the log message
    std::string formatted_message = "[" + std::string(time_str) + "] [" + level_str + "] " + message;

    // Log to console
    std::cout << formatted_message << std::endl;
    
    // Log to file if specified
    if (!log_file_.empty()) {
        std::ofstream ofs(log_file_, std::ios_base::app);
        if (ofs.is_open()) {
            ofs << formatted_message << std::endl;
            ofs.close();
        } else {
            std::cerr << "Failed to open log file: " << log_file_ << std::endl;
        }
    }


}