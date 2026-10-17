"""Reports missing native toolchain honestly. Does not download SDKs, accept licenses or submit apps."""
import json, os, platform, shutil, subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]
javac=shutil.which('javac');xcode=shutil.which('xcodebuild');sdk=os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
result={'android':{'java_compiler':javac,'sdk_configured':bool(sdk),'platform_36':bool(sdk and (Path(sdk)/'platforms/android-36/android.jar').exists()),'adb':shutil.which('adb'),'native_compile':'NOT_RUN','apk':'NOT_PRODUCED','aab':'NOT_PRODUCED'},'ios':{'host_os':platform.system(),'xcodebuild':xcode,'native_compile':'NOT_RUN','ipa':'NOT_PRODUCED'},'device_install':'NOT_RUN','store_upload':'NOT_RUN'}
if javac:result['android']['javac_version']=subprocess.run([javac,'-version'],capture_output=True,text=True).stdout.strip()
if xcode:result['ios']['xcode_version']=subprocess.run([xcode,'-version'],capture_output=True,text=True).stdout.strip()
path=root/'docs/native-build-preflight.json';path.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
