#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Glances - An eye on your system
#
# Copyright (C) 2014 Nicolargo <nicolas@nicolargo.com>
#
# Glances is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Glances is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Import system libs
# Check for PSUtil already done in the glances_core script
import psutil

# from ..plugins.glances_plugin import GlancesPlugin
from glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """
    Glances's swap memory Plugin

    stats is a dict
    """

    def __init__(self):
        GlancesPlugin.__init__(self)

        # We want to display the stat in the curse interface
        self.display_curse = True
        # Set the message position
        # It is NOT the curse position but the Glances column/line
        # Enter -1 to right align 
        self.column_curse = 3
        # Enter -1 to diplay bottom
        self.line_curse = 1


    def update(self):
        """
        Update MEM (SWAP) stats
        """

        # SWAP
        # psutil >= 0.6
        if hasattr(psutil, 'swap_memory'):
            # Try... is an hack for issue #152
            try:
                virtmem = psutil.swap_memory()
            except Exception:
                self.stats = {}
            else:
                self.stats = {'total': virtmem.total,
                              'used': virtmem.used,
                              'free': virtmem.free,
                              'percent': virtmem.percent}

        # psutil < 0.6
        elif hasattr(psutil, 'virtmem_usage'):
            virtmem = psutil.virtmem_usage()
            self.stats = {'total': virtmem.total,
                          'used': virtmem.used,
                          'free': virtmem.free,
                          'percent': virtmem.percent}
        else:
            self.stats = {}


    def msg_curse(self, args=None):
        """
        Return the dict to display in the curse interface
        """
        # Init the return message
        ret = []

        # Build the string message
        # Header
        msg = "{0:5} ".format(_("SWAP"))
        ret.append(self.curse_add_line(msg, "TITLE"))
        # Percent memory usage
        msg = "{0}".format(format(self.stats['percent'] / 100, '>6.1%'))
        ret.append(self.curse_add_line(msg))
        # New line
        ret.append(self.curse_new_line())
        # Total memory usage
        msg = "{0:8}".format(_("total:"))
        ret.append(self.curse_add_line(msg))
        msg = "{0}".format(format(self.auto_unit(self.stats['total'], '>6')))
        ret.append(self.curse_add_line(msg))
        # New line
        ret.append(self.curse_new_line())
        # Used memory usage
        msg = "{0:8}".format(_("used:"))
        ret.append(self.curse_add_line(msg))
        msg = "{0}".format(format(self.auto_unit(self.stats['used'], '>6')))
        ret.append(self.curse_add_line(msg, 
                                       self.get_alert_log(self.stats['used'], 
                                                          max=self.stats['total'])))
        # New line
        ret.append(self.curse_new_line())
        # Free memory usage
        msg = "{0:8}".format(_("free:"))
        ret.append(self.curse_add_line(msg))
        msg = "{0}".format(format(self.auto_unit(self.stats['free'], '>6')))
        ret.append(self.curse_add_line(msg))

        return ret
