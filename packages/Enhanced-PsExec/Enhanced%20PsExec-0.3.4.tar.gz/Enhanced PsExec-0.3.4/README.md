#### !!!!!!!!!! Use "help(Epsexec)" This will show you the available methods. (This usage form will contain it, but it is yet to be completed.) !!!!!!!!!!

### About
Epsexec (Enhanced psexec) uses Microsoft's Sysinternals PsExec utility uses SMB to execute programs on remote systems.
PsExec is a light-weight telnet replacement.    

### Installation
Run the following to install:   
```
pip install Epsexec   
```

### Requirements
1) You MUST have a 64-bit version of python.   
2) You MUST have psexec installed and in your system32 folder.   

### Import
To import the package, use 'import Epsexec'.   

## Usage
1) Create a psPc class instance.   
```python
pc1 = psPc("IPv4","username","password")   
```
General settings:   

**sleepBefore** - This waits before starting the operation in millisecond.         (defualt 100)   
**runAsAdmin**  - If true, it will run the operation in administrative privileges. (default True)   

### firewallChange
This is probably the most important method. why?   
Well, because firewall makes the psexec process extremely slow (It takes about 12 seconds instead of 1).   
So, it becomes very frustrating.   

### downloadNirCmd
NirCMD is A windows command-line utility that allows you to do useful tasks without displaying any user interface.   
Unfortunately, NirCMD is NOT installed by default on windows systems.   
Thats why this method exists. all this method do, is download NirCMD on the remote PC using powershell.   
Nircmd is required for the following methods:   
1. beep   
2. sendScreenshot   
3. setVolume   
4. textToSpeech   

### beep
The beep method takes frequency(hz) and duration(millisecond) parameters.   
Then it plays the sound at the given frequency and duration.   

### sendScreenshot
The sendScreenshot takes email address and sleepBefore.    
It uses NirCMD to take A screenshot, save it to C:\Epsexecscreenshot.png   
Then, it uses powershell SMTPClient.send() to send an email to the given Email Address   

### OpenURL 
The openURL method can potentially take a lot of arguments, but there is one specifically that I want to explain: **fromFile=**"filename.txt".   
This will take a text file, that is orignized by the following schematic:   

```python
urls:   
    shortname URL   
endurl   
```
**Example:**   
```python
urls:   
		google https://www.google.com   
		youtube http://www.youtube.com   
endurl   
```
And it will get values from the file, then output the shortcuts to the user.   
The user can choose which one to use.   
This is useful in a situation where you have for example A YouTube link.   
YouTube links can easily get hard to manage, due to their meaningless URLs   

Available class methods:   
```python
psPc(ip, username, password)   
     
       beep(frequency, durationMs, sleepBefore=100)   
     
       closeChrome(runAsAdmin=True, sleepBefore=100)   
     
       closeProcess(procNameOrID, sleepBefore=100)   
     
       downloadNirCMD()   
     
       firewallChange(state='off', sleepBefore=100)   
     
       getShell(shell='cmd.exe', runAsAdmin=True)   
     
       openURL(URL='*://*/*', fromFile='@fileName.txt', tabs=1, newWindow=False, delayBeforeOpening=100, delayBetweenTabs=100, incognito=False, invisible=False)   
     
       sendScreenshot(emailRecipientAddr, sleepBefore=100)   
     
       setVolume(precent, sleepBefore=100)   
     
       startRemoteDesktop()   
      
       textToSpeech(text, MaleVoice=True, sleepBefore=100)   

```

### Credits
Epsexec was created by Ori Shamir.   