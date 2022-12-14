#! /opt/microsoft/powershell/7/pwsh
# Run
# Edit-DTWBeautifyScript ([IO.Path]::Combine('.', 'Build.ps1'))
# to format this
$Folders = @('pyVoiceMessagesServer.build','pyVoiceMessagesServer.dist','pyVoiceMessagesServer.onefile-build',
  'pyVoiceMessagesClient.build','pyVoiceMessagesClient.dist','pyVoiceMessagesClient.onefile-build',
  'dist, build')

foreach ($FolderName in $Folders) {
  if (Test-Path $FolderName) {
    Write-Host "Folder $FolderName Exists. Deleting it"
    Remove-Item $FolderName -Force -Recurse
  }
}

if ($IsWindows) {
  .  ([IO.Path]::Combine('.', 'venv', 'Scripts', 'Activate.ps1'))
} else {
  . ([IO.Path]::Combine('.', 'venv', 'bin', 'Activate.ps1'))
}

  pyinstaller --clean --noconfirm --onefile --console ([IO.Path]::Combine('.', 'pyVoiceMessagesClient.py'))
  #python -m nuitka --mingw64 --standalone --onefile pyVoiceMessagesClient.py
  $ClientExitCode = $LASTEXITCODE
  pyinstaller --clean --noconfirm --onefile --console ([IO.Path]::Combine('.', 'pyVoiceMessagesServer.py'))
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
