"""Build an installable debug APK with an existing JDK21/Android SDK; no device mutation."""
import os,subprocess,urllib.parse
from pathlib import Path
root=Path(__file__).resolve().parents[1]
env=os.environ.copy();sdk=env.get('ANDROID_HOME') or env.get('ANDROID_SDK_ROOT')
if not sdk or not (Path(sdk)/'platforms/android-36/android.jar').exists():raise SystemExit('Set ANDROID_HOME to an SDK with platforms;android-36')
# Java does not consume HTTPS_PROXY automatically. Use only unauthenticated proxies.
p=urllib.parse.urlsplit(env.get('HTTPS_PROXY') or env.get('https_proxy') or '')
if p.hostname and not p.username and not p.password:
 env['GRADLE_OPTS']=f'-Dhttps.proxyHost={p.hostname} -Dhttps.proxyPort={p.port or 80} -Dhttp.proxyHost={p.hostname} -Dhttp.proxyPort={p.port or 80}'
wrapper='gradlew.bat' if os.name=='nt' else './gradlew'
raise SystemExit(subprocess.call([wrapper,'--no-daemon','--max-workers=2',':app:assembleDebug'],cwd=root/'android',env=env))
