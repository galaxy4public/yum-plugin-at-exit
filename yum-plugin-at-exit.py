# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright 2014 Openwall Pty Ltd
# written by (GalaxyMaster) <galaxy-at-openwall.com.au>

"""
This plugin runs actions following the yum execution based on the yum
command that yum was invoked with.
"""


from yum.plugins import PluginYumExit, TYPE_CORE
from yum.constants import *
import os
import sys

requires_api_version = '2.4'
plugin_type = (TYPE_CORE,)

all = {}
removes = {}
installs = {}
updates = {}

def posttrans_hook(conduit):
    global all
    global removes
    global installs
    global updates
    ts = conduit.getTsInfo()
    all = ts.getMembers()
    removes = ts.getMembersWithState(output_states=TS_REMOVE_STATES)
    installs = ts.getMembersWithState(output_states=TS_INSTALL_STATES)
    updates = ts.getMembersWithState(output_states=[TS_UPDATE, TS_OBSOLETING])

def close_hook(conduit):
    action = conduit.confString('main','action','')
    if not action:
        return

    if not all:		# no work was done
        return

    command = action

    if installs:
        command += ' install'

    if updates:
        command += ' update'

    if removes:
        command += ' remove'

    conduit.info(2,'\nRunning at-exit command: %s' % command)

    if 0 != os.system(command):
        conduit.error(2,'The at-exit command exited with non-zero error code!')
        sys.exit(-1)
