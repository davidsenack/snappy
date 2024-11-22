#!/usr/bin/python3

import subprocess
import datetime
import os 

def get_current_pkgs():
    get_packages_cmd = "apt list --installed"
    tmp = subprocess.run(get_packages_cmd, shell=True, capture_output=True, text=True)
    pkg_list = tmp.stdout.strip()
    new_pkg_list = pkg_list.split('\n')

    pkg_arr = []

    for pkg in new_pkg_list[1:]:
        pkg_name = get_pkg_name(pkg)
        pkg_version = get_pkg_version(pkg)
        pkg_arr.append("{} {}".format(pkg_name, pkg_version))

    return pkg_arr

def get_snapshot_pkgs(snapshot_file_path):
    pkg_arr = []

    with open(snapshot_file_path, "r") as file:
        for line in file:
            line = line.strip()
            pkg_name = line.split(" ")[0]
            pkg_version = line.split(" ")[1]
            pkg_arr.append("{} {}".format(pkg_name, pkg_version))
    
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

def delete_pkg(pkg_name):
    cmd = "sudo apt remove {}".format(pkg_name)
    subprocess.run(cmd, shell=True)
    return

def compare_pkgs(current_pkg_arr, snapshot_pkg_arr):
    pkgs_to_remove = []
    pkgs_to_add = []
    
    for pkg in current_pkg_arr:
        if pkg not in snapshot_pkg_arr:
            pkgs_to_remove.append(pkg)

    for pkg in snapshot_pkg_arr:
        if pkg not in current_pkg_arr:
            pkgs_to_add.append(pkg)

    return (pkgs_to_add, pkgs_to_remove)


def create_snapshot():
    # Check for .snappy directory
    directory = os.path.expanduser("~/.snappy")
    os.makedirs(directory, exist_ok=True)

    # Set filename based on timestamp
    current_time = datetime.datetime.now()
    file_name = current_time.strftime("%Y-%m-%d_%H-%M-%s") + ".pkg.snapshot"
    
    # Set full file path
    file_path = os.path.join(directory, file_name)

    # Get current package data
    pkg_list = get_current_pkgs()

    # Write current pacakge data to output file
    with open(file_path, "w") as file:
        for pkg in pkg_list:
            pkg_name = get_pkg_name(pkg)
            pkg_version = get_pkg_version(pkg)
            file.write("{} {}\n".format(pkg_name, pkg_version))

    print(f"Current package snapshot has been written to '{file_path}'")
    return

def restore_from_snapshot(snapshot_file_path):
    #::TODO fix the multiple .snappy dir refs to different functions
    current_pkgs = get_current_pkgs()
    snapshot_pkgs = get_snapshot_pkgs(snapshot_file_path)
    pkgs_to_install, pkgs_to_remove = compare_pkgs(current_pkgs, snapshot_pkgs)
    
    for pkg in pkgs_to_remove:
        pkg_name = pkg.split(" ")[0]
    #   pkg_version = line.split(" ")[1]
        rcmd = "sudo apt remove -y {}".format(pkg_name)
        subprocess.run(rcmd, shell=True)
        print("Remove: " + pkg)

    for pkg in pkgs_to_install:
       pkg_name = pkg.split(" ")[0]
       pkg_version = pkg.split(" ")[1]
       icmd = "sudo apt install -y --allow-downgrades {}={}".format(pkg_name, pkg_version)
       subprocess.run(icmd, shell=True)
       print("Install: " + pkg)
    
    
    for pkg in pkgs_to_remove:
        print("Package " + pkg + " Removed")

    print("Restore Packages from Snapshot Complete!")
    return

def main():

    #create_snapshot()
    snapshot_filename = "2024-11-22_12-24-1732296292.pkg.snapshot"
    snapshot_path = "/home/david/.snappy/"    

    restore_from_snapshot(snapshot_path + snapshot_filename)

if __name__=="__main__":
    main()

# We need to write a comparison function for the restore function to use. 
# It should compare the current installed packages and versions to the snapshot
# we're restoring from and create a list of packages that either aren't installed
#  or are install with the wrong version. This should significantly imporve the speed
#  of the restore process.
#
#
#  We should also include output after resotre that shows the changes made to
#  the system like so: 
#
#   nvim 8.1.3 -> nvim 8.0.4
#
#
'''
for pkg in snapshot:
    if pkg not in current_pkgs:
        install package

for pkg in current_pkgs:
    if pkg not in snapshot:
        remove pkg 
'''
