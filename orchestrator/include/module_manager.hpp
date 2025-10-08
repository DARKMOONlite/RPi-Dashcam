#ifndef ORCHESTRATOR_MODULE_MANAGER
#define ORCHESTRATOR_MODULE_MANAGER 

#include <string>
#include <unordered_map>
#include <vector>
#include <memory>
#include <mutex>
#include <chrono>
#include <thread>
#include <data_types.hpp>
namespace dashcam {

// Forward declarations
class Logger;



/**
 * @brief Manages the lifecycle and monitoring of all system modules
 * 
 * The ModuleManager is responsible for:
 * - Discovering and registering modules
 * - Starting and stopping module processes
 * - Monitoring module health via heartbeats
 * - Handling module crashes and auto-restart
 * - Managing module dependencies and startup order
 */
class ModuleManager {
public:
    ModuleManager(Logger* logger);
    ~ModuleManager();

    // Lifecycle management
    bool initialize(const ModuleLaunchOrder & modules);
    bool shutdown();
    bool start();

    // Module control
    bool start_module(const std::string& module_id);
    bool start_module(ModuleInfo module_info);
    bool stop_module(const std::string& module_id);
    bool restart_module(const std::string& module_id);
    bool configure_module(const std::string& module_id, const std::string& config);
    private:
    Logger* logger_;
    ModuleLaunchOrder modules_to_launch
};

} // namespace dashcam


#endif