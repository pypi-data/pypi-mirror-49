# Copyright (c) 2012-2019 Chintalagiri Shashank
#
# This file is part of pysamloader.

# pysamloader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pysamloader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysamloader.  If not, see <http://www.gnu.org/licenses/>.


from pysamloader.samdevice import SAMDevice


class ATSAM3U4E(SAMDevice):
    EFC_FMR = '400E0800'
    EFC_FCR = '400E0804'
    EFC_FSR = '400E0808'
    EFC_FRR = '400E080C'
    CHIPID_CIDR = '400E0740'
    CHIPID_EXID = '400E0744'
    AutoBaud = False
    FullErase = False
    WP_COMMAND = None
    EWP_COMMAND = '03'
    EA_COMMAND = None
    FS_ADDRESS = '00080000'
    PAGE_SIZE = 256
    SGPB_CMD = '0B'
    CGPB_CMD = '0C'
    GD_CMD = '00'
    STUI_CMD = '0E'
    SPUI_CMD = '0F'
    SGP = [0, 1, 0]

    def __init__(self):
        super(ATSAM3U4E, self).__init__()
