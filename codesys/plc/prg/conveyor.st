PROGRAM PLC_PRG
VAR
	start_cmd		: BOOL := FALSE;
    start_button    : BOOL := FALSE;
	start_request	: BOOL := FALSE;
	start_pulse		: BOOL := FALSE;
	
	stop_cmd		: BOOL := FALSE;
    stop_button     : BOOL := FALSE;
	stop_request	: BOOL := FALSE;
	stop_pulse		: BOOL := FALSE;
	
	e_stop			: BOOL := FALSE;
	
	reset_cmd		: BOOL := FALSE;
	reset_request	: BOOL := FALSE;
	reset_pulse		: BOOL := FALSE;
	
    r_start         : R_TRIG;
    r_stop          : R_TRIG;
	r_reset         : R_TRIG;

	motor_running   : BOOL := FALSE;
    part_detected   : BOOL := FALSE;
    alarm_active    : BOOL := FALSE;
	
	system_ready	: BOOL := TRUE;
	auto_mode		: BOOL := TRUE;
	starvation		: BOOL := FALSE;
	
	t_starvation_delay	: TON;
	t_fault_delay	    : TON;
	
END_VAR

system_ready := auto_mode AND NOT e_stop AND NOT starvation AND NOT alarm_active;
stop_request := stop_cmd OR stop_button;
start_request := (start_cmd OR start_button) AND system_ready;
reset_request := reset_cmd AND NOT e_stop;


r_start(CLK := start_request);
r_stop(CLK := stop_request);
r_reset(CLK := reset_request);

IF e_stop THEN
    motor_running := FALSE;
END_IF;

start_pulse := r_start.Q;
stop_pulse := r_stop.Q;
reset_pulse := r_reset.Q;

IF stop_pulse THEN
    motor_running := FALSE;
ELSIF start_pulse THEN
    motor_running := TRUE;
END_IF;

t_starvation_delay(
	IN := NOT part_detected AND motor_running, (*absence of product*)
	PT := T#15S (*time just fot simulation purposes*)
);

IF t_starvation_delay.Q THEN
	starvation := TRUE;
	motor_running := FALSE;
END_IF;

t_fault_delay(
	IN := part_detected AND motor_running, (*something obstructing*)
	PT := T#10S (*time just fot simulation purposes*)
);

IF t_fault_delay.Q THEN
    alarm_active := TRUE;
	motor_running := FALSE;    
END_IF;

IF reset_pulse THEN
	starvation := FALSE;
	alarm_active := FALSE;
END_IF;

END_PROGRAM