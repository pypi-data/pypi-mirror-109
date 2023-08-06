#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""ebookatty __main__ CLI interface."""


########################################################################
#  Copyright (C) 2021  alexpdev
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#########################################################################


from argparse import ArgumentParser
from ebookatty.atty import get_metadata

if __name__ == "__main__":
    parser = ArgumentParser(description="get ebook metadata")

    parser.add_argument('path', type=str,help='path to ebook file')
    args = parser.parse_args()
    print(get_metadata(args.path))
