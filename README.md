# rdp-com
Exfiltrate data from a remote session where the only way to get data out is via the rdp screen.

## Introduction 
This tool allows to copy data from a remote system that has no internet access.
Even if DNS requests are blocked (and the only way to communicate with the system is via the rdp screen), this tool can be used.
This tool communicates with the host computer by displaying characters
in different colors on the powershell console.
The script grabs the screen content, detects the colors and converts them back into binary data.

The scripts have very few dependencies.
On the remote system only a working powershell console is required.
No fancy packages have to be installed.

However, the bit rate is not that good.
A 5kB text file is transmitted in 45 seconds which results in about 90 Bytes per seconds.

## Prerequisites
To met the tool's dependencies on the host computer, the following command can be issued:
```
pip install --user -r requirements.txt
```
The sender script (`rdp-com.ps1`) needs no additional software and can be run everywhere where a powershell console is accessible.

## Usage
To copy data from the remote to the host computer, first the script `rdp-com.ps1` must be copied onto the remote system.
For this, a simple Linux command can be used that automatically types the script after an initial delay of five seconds:
```
sleep 5; cat rdp-com.ps1 | xargs -i{} xdotool type {} --delay 10
```

After that, start the receiver script on the host computer.
For example, in this case the data is read from the initial screen coordinates (200, 800):
```
./receiver.py --posX 200 --posY 800 --pack 24
```
Position the sender console so that the colored blocks are visible in the red rectangle.

If the receiver script is running, the sender script can be executed on the remote system:
```
Import-Module .\rdp-com.ps1 -force; rdp-com -delay 50 -pack 24 -path <path/to/file/to/transmit>
```

## Demonstration
A video of the scripts in action can be found [here](https://drive.google.com/file/d/1awvEpWflo1hlVaV1iR3KTR9d2eQTQkh8/view?usp=sharing).
![Screenshot](https://github.com/MKesenheimer/rdp-com/blob/master/screenshot.png)