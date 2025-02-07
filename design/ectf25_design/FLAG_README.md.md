## to activate 
source .venv/bin/activate 


### 
 directories, 64 files
(ectf-vivek) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/ECTF_CODE/2025-ectf-insecure-example/decoder$ tree -L 1
.
├── Dockerfile
├── Makefile
├── build
├── build_out
├── firmware.ld
├── inc
├── project.mk
├── src
└── startup_firmware.S

4 directories, 5 files
(ectf-vivek) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/ECTF_CODE/2025-ectf-insecure-example/decoder$ cd ..
(ectf-vivek) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/ECTF_CODE/2025-ectf-insecure-example$ ls
LICENSE.txt  README.md  decoder  design  frames  secrets  tools
(ectf-vivek) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/ECTF_CODE/2025-ectf-insecure-example$ python -m ectf25_design.gen_subscription secrets/secrets.json subscription.bin 0xDEADBEEF 32 128 1
/mnt/c/Users/rajvi/OneDrive/Desktop/ECTF_CODE/2025-ectf-insecure-example/.venv/bin/python: Error while finding module specification for 'ectf25_design.gen_subscription' (ModuleNotFoundError: No module named 'ectf25_design')
(ectf-vivek) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/ECTF_CODE/2025-ectf-insecure-example$ python3.11 -m ectf25_design.gen_subscription secrets/secrets.
json subscription.bin 0xDEADBEEF 32 128 1
2025-01-22 14:49:11.147 | DEBUG    | __main__:main:95 - Generated subscription: b'\xef\xbe\xad\xde \x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
2025-01-22 14:49:11.167 | SUCCESS  | __main__:main:102 - Wrote subscription to /mnt/c/Users/rajvi/OneDrive/Desktop/ECTF_CODE/2025-ectf-insecure-example/subscription.bin
(ectf-vivek) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/ECTF_CODE/2025-ectf-insecure-example$ 




#######################################

# Update WSL2 and Ubuntu:
In PowerShell, run:

wsl --update
wsl -d Ubuntu


# In your Ubuntu WSL2 terminal, install the required packages

