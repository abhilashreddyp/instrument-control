#####################################
# Example how to control Agilent Function egenrator over GPIB
# Author, Peter Vago, NI Systems Engineer, 2016
#
# PyVISA 1.8 version is used. 
# For migrating from older version (<1.5) read this: https://media.readthedocs.org/pdf/pyvisa/master/pyvisa.pdf 
#
####################################


import time

import sys

def open_instrument():
    import visa
    import socket
    rm = visa.ResourceManager('') # If you have NI-VISA installed
    #rm = visa.ResourceManager('@py') # If you have PyVisa-Py installed

    ## If you want discover your instruments - GPIB
    #rm.list_resources()
    ## response will be like this: ('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::14::INSTR')
    try:
        #my_instrument = rm.open_resource('TCPIP0::127.0.0.1::6340::SOCKET')
        my_instrument = rm.open_resource('TCPIP::10.92.7.134::40010::SOCKET')
        return my_instrument,0
    except:
        print("Error: Server seems to be not running.")
        return 0,2 #2 ->Error code

def close_instrument(instr):
    instr.close()
    
def manage_client_parameters(my_instrument):
    # print (my_instrument.read_termination)
    my_instrument.chunk_size = 15
    #print(my_instrument.query_delay);	# messagebased.py, line 118
    my_instrument.query_delay=2; 
    print("=== Query delay: %d sec"%my_instrument.query_delay); 	# messagebased.py, line 118
    #my_instrument._read_termination = 'R';
    print("=== Read termination character: %s"%str(my_instrument._read_termination));

def control(args, inst):
    command='nocommand'
    examples=['MEASure:STARt','MEASEurement:STOP','SENSe:FREQuency:CENTer 2.401G','SENS:FREQ:CENT 2400M','SENS:RLEV -5', \
    'SENS:FREQ:SPAN 40M','SENS:BAND:RES 10k']
    if args[1]=='start':
        command='start'
    
    elif args[1]=='stop':
        command='stop'
    elif args[1]=='config':
        if len(args)<3: 
            return 2, ".."
        cmd='config'
        param1=args[2]
        command="%s"%(cmd, param1, param2)
        #params={"freq":999000,"reflev":-10}
    elif args[1]=='scpi-short':
        if len(args)<3:
            ind=0
            for i in examples:
                print("%d: %s"%(ind,i))
                ind+=1
            return 0, "Usage: python test_tcp.py scpi-short <num>"
        else:
            index=int(args[2])
            command=examples[index]
    elif args[1]=='scpi':
        if len(args)<3: 
            return 2, "--"
        cmd=args[2] # e.g. SENS:RLEV
        if cmd[0:4]=="MEAS":
            parameter = ""
        elif cmd[0:4]=="SENS":
            if len(args)<4:
                return 2, "-"
            else:
                parameter=args[3] # e.g. -10
        elif cmd[0:5]=="*IDN?":
            cmd="*IDN?"
            parameter=""
        else:
            return 2 , cmd[0:4]
        command=cmd+" "+parameter
    elif args[1]=='file':
        f=open(args[2],'r')
        i=0
        print("----Script started----")
        for line in f:
            if line[0]!="#":
                print("%02d: %s"%(i,line[:-1]))
                inst.write(line)
            else:
                print("%02d: %s"%(i,line[:-1]))
                
            i+=1
        print("----Script finished----")
        return 0, ""
    else:
        return 2, "...."
    
    inst.write(command)
    print("*Command sent: %s"%command)
    return 0, ""
    
def temp():    
    #print(my_instrument.query('*IDN?',13)); # 13 sec query delay, optional 
    #print(my_instrument.query('*IDN?',2));
    #my_instrument.write('*IDN?',1)
    #print(my.intrument.read())

    return 0
    
def temp_sweep():
    # Linear Sweep
    #print(my_instrument.write('outp:load 50'))
    #print(my_instrument.write('sweep:time 1'))
    #print(my_instrument.write('freq:start 5000'))
    #print(my_instrument.write('freq:stop 20000'))
    #print(my_instrument.write('sweep:stat on'))
    
    #Wait for 2 seconds
    #time.sleep(2)

    # Stop generation
    #print(my_instrument.write('sweep:stat off'))
    pass
    
def check_arguments(args):
    help="=========================== \n \
    Usage: python test_tcp.py <operation> <argument> \
    Where operations are: \n \
    \n \
    config : set Analyzer parameters\n \
        config freq <Hz> \
        config reflev <dBm> \
        config span <Hz> \
        config rbw <Hz> \
    start : no argument needed\n \
    stop : no argument needed\n \
    ==========================="
    if len(args)==1:
        print ("%s"%help)
        return 1, ""
    else:
        return 0, ""

def main(args):
    ret=[3, ""]
    ret=check_arguments(args)
    if ret[0]==1:
        return 1, "Invalid arguments."
    else:
        print("=== Program started");
        inst, ret = open_instrument() # opening reference
        if ret>0: return 2 # 2--> Exit with error
        #manage_client_parameters(inst)
        ret = control(args, inst)
        try:
            close_instrument(inst)
        except:
            pass
    #print("=====%s"%str(ret))
    print("=== Program stopped, Ret: %d, %s"%(ret[0],str(ret[1])));
    return ret[0]
    
if __name__ == '__main__':
    ret = main(sys.argv)
    sys.exit(ret)
