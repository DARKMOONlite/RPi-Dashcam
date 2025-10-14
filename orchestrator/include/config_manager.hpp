#ifndef ORCHESTRATORCONFIGMANAGER
#define ORCHESTRATORCONFIGMANAGER

#include <string>
#include <memory>
#include <vector>
#include <data_types.hpp>
#include <nlohmann/json.hpp>
#include <optional>
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
    explicit ConfigManager(std::shared_ptr<Logger> logger, std::string file_path);
    ~ConfigManager();




    // getters for specific pieces of information from the json file
    std::optional<ModuleInfo> get_module_info(const std::string& module_id) const;
    std::optional<ModuleLaunchOrder> get_launch_modules() const;
    std::optional<DDSInfo> get_dds_info() const;
    std::optional<LoggingInfo> get_logging_info() const;

    // setters for specific pieces of information from the json file
    // bool set_module_config(const std::string& module_id, const std::map<std::string,std::variant<int,float,std::string>>& config);
    // bool set_json_value(const std::string& json_pointer, std::variant<int, float, std::string> value);


    friend std::ostream& operator<< (std::ostream& os, const ConfigManager& configmanager){
        os << std::string(get_terminal_width()/3,'-') << "  MODULE INFO  " << std::string(get_terminal_width()/3,'-') << std::endl;
        os << configmanager.get_launch_modules().value_or(dashcam::ModuleLaunchOrder()) << "\n";
        os << std::string(get_terminal_width()/3,'-') << "  DDS INFO  " << std::string(get_terminal_width()/3,'-') << std::endl;
        os << configmanager.get_dds_info().value_or(dashcam::DDSInfo()) << "\n";
        os << std::string(get_terminal_width()/3,'-') << "  LOGGING INFO  " << std::string(get_terminal_width()/3,'-') << std::endl;
        os << configmanager.get_logging_info().value_or(dashcam::LoggingInfo()) << "\n";
        return os;
    }

private:
    std::optional<json> load_config(const std::string& file_path);
    bool save_config(const std::string& file_path) const;

    std::shared_ptr<Logger> logger_;
    const json config_data_;
    std::vector<ModuleInfo> modules_;
};

} // namespace dashcam

#endif