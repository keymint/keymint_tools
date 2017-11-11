import sys

from setuptools import find_packages
from setuptools import setup

if sys.version_info < (3, 5):
    print('keymint requires Python 3.5 or higher.', file=sys.stderr)
    sys.exit(1)

setup(
    name='keymint_tools',
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    install_requires=['osrf_pycommon'],  # 'ament-package',
    author='Ruffin White',
    author_email='ruffin@osrfoundation.org',
    maintainer='Ruffin White',
    maintainer_email='ruffin@osrfoundation.org',
    url='https://github.com/keymint/keymint_tools/wiki',
    download_url='https://github.com/keymint/keymint_tools/releases',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Keymint is a build system for keystores.',
    long_description="""\
Keymint defines metainformation for keys, their certificats,
and provides tooling to build these federated keystores together.""",
    license='Apache License, Version 2.0',
    test_suite='test',
    entry_points={
        'keymint_cli.command': [
            'keystore = keymint_tools.command.keystore:KeystoreCommand',
        ],
        'keymint_cli.extension_point': [
            'keymint_tools.keystore.verb = keymint_tools.verb:VerbExtension',
        ],
        'keymint_tools.keystore.verb': [
            # 'auto = keymint_tools.command.keystore.verb.auto:AutoVerb',
            'build = keymint_tools.command.keystore.verb.build:BuildVerb',
            'build_pkg = keymint_tools.command.keystore.verb.build_pkg:BuildPkgVerb',
            # 'create = keymint_tools.command.keystore.verb.create:CreateVerb',
            'init = keymint_tools.command.keystore.verb.init:InitVerb',
            # 'sign = keymint_tools.command.keystore.verb.sign:SignVerb',
            # 'test = keymint_tools.command.keystore.verb.test:TestVerb',
        ],
        'keymint.build_types': [
            'keymint_ros2_dds = keymint_tools.build_types.keymint_ros2_dds:KeymintROS2DDSBuildType',
        ],
        'keymint.package_types': [
            'keymint_ros = keymint_tools.package_types.keymint_ros:entry_point_data',
        ],
    },
)
