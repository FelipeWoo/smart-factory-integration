{attribute 'qualified_only'}
VAR_GLOBAL
    (* --- PROCESS STATES --- *)
    bMotorIsRunning : BOOL := FALSE;
    bPartDetected  : BOOL := FALSE;
    bAlarmActive    : BOOL := FALSE;
    bStarvation     : BOOL := FALSE;

    (* --- SYSTEM CONDITIONS --- *)
    bSystemReady    : BOOL := TRUE;
    bAutoMode       : BOOL := TRUE;
END_VAR