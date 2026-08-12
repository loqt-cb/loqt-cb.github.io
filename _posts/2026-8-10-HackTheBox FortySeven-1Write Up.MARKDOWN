---
title: Basic APT Threat Intelligence with FortySeven-1 (HTB Sherlock)
date: 2026-8-10 05:00:01 +/-0000
categories: [Education, Write Ups]
tags: [hackthebox, osint, threat intelligence]
author: cblake
description: A Write-up of the FortySeven-1 sherlock on HackTheBox
comments: false
image:
  path: /assets/img/fortyseven1/logo.png
  alt: The default HackTheBox logo.

---

### Scenario

FortySeven is a Very Easy ranked Threat Intelligence Sherlock on Hack the Box. It consists of utilizing OSINT and research to solve it's challenges, just like other Threat Intelligence challenges on HTB. The scenario is as follows:

```
An APT group is using Hajj-themed phishing lures to target and steal WhatsApp data from government and diplomatic officials.
Our team has gathered fragmented intelligence from public cybersecurity vendor reports, blog posts, and internal security alerts.
Your task is to build a comprehensive profile of the threat actor responsible. You must connect the dots between different reports to answer questions about their identity, tools, and motives.
```

Within the scenario, we are linked to three articles that we will use as evidence throughout our investigation:

```
Evidence - 1 - `https://securelist.com/mysterious-elephant-apt-ttps-and-tools/117596/`
Evidence - 2 - `https://medium.com/@knownsec404team/apt-k-47-mysterious-elephant-a-new-apt-organization-in-south-asia-5c66f954477`
Evidence - 3 - `https://medium.com/@knownsec404team/unveiling-the-past-and-present-of-apt-k-47-weapon-asyncshell-5a98f75c2d68`
```
### Tasks

#### Task 1

What is the primary name of the APT group described in the SecureList report?

For this question we can refer to Evidence 1, where we see the primary name provided for the APT group to be `Mysterious Elephant`.
![img-description](assets/img/fortyseven1/1.png)

#### Task 2

According to the Knownsec 404 team's analysis(Evidence -3), since which year has this group's attack activity been dated back to?

When referring to evidence 2, and reading through the information on the article, we see it quotes:
```
"At the same time, after backtracking analysis, we found that the earliest attack activities of the organization should start around March 2022. This article will publish the details of the APt group's attacks and the relevant IOCS."
```

Making our answer `2022`.

![img-description](assets/img/fortyseven1/3.png)

#### Task 3

The group uses a custom backdoor that communicates via Office Remote Procedure Call (ORPCBackdoor). According to the Knownsec 404 team's analysis(Evidence -2), what is the name of the first malicious exported entry function?

The same article found in evidence 2 also says directly:

```
There are two malicious entries of ORPCBackdoor, the first is GetFileVersionInfoBy-HandleEx(void) export function, second place ios DllEntryPoint
```

We do see that the relevant export function name is listed above in the following screenshot:

![img-description](assets/img/fortyseven1/4.png)

#### Task 4

The previously mentioned backdoor checks for a file before creating persistence. What is the name of the file?

Further in the article, we see that it checks for a file named `ts.dat` where it mentions that the ORPCBackdoor checks for a `ts.dat` file.


![img-description](assets/img/fortyseven1/5.png)

#### Task 5

The use of the backdoor links the APT to another well-known South Asian APT group. What is the name of this other group?

The article makes a comparison with an APT group named BITTER at the following quote:
```
The ORPCBackdoor attack chain overlaps with the tactics used by the Indian direction, BITTER’s tactics and code structure are particularly similar.
```
![img-description](assets/img/fortyseven1/6.png)


#### Task 6

The APT group we are currently investigating has consistently used and updated another backdoor since 2023, with its C2 communication evolving from TCP to HTTPS. What is the name of this tool?

In evidence 3, there is a quote mentioning that Asyncshell-v2 makes a change from TCP to HTTPS. There is also a table within the article that tracks a version history of Asyncshell.

![img-description](assets/img/fortyseven1/8.png)

#### Task 7

To evade sandbox analysis, the MemLoader HidenDesk tool checks the number of active processes before running. What is the minimum number of processes required for it to proceed?

For this question we can refer back to evidence 1, the Securelist article. There is a section in the article that goes over how MemLoader HidenDesk functions:

![img-description](assets/img/fortyseven1/9.png)

In this section we can directly see that it terminates itself if fewer than `40` processes are running.

#### Task 8

The MemLoader HidenDesk tool creates a covert environment for its activities by creating and switching to a specific environment. What is the name of this hidden desktop?

In the same section that we mentioned in the previous task, in the third section, it mentions that a hidden desktop is created, named `MalwareTech_Hidden`.

![img-description](assets/img/fortyseven1/10.png)

#### Task 9

The MemLoader HidenDesk tool achieves persistence by placing a shortcut in the autostart folder to ensure it runs after a system reboot. What is the MITRE ATT&CK ID for the 'Registry Run Keys / Startup Folder' technique?

For this question we can refer to MITRE's offical ATT&CK page, and find the specific ID for "Registry Run Keys / Startup Folder". In which we find `T1547.001` to be the result.

#### Task 10

The actor uses several custom exfiltration tools targeting WhatsApp. What is the name of the tool that recursively searches specific directories, including the “Desktop” and “Downloads” folders?

In the Securelist article, we see it mentions multiple exfiltration tools just like the task mentions. There is a specific one that targets the Desktop and Downloads folders just like the task mentions as well, and this specific tool is the `Stom Exfiltrator`.

![img-description](assets/img/fortyseven1/11.png)



#### Task 11

Kaspersky's analysis highlights the actor's heavy use of scripts for execution and deploying payloads. What is the MITRE ATT&CK ID for the 'PowerShell' technique?

A browser search on the MITRE ATT&CK ID site would bring up `T1059.001`.


#### Task 12

In their early attack chains, Mysterious Elephant used a downloader that was previously associated with the Origami Elephant group. What was the name of this downloader?

The Securelist article explains more specific attributes of Mysterious Elephant, where they directly mention a a downloader named "Vtyrei"

![img-description](assets/img/fortyseven1/12.png)



#### Task 13

In a January 2024 campaign delivering an Asyncshell payload, which CVE was exploited in the malicious archive file? Be careful to use a hyphen `-` and not an emdash `—` in the flag.

Going back to the knownsec404 article that is used for Evidence 3, we see it mentions that the Asyncshell payload exploits the `CVE-2023-38831` vulnerability.
![img-description](assets/img/fortyseven1/13.png)


#### Task 14

What is the MD5 hash of the ChromeStealer Exfiltrator sample named WhatsAppOB.exe?

The MD5 Hash of the ChromeStealer Exfiltrator could be found on the Securelist article towards the bottom, and easily located if you just search for the ChromeStealer Exfiltrator.
`9e50adb6107067ff0bab73307f5499b6`

#### Task 15

The intelligence describes multiple custom tools designed to upload stolen data to the actor's servers. According to the MITRE ATT&CK framework, what is the ID for the 'Exfiltration Over C2 Channel' technique?

A quick browser search for the `Exfiltrator Over C2 Channel` technique will result in `T1041`!

### Conclusion

This was a very simple, and straightforward threat intelligence sherlock challenge. I'd certainly recommend it for anyone that is looking for a starting point in sherlocks, aside from Brutus, which is the most widely known and completed sherlock challenge.



