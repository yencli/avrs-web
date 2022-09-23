# -*- coding: utf-8 -*-
#
# This file is part of avrs Associated Video Recommendation System
#
# Developed for ioga.app.
# This product includes software developed by the Yen C. Li
# (https://github.com/yencli/avrs-web).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
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
#
import configparser
import os
import subprocess
import re

# Import config file
cwd = os.getcwd()
maindir = re.split('avrs-web', cwd)[0]
maindir = ''.join([maindir, 'avrs-web'])
os.chdir(maindir)
configpath = os.path.join('avrs', 'config.ini')

config = configparser.ConfigParser()
config.read(configpath)

# Add exemple data to config
config['DB Paths']['DATA_DIR'] = "./tests/samples"
config['avrs-web']['cid'] = "839038621007740928"

with open(configpath, 'w') as configfile:
    config.write(configfile)

# Run the app avrs-web
mainfile = 'python ' + os.path.join(cwd, 'avrs', 'main.py')
subprocess.run(mainfile, shell=True)
