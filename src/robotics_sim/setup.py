from setuptools import find_packages, setup

package_name = 'robotics_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bradleykt',
    maintainer_email='bradley.m.karstadt@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'status_node = robotics_sim.status_node:main',
            'sim_command = robotics_sim.sim_command:main',
        ],
    },
)
