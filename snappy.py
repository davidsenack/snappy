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

def get_pkg_info(pkg_line: str, index: int) -> str:
    tmp = pkg_line.split(" ")
    pkg_version = tmp[index]
    return pkg_version


def pkg_name_cleanup(pkg_line: str) -> str:
    pkg_name = pkg_line.split(",")[0]
    return pkg_name

pkg_list = get_packages()

for pkg in pkg_list[1:]:
    pkg_name = get_pkg_info()
