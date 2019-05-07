import sys
import struct

digital_names={0:"X", 1:"square", 2:"circle", 3:"triangle", 4:"R-paddle", 5:"L-paddle", 6:"R-bumper", 7:"L-bumper", 
        8:"select", 9:"start", 10:"R-button", 11:"L-button", 12:"shift-down", 13:"shift-up", 14:"enter", 15:"plus", 
        16:"sel-wheel-cw", 17:"sel-wheel-ccw", 18:"minus", 19:"beep", 20:"PS"}

analog_names={3:"dpad-lr", 4:"dpad-ud"}


js_file='/dev/input/js0'
print(js_file)

with open(js_file, 'rb') as joystick:
    while True:
        js_data=joystick.read(8)
        if js_data!=-1:
            time, value, input_type, input_id =struct.unpack('IhBB', js_data)#.get_buffer())
            if input_type==1 and value==1:
                print("digital input: "+digital_names[input_id])
            elif input_type==1 and input_id in digital_names:
                continue
            elif input_type==2 and input_id==0:
                print("steering_wheel: "+str(value))
            elif input_type==2 and input_id==3:
                if value==0:
                    print("DPad-LR centered")
                elif value==-32767:
                    print("DPad-LR left")
                elif value==32767:
                    print("DPad-LR right")
                else:
                    print("DPad-LR: "+str(value))
            elif input_type==2 and input_id==4:
                if value==0:
                    print("DPad-UD centered")
                elif value==-32767:
                    print("DPad-UD up")
                elif value==32767:
                    print("DPad-UD down")
                else:
                    print("DPad-UD: "+str(value))
            else:
                print("unexpected value: ")
                print("\tid="+str(input_id)+"\ttype="+str(input_type)+"\tvalue="+str(value))

