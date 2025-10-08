#ifndef ORCHESTRATORCONFIGMANAGER
#define ORCHESTRATORCONFIGMANAGER

#include <string>
#include <memory>
#include <vector>
#include <data_types.hpp>
#include <nlohmann/json.hpp>

#include <logger.hpp>
#include <module_manager.hpp>


#include <fstream>
using json = nlohmann::json;
namespace dashcam {

class Logger;


/**
 * @brief Manages system configuration using JSON, 
 */
class ConfigManager {
public:
    explicit ConfigManager(Logger* logger, std::string file_path);
    ~ConfigManager();




    // getters for specific pieces of information from the json file
    bool get_module_info(const std::string& module_id, ModuleInfo & module_info_struct);
    bool get_launch_modules(ModuleLaunchOrder & modules_struct);
    bool get_dds_info(DDSInfo & dds_struct);
    bool get_logging_info(LoggingInfo & logging_struct);

    // setters for specific pieces of information from the json file
    // bool set_module_config(const std::string& module_id, const std::map<std::string,std::variant<int,float,std::string>>& config);
    // bool set_json_value(const std::string& json_pointer, std::variant<int, float, std::string> value);




private:
    json load_config(const std::string& file_path);
    bool save_config(const std::string& file_path) const;

    Logger* logger_;
    const json config_data;
    std::vector<ModuleInfo> modules_;
};

} // namespace dashcam

#endif