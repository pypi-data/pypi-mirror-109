pyepisodate
===========

A python wrapper for the `EpisoDate
API <https://www.episodate.com/api>`__

Install
-------

``pip install pyepisodate``

Usage
-----

Create an object
~~~~~~~~~~~~~~~~

.. code:: python

   from pyepisodate import pyepisodate
   episodate = pyepisodate()

Methods
~~~~~~~

.. code:: python

   episodate.popular() #returns an array of 20 most popular shows
   episodate.search('toh') # returns an array of shows
   show = episodate.show('the-owl-house') # creates a show object

Display show info
~~~~~~~~~~~~~~~~~

.. code:: python

   show.name # The Owl House 
   show.description # The Owl House follows Luz...
   show.start_date # 2020-01-10
   show.country # US
   show.status # Running
   show.runtime # 30
   show.network # Disney Channel
   show.genres # ['Comedy', 'Children', 'Fantasy']
   show.rating # 9.9032
   show.countdown # dict with next episode
   show.episodes # list with all episodes
