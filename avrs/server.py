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
from flask import Flask, render_template, request
import json
import logging

from utils.settings import embed_folder, result_folder, cid, n_reco
from utils.load import *
from utils.reco import *
from utils.chart import *


# Initialization of the Flask App
app = Flask(__name__)


# Index
@app.route('/')
def homepage():
    return render_template('index.html')


# Recommendation homepage
@app.route('/home')
def choose_videos():

    videos = get_videos(load_data(cid, embed_folder))
    result = load_data(cid, result_folder, "_result")
    script, div, cdn_js = plot_clustering(result)
    return render_template('recommendations.html',
                           videos=videos, cid=cid,
                           script=script, div=div,
                           cdn_js=cdn_js)


# Retrieve recommendations (POST method)
@app.route('/get_recommandations', methods=['POST', 'GET'])
def get_recommandations():

    result = load_data(cid, result_folder, "_result")
    script, div, cdn_js = plot_clustering(result)
    # We retrieve the list of vids selected by the user
    input = request.form.getlist("vid")
    vid = input[0]
    # We retrieve the list of video names of the vids selected by the user
    videos = get_videos(load_data(cid, embed_folder))
    name = videos[vid]

    # When the user clicks on submit
    if request.method == 'POST':
        result = load_data(cid, result_folder, "_result")
        recos = get_recos(result, vid, n_reco)

    return render_template('recommendations.html', videos=videos, recos=recos,
                           script=script, div=div,
                           cdn_js=cdn_js, selection=name, cid=cid)


# API: Retrieve recommendations (GET and POST method)
@app.route('/api/hubs/<hubid>/video/<vid>', methods=['POST', 'GET'])
def get_recommandations_by_vid(hubid, vid):
    '''Return up to N associated videos if there are associated videos

    This function takes the video ID and return up to N associated
    videos. N can be defined in config.ini

    :param hubid: The client ID
    :type hubid: str
    :param vid: The video ID
    :type vid: str
    :return: IDs of associated videos.
    :rtype: JSON
    '''
    result = load_data(hubid, result_folder, "_result")
    global n_reco
    if request.method == 'POST':
        option = json.loads(request.data)
        n_reco = option['n_reco']

    return json.dumps(dict(enumerate(get_recos(result, vid, n_reco))))


# API: Update model with new record (POST method)
@app.route('/api/hubs/<hubid>/video', methods=['POST'])
def update_video(hubid):
    '''Update new video to video content data as well as clustering result.

    This function takes a record of new video in JSON format. Parsing the
    result and appending the new record into embeddings database. With the
    updated embeddings database, new clustering result will be generated.
    The result from database will be updated.

    :param hubid: The client ID
    :type hubid: str
    :return: A dictionary of client ID and response code.
    :rtype: JSON
    '''
    logging.info("Load JSON...............")
    data = json.loads(request.data)
    one_video = video_json_to_df(data)
    logging.info("The data has been extracted from JSON.")
    logging.info("Parsing video content...")
    one_video = parse_video_content(one_video)
    # Update the client data
    updated_df = insert_video(one_video, hubid)
    update_json(updated_df, hubid, embed_folder)
    logging.info("The video content data has been updated.")
    # Update the clustering result
    result = update_clustering_result(updated_df)
    update_json(result, hubid, result_folder, "_result")
    logging.info("The video clustering result has been updated.")
    return {'hubid': hubid, 'response': 200}


# API: Update model with new settings (POST method)
@app.route('/api/hubs/<hubid>/settings', methods=['POST'])
def update_model(hubid):
    '''Update clustering result by changing the model settings.

    This function takes a config file in JSON format. Parsing the
    file and regenerating new clustering result and update
    the database.

    :param hubid: The client ID
    :type hubid: str
    :return: Clustering result from new settings.
    :rtype: JSON
    '''
    logging.info("Load JSON...............")
    new_settings = json.loads(request.data)
    for set_key, set_val in new_settings.items():
        logging.info(f'The {set_key} will be chage to {set_val}.')
    embed_data = load_data(hubid, embed_folder)
    result = update_clustering_result(embed_data, new_settings)
    update_json(result, hubid, result_folder, "_result")
    logging.info("The video clustering result has been updated.")
    return result.to_json(orient='table')


# API: Retrieve plotting data (GET method)
@app.route('/api/hubs/<hubid>/clustering', methods=['GET'])
def get_chart_table(hubid):
    '''Return data points and label information for plotting

    Take the Client ID and return the plotting information
    on clustering result

    :param hubid: The client ID
    :type hubid: str
    :return: DataFrame in JSON object
    :rtype: JSON
    '''
    return load_data(hubid, result_folder, "_result").to_json(orient='table')
