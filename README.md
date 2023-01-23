# Disclaimer
The binaries in our releases created using the pyinstaller and therefore are recognized as false positives by many antivirus including windows defender. There is nothing wrong with them however you can build your own from source. Just run the Build script. (The alternative compilers nuitka and py2exe produce more false positives than pyinstaller)

# Description
This is a small handy utility to help you get notified when your background script/app etc has no way to notify you other than voice aka you are out of network.

# Why
Lets say that you have a backgrount script that depends on internet access.
Everything is fine while you have a network connection. Remember as you run it in background there is no console and even if it was you don't want to spend your time staring at it.
Then your network connection fails and your script cannot use mqtt or other means to notify you. There is nothing else left other than voice.

Ok then voice is a nice option but a connection failure can last from hours to days. You want to be notified not mad by hearing a "connection is down" message over and over again.

So use the pyVoiceMessagesClient at your script.
When the 'bad' situation happens you will hear a message YOU define for a number of times and at interval YOU specify.

The server will ignore every additional requests for a message until is completed. Of cource if the situation turns to 'good' you can cancel your message at anytime.

# Usage
##Server
```
pyVoiceMessagesServer.py -h

usage: pyVoiceMessagesServer.py [-h] [-V | --verbose | --no-verbose] [-L | --list | --no-list] [port]

positional arguments:
  port                  Port to listen

options:
  -h, --help            show this help message and exit
  -V, --verbose, --no-verbose
                        Prints server activity messages
  -L, --list, --no-list
                        List available voices and exit
```

You can run a binary pyVoiceMessagesServer.exe for windows or pyVoiceMessagesServer for linux or run from source like

### Windows Powershell Terminal
```
.\create_environment.ps1 # Run this one time only to create a virtual environment
.\venv\Scripts\Activate.ps1 # Activate the virtual environment
python .\pyVoiceMessagesServer.py 
```
Tip. Use a tool like nssm to run pyVoiceMessagesServer.exe as service

### Linux Terminal
```
./create_environment.sh # Run this one time only to create a virtual environment
source ./venv/bin/activate # Activate the virtual environment
python ./pyVoiceMessagesServer.py 
```

##Client
Because of the inconvenience of activating a virtual environment use a binary for client.
```
pyVoiceMessagesClient.py -h
usage: pyVoiceMessagesClient.py [-h] [-H HOST] [-P PORT] [-D | --debug | --no-debug] {list,on,off} ...

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Provide destination host. Defaults to localhost
  -P PORT, --port PORT  Provide destination port. Defaults to 8888
  -D, --debug, --no-debug
                        Prints the server response

Subcommands:
  valid subcommands

  {list,on,off}         additional help
    list                List server voices
    on                  Create new message
    off                 Cancel existing message
```
```
pyVoiceMessagesClient.py list -h
usage: pyVoiceMessagesClient.py list [-h] [-J | --outputjson | --no-outputjson]

options:
  -h, --help            show this help message and exit
  -J, --outputjson, --no-outputjson
                        Output voices in JSON format
```
```
\pyVoiceMessagesClient.py on -h
usage: pyVoiceMessagesClient.py on [-h] [-R REPEAT] [-I INTERVAL] [-V VOICE] message

positional arguments:
  message               Provide text to say

options:
  -h, --help            show this help message and exit
  -R REPEAT, --repeat REPEAT
                        Provide how many times to repeat the message. Defaults to 1
  -I INTERVAL, --interval INTERVAL
                        Provide how many seconds to wait before repeating the message. Defaults to 15 seconds
  -V VOICE, --voice VOICE
                        Provide how many times to repeat the message. Defaults to 1
```
```
pyVoiceMessagesClient.py off -h
usage: pyVoiceMessagesClient.py off [-h] message

positional arguments:
  message     Message to cancel

options:
  -h, --help  show this help message and exit
```

### Example

#### Server runs on windows

```
#! /opt/microsoft/powershell/7/pwsh
param(
  [Parameter(HelpMessage = "Interval for checking")]
  [int]$CheckInterval = 10
)

try
{
  $servers = @('www.google.com','www.microsoft.com')
  while ($true) {
    $CombinedConnectivity = $true
    foreach ($server in $servers) {
      $connectivity = (Test-NetConnection -ComputerName "$server" -InformationLevel "Quiet")
      $CombinedConnectivity = $CombinedConnectivity -and $connectivity
      if ($connectivity)
      {
        Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) $server is responding" -ForegroundColor Green
        pyVoiceMessagesClient.exe off "$server is NOT responding"
      } else {
        Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) $server is NOT responding" -ForegroundColor DarkRed
        pyVoiceMessagesClient.exe -V 0 -R 5 -I 30 on "$server is NOT responding"
      }
    }
    Start-Sleep -Seconds $CheckInterval
  }
}

finally
{

}
```



That's it.
