#! /opt/microsoft/powershell/7/pwsh
# Run
# Edit-DTWBeautifyScript ([IO.Path]::Combine('.', 'create_environment.ps1'))
# to format this
$FolderName = [IO.Path]::Combine('.', 'venv')
if (Test-Path $FolderName) {

  Write-Host "Folder $FolderName Exists. Deleting it"
  Remove-Item $FolderName -Force -Recurse
}
else
{
  Write-Host "Folder {$FolderName} Doesn't Exists. Creating it"
}

if ($IsWindows) {
    $python = "python"
} else {
    $python = "python3"
}

Write-Host "Creating virtual environment"
Invoke-Expression "$python -m venv venv"
Write-Host "Virtual environment created"
if ($IsWindows) {
  .  ([IO.Path]::Combine('.', 'venv', 'Scripts', 'Activate.ps1'))
} else {
  . ([IO.Path]::Combine('.', 'venv', 'bin', 'Activate.ps1'))
}
Write-Host "Upgraging pip"
Invoke-Expression "$python -m pip install --upgrade pip"
# Invoke-Expression "$python -m pip install ordered-set zstandard nuitka"
Write-Host "Installing packages"
pip install wheel
pip install auto-py-to-exe pyttsx3 aiorun colorama
deactivate

