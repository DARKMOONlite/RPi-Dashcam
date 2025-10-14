#ifndef ORCHESTRATOR
#define ORCHESTRATOR

#include <string>
#include <vector>
#include <unordered_map>
#include <memory>
#include <chrono>
#include <config_manager.hpp>
#include <module_manager.hpp>
#include <logger.hpp>
#include <data_types.hpp>
namespace dashcam {


/**
 * @brief Main orchestrator class that coordinates the entire dashcam system
 * 
 * The Orchestrator is responsible for:
 * - Managing module lifecycle (start, stop, monitor)
 * - Coordinating data flow between modules via DDS
 * - Handling system configuration and pipeline management
 * - Providing centralized logging and error handling
 * - Exposing control interfaces for external management
 */
class Orchestrator {
public:
    explicit Orchestrator(const std::string& config_file = "");
    ~Orchestrator();




    // Run the main orchestrator loop
    void run();


    //getters for core components
    std::shared_ptr<Logger> get_logger() const { return logger_; }
    std::shared_ptr<ConfigManager> get_config_manager() const { return config_manager_; }
    std::shared_ptr<ModuleManager> get_module_manager() const { return module_manager_; }

private:
    // Core components
    std::shared_ptr<ModuleManager> module_manager_;
    std::shared_ptr<ConfigManager> config_manager_;
    std::shared_ptr<Logger> logger_;
    
};

} // namespace dashcam

#endif