EESchema Schematic File Version 4
EELAYER 30 0
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
F 0 "J2" V 5200 1800 50  0000 C CNN
F 1 "BOTTOM_HALF" V 5300 1600 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical" H 5250 2800 50  0001 C CNN
F 3 "~" H 5250 2800 50  0001 C CNN
	1    5250 2800
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_02x03_Counter_Clockwise J4
U 1 1 5D13893A
P 6400 2700
F 0 "J4" H 6450 3017 50  0000 C CNN
F 1 "PWM_Output" H 6450 2926 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Horizontal" H 6400 2700 50  0001 C CNN
F 3 "~" H 6400 2700 50  0001 C CNN
	1    6400 2700
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x03_Counter_Clockwise J3
U 1 1 5D13BA5A
P 6400 2000
F 0 "J3" H 6450 2317 50  0000 C CNN
F 1 "PWM_Input" H 6450 2226 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x03_P2.54mm_Horizontal" H 6400 2000 50  0001 C CNN
F 3 "~" H 6400 2000 50  0001 C CNN
	1    6400 2000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic_MountingPin:Conn_01x14_MountingPin J1
U 1 1 5D123A95
P 5250 2000
F 0 "J1" V 5200 950 50  0000 C CNN
F 1 "TOP_HALF" V 5300 800 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical" H 5250 2000 50  0001 C CNN
F 3 "~" H 5250 2000 50  0001 C CNN
	1    5250 2000
	0    1    1    0   
$EndComp
Wire Wire Line
	5050 2600 5050 2500
Wire Wire Line
	6200 2100 6200 2200
Wire Wire Line
	6200 2200 6450 2200
Wire Wire Line
	6700 2200 6700 2100
Wire Wire Line
	6200 2800 6200 2900
Wire Wire Line
	6200 2900 6450 2900
Wire Wire Line
	6700 2900 6700 2800
Wire Wire Line
	6700 2000 6850 2000
Wire Wire Line
	6850 2000 6850 1600
Wire Wire Line
	5050 1600 5050 1800
Wire Wire Line
	6750 1650 6750 1900
Wire Wire Line
	6750 1900 6700 1900
Wire Wire Line
	5150 1650 5150 1800
Wire Wire Line
	6700 2600 6800 2600
Wire Wire Line
	6800 2600 6800 2500
Wire Wire Line
	6850 2450 6850 2700
Wire Wire Line
	6850 2700 6700 2700
Wire Wire Line
	4950 2450 4950 2600
Wire Wire Line
	6450 2200 6450 2900
Connection ~ 6450 2200
Wire Wire Line
	6450 2200 6700 2200
Connection ~ 6450 2900
Wire Wire Line
	6450 2900 6700 2900
$Comp
L Connector_Generic:Conn_01x01 J5
U 1 1 5D24D8A7
P 6400 1350
F 0 "J5" H 6479 1392 50  0000 L CNN
F 1 "BattMon" H 6479 1301 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 6400 1350 50  0001 C CNN
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
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Horizontal" V 5980 1350 50  0001 C CNN
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
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Horizontal" V 5130 1350 50  0001 C CNN
F 3 "~" H 5200 1350 50  0001 C CNN
	1    5200 1350
	0    1    1    0   
$EndComp
Wire Wire Line
	5050 1350 4650 1350
Wire Wire Line
	5350 1350 5650 1350
Wire Wire Line
	5650 1800 5650 1350
Connection ~ 5650 1350
Wire Wire Line
	5650 1350 5900 1350
Text Notes 5350 1250 0    50   ~ 0
Voltage Divider
Text Label 3850 1900 0    50   ~ 0
teensy_3.2
Text Label 4550 2500 1    50   ~ 0
USB_Side
Text GLabel 4550 2600 0    50   Input ~ 0
GND
Text GLabel 6200 1950 0    50   Input ~ 0
GND
Text GLabel 4650 1350 0    50   Input ~ 0
GND
Wire Wire Line
	5250 1800 5300 1800
Wire Wire Line
	5300 1800 5300 2150
Wire Wire Line
	5350 1800 5400 1800
Wire Wire Line
	6200 2600 6200 2700
Wire Wire Line
	6200 1900 6200 2000
Text GLabel 6200 2650 0    50   Input ~ 0
GND
Wire Wire Line
	5050 1600 6850 1600
Wire Wire Line
	5150 1650 6750 1650
Wire Wire Line
	4950 2450 6850 2450
Wire Wire Line
	5050 2500 6800 2500
Text GLabel 5300 2150 0    50   Input ~ 0
SCL0
Text GLabel 5400 2200 0    50   Input ~ 0
SDA0
Wire Wire Line
	5400 1800 5400 2200
Text GLabel 8250 1350 0    50   Input ~ 0
SCL0
Text GLabel 8650 1350 0    50   Input ~ 0
SDA0
$Comp
L Device:R R3
U 1 1 5F41DA94
P 8250 2150
F 0 "R3" H 8320 2196 50  0000 L CNN
F 1 "R" H 8320 2105 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Horizontal" V 8180 2150 50  0001 C CNN
F 3 "~" H 8250 2150 50  0001 C CNN
	1    8250 2150
	1    0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 5F41E9D9
P 8650 2150
F 0 "R4" H 8720 2196 50  0000 L CNN
F 1 "R" H 8720 2105 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Horizontal" V 8580 2150 50  0001 C CNN
F 3 "~" H 8650 2150 50  0001 C CNN
	1    8650 2150
	1    0    0    -1  
