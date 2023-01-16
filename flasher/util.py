# Returns flasher usage message.
import struct


def usage_flasher():
    return str("Usage: main.py port filepath [BASE_ADDR] \nFor example: main.py /dev/ttyUSB0 ~/pico/test.elf")


# Wrapper function to be able to easily disable/alter all debugging string output.
def debug(self, *args):
    # print(self, *args, sep=' ', end='\n', file=None)
    pass


# Wrapper function to be able to easily disable/alter all user string output.
def puts(self, *args):
    print(self, *args, sep=' ', end='\n', file=None)


# Wrapper function to easily change behaviour before exiting program.
def exit_prog(before_flash: bool = True):
    if before_flash:
        puts("Program was exited before flashing the target device.")
    else:
        puts("Program has exited after/during flash. Be careful, flash might be damaged.")
    exit()


def hex_bytes_to_int(hex_bytes: bytes) -> []:
    tup = struct.unpack('<' + 'B' * len(hex_bytes), hex_bytes)
    test_list = list()
    for val in tup:
        test_list.append(val)
    return test_list


def bytes_to_little_end_uint32(b: bytes):
    new_int = int(b[0]) | int(b[1]) << 8 | int(b[2]) << 16 | int(b[3]) << 24
    return new_int


def little_end_uint32_to_bytes(v: int):
    return v.to_bytes((v.bit_length() + 7) // 8, 'little')


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    puts(f'\r{prefix} |{bar}| {percent}% {suffix}')
    # Print New Line on Complete
    if iteration == total:
        puts("")
