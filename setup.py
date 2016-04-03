import setuptools

setuptools.setup(
    name="ssh-proxy-config",
    version="0.1.0",
    url="https://github.com/vmfarms/ssh-proxy-config",

    author="VM Farms Inc.",
    author_email="ops@vmfarms.com",

    description="Generate an SSH config for accessing hosts inside a VPC.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    package_data={
        'ssh_proxy_config': ['templates/*'],
    },

    install_requires=[
        'boto3',
        'jinja2 >= 2.7',
    ],

    entry_points={
        'console_scripts': [
            'ssh-proxy-config = ssh_proxy_config:main',
        ],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
