#include <orchestrator.hpp>


int main() {
    dashcam::Orchestrator orchestrator("config/default_config.json");
    orchestrator.run();
    return 0;
}