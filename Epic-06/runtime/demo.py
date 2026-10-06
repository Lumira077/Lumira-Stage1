import json
from core import *
g=CommandGate();generation=g.activate();m=MockMotor();m.enable()
p={'robot':'lumira_sim','schema':'joint-v1','generation':generation,'seq':1,'timestamp':10,'yaw':.2}
r=g.accept(p,10);m.command(r['yaw'],10);m.tick(10);position=m.tick(10.1);m.stop();g.cancel()
print(json.dumps({'mock_position':position,'latched':m.latched,'command':r,'actual_hardware_calls':0}))
