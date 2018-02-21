# keymint_tools

[![pypi](https://img.shields.io/pypi/v/keymint_tools.svg?branch=master)](https://pypi.python.org/pypi/keymint_tools/)
[![docs](https://readthedocs.org/projects/keymint/badge/?version=latest)](https://readthedocs.org/projects/keymint)
[![build](https://travis-ci.org/keymint/keymint_tools.svg?branch=master)](https://travis-ci.org/keymint/keymint_tools)
[![codecov](https://codecov.io/github/keymint/keymint_tools/coverage.svg?branch=master)](https://codecov.io/github/keymint/keymint_tools?branch=master)
[![docker](https://img.shields.io/docker/build/keymint/keymint_tools.svg)](https://hub.docker.com/r/keymint/keymint_tools/builds/)


Keymint is a framework for generating cryptographic artifacts used in securing middleware systems like ROS, DDS, etc. Keymint is akin to other build systems, yet instead of compiling source code and installing executables in workspaces like with [`ament`](https://github.com/ament), [`keymint`](https://github.com/keymint) mints keys and notarizes documents in keystores, as the project name's alteration plays upon. Keymint provides users pluggable tools for automating the provision process for customizing PKI artifacts used with SROS, or Secure DDS plugins.
Command line tools for using keymint are collected within the [`keymint_tools`](https://github.com/keymint/keymint_tools) python module.


## Overview

To provide privacy, authenticity and integrity in middleware systems such as SROS or Secure DDS, each node in the disturbed computation graph or participant on the data buss is attributed to an identity. This is commonly done by provisioning each with a certificate, singed by a trusted Certificate Authority (CA), using established Public Key Infrastructure (PKI). In addition, access control may also be enforced by allocating given roles or attributes to participants, e.g scope of actions or topics permitted, by way of singed and verifiable control policy. Properly generating, maintaining and distributing the number of singed public certificates, ciphered private keys, and access control documents attributed to every identity within a scalable and distributed network can prove beyond tedious and error prone. To help mitigate the risks of improper provisioning, keymint has been developed to provide users an automation approach for systematic generation of necessary cryptographic artifacts in a familiar yet expandable build system layout via workspaces and plugins.

Keymint's approach in minting cryptographic artifacts resembles that other common build systems, such as ament, used to compile binary artifacts from source code. Similarly, users create `keymint_package`s within an workspace initialized by a `keymint_profile`; a package being a structured source manifest describing how and what artifacts to be generated for an identity, while the workspace provides a tunable profile to adjust the global build context for all packages. In addition, keymint shares a staggered development cycle, where a workspace is "initialized", "built", and "installed". While each stage in the cycle is subject to the behavior of the plugin invoked, an expected use case for SROS or Secure DDS middlewares are as follows:

1. TODO



## Installation

For detailed instillation setup, please view the included Dockerfile provided within the `.docker` directory. While keymint also provides `package.xml` files for ament instillation, pre-built Docker images are also hosted on Docker Hub:

``` bash
docker run -it keymint/keymint_tools
```

## Example
As a simple example, we'll create a working keystore for SROS2 to enable talker listener node pair. To start, the keymint keystore first needs to be initialized. Using the bootstrap argument, a template is used to generate a generic profile. In addition, designated certificate authorities (CA) specified with in the generated keymint profile is created.

``` bash
mkdir ~/keystore_ws
cd ~/keystore_ws
keymint keystore init --bootstrap keymint_ros
tree .
.
├── private
│   ├── ca.csr.pem
│   └── ca.key.pem
├── profile
│   ├── authorities.xml
│   ├── comarmor.d
│   │   └── example.xml
│   ├── keymint_profile.xml
│   ├── package.defaults
│   │   ├── governance.xml
│   │   ├── identities.xml
│   │   └── permissions.xml
│   ├── policies.xml
│   └── profile.defaults
│       └── authorities.xml
└── public
    └── ca.cert.pem
```

Using the ComArmor profile provided by the template we next create a set of keymint packages to encapsulate the intermediate configuration of the cryptographic artifacts necessary for SROS.

``` bash
keymint keystore create_pkg talker
keymint keystore create_pkg listener
tree .
.
...
└── src
    ├── listener
    │   ├── governance.xml
    │   ├── identities.xml
    │   ├── keymint_package.xml
    │   ├── package.defaults -> ../../profile/package.defaults
    │   └── permissions.xml
    └── talker
        ├── governance.xml
        ├── identities.xml
        ├── keymint_package.xml
        ├── package.defaults -> ../../profile/package.defaults
        └── permissions.xml
```

Finlay, we'll build and install our new keymint packages to generate the sing the resulting artifacts used directly by SROS2. This stage of the processes essentially translates the ROS centric policies and permission definitions into transport specific documents used by Secure DDS plugins.

``` bash
keymint keystore build_pkg src/talker
keymint keystore build_pkg src/listener
tree .
.
├── build
│   ├── listener
│   │   ├── csr.pem
│   │   ├── governance.xml
│   │   ├── key.pem
│   │   └── permissions.xml
│   └── talker
│       ├── csr.pem
│       ├── governance.xml
│       ├── key.pem
│       └── permissions.xml
├── install
│   ├── listener
│   │   ├── cert.pem
│   │   ├── governance.p7s
│   │   ├── key.pem
│   │   └── permissions.p7s
│   └── talker
│       ├── cert.pem
│       ├── governance.p7s
│       ├── key.pem
│       └── permissions.p7s
...
```

To use our keystore with SROS2, we can adapt install directory to accommodate ROS2 Ardent expected location of the certificate authority.

``` bash
cp public/ca.cert.pem install/talker
cp public/ca.cert.pem install/listener

export ROS_SECURITY_ROOT_DIRECTORY=~/keymint_ws/install
export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_STRATEGY=Enforce

ros2 run demo_nodes_cpp listener &
ros2 run demo_nodes_cpp talker
# To stop
^-C
kill %1
```

## Commands

Keymint provides a number of CLI subcommands, including:

### `keystore`

#### `build_pkg` Build Package

``` terminal
$ keymint keystore build_pkg -h
Build Package

positional arguments:
  path                  Path to the package (default '.')

optional arguments:
  -h, --help            show this help message and exit
  --build-space BUILD_SPACE
                        Path to the build space (default 'CWD/build')
  --install-space INSTALL_SPACE
                        Path to the install space (default 'CWD/install')
  --public_space PUBLIC_SPACE
                        Path to the public space (default 'CWD/public')
  --private_space PRIVATE_SPACE
                        Path to the private space (default 'CWD/private')
  --skip-build          Skip the build step (this can be used when installing
                        or testing and you know that the build has
                        successfully run)
  --skip-install        Skip the install step (only makes sense when install
                        has been done before using symlinks and no new files
                        have been added or when testing after a successful
                        install)

'keymint_ros2_dds' build_type options:
  -f, --force           overwrite existing builds
  -u, --unsigned        leave builds unsigned
```

#### `create_pkg` Create Package

``` terminal
$ keymint keystore create_pkg -h
Create Package

positional arguments:
  name                  Name of the package

optional arguments:
  -h, --help            show this help message and exit
  --source-space SOURCE_SPACE
                        Path to the source space (default 'CWD/src/NAME')
  --profile-space PROFILE_SPACE
                        Path to the profile space (default 'CWD/profile')
  --public_space PUBLIC_SPACE
                        Path to the public space (default 'CWD/public')
  --private_space PRIVATE_SPACE
                        Path to the private space (default 'CWD/private')
```


#### `init` Initialize Profile

``` terminal
$ keymint keystore init -h
Initialize Profile

optional arguments:
  -h, --help            show this help message and exit
  --source-space SOURCE_SPACE
                        Path to the source space (default 'CWD/src')
  --profile-space PROFILE_SPACE
                        Path to the profile space (default 'CWD/profile')
  --public_space PUBLIC_SPACE
                        Path to the public space (default 'CWD/public')
  --private_space PRIVATE_SPACE
                        Path to the private space (default 'CWD/private')
  --skip-build          Skip the build step (this can be used when installing
                        or testing and you know that the build has
                        successfully run)
  --skip-install        Skip the install step (only makes sense when build has
                        been done before and no new files have been added)
```

## Tutorial

TODO
