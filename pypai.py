
import os
import sys
import re
from pydatagen import *

gen = sys.argv[1]
mycode = sys.argv[2]
std = sys.argv[3]
count = int(sys.argv[4])
gpp_invoke = '"C:\\Program Files (x86)\\Dev-Cpp\\MinGW64\\bin\\g++" %s -o %s'

# Pre-run compilation

printf('$ Compiling...\r')
mycode_e = re.sub('\\.cpp$', '.exe', mycode)
std_e = re.sub('\\.cpp$', '.exe', std)
if not os.path.exists(mycode_e):
    os.system(gpp_invoke % (mycode, mycode_e))
if not os.path.exists(std_e):
    os.system(gpp_invoke % (std, std_e))
printf('$ Compiling... OK\n')

# Execution and judging

same_count = 0

for i in range(0, count):
    printf('$ Checking round #%s: Generating data...%s\r' % (str(i + 1), ' ' * 16))
    os.system('python %s > __input__.txt' % gen)
    printf('$ Checking round #%s: Running "%s"...%s\r' % (str(i + 1), mycode, ' ' * 16))
    os.system('cat __input__.txt | %s > __out1__.txt' % mycode_e)
    printf('$ Checking round #%s: Running "%s"...%s\r' % (str(i + 1), std, ' ' * 16))
    os.system('cat __input__.txt | %s > __out2__.txt' % std_e)
    printf('$ Checking round #%s: Judging...%s\r' % (str(i + 1), ' ' * 16))
    f1 = open('__out1__.txt', 'r', encoding='utf-8')
    f2 = open('__out2__.txt', 'r', encoding='utf-8')
    str1 = f1.read().replace(r'[ \t\r\n]', '')
    str2 = f2.read().replace(r'[ \t\r\n]', '')
    f1.close()
    f2.close()
    same = str1 == str2
    if same:
        printf('$ Checking round #%s: OK%s\r' % (str(i + 1), ' ' * 16))
        same_count += 1
    else:
        printf('$ Checking round #%s: CORRECT%s\r' % (str(i + 1), ' ' * 16))
    printf('\n')

printf('$ Cleaning up...\r')
os.system('rm -f __input__.txt __out1__.txt __out2__.txt')
printf('$ Finished %d rounds, of which %d are correct\n' % (count, same_count))
