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
