# privilege escalation POC for deepin 15

### Vulnerability Description:
* In Deepin Linux 15.1, they designed a daemon (called lastore-daemon) based on dbus and apt to support deepin-appstore.
* Lastore-daemon runs with root privilege to run apt-get commands and listens  to dbus message from every user.
* So, we can send the package name along with some options to lastore-daemon to install or remove any package, even to destroy the host system.
* Apart from that, if we prepare a malicious package and try to cheat lastore-daemon into installing it, then anyone can have root privilege.

		
		Exploit Title: Lastore-daemon in Deepin 15 results in privilege escalation
 		Date: 20160208
 		Exploit Author: King's Way <root#kings-way.info>
	 	Vendor Homepage: http://www.deepin.org
		Software Link: http://cdimage.linuxdeepin.com/releases/15.1/deepin-15.1-amd64.iso
		Version: Deepin 15 & 15.01
 		Tested on: Deepin 15 & 15.01
 		CVE : null