$EndComp
$Comp
L Jumper:Jumper_2_Open JP2
U 1 1 5F40F661
P 8250 1700
F 0 "JP2" V 8350 1750 50  0000 L CNN
F 1 "Jumper_2_Open" V 8295 1798 50  0001 L CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 8250 1700 50  0001 C CNN
F 3 "~" H 8250 1700 50  0001 C CNN
	1    8250 1700
	0    1    1    0   
$EndComp
$Comp
L Jumper:Jumper_2_Open JP3
U 1 1 5F432BF3
P 8450 1700
F 0 "JP3" V 8550 1750 50  0000 L CNN
F 1 "Jumper_2_Open" V 8495 1798 50  0001 L CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 8450 1700 50  0001 C CNN
F 3 "~" H 8450 1700 50  0001 C CNN
	1    8450 1700
	0    1    1    0   
$EndComp
$Comp
L Jumper:Jumper_2_Open JP4
U 1 1 5F433E3D
P 8650 1700
F 0 "JP4" V 8750 1800 50  0000 L CNN
F 1 "Jumper_2_Open" V 8695 1798 50  0001 L CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 8650 1700 50  0001 C CNN
F 3 "~" H 8650 1700 50  0001 C CNN
	1    8650 1700
	0    1    1    0   
$EndComp
$Comp
L Jumper:Jumper_2_Open JP1
U 1 1 5F434E4F
P 8050 1700
F 0 "JP1" V 8150 1750 50  0000 L CNN
F 1 "Jumper_2_Open" V 8095 1798 50  0001 L CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 8050 1700 50  0001 C CNN
F 3 "~" H 8050 1700 50  0001 C CNN
	1    8050 1700
	0    1    1    0   
$EndComp
Wire Wire Line
	8250 1350 8250 1500
Wire Wire Line
	8050 1500 8250 1500
Connection ~ 8250 1500
Wire Wire Line
	8450 1500 8650 1500
Wire Wire Line
	8650 1350 8650 1500
Connection ~ 8650 1500
Wire Wire Line
	8250 2000 8250 1900
Wire Wire Line
	8650 2000 8650 1900
Wire Wire Line
	8050 1900 8050 2300
Wire Wire Line
	8250 2300 8250 2450
Wire Wire Line
	8250 2450 8400 2450
Wire Wire Line
	8650 2450 8650 2300
Wire Wire Line
	8500 2450 8650 2450
Wire Wire Line
	8450 1900 8450 2300
Wire Wire Line
	8450 2300 8650 2300
Connection ~ 8650 2300
Wire Wire Line
	8050 2300 8250 2300
Connection ~ 8250 2300
Text Notes 8300 1250 0    50   ~ 0
i2c\n
Text Notes 9300 2050 0    50   ~ 0
Connect J1/J3 for "normal" operation\n and J2/J4 for resistor in-line.
Wire Wire Line
	5150 2600 5200 2600
Wire Wire Line
	5200 2600 5200 3150
Wire Wire Line
	5250 2600 5300 2600
Wire Wire Line
	5300 2600 5300 3150
$Comp
L Connector_Generic:Conn_01x04 J6
U 1 1 5F46C815
P 8500 2750
F 0 "J6" V 8450 2950 50  0000 L CNN
F 1 "Conn_01x04" V 8550 2950 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal" H 8500 2750 50  0001 C CNN
F 3 "~" H 8500 2750 50  0001 C CNN
	1    8500 2750
	0    1    1    0   
$EndComp
Wire Wire Line
	8400 2450 8400 2550
Wire Wire Line
	8500 2450 8500 2550
Text GLabel 4750 1800 1    50   Input ~ 0
3v3
Text GLabel 8600 2550 2    50   Input ~ 0
3v3
Text GLabel 8300 2550 0    50   Input ~ 0
GND
Text Label 8250 2450 0    50   ~ 0
SCL
Text Label 8500 2450 0    50   ~ 0
SDA
$Comp
L Connector_Generic:Conn_01x04 J7
U 1 1 5F48D985
P 5300 3350
F 0 "J7" V 5250 3550 50  0000 L CNN
F 1 "Conn_01x04" V 5350 3550 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal" H 5300 3350 50  0001 C CNN
F 3 "~" H 5300 3350 50  0001 C CNN
	1    5300 3350
	0    1    1    0   
$EndComp
Text GLabel 5100 3150 0    50   Input ~ 0
GND
Text GLabel 5400 3150 2    50   Input ~ 0
3v3
Text Notes 4950 3550 0    50   ~ 0
encoder in (quadrature)\n
$Comp
L Mechanical:MountingHole H2
U 1 1 5F4B0E4F
P 8250 3750
F 0 "H2" H 8350 3796 50  0000 L CNN
F 1 "MountingHole" H 8350 3705 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.5mm_Pad" H 8250 3750 50  0001 C CNN
F 3 "~" H 8250 3750 50  0001 C CNN
	1    8250 3750
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H1
U 1 1 5F4B2276
P 8200 4200
F 0 "H1" H 8300 4246 50  0000 L CNN
F 1 "MountingHole" H 8300 4155 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.5mm_Pad" H 8200 4200 50  0001 C CNN
F 3 "~" H 8200 4200 50  0001 C CNN
	1    8200 4200
	1    0    0    -1  
$EndComp
$EndSCHEMATC
