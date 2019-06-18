from enoslib.api import play_on
from enoslib.infra.enos_g5k.provider import G5k
from enoslib.infra.enos_g5k.configuration import Configuration, NetworkConfiguration

import logging
import os

logging.basicConfig(level=logging.INFO)

# path to the inventory
inventory = os.path.join(os.getcwd(), "hosts")

# claim the resources
network = NetworkConfiguration(id="n1",
                               type="prod",
                               roles=["my_network"],
                               site="rennes")

force_deploy = True if os.environ.get("G5K_FORCE") else False

conf = Configuration.from_settings(job_name="Miguel_test",
                                   env_name="debian9-x64-std",
                                   force_deploy=force_deploy,
                                   walltime="06:00:00")\
    .add_network_conf(network)\
    .add_machine(roles=["control"],
                 cluster="parasilo",
                 nodes=1,
                 primary_network=network)\
    .finalize()

provider = G5k(conf)
roles, network = provider.init()

VAGRANT_URL = "https://releases.hashicorp.com/vagrant/2.0.3/vagrant_2.0.3_x86_64.deb"
VBOX_URL = "https://download.virtualbox.org/virtualbox/5.2.10/virtualbox-5.2_5.2.10-122088~Debian~stretch_amd64.deb"

with play_on("all", roles=roles) as p:
    p.shell("update-alternatives --install /usr/bin/python python /usr/bin/python3 1")
    p.apt(name="linux-headers-amd64", state="present", update_cache="yes")
    p.shell(f"ls vagrant.deb || wget {VAGRANT_URL} -O vagrant.deb", display_name="Download vagrant")
    p.shell("dpkg -i vagrant.deb")
    p.shell("apt-get -f -y install")
    p.shell(f"ls vbox.deb || wget {VBOX_URL} -O vbox.deb", display_name="Download vbox")
    p.shell("dpkg -i vbox.deb || true")
    p.shell("apt-get -f -y install")
    p.copy(src="./reservation.yaml", dest="/tmp/reservation.yaml")
    p.apt(name="python-pip", state="present")
    p.pip(name="enos", state="present")
    p.shell("""
        dir=".vagrant.d"
        mkdir -p "/tmp/$dir"
        mkdir -p "/root/$dir"
        (mount|grep vagrant) || mount -o bind "/tmp/$dir" "/root/$dir"
        dir="VirtualBox VMs"
        mkdir -p "/tmp/$dir"
        mkdir -p "/root/$dir"
        (mount|grep VirtualBox) || mount -o bind "/tmp/$dir" "/root/$dir"
    """, display_name="mounts")
    p.pip(name="docker-py", state="present")
    p.shell("which docker || (curl https://get.docker.com | sh)")
    p.docker_container(name="registry",
                       image="registry:2",
                       state="started",
                       env={"REGISTRY_PROXY_REMOTEURL": "https://registry-1.docker.io"},
                       ports=["0.0.0.0:5000:5000"],
                       display_name="Start the external")
