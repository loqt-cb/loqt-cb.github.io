---
title: Write Up of PhishNet (HackTheBox Sherlock)
date: 2025-11-3 7:53:20 +/-0000
categories: [Education, Write Ups]
tags: [hackthebox, soc, incident response, phishing analysis]
author: cblake
description: A short write up of the tasks presented in the PhishNet sherlock on HackTheBox.
comments: false
image:
  path: /assets/img/phishnet/logo.png
  alt: The logo for this HackTheBox challenge.

---


<h2> Introduction </h2>
PhishNet is a 'Very Easy' difficulty sherlock on HackTheBox, focused with a category of SOC. The scenario goes as follows: an accounting team receives a malicious email that contains malware, and it is our duty to analyze the email to understand the attacker's motives.

Inside of the file `PhishNet.zip` we see one singular file, which is `email.eml`


**Tools we will need: **
* Some sort of .eml viewer (Thunderbird was used)
* Sort text editor to see hidden contents of the .eml file (Kate was used)

Upon opening the file within Thunderbird we get a good view of what the phishing email looks like:
![img-description](/assets/img/phishnet/1.png)

<h2> Procedure </h2>
1. What is the originating IP address of the sender?
	1. To find this, we know that source IP addresses are saved within `.eml` files at the very top within the section of the important system information.
	2. Upon viewing the `.eml` file within a text editor, we find the IP address at the very top.
	3. ![img-description](/assets/img/phishnet/2.png)
	4. `45.67.89.10`
2. Which mail server relayed this email before reaching the victim?
	1. Mail server history of an email can be found within the section that contains blocks tagged with "Received:"
	2. They are sorted in chronological order of most to least recent, so we know that the top entry contains the email server that relayed this email before going to the victim.
	3. Since the answer asks us to identify the server via IPv4 address, we'll search for the IPv4 address.
	4. ![img-description](/assets/img/phishnet/3.png)
	5. This leaves us with `203.0.113.25`
3. What is the sender's email address?
	1. This we can easily find by examining the `.eml` file in either Thunderbird or a text editor in the section that displays the sender's email address.
	2. ![img-description](/assets/img/phishnet/4.png)
	3. ![img-description](/assets/img/phishnet/5.png)
	4. So we know that the email address is `finance@business-finance.com`
4. What is the 'Reply-To' email address specified in the email?
	1. This one can also be found directly under the sender's email in both a text editor and on Thunderbird.
	2. ![img-description](/assets/img/phishnet/6.png)
	3. ![img-description](/assets/img/phishnet/7.png)
	4. Leaving us with `support@business-finance.com` as our answer.
5. What is the SPF (Sender Policy Framework) result for this email?
	1. SPF information can be found within `.eml` files under the section of "Authentication Results: "
	2. Searching here, we can see that the SPF authentication results in a pass
	3. ![img-description](/assets/img/phishnet/8.png)
	4. So, we enter in `pass` as our answer.
6. What is the domain used in the phishing URL inside the email?
	1. We can find this in two methods:
		1. Be extremely careful, but copy the download link to your clipboard and paste it in a notepad or text editor, there we can see the domain section of the malicious URL.
		2. Another method is to examine the links that are referenced in the `.eml` file by searching up HTML's hyperlink reference `<href>`
			1. ![img-description](/assets/img/phishnet/9.png)
	2. Either way, we know that the domain is `secure.business-finance.com`
7. What is the fake company name used in the email?
	1. We can investigate the text in the email in general areas where a company's name would be listed. In our case, we find the fake company name at the footer of the email.
	2. ![img-description](/assets/img/phishnet/10.png)
	3. `Business Finance Ltd.` is our fake company name.
8. What is the name of the attachment included in the email?
	1. Attached files in emails can be found at the bottom of the `.eml` file below the HTML code.
	2. Searching there, we find our file.
	3. ![img-description](/assets/img/phishnet/11.png)
	4. The name of the malicious zip is `Invoice_2025_Payment.zip`
9. What is the SHA-256 hash of the attachment?
	1. We see the base64 payload of the file at the bottom below where it is listed.
	2. ![img-description](/assets/img/phishnet/12.png)
	3. There's two ways we can get the SHA256 from this base64 payload.
		1. If you are on Linux simply echo the payload into a base64 decode command, and then input the results of that into the `sha256sum` command.
			1. `echo UEsDBBQAAAAIABh/WloXPY4qcxITALvMGQAYAAAAaW52b2ljZV9kb2N1bWVudC5wZGYuYmF0zL3ZzuzIsR18LQN+h62DPujWX0e7 | base64 -d | sha256sum`
		2. If you are not on Linux, you can use CyberChef by copying the base64 payload, decrypting it by using 'From Base64' and then putting it to SHA256 by using 'SHA2' and setting the size to 256.
			1. ![img-description](/assets/img/phishnet/13.png)
	4. Answer: `8379c41239e9af845b2ab6c27a7509ae8804d7d73e455c800a551b22ba25bb4a`
10. What is the filename of the malicious file contained within the ZIP attachment?
	1. From previously decoding the base64 payload we can notice that inside of the zip there is a file named `invoice_document.pdf.bat`
	2. ![img-description](/assets/img/phishnet/14.png)
	3. So, our answer is `invoice_document.pdf.bat`
11. What MITRE ATT&CK techniques are associated with this attack?
	1. To isolate the specific technique in place, we can trace-back two things that we know about this attack:
		1. It is a phish posing as another organization
		2. Contains a zip file with a batch script inside
	2. With these two pieces of knowledge we can specify it down to it being a Phishing technique, with a sub-technique of using an attachment
	3. Looking on the MITRE ATT&CK Framework, we can see there is a listing for something that matches what we are searching for.
	4. ![img-description](/assets/img/phishnet/15.png)
	5. This gives us the attack ID of `T1566.001`

<h2> Conclusion </h2>
This Sherlock on HackTheBox gives a great introduction to Phishing analysis. I'd strongly recommend it for anyone wanting a small challenge, while also wanting to gain more knowledge of how to investigate Phishing attacks. Over the course of doing this challenge we learned how to analyze the contents of a `.eml` file, how to gain more knowledge of attached files in a `.eml` and finally how we can correlate this to the MITRE ATT&CK Framework.
