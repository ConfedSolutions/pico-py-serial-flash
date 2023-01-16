import sys
import traceback
import os
import serial.tools.list_ports
import serial
from flasher.elf import load_elf
from flasher.util import debug, puts, usage_flasher, exit_prog
from flasher.program import Image, Program


# Called at start of main(), to catch program arguments and respond accordingly.
def handle_args():
    _sys_args = sys.argv[1:]
    debug("All args: " + str(_sys_args))
    debug("Len args: " + str(len(_sys_args)))
    if len(_sys_args) <= 1 or len(_sys_args) > 3:
        return -1
    else:
        return _sys_args


# Runs the flasher program
def run(_sys_args):
    global bin_found, img
    if _sys_args == -1:
        puts(usage_flasher())
        exit_prog(True)

    port = str(_sys_args[0])
    flash_over_air = False

    if port.startswith("tcp:"):
        puts("Flashing over TCP is not yet implemented.")
        flash_over_air = True
        exit_prog(True)
    else:
        pc_port_paths = list()
        [pc_port_paths.append(p[0]) for p in list(serial.tools.list_ports.comports())]
        debug("All available serial communication ports on your machine: " + str(pc_port_paths))
        if port not in pc_port_paths:
            puts("Given serial port was not available.")
            exit_prog(True)
    puts("Serial connection made.")
    file_path = str(_sys_args[1])
    filename, file_extension = os.path.splitext(file_path)

    if file_extension == ".elf":
        debug("Elf found!: " + str(file_extension))
        if len(_sys_args) >= 3:
            puts("Base address for ELF files can't be specified")
            puts(usage_flasher())
            exit_prog(True)
        img = load_elf(file_path)
        debug("Returned .elf address: " + str(img.Addr) + " and data: " + str(img.Data))
        debug("ELF Image Data List Length: " + str(len(img.Data)))
        debug("")

    elif file_extension == ".bin":
        debug("Bin found!: " + str(file_extension))
        if len(_sys_args) != 3:
            puts("When flashing a binary file, make sure to pass a base address.")
            puts(usage_flasher())
            exit_prog(True)
        else:
            bin_found = True
    else:
        puts("Incorrect file extension. Currently supported extensions are: '.elf' and '.bin'.")
        exit_prog(True)
    base_addr: int = -1
    if bin_found:
        base_addr = int(_sys_args[2])
        puts("Binary file flashing not yet implemented.")
        exit_prog(True)

    debug("Base addr: " + str(base_addr))
    debug("Img data: " + str(img.Data))

    conn = None

    if img.Data is None or img.Addr <= -1:
        puts("Image file has not been read correctly.")
        exit_prog(True)

    if flash_over_air:
        puts("Flashing over TCP not yet implemented.")
        exit_prog(True)

    try:
        conn = serial.Serial(port=port, baudrate=921600, inter_byte_timeout=0.1, timeout=0)
    except ValueError as e:
        puts("Serial parameters out of range, with exception: " + str(e))
        exit_prog(True)
    except serial.SerialException as s_e:
        puts("Serial Exception. Serial port probably not available: " + str(s_e))
        exit_prog(True)

    puts("Image file has been read correctly.")
    # puts(conn.baudrate)
    # puts(Opcodes['OpcodeSync'])
    # puts(hex_bytes_to_int(Opcodes['OpcodeSync']))
    program_err = Program(conn, img, None)


# Module level global definitions
bin_found: bool = False
img: Image

# Main of the program, handles args and captures the run function in try except clauses
# to be able to easily catch errors
if __name__ == '__main__':
    sys_args = handle_args()
    try:
        run(sys_args)
        puts("\nJobs done. Pico should have rebooted into the flashed application.")
    except TypeError as err:
        puts(usage_flasher())
    except OSError as err:
        puts("OS error: {0}".format(err))
    except ValueError as err:
        puts("Value error, with error: " + str(err))
    except Exception:
        puts("Unexpected error: ", sys.exc_info()[0])
        puts(traceback.print_exc())
        raise
