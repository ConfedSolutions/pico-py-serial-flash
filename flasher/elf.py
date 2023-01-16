from elftools.elf.elffile import ELFFile
from flasher.util import debug, puts, exit_prog
from dataclasses import dataclass
from flasher.program import Image

FLASH_BASE: int = 0x10000000
FLASH_SIZE: int = 2 * 1024 * 1024


def _is_in_flash(addr, size: int) -> bool:
    return (addr >= FLASH_BASE) and (addr + size <= FLASH_BASE + FLASH_SIZE)


def _is_in_header(vaddr, size, header):
    return (vaddr >= header['p_vaddr']) and (vaddr + size <= (header['p_vaddr'] + header['p_memsz']))


@dataclass
class Chunk:
    PAddr: int
    Data: bytes


def chunk_sort_func(elem):
    return elem['PAddr']


def load_elf(file_name: str):
    debug("")
    chunks = []
    try:
        # Open .elf file on system, and redirect file stream to ELFFile constructor.
        with open(file_name, 'rb') as f_stream:
            f = ELFFile(f_stream)
            debug(f.header)
            count = 0
            # For each program header entry, check program adress and memsize. Check if fits in flash.
            for head_count in range(f.header['e_phnum']):
                prog_head = f.get_segment(head_count).header
                debug("Prog_HEAD: " + str(prog_head))
                p_paddr = prog_head['p_paddr']
                p_memsz = prog_head['p_memsz']
                if not _is_in_flash(p_paddr, p_memsz):
                    debug("IDX: " + str(head_count) + " is not in flash.")
                    debug("This is addr: " + str(p_paddr) + " and memsz: " + str(p_memsz))
                    continue
                # For each segment header entry, get size and address.
                for sec_count in range(f.header['e_shnum']):
                    count += 1
                    sec = f.get_section(sec_count)
                    sec_size = sec.data_size
                    sec_addr = sec.header['sh_addr']
                    is_in_header = _is_in_header(sec_addr, sec_size, prog_head)
                    # debug("Count: " + str(count) + " section header: " + str(sec.header))
                    # debug("Count: " + str(count) + " section size: " + str(sec_size))
                    # debug("Count: " + str(count) + " section addr: " + str(sec_addr))
                    # debug("Count: " + str(count) + " section is_in_header: " + str(is_in_header))
                    if sec_size > 0 and is_in_header:
                        prog_offset = sec_addr - prog_head['p_vaddr']
                        data = sec.data()
                        # debug("Count: " + str(count) + " section prog_offset: " + str(prog_offset))
                        # debug(hex_bytes_to_int(data))
                        this_chunk = Chunk(PAddr=p_paddr + prog_offset, Data=data)
                        chunks.append(this_chunk)
                    # debug("")

    except IOError:
        puts("Failed to read .ELF file. Used filename was: " + file_name)
        exit_prog(True)

    debug("")

    # debug("Chunks list: " + str(chunks))

    chunks.sort(key=lambda x: x.PAddr)

    # debug("Sorted chunks list: " + str(chunks))
    min_p_addr = chunks[0].PAddr
    p_addr_of_last_elem = chunks[len(chunks) - 1].PAddr
    len_of_last_elements_data = len(chunks[len(chunks) - 1].Data)
    max_p_addr = p_addr_of_last_elem + len_of_last_elements_data

    debug("min_p_addr: " + str(min_p_addr))
    debug("p_addr_of_last_elem: " + str(p_addr_of_last_elem))
    debug("len_of_last_elements_data: " + str(len_of_last_elements_data))
    debug("max_p_addr: " + str(max_p_addr))

    img_data = [bytes()] * (max_p_addr - min_p_addr)
    # debug(img_data)

    for c in chunks:
        img_data[c.PAddr-min_p_addr:] = c.Data
    # debug(img_data)

    img_addr = min_p_addr
    img_byte = bytes(img_data)

    img: Image = Image(img_addr, img_byte)
    return img


if __name__ == '__main__':
    debug("Const flash base: " + str(FLASH_BASE))
    debug("Const flash size: " + str(FLASH_SIZE))
