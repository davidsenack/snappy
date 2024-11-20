#!/usr/bin/python3

import subprocess

def get_packages():
    get_packages_cmd = "apt list --installed"
    tmp = subprocess.run(get_packages_cmd, shell=True, capture_output=True, text=True)
    package_list = tmp.stdout.strip()
    return package_list

print(get_packages())
