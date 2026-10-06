// Identity-only firmware draft for UNO R4 Minima. No motor/sensor pins configured.
// Disconnect actuator power. Set BOARD_ROLE to 'B' for the joint-control board.
// This firmware replaces the existing sketch; preserve the old sketch before upload.
#include <Arduino.h>
#include <string.h>
const char BOARD_ROLE = 'A';
char line[32];
size_t used = 0;
bool overflow = false;
void setup() { Serial.begin(115200); }
void handleLine() {
  line[used] = '\0';
  if (overflow || used != 22 || strncmp(line, "HELLO ", 6) != 0) return;
  for (size_t i=6; i<22; ++i)
    if (!((line[i]>='0' && line[i]<='9') || (line[i]>='a' && line[i]<='f'))) return;
  Serial.print("LUMIRA1 "); Serial.print(line+6); Serial.print(' ');
  Serial.print(BOARD_ROLE); Serial.println(" UNO_R4_MINIMA probe-1 MOTION_DISABLED");
}
void loop() {
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c=='\n') { handleLine(); used=0; overflow=false; }
    else if (!overflow) {
      if (used < sizeof(line)-1) line[used++]=c;
      else overflow=true;
    }
  }
}
