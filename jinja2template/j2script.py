from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from jinja2 import Template
import yaml
import sys

junos_hosts = { 'r3-core01':'10.92.38.57' , 'r7-pe01':'10.92.37.241' }

for host in junos_hosts:
    try:
        #open and read the yaml file
        with open(host + '.yml', 'r') as fh:
            data = yaml.load(fh.read())
        #open and read the jianja2 template
        with open ('iflospf.j2', 'r') as t_fh:
            t_format = t_fh.read()

        #associate the t_format to a jinja2 module
        template = Template(t_format)

        #merge the data with Template
        myConfig = template.render(data)

        print "Configuration for", host
        #print myConfig

        #user can't be root or will land in shell
        dev = Device( host = junos_hosts[host], user='lab', password='lab123').open()

        config = Config(dev)
        config.lock()
        config.load(myConfig, merge=True, format="text")
        config.pdiff()
        config.commit(timeout=360)
        config.unlock()
        dev.close()




    except LockError as e:
        print "The config database was locked!"
    except ConnectTimeoutError as e:
        print "Connetion timeout"
