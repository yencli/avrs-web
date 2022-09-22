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
import pandas as pd
import numpy as np

import glob
import os

from utils.settings import datapath, nlp_model, autoencoder, embed_folder


def load_data(cid, folder, result=""):
    '''Load embedded content or pre-generated clustering result'''
    jsonfile = cid + result + '.json'
    df = pd.read_json(os.path.join(datapath, folder, jsonfile))
    df.videoId = df.videoId.astype("string")
    if result:
        df.label = df.label.astype("string")
    return df


def get_videos(df):
    '''Retrive names and ID of all videos from a hub'''
    return {d['videoId']: d['title'] for d in df.to_dict(orient='records')}


def process_text(text):
    '''Takes a document, return lemmatized nouns'''
    import spacy
    nlp = spacy.load(nlp_model)
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.pos_ not in ['NOUN', 'PROPN']:
            continue
        result.append(token.lemma_)
    return " ".join(result)


def parse_video_content(v_df):
    '''Parsing the content of a new video'''
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(autoencoder)
    v_df['content'] = v_df['content'].apply(process_text)
    v_df['embeddings'] = v_df['content'].apply(model.encode)
    return v_df


def insert_video(v_df, cid):
    '''Appends datum of new video to Dataframe'''
    jsonfile = cid + '.json'
    v_df.drop(['hubId', 'content'], axis=1, inplace=True)
    if glob.glob(os.path.join(datapath, embed_folder, jsonfile)):
        df = load_data(cid, embed_folder)
        return pd.concat([df, v_df], ignore_index=True)
    else:
        return v_df


def video_json_to_df(jsondata):
    '''Takes a JSON file and return a DataFrame'''
    df = pd.json_normalize(jsondata)
    df = df.replace(np.nan, "", regex=True)
    df.hubId = df.hubId.astype("string")
    df['content'] = df['title'] + " " + df['description'] + \
        " " + df['text'] + " " + df['tags'].apply(
        lambda x: " ".join([t.split(":")[1] for t in x]))
    df['tags'].replace('', '[]', inplace=True)
    df = df[['hubId', 'videoId', 'title', 'content', 'tags']]
    return df


def update_json(df, cid, folder, result=""):
    '''Write Dataframe to JSON'''
    jsonfile = cid + result + '.json'
    df.to_json(os.path.join(datapath, folder, jsonfile))
