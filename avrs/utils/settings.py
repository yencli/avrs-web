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
import re

cwd = os.getcwd()
maindir = re.split('avrs-web', cwd)[0]
maindir = ''.join([maindir, 'avrs-web'])
os.chdir(maindir)
configpath = os.path.join('avrs', 'config.ini')

settings = configparser.ConfigParser()
settings.read(configpath)

host = settings['avrs-web'].get('host')
port = settings['avrs-web'].getint('port')
debug = settings['avrs-web'].getboolean('debug')

cid = settings['avrs-web'].get('cid')
n_reco = settings['Output Settings'].getint('n_reco')

nlp_model = settings['Models'].get('NLP_MODEL')
autoencoder = settings['Models'].get('AUTOENCODER')

datapath = settings['DB Paths'].get('DATA_DIR')
embed_folder = settings['DB Paths'].get('EMBED_FOLDER')
result_folder = settings['DB Paths'].get('RESULT_FOLDER')

n_neighbors = settings['Output Settings'].getint('n_neighbors')
n_components = settings['Output Settings'].getint('n_components')
min_cluster_size = settings['Output Settings'].getint('min_cluster_size')
