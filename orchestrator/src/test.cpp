#include <orchestrator.hpp>
#include <data_types.hpp>
#include <iostream>
int main() {
    dashcam::Orchestrator orchestrator("config/default_config.json");
    // orchestrator.run();
    
    // Store the shared_ptr in a variable first, then take its address
    auto config_manager = orchestrator.get_config_manager();
    std::cout << *config_manager;

    auto module_manager = orchestrator.get_module_manager();
    module_manager->initialize(config_manager->get_launch_modules().value());
    module_manager->start();

    return 0;
}