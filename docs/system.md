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