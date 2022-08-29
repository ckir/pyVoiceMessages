$FolderName = ".\dist\"
if (Test-Path $FolderName) {
 
    Write-Host "Folder $FolderName Exists. Deleting it"
    Remove-Item $FolderName -Force -Recurse
}
else
{
    Write-Host "Folder $FolderName Doesn't Exists. Creating it"
}
$FolderName = ".\build\"
if (Test-Path $FolderName) {
 
    Write-Host "Folder $FolderName Exists. Deleting it"
    Remove-Item $FolderName -Force -Recurse
}
else
{
    Write-Host "Folder $FolderName Doesn't Exists. Creating it"
}
. .\venv\Scripts\Activate.ps1
pyinstaller --noconfirm --onefile --console  "C:/Users/User/Documents/DEVELOPMENT/pyVoiceMessages/pyVoiceMessagesClient.py"
$ClientExitCode = $LASTEXITCODE
pyinstaller --noconfirm --onefile --console  "C:/Users/User/Documents/DEVELOPMENT/pyVoiceMessages/pyVoiceMessagesServer.py"
$ServerExitCode = $LASTEXITCODE

if ($ClientExitCode -eq 0) {
    Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) pyVoiceMessagesClient.py build OK" -ForegroundColor Green
} else {
    Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) pyVoiceMessagesClient.py build OK" -ForegroundColor DarkRed
}
if ($ServerExitCode -eq 0) {
    Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) pyVoiceMessagesServer.py build OK" -ForegroundColor Green
} else {
    Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) pyVoiceMessagesServer.py build OK" -ForegroundColor DarkRed
}