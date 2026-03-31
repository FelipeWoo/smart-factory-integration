FUNCTION_BLOCK FSM
VAR
END_VAR

FUNCTION_BLOCK FSM

VAR_INPUT
    START_CMD : BOOL;
    STOP_CMD : BOOL;
    ESTOP_CMD : BOOL;
END_VAR

VAR_OUTPUT
    RUNNING : BOOL;
    STOPPED : BOOL;
    FAULT   : BOOL;
END_VAR

VAR
    state : INT := 0; // 0=IDLE, 1=RUNNING, 2=STOPPED, 3=FAULT
END_VAR


// lógica principal
IF ESTOP_CMD THEN
    state := 3;
ELSIF STOP_CMD THEN
    state := 2;
ELSIF START_CMD AND (state = 0 OR state = 2) THEN
    state := 1;
END_IF;


// salidas según estado
CASE state OF
    0: // IDLE
        RUNNING := FALSE;
        STOPPED := FALSE;
        FAULT   := FALSE;

    1: // RUNNING
        RUNNING := TRUE;
        STOPPED := FALSE;
        FAULT   := FALSE;

    2: // STOPPED
        RUNNING := FALSE;
        STOPPED := TRUE;
        FAULT   := FALSE;

    3: // FAULT (E-STOP)
        RUNNING := FALSE;
        STOPPED := FALSE;
        FAULT   := TRUE;
END_CASE;

END_FUNCTION_BLOCK

END_FUNCTION_BLOCK