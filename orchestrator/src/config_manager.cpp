#include <config_manager.hpp>
using namespace dashcam;

ConfigManager::ConfigManager(std::shared_ptr<Logger> logger, std::string file_path): 
    logger_(logger), 
    config_data_(load_config(file_path).value_or(json()))
    {
    if (config_data_.is_null()){
        logger_->critical("Failed to load configuration file: " + file_path);
        // throw std::runtime_error("Failed to load configuration file: " + file_path);
    } else {
        logger_->info("Configuration file loaded successfully: " + file_path);
    }

}

ConfigManager::~ConfigManager(){

}

std::optional<json> ConfigManager::load_config(const std::string& file_path){
    std::ifstream file(file_path);
    if (!file.is_open()) {
        logger_->error("Failed to open config file: " + file_path);
        return std::nullopt;
    }
    return json::parse(file);
}
bool ConfigManager::save_config(const std::string& file_path) const {
    
return(true);
}

// bool ConfigManager::set_json_value(const std::string& json_pointer, std::variant<int, float, std::string> value){
//     try {
//         json::json_pointer ptr(json_pointer);
//         if (std::holds_alternative<int>(value)) {
//             config_data[ptr] = std::get<int>(value);
//         } else if (std::holds_alternative<float>(value)) {
//             config_data[ptr] = std::get<float>(value);
//         } else if (std::holds_alternative<std::string>(value)) {
//             config_data[ptr] = std::get<std::string>(value);
//         } else {
//             logger_->error("Unsupported variant type for JSON value");
//             return false;
//         }
        
//     } catch (const std::exception& e) {
//         logger_->error(std::string("Failed to set JSON value: ") + e.what());
//         return false;
//     }
// }

std::optional<ModuleInfo> ConfigManager::get_module_info(const std::string& module_id) const{
    ModuleInfo module_info_struct;
    for (const auto& module_ : config_data_.at("modules")){
        if (module_["id"] == module_id) {
            module_info_struct.id = module_.value("id","");
            module_info_struct.name = module_.value("name","");
            module_info_struct.type = fromString<ModuleType>(module_.value("type","")).value_or(ModuleType::Unknown);
            module_info_struct.language = fromString<Languages>(module_.value("language","")).value_or(Languages::Unknown);
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
            return module_info_struct;
        }
    }
    return std::nullopt;

}

std::optional<ModuleLaunchOrder> ConfigManager::get_launch_modules() const{
    ModuleLaunchOrder modules_struct;
    if (config_data_.contains("startup_order")){
        for (const auto& module_ : config_data_.at("startup_order")){
            if (module_.contains("modules")){
                for (const auto& mod : module_["modules"]){
                    auto mod_info = get_module_info(mod.get<std::string>());
                    if (mod_info.has_value()){
                        modules_struct.modules.push_back(mod_info.value());
                    } 
                    else{
                        logger_->warning("Module ID " + mod.get<std::string>() + " in startup_order not found in modules list");
                    }
                }
            }
        }
    } 

    if (config_data_.contains("modules")|| (config_data_.contains("startup_order") && config_data_.at("startup_order").size()==0)){
        logger_->warning("No startup_order found, loading all modules in modules list in the order they are listed");

        for (const auto& module_ : config_data_.at("modules")){
            auto mod_info = get_module_info(module_["id"].get<std::string>());
            modules_struct.modules.push_back(mod_info.value());
        }
    } 
    else{
        return std::nullopt;
    }

        modules_struct.module_directories = config_data_.value("module_directories",std::vector<std::string>{});
        modules_struct.auto_start_modules = config_data_.value("auto_start_modules",false);
    return modules_struct;
}

std::optional<DDSInfo> ConfigManager::get_dds_info() const{
    DDSInfo dds_struct;
    if (config_data_.contains("dds")){
        const auto& dds_config = config_data_.at("dds");
        dds_struct.domain_id = dds_config.value("domain_id",0);
        dds_struct.qos_profile = dds_config.value("qos_profile","default");
        dds_struct.discovery_timeout_ms = dds_config.value("discovery_timeout_ms",1000);
        dds_struct.heartbeat_interval_ms = dds_config.value("heartbeat_interval_ms",5000);
        return dds_struct;
    } else {
        logger_->warning("No dds configuration found");
        return std::nullopt;
    }
}

std::optional<LoggingInfo> ConfigManager::get_logging_info() const{
    LoggingInfo logging_struct;
    if (config_data_.contains("logging")){
        const auto& log_config = config_data_.at("logging");
        logging_struct.file = log_config.value("log_file","dashcam.log");
        logging_struct.logging_topic_string = log_config.value("logging_topic","/logging");
        return logging_struct;
    } else {
        logger_->warning("No logging configuration found");
        return std::nullopt;
    }
}
