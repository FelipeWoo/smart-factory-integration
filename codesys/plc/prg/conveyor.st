PROGRAM PRG_Main
VAR
    (* --- COMMANDS / INPUTS --- *)
    bStartCmd      : BOOL := FALSE;
    bStartBtn      : BOOL := FALSE;
    bStopCmd       : BOOL := FALSE;
    bStopBtn       : BOOL := FALSE;
    bResetCmd      : BOOL := FALSE;
    bEStop         : BOOL := FALSE;

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

    (* --- PROCESS STATES --- *)
    bMotorIsRunning : BOOL := FALSE;
    bPartDetected   : BOOL := FALSE;
    bAlarmActive    : BOOL := FALSE;
    bStarvation     : BOOL := FALSE;

    (* --- SYSTEM CONDITIONS --- *)
    bSystemReady   : BOOL := TRUE;
    bAutoMode      : BOOL := TRUE;

    (* --- TIMERS --- *)
    tStarvation    : TON;
    tFault         : TON;

END_VAR


(* --- SYSTEM READY --- *)
bSystemReady := bAutoMode AND NOT bEStop AND NOT bStarvation AND NOT bAlarmActive;

(* --- REQUEST GENERATION --- *)
bStopReq  := bStopCmd OR bStopBtn;
bStartReq := (bStartCmd OR bStartBtn) AND bSystemReady;
bResetReq := bResetCmd AND NOT bEStop;


(* --- EDGE DETECTION --- *)
rTrigStart(CLK := bStartReq);
rTrigStop(CLK := bStopReq);
rTrigReset(CLK := bResetReq);

bStartPulse := rTrigStart.Q;
bStopPulse  := rTrigStop.Q;
bResetPulse := rTrigReset.Q;


(* --- EMERGENCY STOP --- *)
IF bEStop THEN
    bMotorIsRunning := FALSE;
END_IF;


(* --- START / STOP LOGIC --- *)
IF bStopPulse THEN
    bMotorIsRunning := FALSE;
ELSIF bStartPulse THEN
    bMotorIsRunning := TRUE;
END_IF;


(* --- STARVATION DETECTION --- *)
tStarvation(
    IN := NOT bPartDetected AND bMotorIsRunning,
    PT := T#15S
);

IF tStarvation.Q THEN
    bStarvation := TRUE;
    bMotorIsRunning := FALSE;
END_IF;


(* --- FAULT DETECTION --- *)
tFault(
    IN := bPartDetected AND bMotorIsRunning,
    PT := T#10S
);

IF tFault.Q THEN
    bAlarmActive := TRUE;
    bMotorIsRunning := FALSE;
END_IF;


(* --- RESET --- *)
IF bResetPulse THEN
    bStarvation  := FALSE;
    bAlarmActive := FALSE;
END_IF;

END_PROGRAM