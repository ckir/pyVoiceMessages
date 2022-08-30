$FolderName = ".\venv\"
if (Test-Path $FolderName) {
 
    Write-Host "Folder venv Exists. Deleting it"
    Remove-Item $FolderName -Force -Recurse
}
else
{
    Write-Host "Folder Doesn't Exists. Creating it"
}

python -m venv venv
. .\venv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip
python -m pip install nuitka
pip install wheel
pip install auto-py-to-exe pyttsx3 aiorun colorama ordered-set zstandard
deactivate