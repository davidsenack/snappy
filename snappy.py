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

def get_pkg_name(pkg_line: str) -> str:
    tmp = pkg_line.split("/")
    pkg_name_dirty = tmp[0]
    pkg_name_clean = pkg_name_dirty.split(",")[0]
    return pkg_name_clean


def get_pkg_version(pkg_line: str) -> str:
    tmp = pkg_line.split(" ")
    pkg_version = tmp[1]
    return pkg_version

def install_pkg(pkg_name, pkg_version):
    cmd = "sudo apt install {}={}".format(pkg_name, pkg_version)
    subprocess.run(cmd, shell=True)
    return

def create_snapshot():
    return

def restore_from_snapshot():
    return

pkg_list = get_packages()

for pkg in pkg_list[1:5]:
    pkg_name = get_pkg_name(pkg)
    pkg_version = get_pkg_version(pkg)
    #print(pkg_name)
    #print(pkg_version)
    install_pkg(pkg_name, pkg_version)
    # comment
