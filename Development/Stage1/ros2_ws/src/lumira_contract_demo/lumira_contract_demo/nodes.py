"""ROS2 adapter; simulation namespace only. No physical motor driver."""
import json,time,sys
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile,ReliabilityPolicy,DurabilityPolicy
from std_msgs.msg import String
from .contract_core import TOPICS,PREFIX,Validator,Reject,envelope,fixtures

def qos(t):
 return QoSProfile(depth=1 if t in ('safety_state','gesture_request','expression_state') else (5 if t=='joint_states' else 10),reliability=ReliabilityPolicy.BEST_EFFORT if t=='joint_states' else ReliabilityPolicy.RELIABLE,durability=DurabilityPolicy.TRANSIENT_LOCAL if t=='safety_state' else DurabilityPolicy.VOLATILE)
class Subscriber(Node):
 def __init__(self):
  super().__init__('sprint1_subscriber');self.gate=Validator('sprint1_demo')
  self.subs=[self.create_subscription(String,PREFIX+t,lambda msg,t=t:self.receive(t,msg),qos(t)) for t in sorted(TOPICS)]
 def receive(self,topic,msg):
  try:
   if len(msg.data.encode())>4096:raise Reject('size')
   m=json.loads(msg.data)
   if m.get('topic')!=PREFIX+topic:raise Reject('topic_binding')
   r=self.gate.accept(m);self.get_logger().info(json.dumps(r))
  except (Reject,ValueError,TypeError,AttributeError) as e:self.get_logger().warning('REJECT '+str(e))
class Publisher(Node):
 def __init__(self):
  super().__init__('sprint1_publisher');self.pubs={t:self.create_publisher(String,PREFIX+t,qos(t)) for t in TOPICS};self.i=0
  self.timer=self.create_timer(.05,self.emit)
 def emit(self):
  # Wait for discovery. Two processes must run on the same host monotonic clock.
  if not all(p.get_subscription_count()>0 for p in self.pubs.values()):return
  # Each cycle: fresh safety then expression. Cross-topic order is not guaranteed;
  # validator conservatively rejects gesture arriving before valid safety.
  for t,payload in fixtures()[:5]:
   m=String();m.data=json.dumps(envelope(t,payload,self.i));self.pubs[t].publish(m)
  self.i+=1
  if self.i>=20:self.timer.cancel();self.get_logger().info('20 mock cycles published; hardware_execution=false')
def subscriber_main():
 rclpy.init();n=Subscriber()
 try:rclpy.spin(n)
 except KeyboardInterrupt:pass
 finally:n.destroy_node();rclpy.shutdown()
def publisher_main():
 rclpy.init();n=Publisher()
 try:rclpy.spin(n)
 except KeyboardInterrupt:pass
 finally:n.destroy_node();rclpy.shutdown()
