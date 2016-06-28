#!/usr/bin/env python3
import sys
import argparse

OFFSET = 0xc0e0
# Not at all sure about the max length of the binary path to be started but
LENGTH = 32
CONTENT = b'/\x00b\x00i\x00n\x00/\x00b\x00a\x00s\x00h'


def find_offset(binary):
    for i in range(0, len(binary)):
        if binary[i:i+len(CONTENT)] == CONTENT:
            return i

    return -1


def check_offset(binary):
    orig = binary[OFFSET:OFFSET+len(CONTENT)]

    return orig == CONTENT


def stob(val):
    val = val.encode('ascii')
    ret = bytearray()

    for i in range(0, LENGTH):
        if (i != 0 and i % 2 == 1) or i >= 2 * len(val):
            ret += b'\x00'
            continue

        if i % 2 == 0:
            ret += val[i // 2].to_bytes(1, byteorder=sys.byteorder)

    assert len(ret) == LENGTH
    return ret


def parse_args(argv):
    parser = argparse.ArgumentParser(description='''Patch Windows Subsystem for Linux\'s bash.exe to be able run any
        Linux executable file present in the WSL container.''')
    parser.add_argument('binary', type=argparse.FileType('rb'),
        help='Path to the original WSL bash.exe')
    parser.add_argument('path', type=str,
        help='New path to be applied to the binary')

    parser.add_argument('-o', '--output', type=str, default='launcher.exe',
        help='Where to output the newly created binary')

    return parser.parse_args()


def main(argv, argc):
    args = parse_args(argv)
    print("Opened '%s' for reading" % args.binary.name)

    content = bytearray(args.binary.read())

    offset = OFFSET if check_offset(content) else find_offset(content)
    if offset != -1:
        print('Found valid char sequence at %s' % hex(offset))
    else:
        print('ERROR: Unable to find valid char sequence. Cannot continue!')
        exit(1)

    if 2 * len(args.path) >= LENGTH:
        print('ERROR: value to be patched in is too long. must not exceed %d characters' % (LENGTH // 2))
        exit(1)

    print('Patching file and writing to \'%s\'... ' % args.output, end='')
    content[offset:offset+LENGTH] = stob(args.path)

    with open(args.output, 'wb') as f:
        f.write(content)
        print('wrote %d bytes' % f.tell())


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))
