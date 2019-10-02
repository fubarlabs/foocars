EESchema Schematic File Version 4
LIBS:foocars-pwm-teensy-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector_Generic_MountingPin:Conn_01x14_MountingPin J2
U 1 1 5D123AF0
P 5250 2800
F 0 "J2" V 5382 2669 50  0000 C CNN
F 1 "BOTTOMBOTTOM-14-LEFT" V 5473 2669 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical" H 5250 2800 50  0001 C CNN
F 3 "~" H 5250 2800 50  0001 C CNN
	1    5250 2800
	0    1    1    0   
$EndComp
Wire Wire Line
	4400 2200 4300 2200
Wire Wire Line
	4300 2200 4300 2500
Wire Wire Line
	4300 2500 4400 2500
Wire Wire Line
	4400 2500 4400 2200
$Comp
L power:GND #PWR01
U 1 1 5D13879E
P 4650 1250
F 0 "#PWR01" H 4650 1000 50  0001 C CNN
F 1 "GND" H 4655 1077 50  0000 C CNN
F 2 "" H 4650 1250 50  0001 C CNN
F 3 "" H 4650 1250 50  0001 C CNN
	1    4650 1250
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_02x03_Counter_Clockwise J4
U 1 1 5D13893A
P 6250 2700
F 0 "J4" H 6300 3017 50  0000 C CNN
F 1 "PWM_Output" H 6300 2926 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Horizontal" H 6250 2700 50  0001 C CNN
F 3 "~" H 6250 2700 50  0001 C CNN
	1    6250 2700
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x03_Counter_Clockwise J3
U 1 1 5D13BA5A
P 6250 2000
F 0 "J3" H 6300 2317 50  0000 C CNN
F 1 "PWM_Input" H 6300 2226 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x03_P2.54mm_Horizontal" H 6250 2000 50  0001 C CNN
F 3 "~" H 6250 2000 50  0001 C CNN
	1    6250 2000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic_MountingPin:Conn_01x14_MountingPin J1
U 1 1 5D123A95
P 5250 2000
F 0 "J1" V 5382 1869 50  0000 C CNN
F 1 "TOPTOP-14-LEFT" V 5473 1869 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical" H 5250 2000 50  0001 C CNN
F 3 "~" H 5250 2000 50  0001 C CNN
	1    5250 2000
	0    1    1    0   
$EndComp
Wire Wire Line
	5050 2600 5050 2500
Wire Wire Line
	6050 1900 6050 1950
Wire Wire Line
	6050 2100 6050 2200
Wire Wire Line
	6050 2200 6300 2200
Wire Wire Line
	6550 2200 6550 2100
Wire Wire Line
	6050 2600 6050 2650
Wire Wire Line
	6050 2800 6050 2900
Wire Wire Line
	6050 2900 6300 2900
Wire Wire Line
	6550 2900 6550 2800
Wire Wire Line
	6550 2000 6700 2000
Wire Wire Line
	6700 2000 6700 1600
Wire Wire Line
	6700 1600 5050 1600
Wire Wire Line
	5050 1600 5050 1800
Wire Wire Line
	5150 1650 6600 1650
Wire Wire Line
	6600 1650 6600 1900
Wire Wire Line
	6600 1900 6550 1900
Wire Wire Line
	5150 1650 5150 1800
Wire Wire Line
	6550 2600 6650 2600
Wire Wire Line
	6650 2600 6650 2500
Wire Wire Line
	6650 2500 5050 2500
Wire Wire Line
	4950 2450 6700 2450
Wire Wire Line
	6700 2450 6700 2700
Wire Wire Line
	6700 2700 6550 2700
Wire Wire Line
	4950 2450 4950 2600
Wire Wire Line
	6050 1950 6000 1950
Wire Wire Line
	6000 1950 6000 2350
Wire Wire Line
	6000 2650 6050 2650
Connection ~ 6050 1950
Wire Wire Line
	6050 1950 6050 2000
Connection ~ 6050 2650
Wire Wire Line
	6050 2650 6050 2700
Wire Wire Line
	6300 2200 6300 2900
Connection ~ 6300 2200
Wire Wire Line
	6300 2200 6550 2200
Connection ~ 6300 2900
Wire Wire Line
	6300 2900 6550 2900
Wire Wire Line
	4650 2350 6000 2350
Wire Wire Line
	4650 1250 4650 1350
Connection ~ 4650 1800
Wire Wire Line
	4650 1800 4650 2350
Connection ~ 6000 2350
Wire Wire Line
	6000 2350 6000 2650
$Comp
L Connector_Generic:Conn_01x01 J5
U 1 1 5D24D8A7
P 6400 1350
F 0 "J5" H 6479 1392 50  0000 L CNN
F 1 "BattMon" H 6479 1301 50  0000 L CNN
F 2 "" H 6400 1350 50  0001 C CNN
F 3 "~" H 6400 1350 50  0001 C CNN
	1    6400 1350
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5D24E18B
P 6050 1350
F 0 "R2" V 5843 1350 50  0000 C CNN
F 1 "R" V 5934 1350 50  0000 C CNN
F 2 "" V 5980 1350 50  0001 C CNN
F 3 "~" H 6050 1350 50  0001 C CNN
	1    6050 1350
	0    1    1    0   
$EndComp
$Comp
L Device:R R1
U 1 1 5D24FB65
P 5200 1350
F 0 "R1" V 4993 1350 50  0000 C CNN
F 1 "R" V 5084 1350 50  0000 C CNN
F 2 "" V 5130 1350 50  0001 C CNN
F 3 "~" H 5200 1350 50  0001 C CNN
	1    5200 1350
	0    1    1    0   
$EndComp
Wire Wire Line
	5050 1350 4650 1350
Connection ~ 4650 1350
Wire Wire Line
	4650 1350 4650 1800
Wire Wire Line
	5350 1350 5650 1350
Wire Wire Line
	5650 1800 5650 1350
Connection ~ 5650 1350
Wire Wire Line
	5650 1350 5900 1350
Text Notes 5350 1250 0    50   ~ 0
Voltage Divider
Text Notes 4400 2400 1    50   ~ 0
USB\n
$EndSCHEMATC
