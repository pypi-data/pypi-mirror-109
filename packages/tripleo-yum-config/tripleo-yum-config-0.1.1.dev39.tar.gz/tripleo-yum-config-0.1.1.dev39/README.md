# tripleo-yum-config

*tripleo-yum-config* utility was designed to simplify the way that TripleO
deployments manage their yum configuration. This tool helps on updating
specific configuration options for different yum configuration files like yum
repos, yum modules and yum global configuration file.

## Quick start

### Using as a python module

It is possible to use *tripleo-yum-config* as a standalone module by cloning
its repository and invoking in command line:
```
python -m tripleo-yum-config repo appstream --enable --set-opts baseurl=http://newbaseurl exclude="package*"
python -m tripleo-yum-config module container-tools --enable --set-opts stream=rhel8
python -m global --set-opts keepcache=1 cachedir="/var/cache/dnf"
```

#### Install using setup.py

Installation using python setup.py requires sudo, because the python source
is installed at /usr/local/lib/python.

```
sudo python setup.py install
```

#### Install using pip
Alternatively you can install tripleo-yum-config with python pip:
```
pip install tripleo-yum-config --user
```
See PyPI [tripleo-yum-config](https://pypi.org/project/tripleo-yum-config/) 
project for more details.

## Usage

The utility provides a command line interface with various options. You can
invoke *tripleo-yum-config --help* to see all the available commands.
```
tripleo-yum-config --help
```

## Ansible Module

An ansible module [tripleo_yum_config](https://opendev.org/openstack/tripleo-repos/src/branch/master/tripleo-yum-config/tripleo_yum_config.py)
is available for you when you install tripleo-yum-config, either by using
setup.py or pip. The module is installed at the relative path
*share/ansible/plugins/modules*, which may land on a different directory, 
depending on how you are installing this package. Check your ansible
configuration to see if the directory is included in your ansible library path.
An [example playbook](https://opendev.org/openstack/tripleo-repos/src/branch/master/tripleo-yum-config/example_playbook.yaml)
is available to assist on module usage.