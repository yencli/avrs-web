Cookbook
========= 

AVRS help you find associated videos by ID, let's walk through on what
AVRS can do for you.  

Run the app
--------------

The most simple way to see how program is like is to run with our demo data:
::

    python tests/run_app.py


Or you may choose to run with your own data. Please indicate the location of
your data by completing the section [DB Paths] under config.ini

Please specify the location of embedding data and clustering data if they are
in diffrent folder.

.. code-block:: yaml
   :linenos:

    [DB Paths]
    DATA_DIR: [Path to data file]
    EMBED_FOLDER: [Embedding data folder]
    RESULT_FOLDER: [Clustering data folder]

The embedding data should be a JSON format file containing the following keys:
* videoId
* title
* tags
* embeddings
It should look like this:

.. code-block:: javascript
   :linenos:

    {
        "videoId": {"0":"987654321","1":"876543219"},
        "title": {"0":"title1","1":"title2"},
        "tags": {"0":"[]","1":"["tag1","tag2"]"},
        "embeddings": {"0":[...],"1":[...]},
    }

However, the script that transform the existing video data to embedding data is not
included in this app due to the fact that this program is designed specificly for
the purpose to use in ioga.app Only the insertion of new record method has been kept
in api. You may create your own data as per instructions :ref:`2. Update models`.

Since AVRS is designed specificly for ioga.app the records are grouped by client and
named by client ID. eg. 6234567890123.json, 72345678901.json...

Once you have your embedding data, the clustering data is generated accordingly if you
generate your data with avrs api. The files are named with [Client ID]_result.json 
eg. 6234567890123_result.json, 72345678901_result.json...

Oh right, now you have every data you need you may simply run:
::

    python main.py 

To visualize the app, type the address and the port displayed as you run the app
under the browser of your choice. eg. https://localhost:5000

Make http request to AVRS API
-----------------------------

The AVRS-web app part is simply made for demo purpose. The main usage of AVRS-web is
via AVRS API. You may choose your favorite HTTP request tool eg. curl, postman... to
make request.

As mentioned in :ref:`AVRS Python API`. There are four main usages provided
in AVRS:

1. Get IDs of associated videos by one video ID
++++++++++++++++++++++++++++++++++++++++++++++++

.. py:function:: get_recommandations_by_vid(hubid, vid)

Make a GET request by indicate the client ID (Hub ID) and video ID.
It shoud look like this:

::

    GET [SERVER_ADDRESS]/api/hubs/[Hub ID]/video/[Video ID]

eg.
::

    GET https://localhost:5000/api/hubs/67201997558/video/67233338359

This will return associated video IDs in JSON format like this:

.. code-block:: javascript
   :linenos:

    {
        "0": "751352883781304320", 
        "1": "672020501882732544"
    }


The maximun number of associated videos(there will be less if there are not
enough associated videos) to display can be define in congif.ini by changing
"n_reco" (default = 4). However, you may also change this setting simply by
making a POST request instead of GET and include this JSON in the body:

.. code-block:: javascript
   :linenos:

    { "n_reco": 6 }


2. Update models
++++++++++++++++++

This can be done with two methods:

    * By adding a new video.

.. py:function:: update_video(hubid)

The data should look like the following example that contains the fields below:

.. code-block:: javascript
   :linenos:

    {
        "videoId": "1020337500092104704",
        "title": "10193779",
        "hubId": "922392682985160704",
        "description": "FEL",
        "text":"un, deux trois Je vais dans les bois quatre cinq six Je sors ma scie",
        "tags": [
                    "990875315418955776:2",
                    "- >2h Cause connue, délai maîtrisé"
                ]
    }


Only the "description", "text"(the transcription obtained from video) and "tags"
can be empty. The fields "hubId", "videoId" and "title" must contain value. AVRS
is multilingual so no worries.

Your POST request should look like this:

::

    POST [SERVER_ADDRESS]/api/hubs/[Hub ID]/video/

eg.
::

    POST https://localhost:5000/api/hubs/67201997558/video/

And the video data to insert is contain in the body of request. This request will
update the embedding data as well as the clustering model.

You may also update the model:

    * By changing output settings.

.. py:function:: update_model(hubid)

The request will use POST method and it will look like:

::

    POST [SERVER_ADDRESS]/api/hubs/[Hub ID]/video/

eg.
::

    POST https://localhost:5000/api/hubs/67201997558/settings/


The output settings contains three variables: 

        * n_neighbors
        * n_components
        * min_cluster_size

"n_neighbors" define how local or how global the structure the model
should emphasis on. 
See `UMAP <https://umap-learn.readthedocs.io/en/latest/parameters.html#n-neighbors>`_
for furthur details.

"n_components" are the final dimension after reducing from the original dimention(512).

"min_cluster_size" defines at least how many videos that share some common points should
there be to be considered as a group insdead of outliner.
See `HDBSCAN <https://hdbscan.readthedocs.io/en/latest/parameter_selection.html#selecting-min-cluster-size>`_
for furthur details.

Therefore the JSON to put in the body of request should look like:

.. code-block:: javascript
   :linenos:

    {
        "n_neighbors": 5,
        "n_components": 20,
        "min_cluster_size": 3
    }


This request will update the model and save the new model to [client ID]_result.json

3. Retrieve plotting data
++++++++++++++++++++++++++

The plotting data that you may use for your own demostration like displayed
in the AVRS-web app can be retrieve via this GET request:
.. py:function:: get_chart_table(hubid)

It shoud look like this:

::

    GET [SERVER_ADDRESS]/api/hubs/[Hub ID]/clustering

eg.
::

    GET https://localhost:5000/api/hubs/67201997558/clustering

This will return a JSON file like this:

.. code-block:: javascript
   :linenos:

    {
        "schema":
        {
            "fields":
                [
                    {"name":"index","type":"integer"},
                    {"name":"videoId","type":"any","extDtype":"string"},
                    {"name":"title","type":"string"},
                    {"name":"x","type":"number"},
                    {"name":"y","type":"number"},
                    {"name":"label","type":"integer"}
                ],
            "primaryKey":["index"],
            "pandas_version":"x.y.z"},
            "data":[
                    {
                        "index":0,"videoId":"751352883781304320",
                        "title":"test dnd",
                        "x":-5.9736323357,
                        "y":-4.7278847694,
                        "label":-1
                    },
                    {
                        "index":1,
                        "videoId":"751345947757248512",
                        "title":"test upload",
                        "x":-5.4844770432,
                        "y":-4.1368937492,
                        "label":-1}
                    ]
    }

With the "videoId", "x", "y" and "label", you can easily plotting
a chart of your own style to visualizing the clustering result.
 
