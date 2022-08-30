# Disclaimer
The binaries in our releases created using the pyinstaller and therefore are recognized as false positives by many antivirus including windows defender. There is nothing wrong with them however you can build your own from source. Just run the Build script. (The alternative compilers nuitka and py2exe produce more false positives than pyinstaller)

# Description
This is a small handy utility to help you get notified when your background script/app etc has no way to notify you other than voice aka you are out of network.

# Usage
First in a terminal start the server (run pyVoiceMessagesServer.exe) and copy the client (pyVoiceMessagesClient.exe) to a folder that is in your path. Thats it. you are good to go. Later you can use nssm or the tool of your choice to install pyVoiceMessagesServer.exe as service.

# Example
Lets say that you have a backgrount script that monitors a number of servers something like the following

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

Everything fine while you have a network connection. Then your network connection fails and your script cannot use mqtt or other means to notify you other than voice. Remember as you run it in background there is no console and even if it was you don't want to spend your time staring at it.

Also the connection failure can last from hours to days. You want to be notified not mad by hearing a "connection is down" message over and over again.

So take a look of the usage of the pyVoiceMessagesClient at the script.
When the 'bad' situation happens you will hear your message for a number of times and at interval YOU specify.

The server will ignore every additional requests for a message until is completed. Of cource if the situation turns to 'good' you can cancel your message at anytime.

That's it.




 
