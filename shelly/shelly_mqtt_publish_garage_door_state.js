let config = {
    OPENING_TIME: 18000, // time to open the door in ms
    CLOSING_TIME: 20000, // time to open the door in ms
    DEBUG: true
};

let state = {
    OPEN: "open",
    OPENING: "opening",
    CLOSED: "closed",
    CLOSING: "closing",
    STOPPED: "stopped"
};

let mqttStateTopic = null; // set at startup by reading the Mqtt.GetConfig result
let previousState = null;
let currentState = null;
let timerOpening = null;
let timerClosing = null;

function handleInputOn() {
    if (config.DEBUG) {
        print("Input ON -> door is closed");
    }
    handleCoverState(state.CLOSED);
    Timer.clear(timerOpening);
    Timer.clear(timerClosing);
}

// This function is needed if you open the door via the normal remote to detect it's opening!
function handleInputOff() {
    if (config.DEBUG) {
        print("Input OFF -> door is opening");
    }
    // Only update state when it's not already opening (as the 'switch on' event is also triggering the opening state)
    // When the state is not opening yet, it means the trigger came from the remote, which doesn't send mqtt commands!
    if (currentState !== state.OPENING) {
        handleCoverState(state.OPENING);
        handleOpeningStateTimer();
    }
}

function handleSwitchOn() {
    if (currentState === state.CLOSED) {
        if (config.DEBUG) {
            print("Switch ON -> current state is closed -> door is opening");
        }
        handleCoverState(state.OPENING); // if it was closed before, we assume it is opening
        handleOpeningStateTimer();
    } else if (currentState === state.OPEN) {
        if (config.DEBUG) {
            print("Switch ON -> current state is open -> door is closing");
        }
        handleCoverState(state.CLOSING); // if it was open before, we assume it is closing
        handleClosingStateTimer();
    } else if (currentState === state.CLOSING) {
        if (config.DEBUG) {
            print("Switch ON -> current state is closing -> door is stopped");
        }
        handleCoverState(state.STOPPED);
        Timer.clear(timerClosing);
    } else if (currentState === state.OPENING) {
        if (config.DEBUG) {
            print("Switch ON -> current state is opening -> door is stopped");
        }
        handleCoverState(state.STOPPED);
        Timer.clear(timerOpening);
    } else if (currentState === state.STOPPED && previousState === state.OPENING) {
        if (config.DEBUG) {
            print("Switch ON -> current state is stopped and previous state is opening  -> door is closing");
        }
        handleCoverState(state.CLOSING);
        handleClosingStateTimer();
    } else if (currentState === state.STOPPED && previousState === state.CLOSING) {
        if (config.DEBUG) {
            print("Switch ON -> current state is stopped and previous state is closing  -> door is opening");
        }
        handleCoverState(state.OPENING);
        handleOpeningStateTimer();
    } else {
        print("Switch ON -> current state is unknown -> ???");
    }
}

function handleOpeningStateTimer() {
    // Assume it's open after the opening time
    Timer.clear(timerOpening);
    timerOpening = Timer.set(config.OPENING_TIME, false, function () {
        if (config.DEBUG) {
            print("Opening timer expired -> door is open");
        }
        handleCoverState(state.OPEN);
    }, null);
}

function handleClosingStateTimer() {
    // Assume it's closed after the closing time
    Timer.clear(timerClosing);
    timerClosing = Timer.set(config.CLOSING_TIME, false, function () {
        if (config.DEBUG) {
            print("Closing timer expired -> door is closed");
        }
        handleCoverState(state.CLOSED);
    }, null);
}

// Handle cover state
function handleCoverState(newstate) {
    if (config.DEBUG) {
        print("Setting and publishing mqtt state: " + newstate);
    }
    MQTT.publish(mqttStateTopic, newstate, 0, true); // publish with retain=true to keep the state in homeassistant when homeassistant is restarted
    previousState = currentState || newstate; // set current state as previous state (or new state if there is no current state yet)
    currentState = newstate; // set new state as current state
}

// Set mqtt state topic
function setMqttStateTopic() {
    Shelly.call(
        "MQTT.GetConfig",
        {},
        function (result, error_code, error_message, user_data) {
            if (error_code === 0) {
                // result: {"enable":true,"server":"...","client_id":"...","user":"...","topic_prefix":"...","rpc_ntf":true,"status_ntf":true,"use_client_cert":false,"enable_rpc":true,"enable_control":true}            
                mqttStateTopic = result.topic_prefix + '/state';
                if (config.DEBUG) {
                    print("Mqtt state topic: " + mqttStateTopic);
                }
            }
        },
        null
    );
}

// Determine the current status to handle the current cover state (door must be closed or fully open when started)
function setInitialCoverState() {
    Shelly.call(
        "Input.GetStatus",
        { id: 0 },
        function (result, error_code, error_message, user_data) {
            if (error_code === 0) {
                // result: {"id":0,"state":true}
                if (result.state === true) {
                    handleCoverState(state.CLOSED);
                } else {
                    handleCoverState(state.OPEN);
                }
            }
        },
        null
    );
}

// Event handler to react on changes of the input sensor
Shelly.addEventHandler(
    function (event, user_data) {
        if (config.DEBUG) {
            print("Event: " + JSON.stringify(event));
        }
        // Input event
        if (event.name === "input") {
            if (event.info.state === true) {
                handleInputOn();
            } else {
                handleInputOff();
            }
        }
        // Switch event
        if (event.name === "switch") {
            // Only handle the 'switch on' (as we have auto off to simulate a push button, so nothing to do when switch is turned 'off')
            if (event.info.state === true) {
                handleSwitchOn();
            }
        }
    },
    null
);

setMqttStateTopic();
setInitialCoverState();
MQTT.setConnectHandler(setInitialCoverState); // set initial cover state when mqtt connection is established