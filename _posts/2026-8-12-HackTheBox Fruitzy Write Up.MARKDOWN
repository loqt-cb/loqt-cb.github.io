---
title: Combining Windows Forensics and OSINT on VirusTotal with Fruitzy (HTB Sherlock)
date: 2026-8-12 05:00:01 +/-0000
categories: [Education, Write Ups]
tags: [hackthebox, osint, digital forensics, incident response, linux, malware analysis, bash]
author: cblake
description: A Write-up of the Fruitzy sherlock on HackTheBox
comments: false
image:
  path: /assets/img/fruitzy/logo.png
  alt: The default HackTheBox logo.

---



## Introduction
Fruitzy is a DFIR Sherlock on HackTheBox that starts off with Phishing Analysis and later dives into using Windows Artifacts to understand how a system was hijacked.

Here is the scenario:
```
CyberJunkie started out as a junior QA Analyst at his friend's startup.
He called the CEO of the startup because he believed he had mistakenly downloaded something malicious.
The CEO sought help from you, his friend in the cybersecurity field.
You sent him a guide on collecting evidence from the machine using KAPE.
Now you have been given the forensic image so you can analyze and help your friends, as they cannot afford to hire an MSSP.
```

## Analysis
We start off like most sherlocks by downloading the zip file that we will investigate.
* Fruitzy.zip
	* 2026-03-04T171958_forensicdata.zip - KAPE Triage
	* "Special Party Invigation from JANET CARNAHAN.eml" - Phishing Email

#### Phishing Email

This is a very standard phishing email that was tailored towards the victim outlined in the scenario. Some important artifacts within this email include the malicious URLs and the obvious suspicious address in use.

```
From: Business invitation <businessinvitation432@gmail.com>

Please find your exclusive invitation at the following link
<https://pomi.digital/premium?__cf_chl_tk=6SX3C1utT5mfbwmflZyMDU.WICiyPkGsBkaOTitVBss-1772039836-1.0.1.1-JvMwxVsDmAF0zIVuaF0XNh73a8usyjzPeFDOJpaT4j8>

We look forward to welcoming you at the event.

Regards
Janet


<div dir=3D"ltr">Please find your exclusive invitation at the following <a =
href=3D"https://pomi.digital/premium?__cf_chl_tk=3D6SX3C1utT5mfbwmflZyMDU.W=
ICiyPkGsBkaOTitVBss-1772039836-1.0.1.1-JvMwxVsDmAF0zIVuaF0XNh73a8usyjzPeFDO=
JpaT4j8">link</a><br><br>We look forward to welcoming you at the=C2=A0event=
.<br><br>Regards<br>Janet</div>
```


#### Triage
This triage is contained in a vhdx file, which is for Windows Hypervisor specifically, however I was able to change the format to something Autopsy could read by using FTKImager (AUR version)

Try using this command:
```bash
ftkimager  2026-03-04T171958_forensicdata.vhdx triage.dd
```

Once we have it converted, we can open it in Autopsy. From here we have the following artifacts open to us:
```
C:
	$Extend
		$RmMetadata
	$Recycle.Bin
		S-1-5-21-2794582496-788221845-218393293-1002
	ProgramData
		Microsoft
			search
			Windows
			Windows Defender
	Users
		abdul
		cyberjunkie
		Default
		Public
	Windows
		AppCompat
		inf
		prefetch
		ServiceProfiles
		System32
```



### Tasks

1. What is the Subject/topic of the Phishing email?
This is just the title of the .eml file we downloaded at the start.
`Special Party Invitation from JANET CARNAHAN`

2. What is the malicious URI that the malicious link redirected to?
For this question, instead of opening one of the malicious links I maintained security by viewing the browser history of the cyberjunkie user. You can do this by going to `C:\Users\cyberjunkie\AppData\Local\Microsoft\Edge\User Data\Default` and exporting `History`. Once the file is exported to your working directory, you can view the data in SQLlite or any preferred database viewing application. You can find our answer as the last link under the `urls` table.
`https://pomi.digital/premium/windows_download.php`


3. What is the name of the downloaded file?
You can find this under the Edge history as well, by viewing the downloads table. The one and only download is our answer.
`premium.exe`

4. When was the downloaded file executed by the victim according to Amcache?
We were provided a hint that we need to look at Amcache to find our answer. Amcache files are stored at `C:\Windows\AppCompat\Programs`, where we can export the main Amcache file and the two logs. Once they are exported, we can use the AmcacheParser by Eric Zimmerman.

