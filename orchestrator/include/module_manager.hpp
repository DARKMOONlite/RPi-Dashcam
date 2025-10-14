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
    ModuleManager(std::shared_ptr<Logger> logger);
    ~ModuleManager();

    // Lifecycle management
    bool initialize(const ModuleLaunchOrder & modules);
    bool shutdown();
    bool start();

    // Module control
    bool start_module(const std::string& module_id);
    bool start_module(ModuleInfo module_info);
    int run_module_thread(Languages language, std::string executable,std::vector<std::string> command_args, std::map<std::string,std::variant<int,float,std::string>> configuration);
    bool stop_module(const std::string& module_id);
    bool restart_module(const std::string& module_id);
    bool configure_module(const std::string& module_id, const std::string& config);
    private:
    std::shared_ptr<Logger> logger_;
    ModuleLaunchOrder modules_to_launch;

    private:
    // functions for creating each module's process
    int create_cpp_process();
    int create_rust_process();
    int create_py_process();
    int create_go_process();
    int create_zig_process();

    //functions for stoping each module's process
    bool stop_cpp_process();
    bool stop_rust_process();
    bool stop_py_process();
    bool stop_go_process();
    bool stop_zig_process();

    bool cleanup(); // cleanup loose threads/processes

    bool monitor_heartbeat();


};

} // namespace dashcam


#endif