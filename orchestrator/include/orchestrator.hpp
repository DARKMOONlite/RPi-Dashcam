#ifndef ORCHESTRATOR
#define ORCHESTRATOR

#include <string>
#include <vector>
#include <unordered_map>
#include <memory>
#include <chrono>

namespace dashcam {

// Forward declarations
class ModuleManager;
class ConfigManager;
class Logger;


// struct OrchestratorConfig {
//     unsigned int heartbeat_interval_ms;
//     unsigned int module_check_interval_ms;
//     bool auto_restart_modules;
//     int logging_level;
// };

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


    // // Module management
    // bool start_module(const std::string& module_id);
    // bool stop_module(const std::string& module_id);
    // bool restart_module(const std::string& module_id);
    // std::vector<std::string> list_modules() const;
    
    // // Pipeline management
    // bool start_pipeline(const std::string& pipeline_id);
    // bool stop_pipeline(const std::string& pipeline_id);
    // bool create_pipeline(const std::string& pipeline_config);
    // std::vector<std::string> list_pipelines() const;

    // Run the main orchestrator loop
    void run();

private:
    // Core components
    // std::unique_ptr<ModuleManager> module_manager_;
    // std::unique_ptr<ConfigManager> config_manager_;
    // std::unique_ptr<Logger> logger_;
    
};

} // namespace dashcam

#endif