Before we utilize these tools, we need to make sure that our file names are all related. When I export files out of Autopsy, some times it may add numbers as prefixes to the name, so I changed them like so:

```
725-Amcache.hve -> Amcache.hve
726-Amcache.hve.LOG1 -> Amcache.hve.LOG1
728-Amcache.hve.LOG2 -> Amcache.hve.LOG2
```

To utilize this tool, I ran the following command:
```bash
dotnet /opt/AmcacheParser/AmcacheParser.dll -f Amcache.hve --csv ./ --csvf Amcache.csv
```
Please bear in mind that I store these applications in /opt/ as a quick area I can refer to.

From here there are many .csv files we can look at, but since we are looking for a an execution time of an unassociated file, we will look under `Amcache_UnassociatedFileEntries.csv`. You can either use some sort of spreadsheet viewer, I find csvlens to be straightforward, so I found the answer by using the following filter
```
csvlens Amcache_UnassociatedFileEntries.csv --filter premium.exe
```
We find our answer to be `2026-03-04 16:44:33`

5. What is the SHA256 hash of the malicious executable downloaded from the phishing website?
The same exact csv entry has a SHA1 hash, `405481d3d5529445c546d4429b72c5827ebde840`, which we can use to search on [VirusTotal](https://www.virustotal.com/gui/file/af240a2c2a4b42e3a130f47ccaab9aa2e20a1a586bc959ee9efd7475055ea7e3/details) to find a correlated SHA256.
`af240a2c2a4b42e3a130f47ccaab9aa2e20a1a586bc959ee9efd7475055ea7e3`

6. The user executed the file, but no invitation appeared or was found. They then used Microsoft Defender to scan the file. When was this scan initiated?
We were provided another hint in this question, where we know to search for specifically Microsoft Defender events. We can pull the .evtx file for Microsoft Defender and search from there. This file can be found at `C:\Windows\System32\winvet\logs\Microsoft-Windows-Windows Defender%4Operational.evtx`. Go ahead and export it so we can parse for the necessary information.
I used the following command:
```bash
dotnet /opt/EvtxeCmd/EvtxECmd.dll -f WindowsDefender.evtx --csv ./ --csvf defender.csv
```
From here, using a browser search we can find out that we're looking for an Event ID of 1000 which means a scan was initiated. So, we can use the same filter command and csvlens to nail it down.
```bash
csvlens defender.csv --filter 1000
```
Which will find our answer to be:
`2026-03-04 16:48:00`

7. The malware installed a Remote Monitoring and Management (RMM) tool as a backdoor for potential remote access. What was the service name?
We can look at the same [VirusTotal][https://www.virustotal.com/gui/file/af240a2c2a4b42e3a130f47ccaab9aa2e20a1a586bc959ee9efd7475055ea7e3/details] page to find services that are used by the malware. Under the `Behavior` tab, we see CentraStage is written all over it, which is our answer:
`CentraStage`

8. The malicious backdoor installation time stomped the RMM executables. What was the modified timestamp set to these executables?
A lot of crucial file information such as modified timestamps can be found in the Master File Table, or $MFT. Just like the other artifacts, the first thing we're going to do is extract it from Autopsy. This can be found within `C:` specifically. Once extracted, I ran this command to convert it to .csv:
```bash
dotnet /opt/MFTECmd/MFTECmd.dll -f MFT --csv ./ --csvf mft.csv
```
From here like the other answers, we can use csvlens to find our answer. Since we are looking specifically for the executables used by the CentraStage service, we can look at VirusTotal again to find specific executables to look for. One in particular VirusTotal mentions is `CagService.exe`
```bash
csvlens mft.csv --filter CagService.exe
```
We find the CagService.exe specifically has a `LastModified0x10` value of `2026-02-09 07:56:40`

9. What is the name of the company whose product is the RMM tool?
This is found on VirusTotal as well, where we see rmm.datto.com as a contacted domain, making `Datto` as the company.

10. Pivoting back to the malicious link, when was the domain registered?
For domain related questions, https://lookup.icann.org/en/lookup is a good website to gather information, and it is what I used to find the answer. Inputting the pomi.digital domain, we find that `2026-02-20 01:06:05` is when it was registered

11. Utilizing threat intelligence sources, what is another name for the executable that was initially downloaded?
Also found on VirusTotal in the Details tab, under the Names section. another name for the executable is `5bxrx.exe`

## Conclusion
This sherlock was a straightforward challenge that really makes you utilize VirusTotal to gain a better understanding of how the used malware works. I recommend this for anyone looking to get better at Easy-ranked sherlocks, but not for someone that's new to these challenges.
