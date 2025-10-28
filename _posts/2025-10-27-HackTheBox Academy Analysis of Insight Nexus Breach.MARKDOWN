---
title: The Analysis of Insight Nexus Breach (HackTheBox Academy)
date: 2025-10-27 7:55:20 +/-0000
categories: [Education, Write Ups]
tags: [hackthebox, soc, incident response]
author: cblake
description: A short write up of the tasks presented in the Analysis of Insight Nexus Breach section on HackTheBox Academy's Incident Handling Process module.
comments: false
image:
  path: /assets/img/htbaoinb/logo.png
  alt: The logo for this HackTheBox module.

---

<h2>Preface</h2>
The Academy of HackTheBox has offered a lot of unique challenges that provide great learning for anyone that is willing to undergo them. Today I was presented with a challenge that required me to conduct Incident Response procedures and investigation in a simulation.

We are presented with the information about 'Insight Nexus' being that they are "a mid-sized market research and data analytics firm headquartered in Singapore." As well as that this company focuses on providing competitive intelligence and consumer insights. This company had fallen victim to a brute force attack on an unsecured internet-facing application. After gaining access, the attackers performed reconnaissance, had created new Active Directory accounts, and escalated their privileges. This incident was discovered when an analyst from the SOC team had found an alert on TheHive regarding suspicious file creation.

<h2>Questions</h2>

<strong>Download the Wazuh exported logs file (i.e, wazuh_export.zip), and identify all events that indicate potential credential compromise. Check the event ID 4688 and verify the full path of the parent process name that exexuted a credential dumping tool. Answer format is C:\\Pr........</strong>

When first posed with this request, we are provided already with a hint telling us to check Windows Event ID 4688, which is the Security Event ID for process creation. To view the logs in the .json file provided, the software I'll be using is Kate. We're also told that the parent process would more than likely come from one located in Program Files. Knowing this we can narrow our search.

After searching to find a suspicious executable that could be a credential dump, we find a log with mimikatz.exe, as well as an alert from Wazuh saying "Possible credential dumping detected." Mimikatz is a well known credential dumping software, and any time it is found in an incident, it is certain to have credential dumping involved.

![img-description](assets/img/htbaoinb/1.png)

We now have found this parent process to be `C:\\Program Files\\Mozilla Firefox\\firefox.exe`

<strong>Identify events that show persistence mechanisms. Type the value of imagePath for a persistence mechanism that took place on the host DB01.</strong>

To start we know that we're looking for persistence mechanisms, and it also tells us we're looking for a log with an imagePath value, implying it is an executable being used. Just by searching for logs that are grouped with persistence we see a new service installed known as PSEXESVC.exe, which is a Microsoft executable designed for remote process execution, showing clear signs of a persistence tactic.
![img-description](assets/img/htbaoinb/3.png)

We know that the imagePath for this is: `C:\\Windows\PSEXESVC.exe`

<strong>Identify exfiltration activity - file(s) uploaded or outbound traffic. What is the external IP address to which the file diagnostics_data.zip was uploaded?</strong>

We know that we're searching for a log entry that contains information regarding diagnostics_data.zip, so doing a quick find for that results in us seeing this:

![img-description](assets/img/htbaoinb/4.png)
Here we can see the post request being sent out to an external IP address, which is `93.184.216.34`.

<strong>Which user tried to connect to the file share \\fs01\projects?</strong>

To search for this we can look up any references to 'fs01\projects' and after doing so we see this:

![img-description](assets/img/htbaoinb/5.png)

Where the user `svc_admin` attempted to connect to this this file share via SMB.

<h2> Conclusion </h2>

This was a short and sweet Incident Response exercise, that helped us learn how to work with Wazuh logs. Wazuh logs are very simple and easy to work with, especially if you are searching them through a SIEM such as TheHive.
