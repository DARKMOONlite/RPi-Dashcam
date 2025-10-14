#include <module_manager.hpp>
using namespace dashcam;

ModuleManager::ModuleManager(std::shared_ptr<Logger> logger) : logger_(logger) {}
ModuleManager::~ModuleManager(){}

bool ModuleManager::initialize(const ModuleLaunchOrder & modules){
    modules_to_launch = modules;
    if(modules.auto_start_modules == true){
        start();
    }
}

bool ModuleManager::shutdown(){}
bool ModuleManager::start(){
    for (auto module : modules_to_launch.modules){
        start_module(module);

    }    
}

bool ModuleManager::start_module(const std::string& module_id){
    for(auto mod : modules_to_launch.modules){
        if(mod.id==module_id){
            start_module(mod);
        }
    }
}
bool ModuleManager::start_module(ModuleInfo mod){
    std::cout << "starting module :" << mod.name << " with path: " << mod.executable_path << "\n";

    // Create thread by passing the member function and its arguments
    std::thread launchThread(&ModuleManager::run_module_thread, this, mod.language, mod.executable_path, mod.command_args, mod.config);
    
    // Detach the thread so it can run independently
    launchThread.detach();
    
    return true;
}

int ModuleManager::run_module_thread(Languages language, std::string executable,std::vector<std::string> command_args, std::map<std::string,std::variant<int,float,std::string>> configuration){
    switch (language){
        case Languages::C:
        break;
        default:
        break;

    }
 return(0);
}

bool ModuleManager::stop_module(const std::string& module_id){}
bool ModuleManager::restart_module(const std::string& module_id){}
bool ModuleManager::configure_module(const std::string& module_id, const std::string& config){}
