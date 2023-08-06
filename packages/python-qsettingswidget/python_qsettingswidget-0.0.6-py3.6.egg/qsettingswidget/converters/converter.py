# python-qsettingswidget
# Copyright (C) 2019  LoveIsGrief
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from enum import Enum, auto


class Signals(Enum):
    CHANGED = auto


class Converter(object):
    """
    A utility to get certain values from widgets
    """

    @classmethod
    def can_convert(cls, widget):
        raise NotImplementedError()

    @classmethod
    def get(cls, widget):
        raise NotImplementedError()

    @classmethod
    def set(cls, widget, value):
        raise NotImplementedError()

    @classmethod
    def signal(cls, widget, signal_enum):
        raise NotImplementedError()
