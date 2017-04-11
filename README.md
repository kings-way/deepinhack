

##dde_daemon_poc.py
#### Intro
* CVE-2016-7622

#### Date & Version
* Date: 20170401
* Tested on:  Deepin15.3,  ArchLinux, Fedora25(copr), Manjaro(with DDE)

#### Vulnerability Description
* dde-daemon, the daemon process of DDE (Deepin Desktop Environment), runs with root privileges and hardly does anything to
identify the user who calls the function through D-Bus. 
* Anybody can change the grub config, even to append some arguments to make a backdoor or privilege escalation, by calling DoWriteGrubSettings() provided by dde-daemon


## lastore_daemon_poc.py
#### Intro
*  (No CVE ID)
* Lastore-daemon in Deepin 15 results in privilege escalation.
* But it has been Invalid since updates in 20160225.

#### Date & Version
* Date: 20160208
* Tested on:  Deepin15 &15.1 

#### Vulnerability Description
* In Deepin Linux 15, they designed a daemon (called lastore-daemon) based on dbus and apt to support deepin-appstore.
* Lastore-daemon runs with root privilege to run apt-get commands and listens  to dbus message from every user.
* So, we can send the package name along with some options to lastore-daemon to install or remove any package, even to destroy the host system.
* Apart from that, if we prepare a malicious package and try to cheat lastore-daemon into installing it, then anyone can have root privilege.