sudo apt update
sudo apt install linux-tools-generic hwdata
sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/*-generic/usbip 20


#  *********In Windows PowerShell (as Administrator), list the USB devices:
usbipd wsl list

# Attach the device to WSL2. Replace <busid> with the bus ID of your device from the previous step:

usbipd wsl attach --busid <busid>

# In your Ubuntu WSL2 terminal, verify the device is attached:

lsusb



## --------------------------- Restart the power shell ################

# Open PowerShell as an administrator.
# List available USB device

usbipd list


# Bind the device you want to use (replace <busid> with the actual bus ID):

usbipd bind --busid <busid>


# Attach the device to WSL:

usbipd attach --wsl --busid <busid>


# Verify the attachment in your WSL distribution:
lsusb



##### --------------- after doing the above thing ----- go to wsl and do this 

ls /dev/tty*


### **  If you don't see any new /dev/tty* devices after attaching, you can also try:

dmesg | grep tty

### 

python3.11 -m ectf25.utils.flash ./decoder/build_out/max78000.bin /dev/ttyACM0



###--------------------------------------------------

raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF$ ls
2025-ectf-bing
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF$ cd 2025-ectf-bing/
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ . ./.venv/bin/activate
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ ls /dev/tty*
/dev/tty    /dev/tty12  /dev/tty17  /dev/tty21  /dev/tty26  /dev/tty30  /dev/tty35  /dev/tty4   /dev/tty44  /dev/tty49  /dev/tty53  /dev/tty58  /dev/tty62  /dev/ttyACM0
/dev/tty0   /dev/tty13  /dev/tty18  /dev/tty22  /dev/tty27  /dev/tty31  /dev/tty36  /dev/tty40  /dev/tty45  /dev/tty5   /dev/tty54  /dev/tty59  /dev/tty63  /dev/ttyS0
/dev/tty1   /dev/tty14  /dev/tty19  /dev/tty23  /dev/tty28  /dev/tty32  /dev/tty37  /dev/tty41  /dev/tty46  /dev/tty50  /dev/tty55  /dev/tty6   /dev/tty7   /dev/ttyS1
/dev/tty10  /dev/tty15  /dev/tty2   /dev/tty24  /dev/tty29  /dev/tty33  /dev/tty38  /dev/tty42  /dev/tty47  /dev/tty51  /dev/tty56  /dev/tty60  /dev/tty8   /dev/ttyS2
/dev/tty11  /dev/tty16  /dev/tty20  /dev/tty25  /dev/tty3   /dev/tty34  /dev/tty39  /dev/tty43  /dev/tty48  /dev/tty52  /dev/tty57  /dev/tty61  /dev/tty9   /dev/ttyS3
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ 



##----------------------------------------------------------------------------------------------------------- OPENOCD COMMAND -----------------------------------
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ python3.11 -m ectf25.utils.flash ./gdb_challenge_25.bin /dev/ttyACM0
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/serial/serialposix.py", line 322, in open
    self.fd = os.open(self.portstr, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/dev/ttyACM0'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/raj/.local/lib/python3.11/site-packages/ectf25/utils/flash.py", line 107, in <module>
    main()
  File "/home/raj/.local/lib/python3.11/site-packages/ectf25/utils/flash.py", line 103, in main
    BootloaderIntf(args.port).update(image)
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/raj/.local/lib/python3.11/site-packages/ectf25/utils/flash.py", line 43, in __init__
    self.ser = serial.Serial(port=port, baudrate=115200, **serial_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/serial/serialutil.py", line 244, in __init__
    self.open()
  File "/usr/lib/python3/dist-packages/serial/serialposix.py", line 325, in open
    raise SerialException(msg.errno, "could not open port {}: {}".format(self._port, msg))
serial.serialutil.SerialException: [Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ ls /dev/tty*
/dev/tty    /dev/tty12  /dev/tty17  /dev/tty21  /dev/tty26  /dev/tty30  /dev/tty35  /dev/tty4   /dev/tty44  /dev/tty49  /dev/tty53  /dev/tty58  /dev/tty62  /dev/ttyACM1
/dev/tty0   /dev/tty13  /dev/tty18  /dev/tty22  /dev/tty27  /dev/tty31  /dev/tty36  /dev/tty40  /dev/tty45  /dev/tty5   /dev/tty54  /dev/tty59  /dev/tty63  /dev/ttyS0
/dev/tty1   /dev/tty14  /dev/tty19  /dev/tty23  /dev/tty28  /dev/tty32  /dev/tty37  /dev/tty41  /dev/tty46  /dev/tty50  /dev/tty55  /dev/tty6   /dev/tty7   /dev/ttyS1
/dev/tty10  /dev/tty15  /dev/tty2   /dev/tty24  /dev/tty29  /dev/tty33  /dev/tty38  /dev/tty42  /dev/tty47  /dev/tty51  /dev/tty56  /dev/tty60  /dev/tty8   /dev/ttyS2
/dev/tty11  /dev/tty16  /dev/tty20  /dev/tty25  /dev/tty3   /dev/tty34  /dev/tty39  /dev/tty43  /dev/tty48  /dev/tty52  /dev/tty57  /dev/tty61  /dev/tty9   /dev/ttyS3
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ python3.11 -m ectf25.utils.flash ./gdb_challenge_25.bin /dev/ttyACM1
2025-02-04 18:17:59.073 | INFO     | __main__:update:70 - Requesting update
2025-02-04 18:18:00.890 | INFO     | __main__:update:77 - Update started
2025-02-04 18:18:00.891 | INFO     | __main__:update:78 - Sending image data...
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 14336/14336 [00:47<00:00, 299.62it/s]
2025-02-04 18:18:48.788 | INFO     | __main__:update:83 - Listening for installation status...

2025-02-04 18:18:48.789 | SUCCESS  | __main__:update:89 - Update Complete!

(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ ls
LICENSE.txt  README.md  deadbeef_build  decoder  design  frames  gdb_challenge_25.bin  gdb_challenge_25.elf  global.secrets  tools
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ python -c 'print("\x5a"*0xc, end="")' > 5a.bin

(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ openocd -f interface/cmsis-dap.cfg -f target/max78000.cfg -c "init; reset halt; max32xxx mass_erase 0; program gdb_challenge_25.bin verify 0x10000000; program 5a.bin verify 0x10002000; program gdb_challenge_25.elf verify reset exit"
Open On-Chip Debugger (Analog Devices 0.12.0-1.0.0-7)  OpenOCD 0.12.0 (2023-09-27-07:53)
Licensed under GNU GPL v2
Report bugs to <processor.tools.support@analog.com>
Info : CMSIS-DAP: SWD supported
Info : CMSIS-DAP: Atomic commands supported
Info : CMSIS-DAP: Test domain timer supported
Info : CMSIS-DAP: FW Version = 2.1.0
Info : CMSIS-DAP: Serial# = 0423170206a0ca9600000000000000000000000097969906
Info : CMSIS-DAP: Interface Initialised (SWD)
Info : SWCLK/TCK = 1 SWDIO/TMS = 1 TDI = 0 TDO = 0 nTRST = 0 nRESET = 1
Info : CMSIS-DAP: Interface ready
Info : clock speed 2000 kHz
Info : SWD DPIDR 0x2ba01477
Info : [max32xxx.cpu] Cortex-M4 r0p1 processor detected
Info : [max32xxx.cpu] target has 6 breakpoints, 4 watchpoints
Info : starting gdb server for max32xxx.cpu on 3333
Info : Listening on port 3333 for gdb connections
[max32xxx.cpu] halted due to debug-request, current mode: Thread 
xPSR: 0x21000000 pc: 0x10004728 msp: 0x2001ffd8
Info : SWD DPIDR 0x2ba01477
[max32xxx.cpu] halted due to debug-request, current mode: Thread 
xPSR: 0x81000000 pc: 0x00002124 msp: 0x20003ff0
Info : SWD DPIDR 0x2ba01477
[max32xxx.cpu] halted due to debug-request, current mode: Thread 
xPSR: 0x81000000 pc: 0x00002124 msp: 0x20003ff0
** Programming Started **
** Programming Finished **
** Verify Started **
** Verified OK **
Info : SWD DPIDR 0x2ba01477
[max32xxx.cpu] halted due to debug-request, current mode: Thread 
xPSR: 0x81000000 pc: 0x00002124 msp: 0x20003ff0
** Programming Started **
** Programming Finished **
** Verify Started **
** Verified OK **
Info : SWD DPIDR 0x2ba01477
[max32xxx.cpu] halted due to debug-request, current mode: Thread 
xPSR: 0x81000000 pc: 0x00002124 msp: 0x20003ff0
** Programming Started **
** Programming Finished **
** Verify Started **
** Verified OK **
** Resetting Target **
Info : SWD DPIDR 0x2ba01477
shutdown command invoked
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ openocd -s scripts/ -f interface/cmsis-dap.cfg -f target/max78000.cfg -c "bindto 0.0.0.0; init"
Open On-Chip Debugger (Analog Devices 0.12.0-1.0.0-7)  OpenOCD 0.12.0 (2023-09-27-07:53)
Licensed under GNU GPL v2
Report bugs to <processor.tools.support@analog.com>
Info : CMSIS-DAP: SWD supported
Info : CMSIS-DAP: Atomic commands supported
Info : CMSIS-DAP: Test domain timer supported
Info : CMSIS-DAP: FW Version = 2.1.0
Info : CMSIS-DAP: Serial# = 0423170206a0ca9600000000000000000000000097969906
Info : CMSIS-DAP: Interface Initialised (SWD)
Info : SWCLK/TCK = 1 SWDIO/TMS = 1 TDI = 0 TDO = 0 nTRST = 0 nRESET = 1
Info : CMSIS-DAP: Interface ready
Info : clock speed 2000 kHz
Info : SWD DPIDR 0x2ba01477
Info : [max32xxx.cpu] Cortex-M4 r0p1 processor detected
Info : [max32xxx.cpu] target has 6 breakpoints, 4 watchpoints
Info : starting gdb server for max32xxx.cpu on 3333
Info : Listening on port 3333 for gdb connections
Info : Listening on port 6666 for tcl connections
Info : Listening on port 4444 for telnet connections


##### -------------------->in different terminat  use this  after doing the above 
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF$ telnet localhost 4444
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Open On-Chip Debugger
> reg
===== arm v7m registers
(0) r0 (/32)
(1) r1 (/32)
(2) r2 (/32)
(3) r3 (/32)
(4) r4 (/32)
(5) r5 (/32)
(6) r6 (/32)
(7) r7 (/32)
(8) r8 (/32)
(9) r9 (/32)
(10) r10 (/32)
(11) r11 (/32)
(12) r12 (/32)
(13) sp (/32)
(14) lr (/32)
(15) pc (/32)
(16) xPSR (/32)
(17) msp (/32)
(18) psp (/32)
(20) primask (/1)
(21) basepri (/8)
(22) faultmask (/1)
(23) control (/3)
(42) d0 (/64)
(43) d1 (/64)
(44) d2 (/64)
(45) d3 (/64)
(46) d4 (/64)
(47) d5 (/64)
(48) d6 (/64)
(49) d7 (/64)
(50) d8 (/64)
(51) d9 (/64)
(52) d10 (/64)
(53) d11 (/64)
(54) d12 (/64)
(55) d13 (/64)
(56) d14 (/64)
(57) d15 (/64)
(58) fpscr (/32)
===== Cortex-M DWT registers


###---------------------------------------------------------------------------

(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker run --rm -it -p 3333:3333/tcp -v /mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing:/out --workdir=/root --entrypoint /bin/bash build-decoder -c "cp -r /out/* /root/ && gdb-multiarch gdb_challenge_25.elf"
docker: Error response from daemon: driver failed programming external connectivity on endpoint jovial_chatterjee (32b17e14b5bb371e798ba40be3fc5f145e810d4ac7973fec680a7930f3f851fd): Error starting userland proxy: listen tcp4 0.0.0.0:3333: bind: address already in use.
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker run --rm -it -p 5555:3333/tcp -v /mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing:/out --workdir=/root --entrypoint /bin/bash build-decoder -c "cp -r /out/* /root/ && gdb-multiarch gdb_challenge_25.elf"
GNU gdb (Ubuntu 15.0.50.20240403-0ubuntu1) 15.0.50.20240403-git
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from gdb_challenge_25.elf...
(gdb) target remote host.docker.internal:3333
host.docker.internal:3333: cannot resolve name: Name or service not known

(gdb) target remote 172.23.132.151:3333
Remote debugging using 172.23.132.151:3333
0x1000ee6e in MXC_Delay (us=<optimized out>) at /root/msdk-2024_02/Libraries/CMSIS/../PeriphDrivers/Source/SYS/mxc_delay.c:233
233         while (SysTick->VAL > endtick) {}
(gdb) 


## ------------------------------------------------------ to get your dokcer ps  --------------------------------------------
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                                       NAMES
2c31a981feb1   build-decoder   "/bin/bash -c 'cp -r…"   13 minutes ago   Up 13 minutes   0.0.0.0:5555->3333/tcp, :::5555->3333/tcp   beautiful_hugle
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' beautiful_hugle
172.17.0.2
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ . ./.venv/bin/activate
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' beautiful_hugle
172.17.0.2
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ sudo lsof -i tcp:3333
[sudo] password for raj: 
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
openocd 9688  raj    4u  IPv4  75064      0t0  TCP *:3333 (LISTEN)
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' beautiful_hugle

Error: No such object: beautiful_hugle
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                                       NAMES
08d7eea55bfd   build-decoder   "/bin/bash -c 'cp -r…"   2 minutes ago   Up 2 minutes   0.0.0.0:5555->3333/tcp, :::5555->3333/tcp   gallant_pasteur
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' beautiful_hugle

Error: No such object: beautiful_hugle
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                                       NAMES
08d7eea55bfd   build-decoder   "/bin/bash -c 'cp -r…"   2 minutes ago   Up 2 minutes   0.0.0.0:5555->3333/tcp, :::5555->3333/tcp   gallant_pasteur
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ ip addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
172.23.132.151
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ 



### --------------------------------------------------------------------------

raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF$ cd 2025-ectf-bing/
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ . ./.venv/bin/activate
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ sudo minicom -s
[sudo] password for raj: 


after above put your port id
then press enter --->
save


### ----------------------------------------------------------------------------------------------------------

(gdb) x gdb_challenge
0x1000e5d0 <gdb_challenge>:     0x00000000
(gdb) x 0x1000e5d0
0x1000e5d0 <gdb_challenge>:     0x00000000
(gdb) (gdb) b do_some_math
Undefined command: "".  Try "help".
(gdb)  b do_some_math
Breakpoint 2 at 0x1000e290: file src/debugger_challenge.c, line 39.
(gdb) c
Continuing.
[New Thread 1]
[Remote target exited]
[Switching to Thread 1]

Thread 2 "max32xxx.cpu" hit Breakpoint 1, gdb_challenge () at src/debugger_challenge.c:102
warning: 102    src/debugger_challenge.c: No such file or directory
(gdb) info breakpoints
Arguments must be numbers or '$' variables.
(gdb)  b gdb_challenge
Note: breakpoint 1 also set at pc 0x1000e5d0.
Breakpoint 3 at 0x1000e5d0: file src/debugger_challenge.c, line 102.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 2, do_some_math (a=0, b=0, c=268496157, d=537001936) at src/debugger_challenge.c:39
39      in src/debugger_challenge.c
(gdb) x/1i to_hex
   0x1000e738 <to_hex>: push    {r4}
(gdb)


## ===============

value1 = 0x1000e738
value 2  = 0x2001ffe0

value 3 =  0xe13f7732  

set *(int *)($sp) = 0xe13f7732 

set $r2 = 0xcafeca
####  =====

0x1000e738 <to_hex>: push    {r4}
value 1 : 
info registers sp
    -> sp             0x2001ffe0          0x2001ffe0


### ------------------------------------

102     in src/debugger_challenge.c
(gdb)  x/10wx 0x2001ffe0
0x2001ffe0:     0x00000000      0x1000ee55      0x10010f4c      0x00000000
0x2001fff0:     0x00000000      0x1000e701      0x00000000      0x1000eaf1
0x20020000:     0

### -------------------------------- 

41      in src/debugger_challenge.c
r2             0xe13f7732          -515934414
r2             0xe13f7732          -515934414




###  ============================================================


Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = -1057017071
New value = -515934414
do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0xe13f7732          -515934414
r2             0xe13f7732          -515934414
(gdb) info break
Num     Type           Disp Enb Address    What
1       breakpoint     keep y   0x1000e5d0 in gdb_challenge at src/debugger_challenge.c:102
        breakpoint already hit 2 times
2       breakpoint     keep y   0x1000e290 in do_some_math at src/debugger_challenge.c:39
        breakpoint already hit 2 times
3       breakpoint     keep y   0x1000e5d0 in gdb_challenge at src/debugger_challenge.c:102
        breakpoint already hit 1 time
4       breakpoint     keep y   0x1000e5d0 in gdb_challenge at src/debugger_challenge.c:102
        breakpoint already hit 1 time
5       watchpoint     keep y              $r2
        breakpoint already hit 7 times
        info registers r2
6       watchpoint     keep y              $r2
        breakpoint already hit 6 times
        info registers r2


### ---------------------------------------------------------------

b *0x1000e2e0  // setting the break point 

0x1000e2d6 in do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0x0                 0
r2             0x0                 0
(gdb)  info registers r0
r0             0xdeadbeef       


(gdb) info registers r0 r1 r2 r3
r0             0x0                 0
r1             0x0                 0
r2             0x16                22
r3             0x0                 0
Missing register name
(gdb)


### --------------------------------------------------

0x25 is % 


flag :

Welcome to minicom 2.8

OPTIONS: I18n
Port /dev/ttyACM1, 21:12:27

Press CTRL-A Z for help on special keys

%G��Checking arguments...
                         Welcome to the GDB challenge
                                                     0123456789abcde@�@


## ------------------------------------------------------------------  command to get the flag ----------------------------------------------------------------------------

(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker run --rm -it -p 3333:3333/tcp -v /mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing:/out --workdir=/root --entrypoint /bin/bash build-decoder -c "cp -r /out/* /root/ && gdb-multiarch gdb_challenge_25.elf"
docker: Error response from daemon: driver failed programming external connectivity on endpoint jovial_chatterjee (32b17e14b5bb371e798ba40be3fc5f145e810d4ac7973fec680a7930f3f851fd): Error starting userland proxy: listen tcp4 0.0.0.0:3333: bind: address already in use.
(fnu_ectf) raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing$ docker run --rm -it -p 5555:3333/tcp -v /mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing:/out --workdir=/root --entrypoint /bin/bash build-decoder -c "cp -r /out/* /root/ && gdb-multiarch gdb_challenge_25.elf"
GNU gdb (Ubuntu 15.0.50.20240403-0ubuntu1) 15.0.50.20240403-git
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from gdb_challenge_25.elf...
(gdb) target remote host.docker.internal:3333
host.docker.internal:3333: cannot resolve name: Name or service not known

(gdb) target remote 172.23.132.151:3333
Remote debugging using 172.23.132.151:3333
0x1000ee6e in MXC_Delay (us=<optimized out>) at /root/msdk-2024_02/Libraries/CMSIS/../PeriphDrivers/Source/SYS/mxc_delay.c:233
233         while (SysTick->VAL > endtick) {}
(gdb) b gdb_challenge
Breakpoint 1 at 0x1000e5d0: file src/debugger_challenge.c, line 102.
Note: automatically using hardware breakpoints for read-only addresses.
(gdb) info registers
r0             0x363c7f            3554431
r1             0xe000e000          -536813568
r2             0x363c7f            3554431
r3             0x9744cf            9913551
r4             0x20000004          536870916
r5             0x0                 0
r6             0x0                 0
r7             0x2001fff8          537001976
r8             0x0                 0
r9             0x0                 0
r10            0x0                 0
r11            0x0                 0
r12            0xf4240000          -198967296
sp             0x2001ffe8          0x2001ffe8
lr             0x1000ed1d          268496157
pc             0x1000ee6e          0x1000ee6e <MXC_Delay+46>
xPSR           0x21000000          553648128
fpscr          0x0                 0
msp            0x2001ffe8          0x2001ffe8
psp            0x0                 0x0
primask        0x0                 0
basepri        0x0                 0
faultmask      0x0                 0
control        0x0                 0
(gdb) x gdb_challenge
0x1000e5d0 <gdb_challenge>:     0x00000000
(gdb) x 0x1000e5d0
0x1000e5d0 <gdb_challenge>:     0x00000000
(gdb) (gdb) b do_some_math
Undefined command: "".  Try "help".
(gdb)  b do_some_math
Breakpoint 2 at 0x1000e290: file src/debugger_challenge.c, line 39.
(gdb) c
r7             0x2001fff8          537001976
r8             0x0                 0
r9             0x0                 0
r10            0x0                 0
r11            0x0                 0
r12            0xf4240000          -198967296
sp             0x2001ffe8          0x2001ffe8
lr             0x1000ed1d          268496157
pc             0x1000ee6e          0x1000ee6e <MXC_Delay+46>
xPSR           0x21000000          553648128
fpscr          0x0                 0
msp            0x2001ffe8          0x2001ffe8
psp            0x0                 0x0
primask        0x0                 0
basepri        0x0                 0
faultmask      0x0                 0
control        0x0                 0
(gdb) x gdb_challenge
0x1000e5d0 <gdb_challenge>:     0x00000000
(gdb) x 0x1000e5d0
0x1000e5d0 <gdb_challenge>:     0x00000000
(gdb) (gdb) b do_some_math
Undefined command: "".  Try "help".
(gdb)  b do_some_math
Breakpoint 2 at 0x1000e290: file src/debugger_challenge.c, line 39.
(gdb) c
pc             0x1000ee6e          0x1000ee6e <MXC_Delay+46>
xPSR           0x21000000          553648128
fpscr          0x0                 0
msp            0x2001ffe8          0x2001ffe8
psp            0x0                 0x0
primask        0x0                 0
basepri        0x0                 0
faultmask      0x0                 0
control        0x0                 0
(gdb) x gdb_challenge
0x1000e5d0 <gdb_challenge>:     0x00000000
(gdb) x 0x1000e5d0
0x1000e5d0 <gdb_challenge>:     0x00000000
(gdb) (gdb) b do_some_math
Undefined command: "".  Try "help".
(gdb)  b do_some_math
Breakpoint 2 at 0x1000e290: file src/debugger_challenge.c, line 39.
(gdb) c
(gdb) c
Continuing.
[New Thread 1]
[Remote target exited]
[Switching to Thread 1]

Thread 2 "max32xxx.cpu" hit Breakpoint 1, gdb_challenge () at src/debugger_challenge.c:102
warning: 102    src/debugger_challenge.c: No such file or directory
(gdb) info breakpoints
Arguments must be numbers or '$' variables.
(gdb)  b gdb_challenge
Note: breakpoint 1 also set at pc 0x1000e5d0.
Breakpoint 3 at 0x1000e5d0: file src/debugger_challenge.c, line 102.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 2, do_some_math (a=0, b=0, c=268496157, d=537001936) at src/debugger_challenge.c:39
39      in src/debugger_challenge.c
(gdb) x/1i to_hex
   0x1000e738 <to_hex>: push    {r4}
(gdb) value1 = 0x1000e738
Undefined command: "value1".  Try "help".
(gdb) info r
r0             0xdeadbeef          -559038737
r1             0xfeedface          -17958194
r2             0xcafecafe          -889271554
r3             0xc0ff3311          -1057017071
r4             0x0                 0
r5             0x0                 0
r6             0x0                 0
r7             0x2001ffe8          537001960
r8             0x0                 0
r9             0x0                 0
r10            0x0                 0
r11            0x0                 0
r12            0xf4240000          -198967296
sp             0x2001ffe0          0x2001ffe0
lr             0x1000e5e3          268494307
pc             0x1000e290          0x1000e290 <do_some_math>
xPSR           0x81000000          -2130706432
fpscr          0x0                 0
msp            0x2001ffe0          0x2001ffe0
--Type <RET> for more, q to quit, c to continue without paging--
psp            0x0                 0x0
primask        0x0                 0
basepri        0x0                 0
faultmask      0x0                 0
control        0x0                 0
(gdb) x/1i to_hex
   0x1000e738 <to_hex>: push    {r4}
(gdb) value1 = 0x1000e738
Undefined command: "value1".  Try "help".
(gdb) info registers sp
sp             0x2001ffe0          0x2001ffe0
(gdb) b gdb_challenge
Note: breakpoints 1 and 3 also set at pc 0x1000e5d0.
Breakpoint 4 at 0x1000e5d0: file src/debugger_challenge.c, line 102.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 1, gdb_challenge () at src/debugger_challenge.c:102
102     in src/debugger_challenge.c
(gdb)  x/10wx 0x2001ffe0
0x2001ffe0:     0x00000000      0x1000ee55      0x10010f4c      0x00000000
0x2001fff0:     0x00000000      0x1000e701      0x00000000      0x1000eaf1
0x20020000:     0x00000000      0x00000000
(gdb) set $r0 = 0x1000e738
sp             0x2001ffe0          0x2001ffe0
(gdb) b gdb_challenge
Note: breakpoints 1 and 3 also set at pc 0x1000e5d0.
Breakpoint 4 at 0x1000e5d0: file src/debugger_challenge.c, line 102.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 1, gdb_challenge () at src/debugger_challenge.c:102
102     in src/debugger_challenge.c
(gdb)  x/10wx 0x2001ffe0
sp             0x2001ffe0          0x2001ffe0
(gdb) b gdb_challenge
Note: breakpoints 1 and 3 also set at pc 0x1000e5d0.
Breakpoint 4 at 0x1000e5d0: file src/debugger_challenge.c, line 102.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 1, gdb_challenge () at src/debugger_challenge.c:102
102     in src/debugger_challenge.c
sp             0x2001ffe0          0x2001ffe0
sp             0x2001ffe0          0x2001ffe0
(gdb) b gdb_challenge
Note: breakpoints 1 and 3 also set at pc 0x1000e5d0.
Breakpoint 4 at 0x1000e5d0: file src/debugger_challenge.c, line 102.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 1, gdb_challenge () at src/debugger_challenge.c:102
102     in src/debugger_challenge.c
(gdb)  x/10wx 0x2001ffe0
0x2001ffe0:     0x00000000      0x1000ee55      0x10010f4c      0x00000000
0x2001fff0:     0x00000000      0x1000e701      0x00000000      0x1000eaf1
0x20020000:     0x00000000      0x00000000
(gdb) set $r0 = 0x1000e738
(gdb) set $r2 = 0x2001ffe0
(gdb)  x/10wx 0x2001ffe0
0x2001ffe0:     0x00000000      0x1000ee55      0x10010f4c      0x00000000
0x2001fff0:     0x00000000      0x1000e67d      0x00000000      0x1000eaf1
0x20020000:     0x00000000      0x00000000
(gdb) watch $r2
Watchpoint 5: $r2
(gdb) commands
Type commands for breakpoint(s) 5, one per line.
End with a line saying just "end".
>info registers r2
>end
(gdb) c
Continuing.
[max32xxx.cpu] target not halted
target max32xxx.cpu was not halted when step was requested

Thread 2 "max32xxx.cpu" hit Breakpoint 2, do_some_math (a=0, b=0, c=268496157, d=537001936) at src/debugger_challenge.c:39
39      in src/debugger_challenge.c
r2             0xcafecafe          -889271554
(gdb) watch $r2
Watchpoint 6: $r2
(gdb) commands
Type commands for breakpoint(s) 6, one per line.
End with a line saying just "end".
>info registers r2
>end
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = -889271554
New value = -559038737

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = -889271554
New value = -559038737
0x1000e2a0 in do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0xdeadbeef          -559038737
r2             0xdeadbeef          -559038737
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = -559038737
New value = -889271554

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = -559038737
New value = -889271554
0x1000e2a8 in do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0xcafecafe          -889271554
r2             0xcafecafe          -889271554
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = -889271554
New value = 0

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = -889271554
New value = 0
do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0x0                 0
r2             0x0                 0
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = 0
New value = -17958194

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = 0
New value = -17958194
0x1000e2c8 in do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0xfeedface          -17958194
r2             0xfeedface          -17958194
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = -17958194
New value = -1057017071

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = -17958194
New value = -1057017071
0x1000e2cc in do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0xc0ff3311          -1057017071
r2             0xc0ff3311          -1057017071
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = -1057017071
New value = -515934414

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = -1057017071
New value = -515934414
do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0xe13f7732          -515934414
r2             0xe13f7732          -515934414
(gdb) info break
Num     Type           Disp Enb Address    What
1       breakpoint     keep y   0x1000e5d0 in gdb_challenge at src/debugger_challenge.c:102
        breakpoint already hit 2 times
2       breakpoint     keep y   0x1000e290 in do_some_math at src/debugger_challenge.c:39
        breakpoint already hit 2 times
3       breakpoint     keep y   0x1000e5d0 in gdb_challenge at src/debugger_challenge.c:102
        breakpoint already hit 1 time
4       breakpoint     keep y   0x1000e5d0 in gdb_challenge at src/debugger_challenge.c:102
        breakpoint already hit 1 time
5       watchpoint     keep y              $r2
        breakpoint already hit 7 times
        info registers r2
6       watchpoint     keep y              $r2
        breakpoint already hit 6 times
        info registers r2
(gdb) b *0x1000e2e0
Breakpoint 7 at 0x1000e2e0: file src/debugger_challenge.c, line 42.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = -515934414
New value = 0

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = -515934414
New value = 0
0x1000e2d6 in do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:41
41      in src/debugger_challenge.c
r2             0x0                 0
r2             0x0                 0
(gdb)  info registers r0
r0             0xdeadbeef          -559038737
(gdb) b check_f
Function "check_f" not defined.
Make breakpoint pending on future shared library load? (y or [n]) n
(gdb)  b *0x1000e2e0
Note: breakpoint 7 also set at pc 0x1000e2e0.
Breakpoint 8 at 0x1000e2e0: file src/debugger_challenge.c, line 42.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 7, 0x1000e2e0 in do_some_math (a=-559038737, b=-17958194, c=-889271554, d=-1057017071) at src/debugger_challenge.c:42
42      in src/debugger_challenge.c
(gdb) info registers r0
r0             0x0                 0
(gdb) set $r0=111
(gdb) info registers r0
r0             0x6f                111
(gdb) set $r0=0
(gdb) x 0x2001fff8
0x2001fff8:     0x00000000
(gdb)  set *0x2001fff8=0x111
(gdb) set *0x2001fff8=0
(gdb) b check_flag
Breakpoint 9 at 0x1000e4b0: file src/debugger_challenge.c, line 74.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = 0
New value = 22

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = 0
New value = 22
0x1000e5e8 in gdb_challenge () at src/debugger_challenge.c:107
107     in src/debugger_challenge.c
r2             0x16                22
r2             0x16                22
(gdb) (gdb) info registers r0 r1 r2 r3
Undefined command: "".  Try "help".
(gdb) info registers r0 r1 r2 r3
r0             0x0                 0
r1             0x0                 0
r2             0x16                22
r3             0x0                 0
Missing register name
(gdb) set $r0 = 0x4c09b410
(gdb) set $r2 = 0x2001ffe0
(gdb) set *(int *)($sp) = 0xe13f7732 
(gdb) info registers
r0             0x1000e738          268494648
r1             0x0                 0
r2             0x2001ffe0          537001952
r3             0x0                 0
r4             0x0                 0
r5             0x0                 0
r6             0x0                 0
r7             0x2001ffe8          537001960
r8             0x0                 0
r9             0x0                 0
r10            0x0                 0
r11            0x0                 0
r12            0xf4240000          -198967296
sp             0x2001ffe0          0x2001ffe0
lr             0x1000e5e3          268494307
pc             0x1000e5e8          0x1000e5e8 <gdb_challenge+24>
xPSR           0x1000000           16777216
fpscr          0x0                 0
msp            0x2001ffe0          0x2001ffe0
psp            0x0                 0x0
primask        0x0                 0
basepri        0x0                 0
faultmask      0x0                 0
control        0x0                 0
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = 22
New value = 537001952

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = 22
New value = 537001952
0x1000e5ea in gdb_challenge () at src/debugger_challenge.c:107
107     in src/debugger_challenge.c
r2             0x2001ffe0          537001952
r2             0x2001ffe0          537001952
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = 537001952
New value = 1074012160

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = 537001952
New value = 1074012160
uart_writebyte (data=37 '%') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
r2             0x40042000          1074012160
r2             0x40042000          1074012160
(gdb) (gdb) p/x $r0  # r0 holds 'data' for uart_writebyte
Undefined command: "".  Try "help".
(gdb)  p/x $r0  # r0 holds 'data' for uart_writebyte
Invalid character '#' in expression.
(gdb)  p/x $r0  
$1 = 0x25
(gdb)  p/x $r0  
$2 = 0x25
(gdb)  stepi
A syntax error in expression, near the end of `
'.
(gdb)  p/c $r0

$3 = 37 '%'
(gdb)  p/c $r0

$4 = 37 '%'
(gdb) c      
A syntax error in expression, near the end of `
'.
(gdb) stepi
0x1000e8d8      66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = 1074012160
New value = 9

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = 1074012160
New value = 9
__sflush_r (ptr=0x20000010 <_impure_data>, fp=0x20000a44 <__sf+104>) at ../../../../../../newlib/libc/stdio/fflush.c:112
warning: 112    ../../../../../../newlib/libc/stdio/fflush.c: No such file or directory
r2             0x9                 9
r2             0x9                 9
(gdb)  p/c $r0

$5 = 16 '\020'
(gdb)  b uart_writebyte
Breakpoint 10 at 0x1000e8d4: file src/simple_uart.c, line 66.
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = 9
New value = 0

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = 9
New value = 0
0x1000e8b2 in write_packet (type=<optimized out>, buf=0x10010efc, len=<optimized out>) at src/host_messaging.c:160
160             result = write_bytes(buf, len, type != DEBUG_MSG);
r2             0x0                 0
r2             0x0                 0
(gdb)  p/c $r0

$6 = 0 '\000'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=67 'C') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$7 = 67 'C'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Watchpoint 5: $r2

Old value = 0
New value = 1074012160

Thread 2 "max32xxx.cpu" hit Watchpoint 6: $r2

Old value = 0
New value = 1074012160
uart_writebyte (data=67 'C') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
r2             0x40042000          1074012160
r2             0x40042000          1074012160
(gdb)  p/c $r0

$8 = 67 'C'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=104 'h') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$9 = 104 'h'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=101 'e') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$10 = 101 'e'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=99 'c') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$11 = 99 'c'
(gdb)  p/c $r0

$12 = 99 'c'
(gdb)  p/c $r0

$13 = 99 'c'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=107 'k') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$14 = 107 'k'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=105 'i') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$15 = 105 'i'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=110 'n') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$16 = 110 'n'
(gdb)  p/c $r0

$17 = 110 'n'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=103 'g') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$18 = 103 'g'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=32 ' ') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$19 = 32 ' '
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=97 'a') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$20 = 97 'a'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=114 'r') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$21 = 114 'r'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=103 'g') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$22 = 103 'g'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=117 'u') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$23 = 117 'u'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=109 'm') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$24 = 109 'm'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=101 'e') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$25 = 101 'e'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=110 'n') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$26 = 110 'n'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=116 't') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$27 = 116 't'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=115 's') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$28 = 115 's'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=46 '.') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$29 = 46 '.'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=46 '.') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$30 = 46 '.'
(gdb) c
Continuing.

Thread 2 "max32xxx.cpu" hit Breakpoint 10, uart_writebyte (data=46 '.') at src/simple_uart.c:66
66          while (MXC_UART_GET_UART(CONSOLE_UART)->status & MXC_F_UART_STATUS_TX_FULL) {
(gdb)  p/c $r0

$31 = 46 '

