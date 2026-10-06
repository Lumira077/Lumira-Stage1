from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
 return LaunchDescription([Node(package='ker_core_sim',executable='simulator',name='ker_core_simulator',output='screen')])
