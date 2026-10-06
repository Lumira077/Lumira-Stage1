"""Generate precise connection diagrams; no inferred connector pin positions."""
from pathlib import Path
from html import escape
P=Path(__file__).parent/'images'
def make(name,title,subtitle,boxes,lines,notes):
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="820" viewBox="0 0 1280 820">','<rect width="1280" height="820" fill="#f4f7fb"/>','<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#486482"/></marker></defs>',f'<text x="40" y="52" font-family="sans-serif" font-size="30" font-weight="bold" fill="#14344e">{escape(title)}</text>',f'<text x="40" y="86" font-family="sans-serif" font-size="18" fill="#486482">{escape(subtitle)}</text>']
 for coords,label,x,y,color in lines:
  parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="3" marker-end="url(#arrow)"/>')
  parts.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="17" fill="{color}">{escape(label)}</text>')
 for x,y,w,h,title,details,color in boxes:
  parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="white" stroke="{color}" stroke-width="2"/>')
  parts.append(f'<text x="{x+18}" y="{y+32}" font-family="sans-serif" font-size="21" font-weight="bold" fill="{color}">{escape(title)}</text>')
  for i,line in enumerate(details):parts.append(f'<text x="{x+18}" y="{y+60+i*23}" font-family="sans-serif" font-size="16" fill="#34485c">{escape(line)}</text>')
 for i,n in enumerate(notes):parts.append(f'<text x="40" y="{740+i*27}" font-family="sans-serif" font-size="18" fill="#8b3c20">{escape(n)}</text>')
 parts.append('</svg>');(P/name).write_text(''.join(parts))
blue='#226080';green='#267264';red='#ae4937'
make('network.svg','Lumira Stage1 | Network and devices','Baseline: Pi5 8GB + AI HAT+13 TOPS. UNO R4 Minima A/B remain subject to physical confirmation.',[
(40,130,290,115,'Development PC',['SSH / source / test logs'],blue),(490,130,290,115,'LAN router',['DHCP reservations / VPN entry'],blue),(930,130,290,115,'Synology NAS',['Development DB / evidence'],blue),
(490,330,290,125,'Raspberry Pi 5',['Application / audio / camera','No direct 5V MCU GPIO wiring'],blue),(930,330,290,125,'AI HAT+ 13 TOPS',['PCIe + stacking header','Supported Hailo-8L models'],green),
(130,555,330,120,'UNO-A via USB',['Wheel / sensor role candidate','Identity-only firmware supplied'],green),(710,555,380,120,'UNO-B via USB',['Joint role candidate','Separate actuator bus interface'],green)],
[('330,180 490,180','Ethernet',355,170,blue),('780,180 930,180','Ethernet',805,170,blue),('635,245 635,330','LAN; Wi-Fi after bench',650,290,blue),('780,390 930,390','PCIe',825,378,green),('560,455 560,510 295,510 295,555','USB data',325,498,blue),('710,455 710,500 900,500 900,555','USB data',915,505,blue)],['Internet/NAS failure must not disable local stop logic.','Motor power is separate. USB identity success is not a motion-safety approval.'])
make('wheel_connection.svg','Wheel motors | Signal and power are separate','Logical terminal names only. Driver model, pin numbering, current limits and voltage must be confirmed.',[
(40,130,300,115,'Bench DC / battery',['Motor-rated supply','Voltage and current TBD'],red),(470,130,330,115,'Fuse + hardware inhibit',['Near-source protection','E-stop design / manual reset'],red),
(40,385,300,150,'UNO-A',['PWM + DIR or IN1/IN2','Encoder A/B inputs','Default driver inhibit'],blue),(470,385,330,150,'Motor driver channels',['Logic voltage compatible','VM / OUT / fault feedback','Current + thermal capability'],green),(930,385,290,150,'Left + right wheels',['One motor per channel','Supported test stand','Encoders if fitted'],green)],
[('340,185 470,185','Power',380,175,red),('635,245 635,385','Protected motor rail',655,310,red),('340,445 470,445','Control',360,432,blue),('800,445 930,445','Motor leads',815,432,red),('1075,535 1075,625 190,625 190,535','Encoder feedback to MCU; separate from motor-current return',335,652,blue)],['Non-isolated logic needs a common reference ground at the distribution point.','Do not route motor current through the Pi/UNO board or USB ground wiring.','Stop mode (coast/brake) and EN polarity depend on the selected driver.'])
make('joint_connection.svg','Joint motors | DYNAMIXEL or PWM servo','Choose the interface and power rail for each exact actuator model before connecting.',[
(40,135,340,130,'UNO-B',['USB from Pi','UART TX/RX + direction control','or dedicated servo output'],blue),(480,135,330,130,'Bus interface',['TTL half-duplex OR RS-485','Voltage-compatible transceiver','One active bus master'],green),(910,135,330,130,'DYNAMIXEL chain',['Unique ID for every actuator','Common protocol / baud rate','Model-specific control table'],green),
(480,435,330,145,'Protected joint supply',['Fuse / inhibit / current limit','Separate rail per voltage class','No power from USB adapter'],red),(40,435,340,145,'Optional PWM servos',['Signal from MCU/controller','Separate servo supply','No fixed pulse range assumed'],blue),(910,435,330,145,'Commissioning option',['PC/Pi + U2D2','Replace normal bus master','Do not drive from two masters'],blue)],
[('380,200 480,200','UART',405,188,blue),('810,200 910,200','Bus',840,188,blue),('645,435 645,340 980,340 980,265','Model-rated power',720,325,red),('480,500 380,500','Power',400,488,red),('1075,435 1075,265','Alternate data path',1085,365,blue)],['Support arms/head before torque-off: the mechanism may fall under gravity.','Example: XL330-M288-T is 3.7–6.0V (5.0V recommended), NOT a 12V actuator.','Connector orientation and wire colors must be checked against the exact model manual.'])
