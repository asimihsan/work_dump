# ----------------------------------------------------------------------------
#   In order to run:
#   -   Use pip to install fabric (pip install fabric)
#   -   Execute:
#           python administer_pest_boxes.py
# ----------------------------------------------------------------------------

import os
import sys
from glob import glob
from fabric.api import env, run, cd, sudo
from fabric.contrib.files import append, contains
from fabric.context_managers import settings
from fabric.operations import put

# ----------------------------------------------------------------------------
#   Constants.
# ----------------------------------------------------------------------------
EAS_BOXES = [ \
               "svr01.hawk",
               "svr02.hawk",
               "svr03.hawk",
               "svr04.hawk",
               "svr05.hawk",
               "svr06.hawk",
               "svr08.hawk",
            ]
ROOT_USERNAME = "root"
ROOT_PASSWORD = "mng2"
CURRENT_DIR = os.path.abspath(os.path.join(__file__, os.pardir))
# ----------------------------------------------------------------------------
         
def install_python():    
    with settings(warn_only=True):
        run("mkdir /opt/dcl/ai")
    with cd("/opt/dcl/ai"):
        run("rm -rf Python-2.7.3*")
        run("rm -rf python*")
    with cd("/opt/dcl/ai"):
        run("wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2")
        run("nice -n 19 ionice -c 3 tar xvf Python-2.7.3.tar.bz2")
    with cd("/opt/dcl/ai/Python-2.7.3"):
        run("nice -n 19 ionice -c 3 ./configure --prefix=/opt/dcl/ai/python")
        run("nice -n 19 ionice -c 3 make")
        run("nice -n 19 ionice -c 3 make install")
    with cd("/opt/dcl/ai"):
        run("rm -rf Python-2.7.3*")
    sudo("curl http://python-distribute.org/distribute_setup.py | /opt/dcl/ai/python/bin/python")
    sudo("curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | /opt/dcl/ai/python/bin/python")    
    sudo("nice -n 19 ionice -c 3 /opt/dcl/ai/python/bin/pip-2.7 install psutil ipython Cython")    

def install_zeromq():
    with cd("/opt/dcl/ai/"):
        run("rm -rf pyzmq-2.2* zeromq*")
    with cd("/opt/dcl/ai"):
        run("wget http://download.zeromq.org/zeromq-3.2.2.tar.gz")
        run("nice -n 19 ionice -c 3 tar xvf zeromq-3.2.2.tar.gz")
    with cd("/opt/dcl/ai/zeromq-3.2.2"):
        run("nice -n 19 ionice -c 3 ./configure --prefix=/opt/dcl/ai/zeromq")
        run("nice -n 19 ionice -c 3 make")
        run("nice -n 19 ionice -c 3 make install")
    with cd("/opt/dcl/ai"):
        run("wget https://github.com/zeromq/pyzmq/downloads/pyzmq-2.2.0.1.tar.gz")
        run("nice -n 19 ionice -c 3 tar xvf pyzmq-2.2.0.1.tar.gz")
    with cd("pyzmq-2.2.0.1"):
        run("/opt/dcl/ai/python/bin/python setup.py configure --zmq=/opt/dcl/ai/zeromq")
        run("/opt/dcl/ai/python/bin/python setup.py install")
    with cd("/opt/dcl/ai/"):
        run("rm -rf zeromq-3.2.2* pyzmq-2.2*")

def main():
    for box in EAS_BOXES:
        with settings(user=ROOT_USERNAME, password=ROOT_PASSWORD, host_string=box):            
            install_python()
            install_zeromq()
               
if __name__ == "__main__":
    main()