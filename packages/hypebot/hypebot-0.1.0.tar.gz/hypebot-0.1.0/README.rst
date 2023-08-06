hypebot
=================

.. image:: https://badge.fury.io/py/hypebot.png
    :target: https://badge.fury.io/py/hypebot

.. image:: https://travis-ci.org/narfman0/hypebot.png?branch=master
    :target: https://travis-ci.org/narfman0/hypebot

YEAAAAAAAAAAH BOIIIIIIIIIIIIIIIIIIIIIIIIII

Prepare for a whole bucket of hype from those that know humans best: computers
	
Twitch bot to connect to twitch/livesplit and post status updates via twitter
and spam everywhichwhere via <math> and <computers> and <retro>

Purpose
-------

Creating content is hard, and dealing with people is harder. Let's let the
robots handle this; they are better at it anyways and amazing communicators.

We shall teach the bot to speak the way you speak by ingesting a corpus of your
words, thus being able to emulate the way you talk by markov chains.

We shall solve having to use twitter by making the bot post updates instead of
having to lug yourself all the way to another [social media] website and wick
off a piece of your soul to the data mongers.

We shall confirm to our followers that indeed, the -10 second pace you see in
chat is real, and that yes you should watch xxtra closely.

Install
-------

Install and configure python3 with pip, then::

	pip install hypebot

Usage
-----

Set the python twitter api environment variables::

	TWITTER_CONSUMER_KEY
	TWITTER_CONSUMER_SECRET
	TWITTER_ACCESS_TOKEN
	TWITTER_ACCESS_SECRET
	
Configure LiveSplit.Server for your livesplit. You could use environment
variables `LIVESPLIT_HOST` and `LIVESPLIT_PASS` to configure how to connect to
livesplit server.

Examples
--------

Super Mario Brothers 3 (because of course) warpless. Say you have, I dunno, a
43:29.3 p.b. pace coming out of world 7. If you are ahead of that pace by 5
seconds, you might want to blast that out to all "your" "loyal" "followers".
DO NOT FRET. THIS IS A THING THIS BOT DOES. YOU DO NOT HAVE TO LOG ON TO
TWITTER. LET SIGHS OF RELIEF COMMENCE.

The bot will, using the magic of argument configuration, allow the user to
declare trigger/actions. When, e.g. smb3/warpless%/world7 delta-5s is hit,
perform the action of tweet blasting some markov chain inspired hype.

To set up the bot to watch for world 7 exit, and include your name in tweet,
run::

	hypebot narfman0 7

TODO
====

* markovify. the real irony would be if we ingest the corpus from your twitter
account itself. i might do it just for mad inception points.

Note: for now we just pass in username and split index to watch for. We may
extend in the future.

License
-------

Copyright (c) 2019 Jon Robison

See included LICENSE for licensing information