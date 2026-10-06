"""Real rclpy/DDS messaging with mock state. No hardware IO or real-time benchmark."""
import sys,pathlib,time,json,unittest,os
sys.path.insert(0,str(pathlib.Path(__file__).parent))
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import String
from std_srvs.srv import SetBool
from sensor_msgs.msg import JointState
from diagnostic_msgs.msg import DiagnosticArray
from ker_core_sim.simulator import Simulator
class Transport(unittest.TestCase):
 def setUp(self):
  rclpy.init();self.sim=Simulator();self.client=Node('ker_transport_test');self.exec=SingleThreadedExecutor();self.exec.add_node(self.sim);self.exec.add_node(self.client);self.diags=[];self.states=[]
  self.pub=self.client.create_publisher(String,'/ker/sim/joint_request',10)
  self.client.create_subscription(DiagnosticArray,'/ker/sim/diagnostics',self.diags.append,10)
  self.client.create_subscription(JointState,'/ker/sim/joint_states',self.states.append,10)
  self.assertTrue(self.wait(lambda:self.pub.get_subscription_count()>0 and len(self.states)>0))
 def wait(self,predicate):
  deadline=time.monotonic()+5
  while time.monotonic()<deadline:
   self.exec.spin_once(timeout_sec=.02)
   if predicate():return True
  return False
 def send(self,seq,yaw):
  m=String();m.data=json.dumps({'robot':'lumira_sim','schema':'joint-v1','generation':1,'seq':seq,'timestamp':time.monotonic(),'yaw':yaw});self.pub.publish(m)
 def has(self,seq,result):
  return any(s.message==result and any(v.key=='request_seq' and v.value==str(seq) for v in s.values) for m in self.diags for s in m.status)
 def test_dds_valid_command_and_feedback(self):
  self.send(1,.2);self.assertTrue(self.wait(lambda:self.has(1,'accepted')));self.assertTrue(self.wait(lambda:any(m.position and m.position[0]>0 for m in self.states)))
 def test_dds_invalid_number(self):
  self.send(2,float('nan'));self.assertTrue(self.wait(lambda:self.has(2,'rejected')));self.assertEqual(self.sim.motor.position,0)
 def test_stop_service_and_late_command(self):
  client=self.client.create_client(SetBool,'/ker/sim/enable_mock');self.assertTrue(client.wait_for_service(timeout_sec=3));req=SetBool.Request();req.data=False;future=client.call_async(req);self.assertTrue(self.wait(future.done));self.assertTrue(future.result().success);self.assertIn('NOT confirmed',future.result().message)
  self.send(3,.2);self.assertTrue(self.wait(lambda:self.has(3,'rejected')));self.assertTrue(self.sim.motor.latched)
 def tearDown(self):
  self.exec.shutdown();self.sim.destroy_node();self.client.destroy_node();rclpy.shutdown()
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Transport);result=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'source_commit':os.environ.get('GITHUB_SHA','local'),'scope':'actual_ROS2_Jazzy_DDS_mock_transport','tests':result.testsRun,'passed':result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors),'actual_hardware_calls':0,'actual_participants':0,'real_time_validated':False,'release_ready':False}
 out=pathlib.Path(__file__).resolve().parents[1]/'evidence';out.mkdir(parents=True,exist_ok=True);(out/'ros-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));raise SystemExit(0 if result.wasSuccessful() else 1)
