#include <module_manager.hpp>
using namespace dashcam;

ModuleManager::ModuleManager(Logger* logger){}
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
bool ModuleManager::start_module(ModuleInfo module_info){
    
}
bool ModuleManager::start_module(const std::string& module_id){}
bool ModuleManager::stop_module(const std::string& module_id){}
bool ModuleManager::restart_module(const std::string& module_id){}
bool ModuleManager::configure_module(const std::string& module_id, const std::string& config){}
