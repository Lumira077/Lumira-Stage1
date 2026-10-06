from setuptools import setup,find_packages
from glob import glob
setup(name='ker_core_sim',version='0.1.0',packages=find_packages(),data_files=[('share/ament_index/resource_index/packages',['resource/ker_core_sim']),('share/ker_core_sim',['package.xml']),('share/ker_core_sim/launch',glob('launch/*.launch.py'))],install_requires=['setuptools'],zip_safe=True,maintainer='KER Robot',maintainer_email='retri01@gmail.com',description='Development-only mock transport',license='Proprietary',entry_points={'console_scripts':['simulator=ker_core_sim.simulator:main']})
