from setuptools import setup
p='lumira_contract_demo'
setup(name=p,version='0.1.0',packages=[p],data_files=[('share/ament_index/resource_index/packages',['resource/'+p]),('share/'+p,['package.xml'])],install_requires=['setuptools'],zip_safe=True,maintainer='Lumira development',maintainer_email='dev@example.invalid',description='Sprint1 simulation contract adapter',license='UNLICENSED',entry_points={'console_scripts':['publisher = lumira_contract_demo.nodes:publisher_main','subscriber = lumira_contract_demo.nodes:subscriber_main']})
