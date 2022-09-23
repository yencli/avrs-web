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
import numpy as np
import pandas as pd

import umap
import hdbscan

from utils.settings import n_neighbors, n_components, min_cluster_size


def add_tags(df):
    embeddings = np.array(list(df['embeddings']))
    tags = df['tags'].str.get_dummies(', ').to_numpy()
    return np.concatenate((embeddings, tags), axis=1)


def reduce_embeddings(embeddings, n_c, n_n, min_dist=0.1):
    return umap.UMAP(n_neighbors=n_n,
                     n_components=n_c,
                     min_dist=min_dist,
                     metric='cosine').fit_transform(embeddings)


def clustering(umap_embeddings, m):
    return hdbscan.HDBSCAN(min_cluster_size=m,
                           metric='euclidean',
                           cluster_selection_method='eom').fit(umap_embeddings)


def update_clustering_result(data, settings={
        "n_neighbors": n_neighbors,
        "n_components": n_components,
        "min_cluster_size": min_cluster_size}):
    n_n = settings['n_neighbors']
    n_c = settings['n_components']
    m = settings['min_cluster_size']
    if len(data) <= 3:
        data = pd.concat([data] * 4, ignore_index=True)
    embeddings_tags = add_tags(data)
    umap_embeddings = reduce_embeddings(
                    embeddings_tags, min(len(data) - 2, n_c), n_n)
    cluster = clustering(umap_embeddings, m)
    umap_data = reduce_embeddings(embeddings_tags, 2, n_n, 0.0)
    result = pd.DataFrame(umap_data, columns=['x', 'y'])
    result['label'] = cluster.labels_
    result[['videoId', 'title']] = data[['videoId', 'title']]
    return result[['videoId', 'title', 'x', 'y', 'label']]


def get_recos(df, vid, n_recos):
    target_label = df.loc[df.videoId == vid, 'label'].values[0]
    result_df = df[df['label'] == target_label]['videoId'].drop(
               df[df.videoId == vid].index).sample(n_recos, replace=True)
    return pd.unique(result_df)
