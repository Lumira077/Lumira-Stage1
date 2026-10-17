param([Parameter(Mandatory=$true)][string]$Serial,[string]$Apk="$PSScriptRoot\Lumira_Caregiver_R4_0.4.0_Debug.apk")
$ErrorActionPreference='Stop'
$expected='3ac5b93219833d1c409d5cfb30ab9fa4948d112519f6d7f9a79271c97e55e909'
if((Get-FileHash -Algorithm SHA256 $Apk).Hash.ToLowerInvariant() -ne $expected){throw 'APK hash mismatch'}
Get-Command adb -ErrorAction Stop | Out-Null
$state=& adb -s $Serial get-state
if($LASTEXITCODE -ne 0 -or $state -ne 'device'){throw 'Connect and authorize the selected Android phone first'}
& adb -s $Serial install -r $Apk
if($LASTEXITCODE -ne 0){throw 'APK installation failed'}
& adb -s $Serial shell am start -n kr.lumira.caregiver.dev/.MainActivity
if($LASTEXITCODE -ne 0){throw 'Application launch failed'}
& adb -s $Serial shell dumpsys package kr.lumira.caregiver.dev | Select-String 'versionName|versionCode'
