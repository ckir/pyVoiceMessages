$Folders=@('pyVoiceMessagesServer.build','pyVoiceMessagesServer.dist', 'pyVoiceMessagesServer.onefile-build',
'pyVoiceMessagesClient.build','pyVoiceMessagesClient.dist', 'pyVoiceMessagesClient.onefile-build',
 'dist, build')

foreach ($FolderName in $Folders) {
    if (Test-Path $FolderName) {
     
        Write-Host "Folder $FolderName Exists. Deleting it"
        Remove-Item $FolderName -Force -Recurse
    }
}

. .\venv\Scripts\Activate.ps1
pyinstaller --clean --noconfirm --onefile --console  "C:/Users/User/Documents/DEVELOPMENT/pyVoiceMessages/pyVoiceMessagesClient.py"
#python -m nuitka --mingw64 --standalone --onefile pyVoiceMessagesClient.py
$ClientExitCode = $LASTEXITCODE
pyinstaller --clean --noconfirm --onefile --console  "C:/Users/User/Documents/DEVELOPMENT/pyVoiceMessages/pyVoiceMessagesServer.py"
#python -m nuitka --mingw64 --standalone --onefile pyVoiceMessagesServer.py
$ServerExitCode = $LASTEXITCODE

if ($ClientExitCode -eq 0) {
    Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) pyVoiceMessagesClient.py build OK" -ForegroundColor Green
} else {
    Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) pyVoiceMessagesClient.py build FAILED" -ForegroundColor DarkRed
}
if ($ServerExitCode -eq 0) {
    Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) pyVoiceMessagesServer.py build OK" -ForegroundColor Green
} else {
    Write-Host "$( Get-Date -Format yyyy-MM-ddTHH:mm:ss.ffffff) pyVoiceMessagesServer.py build FAILED" -ForegroundColor DarkRed
}