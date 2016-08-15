
import os
import sys
import re
from pydatagen import *

__version = '20160815-dev'

mycode = sys.argv[1] if len(sys.argv) > 1 else ''
std = sys.argv[2] if len(sys.argv) > 2 else ''
gen = sys.argv[3] if len(sys.argv) > 3 else ''
count = int(sys.argv[4]) if len(sys.argv) > 4 else 1
gpp_invoke = '"C:\\Program Files (x86)\\Dev-Cpp\\MinGW64\\bin\\g++" %s -o %s'

def main():
    # Pre-run compilation
    printf('$ Compiling...\r')
    mycode_e = re.sub('$', '.exe', mycode)
    std_e = re.sub('$', '.exe', std)
    if not os.path.exists(mycode_e):
        os.system(gpp_invoke % (mycode, mycode_e))
    if not os.path.exists(std_e):
        os.system(gpp_invoke % (std, std_e))
    printf('$ Compiling... OK\n')
    # Execution and judging
    same_count = 0
    err_count = 0
    for i in range(0, count):
        printf('$ Checking round #%s: Generating data...%s\r' % (str(i + 1), ' ' * 16))
        if ('.py' in gen):
            os.system('python %s 1> __input__.txt 2> __error__.txt' % gen)
        else:
            os.system('cp %s __input__.txt' % gen)
        # Detecting potential problems...
        try:
            fe = open('__error__.txt', 'r', encoding='utf-8')
            stre = fe.read()
            fe.close()
        except Exception:
            stre = ''
            pass
        if len(stre) > 4:
            printf('$ Data generation error in round #%s: %s\n' % (str(i + 1), ' ' * 16))
            err_count = err_count + 1
            print(stre)
            continue
        printf('$ Checking round #%s: Running "%s"...%s\r' % (str(i + 1), mycode, ' ' * 16))
        os.system('cat __input__.txt | %s > __out1__.txt' % mycode_e)
        printf('$ Checking round #%s: Running "%s"...%s\r' % (str(i + 1), std, ' ' * 16))
        os.system('cat __input__.txt | %s > __out2__.txt' % std_e)
        printf('$ Checking round #%s: Judging...%s\r' % (str(i + 1), ' ' * 16))
        f1 = open('__out1__.txt', 'r', encoding='utf-8')
        f2 = open('__out2__.txt', 'r', encoding='utf-8')
        str1_orig = f1.read()
        str2_orig = f2.read()
        str1 = re.sub('[ \t\r\n]', '', str1_orig)
        str2 = re.sub('[ \t\r\n]', '', str2_orig)
        f1.close()
        f2.close()
        same = str1 == str2
        if same:
            printf('$ Checking round #%s: OK%s\r' % (str(i + 1), ' ' * 24))
            same_count += 1
        else:
            if '.py' in gen:
                os.system('mv -f __input__.txt input-%d.txt' % int(i + 1))
            printf('$ Checking round #%s: ERROR (Backtrace dumped)%s\r' % (str(i + 1), ' ' * 24))
            if '.py' not in gen:
                printf('\n')
                f3 = open('__input__.txt', 'r', encoding='utf-8')
                str3_orig = f3.read()
                f3.close()
                printf('============ STANDARD OUTPUT ============+++================ OUTPUT ================\n')
                arr1 = str2_orig.split('\n')
                arr2 = str1_orig.split('\n')
                for i in range(0, max(len(arr1), len(arr2))):
                    p = arr1[i] if len(arr1) > i else ''
                    q = arr2[i] if len(arr2) > i else ''
                    printf('%s%s  %s %s\n' % (p[:40], ' ' * (40 - len(p)), '|' if p == q else 'X', q[:40]))
            pass
        printf('\n')
    os.system('rm -f __error__.txt __input__.txt __out1__.txt __out2__.txt 2>nul')
    printf('$ Finished %d rounds, of which %d are correct\n' % (count - err_count, same_count))

if gen == '':
    printf('pypai: Unrecognized supplied null option\n')
    printf('Try `pypai --help` for more information.\n')
    exit(1)
elif gen == '--help':
    printf(
"""Usage: pypai [OPTIONS] CODE STANDARD_CODE INPUT_SOURCE [COUNT]
Validate CODE with STANDARD_CODE through data generated from INPUT_SOURCE.

      --help     display this help and exit
      --version  output version information and exit

With no COUNT or invalid input, will be defaulted to 1 pass.
Programs will be automatically compiled with g++, as provided in the
    source code of this program.
INPUT_SOURCE should be run in Python if specified a *.py file, and automatically
    read into program if is text file.

Examples:
  pypai "mycode.cpp" "std.cpp" "gen.py" 10

Report bugs to <https://github.com/ht35268/pypai/issues>.
""")
    exit(0)
elif gen == '--version':
    printf(
"""pypai  %s

This is free software served in the public domain. You have the rights
to distribute or modify, reference any part of it with or without the
permissions of the author.

Written by Geoffrey, Tang.
""" % __version)
    exit(0)

main()
