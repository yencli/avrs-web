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
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import turbo
from bokeh.transform import factor_cmap

from bokeh.models import HoverTool


def plot_clustering(result):
    '''This function produce an interactive map of video contents'''
    # Create figure object.
    p = figure(title='Videos Clustered by contents',
               plot_height=400,
               plot_width=650,
               toolbar_location='below',
               tools="pan, wheel_zoom, box_zoom, reset")
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.outline_line_color = None
    # Add patch renderer to figure.

    outliers = result.loc[result.label == '-1', :]
    clustered = result.loc[result.label != '-1', :]
    labels = result['label'].nunique()

    label_cmap = factor_cmap('labels', palette=turbo(labels),
                             factors=sorted(clustered.label.unique()))

    videos = ColumnDataSource(data=dict(xc=clustered.x, yc=clustered.y,
                                        labels=clustered.label,
                                        vid=clustered.videoId,
                                        title=clustered.title))

    videos = p.scatter(x="xc", y="yc", fill_color=label_cmap, size=10,
                       fill_alpha=0.5, line_color=label_cmap, source=videos)

    outlier = ColumnDataSource(data=dict(x=outliers.x, y=outliers.y,
                                         labels=outliers.label,
                                         vid=outliers.videoId,
                                         title=outliers.title))

    outlier = p.scatter(x="x", y="y", fill_color="gray", line_color="white",
                        size=10, fill_alpha=0.5, hover_color="red",
                        marker="circle_x", source=outlier)

    # Create hover tool
    p.add_tools(HoverTool(renderers=[videos, outlier],
                          tooltips=[('title', '@title')]))
    script, div = components(p)
    return (script, div, CDN.js_files[0])
