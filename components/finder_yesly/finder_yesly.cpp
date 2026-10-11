#include "finder_yesly.h"
#include "esphome/core/log.h"

namespace esphome {
namespace finder_yesly {

static const char *const TAG = "finder_yesly";

void FinderYeslyComponent::setup() {
  ESP_LOGI(TAG, "Finder YESLY Component initialized successfully");
}

void FinderYeslyComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "Finder YESLY Mesh Gateway:");
}

}  // namespace finder_yesly
}  // namespace esphome
