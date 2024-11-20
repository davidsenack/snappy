#!/usr/bin/python3

import subprocess

def get_packages():
    get_packages_cmd = "apt list --installed"
    tmp = subprocess.run(get_packages_cmd, shell=True, capture_output=True, text=True)
    pkg_list = tmp.stdout.strip()
    new_pkg_list = pkg_list.split('\n')

    pkg_arr = []
    for pkg in new_pkg_list:
        pkg_arr.append(pkg)
    
    return pkg_arr

def get_pkg_version(output_line):
    output = string.split(output_line, " ")
    return output


pkg_list = get_packages()

for pkg in pkg_list:
    print(pkg)
