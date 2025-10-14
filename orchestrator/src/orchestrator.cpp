#include <orchestrator.hpp>
#include <data_types.hpp>
using namespace dashcam;


Orchestrator::Orchestrator(const std::string& config_file):
    logger_(std::make_shared<Logger>())
{
    module_manager_ = std::make_unique<ModuleManager>(logger_);
    config_manager_ = std::make_unique<ConfigManager>(logger_, config_file);

}
Orchestrator::~Orchestrator(){

}
void Orchestrator::run(){
    
}
