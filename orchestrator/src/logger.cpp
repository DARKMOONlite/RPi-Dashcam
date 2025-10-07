#include <logger.hpp>
#include <dss/dds.hpp>

using namespace dashcam;


Logger::Logger(std::string const& log_file, LogLevel log_level) : log_file_(log_file), log_level_(log_level) {

}
Logger::~Logger(){

}
bool Logger::initialise(){
    return true;
}
void Logger::debug(const std::string& message){

}
void Logger::info(const std::string& message){
}
void Logger::warning(const std::string& message){
}
void Logger::error(const std::string& message){
}
void Logger::critical(const std::string& message){
}
void Logger::set_log_level(LogLevel level){
    log_level_ = level;

}
