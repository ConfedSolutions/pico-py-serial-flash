# pico-py-serial-flash

### Information
Flashing application for Raspberry Pi Pico.

Used to serially flash the application firmware of a Pico, using Python.<br>
The Pico is expected to run [UsedBytes](https://github.com/usedbytes/rp2040-serial-bootloader) bootloader C application.
Instructions on how to flash the bootloader can be found on [UsedBytes Blogpost](https://blog.usedbytes.com/2021/12/pico-serial-bootloader/)

Originally the bootloader was written to be used with UsedBytes [GoLang application](https://github.com/usedbytes/serial-flash), 
but since we would prefer to use Python on our deployment systems, the GoLang app has been re-written in Python.

The UART cable used for testing is a [FTDI TTL-232R-3V3](https://docs.rs-online.com/588e/0900766b80d4cba6.pdf).

### Installation
1. Clone or download this repository.
2. Navigate to the downloaded directory `pico-py-serial-flash`.
3. Create a new Python Virtual Environment (tested with Python3.10): `python3 -m venv [name-of-venv]` and replace `[name-of-venv]` with a custom name.
4. Activate the newly created venv: `source [name-of-venv]/bin/activate`.
5. Install the modules in the requirements.txt file: `pip install -r requirements.txt`.
6. Done.

### Usage
1. Follow [UsedBytes instructions](https://blog.usedbytes.com/2021/12/pico-serial-bootloader/) on how to flash the Pico bootloader application to your Pico.
2. Create an application `.elf` binary file that works with the bootloader (as explained in chapter `Building programs to work with the bootloader` in [UsedBytes instructions](https://blog.usedbytes.com/2021/12/pico-serial-bootloader/)).
3. Activate your `pico-py-serial-flash` virtual environment (if not activated already) `source [name-of-venv]/bin/activate`
4. Wire a serial cable to the UART0 (the default UART used for flashing in the bootloader application).
5. The Pico stays in the bootloader, either by pulling down the `BOOTLOADER_ENTRY_PIN` (default is GPIO 15 of the Pico), or if the Pico has no application flashed on it.
6. Run the flasher application: `python3 main.py [port-to-uart-cable] [/path/to/elf/file.elf]`
7. For example: `python3 main.py /dev/ttyUSB0 /home/build/blink_noboot2.elf`
8. Wait for it to finish uploading, and voilà.

### Known issues
None. Please create a `GitHub Issue` when you encounter any.

### Known shortcomings
These are the shortcomings that the current Python implementation has. Please feel free to create a `pull request` if you have implemented any changes or new features.
1. There is no TCP implementation yet, to flash the Pico W over the air (unlike the original [GoLang application](https://github.com/usedbytes/serial-flash)).
2. The application does not support uploading `.bin` files (with according offsets).
3. Could use some kind of progress tracker, even though the flashing process can be quite quick for smaller application.