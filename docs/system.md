# Pastry Cell System

## High-Level Functional Description

The infeed conveyor moves pastries into the SCARA pickup zone. A pickup-area sensor detects when a pastry is present. When a pastry is detected, the system raises an **occupied flag** and stops both the infeed and outfeed conveyors. This creates a stable condition for vision evaluation and robot handling.

The vision system returns only one result:

* `true` = accepted product
* `false` = rejected product (scrap)

If the pastry is rejected, the SCARA moves it to the scrap tray and increments the scrap counter.

If the pastry is accepted, the SCARA places it on the outfeed conveyor in the next indexed position of the current package:

* first good pastry goes to `pos_1`
* second good pastry goes to `pos_2`
* third good pastry goes to `pos_3`

When `pos_3` is completed, the package is complete. The package counter is incremented, the position counter resets, the occupied flag is cleared, and both conveyors move again.

If the cell becomes free and no new product reaches the pickup sensor within 60 seconds, the infeed conveyor stops and the tower light indicates a starvation stop.

---

## Main Components

### PLC

The PLC is the real-time coordinator of the cell. It reads sensors, receives robot and vision handshakes, executes the state machine, controls motors, manages alarms, and publishes data to HMI and web systems.

### SCARA Robot

The SCARA robot picks pastries from the pickup area and routes them to:

* scrap tray
* outfeed position 1
* outfeed position 2
* outfeed position 3

### Vision System

The vision system evaluates pastry quality and returns a boolean result only:

* `quality_ok = true`
* `quality_ok = false`

### Infeed Conveyor

The infeed conveyor feeds pastries into the pickup area.

### Outfeed Conveyor

The outfeed conveyor receives accepted pastries in groups of three and carries complete packages toward packaging.

### HMI

The HMI shows current state, counters, alarms, faults, stop reasons, and operator controls.

### Web Dashboard

The web layer shows operations and results such as production by hour, package count, scrap, downtime, stop categories, and throughput.

### Tower Light

The tower light provides immediate visual status feedback to operators.

### Pushbuttons

The system includes at least:

* Start button
* Stop button
* Emergency stop button
* Reset button

---

## Devices and Signals

### Sensors and buttons
* `pick_sensor`: pastry present in SCARA pickup area
* `infeed_running_fb`: feedback that infeed conveyor motor is running
* `outfeed_running_fb`: feedback that outfeed conveyor motor is running
* `emergency_stop_ok`
* `emergency_stop_pressed`
* `start_pressed`
* `reset_pressed`
* `stop_pressed`

### SCARA and Vision
* `robot_ready`
* `robot_busy`
* `robot_fault`
* `vision_ready`
* `vision_busy`
* `quality_ok`
* `quality_fail`

### Conveyors
* `infeed_motor_run_cmd`
* `outfeed_motor_run_cmd`
* `robot_cycle_start`
* `robot_route_scrap`
* `robot_route_pos1`
* `robot_route_pos2`
* `robot_route_pos3`

### Indicators
* `tower_red`
* `tower_yellow`
* `tower_green`
* `tower_buzzer`

### Internal Variables
* `occupied_flag`
* `position_counter` values `0, 1, 2` before next place command
* `package_count`
* `scrap_count`
* `valid_in_count` individual pastry count
* `good_out_count` collection of three count
* `scrap_out_count` individual pastry count
* `manual_stop_count`
* `starvation_stop_count`
* `technical_stop_count`
* `downtime_seconds`
* `hourly_production`
* `current_state`
* `current_stop_reason`
* `no_product_timer` the total amount of time without product
* `cycle_active` the total amount of time active
