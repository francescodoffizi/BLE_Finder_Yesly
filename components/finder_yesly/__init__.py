import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

CODEOWNERS = ["@francescodoffizi"]
DEPENDENCIES = ["esp32"]
AUTO_LOAD = ["api"]

finder_yesly_ns = cg.esphome_ns.namespace("finder_yesly")
FinderYeslyComponent = finder_yesly_ns.class_("FinderYeslyComponent", cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(FinderYeslyComponent),
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    cg.add_define("USE_API_HOMEASSISTANT_SERVICES")
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

