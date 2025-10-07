#include <module_manager.hpp>
using namespace dashcam;

ModuleManager::ModuleManager(Logger* logger){}
ModuleManager::~ModuleManager(){}
bool ModuleManager::initialize(){}
bool ModuleManager::shutdown(){}
bool ModuleManager::start_module(const std::string& module_id){}
bool ModuleManager::stop_module(const std::string& module_id){}
bool ModuleManager::restart_module(const std::string& module_id){}
bool ModuleManager::configure_module(const std::string& module_id, const std::string& config){}
