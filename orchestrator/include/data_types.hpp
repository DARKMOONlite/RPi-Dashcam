#include <vector>
#include <string>
#include <chrono>
#include <map>
#include <variant>


enum class DataDecimal : u_int64_t {
    B = u_int64_t(1),
    KB = u_int64_t(1e3),
    MB = u_int64_t(1e6),
    GB = u_int64_t(1e9),
    TB = u_int64_t(1e12),
} ;

enum class LogLevel {
    Debug = 0,
    Info = 1,
    Warning = 2,
    Error = 3,
    Critical = 4
};

struct LogMessage {
    time_t timestamp = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    LogLevel logging_level = LogLevel::Debug;
    std::string module_name;
    // LogMessage(long _time, unsigned int _log_level, std::string _module_name) : timestamp(_time), logging_level(static_cast<LogLevel>(_log_level)), module_name(_module_name){} 
};

struct LoggingInfo{
    LogLevel logging_level;
    std::string logging_topic_string;
    std::string file;
    std::uint16_t max_size;
    DataDecimal max_size_unit = DataDecimal::MB;
    bool console_output = true;
    bool file_output = false;
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
    Orchestrator
};

std::map<std::string,ModuleType> string_to_module_type = {
    {"",ModuleType::Unknown},
    {"camera_interface" , ModuleType::CameraInterface},
    {"filter", ModuleType::Filter} ,
    {"neural_network", ModuleType::NeuralNetwork} ,
    {"stream_encoder", ModuleType::StreamEncoder} ,
    {"web_interface", ModuleType::WebInterface} ,
    {"Orchestrator", ModuleType::Orchestrator}
};

struct ModuleInfo {
    std::string module_id;
    std::string module_name;
    ModuleType type;
    ModuleState state;
    std::string version;
    std::string language;
    std::vector<std::string> input_topics;
    std::vector<std::string> output_topics;
    std::string config_schema;
    std::map<std::string,std::variant<int,float,std::string>> config;
    std::string description;
    std::chrono::steady_clock::time_point last_heartbeat;
    std::string executable_path;
    std::vector<std::string> command_args;
    int process_id;
    bool auto_restart;
    int restart_count;
    std::chrono::steady_clock::time_point last_restart;
};

struct ModuleLaunchOrder {
    std::vector<::ModuleInfo> modules; // sorted list of modules
    std::vector<std::string> module_directories; // directories to look for modules at
    bool auto_start_modules;
};



struct DDSInfo {
    std::int32_t domain_id;
    std::string qos_profile;
    unsigned int discovery_timeout_ms;
    unsigned int heartbeat_interval_ms;
};
