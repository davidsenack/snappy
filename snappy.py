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

def get_pkg_version(output_line: str):
    output = output_line.split(" ")
    pkg_version = output[1]
    return pkg_version


def get_pkg_name():
    return

pkg_list = get_packages()

for pkg in pkg_list[1:]:
    split_pkg = get_pkg_version(pkg)
    print(pkg)
