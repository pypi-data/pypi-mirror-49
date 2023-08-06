#  _Tag.py
#  Copyright (C) 2019 University of Waikato, Hamilton, New Zealand
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


def Tag(tag: str):
    """
    Decorator that adds the given tag to the decorated function.

    :param tag:     The tag to add to the function.
    """
    def apply_tag(method):
        if not hasattr(method, '__tags'):
            method.__tags = set()
        method.__tags.add(tag)
        return method

    return apply_tag


def has_tag(method, tag: str) -> bool:
    """
    Checks if the given method has the given tag.

    :param method:  The method to check.
    :param tag:     The tag to check for.
    :return:        True if the tag exists on the method,
                    False if not.
    """
    return hasattr(method, '__tags') and tag in method.__tags