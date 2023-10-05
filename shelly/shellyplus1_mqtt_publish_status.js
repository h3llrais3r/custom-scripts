let mqttTopicPrefix = null; // set at startup by reading the Mqtt.GetConfig result

function setMqttTopicPrefix() {
    Shelly.call("MQTT.GetConfig", {}, function (result, error_code, error_message) {
        if (error_code === 0) {
            mqttTopicPrefix = result.topic_prefix;
            print("Mqtt topic prefix: " + mqttTopicPrefix);
        } else {
            print("MQTT.GetConfig error: " + error_message);
        }
    });
}

// Publish all statuses
function publishAllStatuses() {
    Shelly.call("Shelly.GetStatus", {}, function (result, error_code, error_message) {
        if (error_code === 0) {
            // GetStatus result contains status per component, so let loop over them and publish it for each component individually
            let components = Object.keys(result);
            components.forEach(function (component) {
                let componentStatus = result[component];
                MQTT.publish(mqttTopicPrefix + "/status/" + component, JSON.stringify(componentStatus));
            });
        } else {
            print("Shelly.GetStatus error: " + error_message);
        }
    });
};

// Start script
setMqttTopicPrefix();
publishAllStatuses();
