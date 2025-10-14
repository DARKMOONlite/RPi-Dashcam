#ifndef ORCHESTRATOR_BASE_MODULE
#define ORCHESTRATOR_BASE_MODULE

#include <ddscxx/dds/dds.hpp>
#include <nlohmann/json.hpp>

class BaseDDSModule {
public:
    BaseDDSModule();
    ~BaseDDSModule();
    void configure_callback();
    bool start();
    bool stop();
    void init_module();
    void shutdown_module();
    void get_status();
    void get_metrics();

private:
    nlohmann::json config;
};


#endif