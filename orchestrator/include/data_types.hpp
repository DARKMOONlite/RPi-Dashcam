#ifndef DASHCAM_DATA_TYPES_HPP
#define DASHCAM_DATA_TYPES_HPP

#include <vector>
#include <string>
#include <string_view>
#include <chrono>
#include <magic_enum.hpp>
#include <variant>
#include <sys/ioctl.h>
#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <map>

namespace dashcam {

inline u_int64_t get_terminal_width() {
    int cols = 0;
    int lines = 0;
    #ifdef TIOCGSIZE
        struct ttysize ts;
        ioctl(STDIN_FILENO, TIOCGSIZE, &ts);
        cols = ts.ts_cols;
        lines = ts.ts_lines;
    #elif defined(TIOCGWINSZ)
        struct winsize ts;
        ioctl(STDIN_FILENO, TIOCGWINSZ, &ts);
        cols = ts.ws_col;
        lines = ts.ws_row;
    #endif /* TIOCGSIZE */
    return cols;
}


/**
 * @brief Function that allows converting std::variants into string
 * so long as all the options of the variant can be converted to a string
 *      std::visit(VariantLambda{}, "the variant goes here" )
 * @tparam T : just used internally as it captures the type of whats passed in and checks if its a string
 * @param variant the std::variant to pass in
 * @return std::string the stringified variant.
 */
struct VariantLambda{
    template<typename T>
    std::string operator()(const T &variant) const{
        if constexpr (std::is_same_v<T, std::string>) {
            return variant;
        } else {
            return std::to_string(variant);
        }
    }
};


enum class DataDecimal {
    B = 0,
    KB = 3,
    MB = 6,
    GB = 9,
    TB = 12
} ;

enum class LogLevel {
    Debug = 0,
    Info = 1,
    Warning = 2,
    Error = 3,
    Critical = 4
};
enum class ModuleState {
    Unknown,
    Starting,
    Running,
    Stopping,
    Stopped,
    Error
};

enum class ModuleType{
    Unknown,
    CameraInterface,
    Filter,
    NeuralNetwork,
    StreamEncoder,
    WebInterface,
    Orchestrator,
};

enum class Languages{
    Unknown,
    C,
    Cplusplus,
    Python,
    Rust,
    JavaScript,

};

using magic_enum::enum_name;
using magic_enum::enum_cast;

inline std::string_view toString(ModuleState type){
    return(enum_name(type));
}
inline std::string_view toString(ModuleType type){
    return(enum_name(type));
}
inline std::string_view toString(LogLevel type){
    return(enum_name(type));
}
inline std::string_view toString(DataDecimal type){
    return(enum_name(type));
}
inline std::string_view toString(Languages type){
    return(enum_name(type));
}
template<typename T>
inline std::optional<T> fromString(std::string_view name) {
    return enum_cast<T>(name);
}




struct LogMessage {
    time_t timestamp = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    LogLevel logging_level = LogLevel::Debug;
    std::string name;
    std::string message;
    // LogMessage(long _time, unsigned int _log_level, std::string _module_name) : timestamp(_time), logging_level(static_cast<LogLevel>(_log_level)), name(_module_name){} 

    friend std::ostream& operator<< (std::ostream&os, const LogMessage& log_info) {
        os << "Timestamp: " << std::asctime(std::localtime(&log_info.timestamp));
        os << "Log Level: " << toString(log_info.logging_level) << "\n";
        os << "Module Name: " << log_info.name << "\n";
        os << "Message: " << log_info.message << "\n";
        return os;
    }
};

struct LoggingInfo{
    LogLevel logging_level = LogLevel::Debug;
    std::string logging_topic_string;
    std::string file;
    std::uint16_t max_size = 5;
    DataDecimal max_size_unit = DataDecimal::GB;
    bool console_output = true;
    bool file_output = false;

    friend std::ostream& operator<< (std::ostream&os, const LoggingInfo& log_info) {
        os << "Logging Level: " << toString(log_info.logging_level) << "\n";
        os << "Logging Topic: " << log_info.logging_topic_string << "\n";
        os << "Log File: " << log_info.file << "\n";
        os << "Max Size: " << log_info.max_size << " " << toString(log_info.max_size_unit) << "\n";
        os << "Console Output: " << (log_info.console_output ? "Yes" : "No") << "\n";
        os << "File Output: " << (log_info.file_output ? "Yes" : "No") << "\n";
        return os;
    }
};




struct ModuleInfo {
    std::string id;
    std::string name;
    ModuleType type;
    ModuleState state = ModuleState::Unknown;
    std::string version;
    Languages language;
    std::vector<std::string> input_topics;
    std::vector<std::string> output_topics;
    std::string config_schema;
    std::map<std::string,std::variant<int,float,std::string>> config;
    std::string description;
    std::chrono::steady_clock::time_point last_heartbeat = std::chrono::steady_clock::now();
    std::string executable_path;
    std::vector<std::string> command_args;
    int process_id = -1;
    bool auto_restart = false;
    int restart_count = 0;
    std::chrono::steady_clock::time_point last_restart = std::chrono::steady_clock::now();

    friend std::ostream& operator<< (std::ostream& os, const ModuleInfo& module) {
        os << "Module ID: " << module.id << "\n";
        os << "Module Name: " << module.name << "\n";
        os << std::string(get_terminal_width()/2, '-') << "\n";
        os << "Type: " << toString(module.type) << "\n";
        os << "State: " << toString(module.state) << "\n";
        os << "Version: " << module.version << "\n";
        os << "Language: " << toString(module.language) << "\n";
        os << "Executable Path: " << module.executable_path << "\n";
        os << "Command Args: ";
        for (const auto& arg : module.command_args) {
            os << arg << " ";
        }
        os << "Config Settings: \n";
        for (const auto& config: module.config){
            os << "   " << config.first << " : " << std::visit(VariantLambda{},config.second) << "\n";
        }
        os << "\n";
        os << "Process ID: " << module.process_id << "\n";
        os << "Auto Restart: " << (module.auto_restart ? "Yes" : "No") << "\n";
        os << "Restart Count: " << module.restart_count << "\n";
        return os;
    }
};

struct ModuleLaunchOrder {
    std::vector<ModuleInfo> modules; // sorted list of modules
    std::vector<std::string> module_directories; // directories to look for modules at
    bool auto_start_modules;

    friend std::ostream& operator<< (std::ostream& os, const ModuleLaunchOrder& launch_order) {
        os << "Auto Start Modules: " << (launch_order.auto_start_modules ? "Yes" : "No") << "\n";
        os << "Module Directories: ";
        for (const auto& dir : launch_order.module_directories) {
            os << dir << " ";
        }
        os << "\n";
        os << "Modules to Launch:\n";
        for (const auto& module : launch_order.modules) {
            os << std::string(get_terminal_width(), '-') << "\n";
            os << module << "\n";
        }
        return os;
    }
};



struct DDSInfo {
    std::int32_t domain_id;
    std::string qos_profile;
    unsigned int discovery_timeout_ms;
    unsigned int heartbeat_interval_ms;

    friend std::ostream& operator<< (std::ostream&os, const DDSInfo& dds_info) {
        os << "Domain ID: " << dds_info.domain_id << "\n";
        os << "QoS Profile: " << dds_info.qos_profile << "\n";
        os << "Discovery Timeout (ms): " << dds_info.discovery_timeout_ms << "\n";
        os << "Heartbeat Interval (ms): " << dds_info.heartbeat_interval_ms << "\n";
        return os;
    }
};

} // namespace dashcam

#endif // DASHCAM_DATA_TYPES_HPP