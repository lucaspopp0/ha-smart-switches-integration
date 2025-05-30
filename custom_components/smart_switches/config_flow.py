from homeassistant import data_entry_flow
from homeassistant.data_entry_flow import section
from homeassistant.helpers.selector import selector
import voluptuous as vol

DOMAIN="smart_switches"

class ExampleConfigFlow(data_entry_flow.FlowHandler, domain=DOMAIN):
    """Example config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1
