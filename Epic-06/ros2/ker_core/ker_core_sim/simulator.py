"""ROS2 dev-only transport, no physical drivers or production command topic."""
import json,time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile,ReliabilityPolicy,DurabilityPolicy
from std_msgs.msg import String
from std_srvs.srv import SetBool
from sensor_msgs.msg import JointState
from diagnostic_msgs.msg import DiagnosticArray,DiagnosticStatus,KeyValue
from .contracts import CommandGate,MockMotor,Rejected
class Simulator(Node):
 def __init__(self):
  super().__init__('ker_core_simulator');self.gate=CommandGate();self.gate.activate();self.motor=MockMotor()
  qos=QoSProfile(depth=10,reliability=ReliabilityPolicy.RELIABLE,durability=DurabilityPolicy.VOLATILE)
  self.state_pub=self.create_publisher(JointState,'/ker/sim/joint_states',qos)
  self.diag_pub=self.create_publisher(DiagnosticArray,'/ker/sim/diagnostics',qos)
  self.sub=self.create_subscription(String,'/ker/sim/joint_request',self.command,qos)
  self.service=self.create_service(SetBool,'/ker/sim/enable_mock',self.enable_mock)
  self.timer=self.create_timer(.05,self.tick)
 def diagnostic(self,result,seq=-1):
  status=DiagnosticStatus();status.name='ker_mock';status.hardware_id='no_physical_hardware';status.level=DiagnosticStatus.OK if result=='accepted' else DiagnosticStatus.WARN;status.message=result
  status.values=[KeyValue(key='request_seq',value=str(seq)),KeyValue(key='scope',value='mock_only'),KeyValue(key='generation',value=str(self.gate.generation)),KeyValue(key='physical_stop_confirmed',value='false')]
  m=DiagnosticArray();m.header.stamp=self.get_clock().now().to_msg();m.status=[status];self.diag_pub.publish(m)
 def command(self,msg):
  seq=-1
  try:
   if len(msg.data)>2048:raise Rejected('size')
   p=json.loads(msg.data);seq=p.get('seq',-1) if isinstance(p,dict) else -1
   plan=self.gate.accept(p,time.monotonic())
   if not self.motor.enabled:self.motor.enable()
   self.motor.command(plan['yaw'],time.monotonic());self.diagnostic('accepted',seq)
  except (Rejected,ValueError,TypeError):self.diagnostic('rejected',seq)
 def tick(self):
  self.motor.tick(time.monotonic());m=JointState();m.header.stamp=self.get_clock().now().to_msg();m.name=['mock_neck_yaw'];m.position=[self.motor.position];self.state_pub.publish(m)
 def enable_mock(self,request,response):
  if request.data:
   self.motor.reset(True,True);self.gate.activate()
  else:self.motor.stop();self.gate.cancel()
  response.success=True;response.message='Mock state only; physical stop NOT confirmed';return response

def main():
 rclpy.init();node=Simulator()
 try:rclpy.spin(node)
 finally:node.destroy_node();rclpy.shutdown()
if __name__=='__main__':main()
