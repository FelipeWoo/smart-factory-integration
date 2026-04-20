PROGRAM PRG_MAIN
VAR
    (* --- REQUESTS (LOGIC CONDITIONS) --- *)
    bStartReq      : BOOL := FALSE;
    bStopReq       : BOOL := FALSE;
    bResetReq      : BOOL := FALSE;

    (* --- EDGE DETECTION --- *)
    rTrigStart     : R_TRIG;
    rTrigStop      : R_TRIG;
    rTrigReset     : R_TRIG;

    bStartPulse    : BOOL := FALSE;
    bStopPulse     : BOOL := FALSE;
    bResetPulse    : BOOL := FALSE;

    (* --- TIMERS --- *)
    tStarvation    : TON;
    tFault         : TON;
END_VAR



(* --- SYSTEM READY --- *)
GVL_STATE.bSystemReady := GVL_STATE.bAutoMode AND NOT GVL_IO.bEStop AND NOT GVL_STATE.bStarvation AND NOT GVL_STATE.bAlarmActive;

(* --- REQUEST GENERATION --- *)
bStopReq  := GVL_IO.bStopCmd OR GVL_IO.bStopBtn;
bStartReq := (GVL_IO.bStartCmd OR GVL_IO.bStartBtn) AND GVL_STATE.bSystemReady;
bResetReq := GVL_IO.bResetCmd AND NOT GVL_IO.bEStop;


(* --- EDGE DETECTION --- *)
rTrigStart(CLK := bStartReq);
rTrigStop(CLK := bStopReq);
rTrigReset(CLK := bResetReq);

bStartPulse := rTrigStart.Q;
bStopPulse  := rTrigStop.Q;
bResetPulse := rTrigReset.Q;


(* --- EMERGENCY STOP --- *)
IF GVL_IO.bEStop THEN
    GVL_STATE.bMotorIsRunning := FALSE;
END_IF;


(* --- START / STOP LOGIC --- *)
IF bStopPulse THEN
    GVL_STATE.bMotorIsRunning := FALSE;
ELSIF bStartPulse THEN
    GVL_STATE.bMotorIsRunning := TRUE;
END_IF;

(* --- STARVATION DETECTION --- *)
tStarvation(
    IN := NOT GVL_STATE.bPartDetected AND GVL_STATE.bMotorIsRunning,
    PT := T#15S
);

IF tStarvation.Q THEN
    GVL_STATE.bStarvation := TRUE;
    GVL_STATE.bMotorIsRunning := FALSE;
END_IF;


(* --- FAULT DETECTION --- *)
tFault(
    IN := GVL_STATE.bPartDetected AND GVL_STATE.bMotorIsRunning,
    PT := T#10S
);

IF tFault.Q THEN
    GVL_STATE.bAlarmActive := TRUE;
    GVL_STATE.bMotorIsRunning := FALSE;
END_IF;


(* --- RESET --- *)
IF bResetPulse THEN
    GVL_STATE.bStarvation  := FALSE;
    GVL_STATE.bAlarmActive := FALSE;
END_IF;

END_PROGRAM