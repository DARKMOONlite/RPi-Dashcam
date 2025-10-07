#include <nlohmann/json.hpp>
#include <config_manager.hpp>
#include <logger.hpp>
#include <module_manager.hpp>


#include <fstream>
using json = nlohmann::json;


using namespace dashcam;

ConfigManager::ConfigManager(Logger* logger, std::string file_path): config_data(load_config(file_path)) {

}

ConfigManager::~ConfigManager(){

}

json ConfigManager::load_config(const std::string& file_path){
    std::ifstream file(file_path);
    return(json::parse(file));
}
bool ConfigManager::save_config(const std::string& file_path) const {
    

}


bool ConfigManager::get_module_info(const std::string& module_id, ModuleInfo & module_info_struct){
    for (const auto& module_ : config_data.at("modules")){
        if (module_["id"] == module_id) {
            module_info_struct.module_id = module_.value("id","");
            module_info_struct.module_name = module_.value("name","");
            module_info_struct.type = string_to_module_type.at(module_.value("type",""));
            module_info_struct.language = module_.value("language","");
            module_info_struct.executable_path = module_.value("executable","");
            module_info_struct.auto_restart = module_.value("auto_restart",false);

            for (const auto& config : module_["config"].items()){
                const std::string& key = config.key();
                const auto& value = config.value();
                if (value.is_number_integer()) {
                    module_info_struct.config[key] = value.get<int>();
                } else if (value.is_number_float()) {
                    module_info_struct.config[key] = value.get<float>();
                } else if (value.is_string()) {
                    module_info_struct.config[key] = value.get<std::string>();
                }
                else {
                    logger_->warning("Unsupported config type for key: " + key);
                }
            }

            // Add other fields as needed, depending on ModuleInfo definition
            return true;
        }
    }
    return false;

}

bool ConfigManager::get_launch_modules(ModuleLaunchOrder & modules_struct){
    if (config_data.contains("module_launch_order")){
        for (const auto& module_id : config_data.at("module_launch_order")){
            ModuleInfo module_info;
            if (get_module_info(module_id, module_info)){
                modules_struct.modules.push_back(module_info);
            } else {
                logger_->warning("Module ID in launch order not found in modules: " + module_id);
                return false;
            }
        }
    } else {
        logger_->warning("No module_launch_order found in configuration");
        return false;
    }

    if (config_data.contains("module_directories")){
        for (const auto& dir : config_data.at("module_directories")){
            modules_struct.module_directories.push_back(dir);
        }
    } else {
        logger_->warning("No module_directories found in configuration");
        return false;
    }

    modules_struct.auto_start_modules = config_data.value("auto_start_modules", false);

    return true;
}

bool ConfigManager::get_dds_info(DDSInfo & dds_struct){
    if (config_data.contains("dds")){
        const auto& dds_config = config_data.at("dds");
        dds_struct.domain_id = dds_config.value("domain_id",0);
        dds_struct.qos_profile = dds_config.value("qos_profile","default");
        dds_struct.discovery_timeout_ms = dds_config.value("discovery_timeout_ms",1000);
        dds_struct.heartbeat_interval_ms = dds_config.value("heartbeat_interval_ms",5000);
        return true;
    } else {
        logger_->warning("No dds configuration found");
        return false;
    }
}


bool ConfigManager::get_logging_info(LoggingInfo & logging_struct){
    if (config_data.contains("logging")){
        const auto& log_config = config_data.at("logging");
        logging_struct.file = log_config.value("log_file","dashcam.log");
        logging_struct.logging_topic_string = log_config.value("logging_topic","/logging");
        return true;
    } else {
        logger_->warning("No logging configuration found");
        return false;
    }
}
