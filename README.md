# Smart Switches Home Assistant Integration

A collection of custom Home Assistant components that provide smart switch functionality and example integrations.

## Components

### Hello World Async (`hello_world_async`)

A minimal example component demonstrating the basic structure of a Home Assistant custom component.

**Features:**
- Creates a simple entity with a "Works!" state
- Demonstrates async component setup
- Minimal configuration required

**Configuration:**
```yaml
hello_world_async:
```

### MQTT Basic Async (`mqtt_basic_async`)

An MQTT-based component that demonstrates how to communicate with MQTT brokers in Home Assistant.

**Features:**
- Subscribes to an MQTT topic and updates entity state with received messages
- Provides a service to publish messages to the configured topic
- Configurable MQTT topic
- Async implementation

**Configuration:**
```yaml
mqtt_basic_async:
  topic: "home-assistant/mqtt_example"  # Optional, defaults to "home-assistant/mqtt_example"
```

**Services:**
- `mqtt_basic_async.set_state`: Publishes a message to the configured MQTT topic
  - `new_state`: The message to publish (e.g., "on", "off", or any custom state)

## Installation

### Manual Installation

1. Copy the `custom_components` folder to your Home Assistant configuration directory
2. Restart Home Assistant
3. Add the desired component configuration to your `configuration.yaml`
4. Restart Home Assistant again

### HACS Installation

This integration is compatible with HACS (Home Assistant Community Store).

1. Add this repository as a custom repository in HACS
2. Install the "Smart Switches" integration
3. Restart Home Assistant
4. Add the component configuration to your `configuration.yaml`

## Usage Examples

### Hello World Component

After configuration, the component creates an entity `hello_world_async.Hello_World` with the state "Works!".

### MQTT Component

The MQTT component creates an entity `mqtt_example.last_message` that displays the last message received on the configured topic.

**Publishing a message via service:**
```yaml
service: mqtt_basic_async.set_state
data:
  new_state: "switch_on"
```

**Monitoring MQTT messages:**
The entity state will automatically update when messages are received on the configured topic.

## Development

These components serve as examples for developing custom Home Assistant integrations. They demonstrate:

- Async component setup patterns
- MQTT integration best practices
- Service registration and handling
- Entity state management
- Configuration validation

## Requirements

- Home Assistant 2021.12.0 or newer
- MQTT broker (for `mqtt_basic_async` component)

## License

This project follows Home Assistant's example component patterns and is provided for educational and development purposes.
