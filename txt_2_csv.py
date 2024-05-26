import os
import re

#debug flag
debug = True

#header 
header = "Sleep Stage,Time [hh:mm:ss.xxx],Duration[s],Location\n"

#regex expressions
txt_fl = r"^(\w+)\.(\w+)$"
line_reg = r"(\w+-\w+)\s+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+)\s+(\w+-\w+)\s+([\d\.]+)\s+([\w-]+)"

def get_sleepst(ss):
    match ss :
        case "SLEEP-S0":
            return "W"
        case "SLEEP-S1":
            return "N1"
        case "SLEEP-S2":
            return "N2"
        case "SLEEP-S3":
            return "N3"
        case "SLEEP-SREM":
            return "R"
        
def make_string(retval):
    return retval["sleep_stage"] + "," + retval["time"] + "," + retval["duration"] +  "," +  retval["location"] + "\n"
        
def convert_ip_op(input, output):
    for line in input:
        x = re.search(line_reg, line)
        if x:
            retval = {
                "sleep_stage": get_sleepst(x.group(1)),
                "time": x.group(2),
                "duration": str(int(float(x.group(4)))),
                "location": x.group(5)
            }
            st = make_string(retval)
            output.write(st)
        else:
            if debug:
                print(f"Skipping unmatched line: {line}")   
           

def main():
    
    print("Converting .txt files to .csv files.....")
    
    #get current workign directory 
    cwd = os.getcwd()
    #get all files in folder
    list = os.listdir(path=cwd)
    if debug :
        print(list)
    
    txt_files = {}
    for f in list:
        x = re.search(txt_fl, f)
        if x is not None:
            extension = str(x.group(2))
            filename = str(x.group(1))
            if extension == "txt":
                txt_files[f] = filename
    
    if debug :
        print(txt_files)    
    
    print("List of files that will be converted to csv:") 
    for f in txt_files.keys():
        print(f)   
    
    #for each file in keys 
    #open file 
    #convert to csv 
    for f in txt_files.keys():
        input_file = open(f, "r")
        op_file_name = txt_files[f] + ".csv"
        output_file = open(op_file_name, "a")
        output_file.write(header)
        convert_ip_op(input_file, output_file); 
        output_file.close()
        input_file.close()
    

if __name__ == '__main__':
    main()