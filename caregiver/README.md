# Lumira caregiver R4

Capacitor Android/iOS app, version 0.4.0/build4.

Run npm ci and npm run sync in mobile, then build the Android/Xcode project.
The native CI compiles a debug Android APK and unsigned iOS device/simulator apps. An unsigned IPA is NOT installable on a physical iPhone. Apple development team/provisioning and device registration are required for signed distribution. No production credentials or device tokens are included.

Self-hosted Korean fonts are restored from pinned @fontsource-variable/noto-sans-kr 5.3.1 under its SIL OFL license during build. Source UI shows synthetic telemetry only when reported as simulation by the API.
