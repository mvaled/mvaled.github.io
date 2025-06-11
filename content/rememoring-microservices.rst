Memento: microservices
======================

:date: 2015-04-08
:category: architecture
:tags: memento
:slug: rememoring-microservices

Lately there's been a raise of the debate about Microservices architectures.
Reading about the stuff I realized I did once architect an application called
Pyxel based on the same principles, though different.

Pyxel reached only its first prototype and was never actually deployed.  I'd
say it wasn't given the chance to prove itself.  So I argue it was technically
sound and, although only a prototype and thus needing improvements, it would
have meet its stated requirements [#disagreement]_.

I haven't been given permission to freely distribute the source code.  But the
architecture was published in several public events, so I can freely describe
it here.

Pyxel
-----

Pyxel's goal was simple:

  Be a shared repository of photographs for the news media that wish to
  collaborate.

Pyxel required that images were tagged with IPTC metadata before uploading.
Upon upload, the image went through several processes for extracting the
metadata, and for producing web-friendly versions [#retina]_ for several
standard dimensions before being published.

On the technical side we have also very hard constraints:

- the system would have to be highly accessible.
- it should run on spare machines; introducing a new machine to replace an old
  one should be possible with minimal interruption.

This constraints were the main driver that lead us to design what we called a
distributed system.  Each major component was designed to run in isolation of
the rest.

Pyxel was split in several processes:

- An image queue holding new images.  This was kind of a FIFO queue over the
  network.

- A catalog holding indexes for retrieving images based of queries.  Queries
  were defined a syntax allowing from very simple queries aided with pattern
  recognition (PR) of names and dates, to very specific queries that make the
  PR mostly unused.

- A "feature" index.  This basically allowed to find similar images.  There
  were two indexes, one based on Hu moments and the other based on wavelets.

- Several image processing nodes, that take images from the queue and:

  - Extract IPTC metadata and put it the catalog

  - Extract image features to allow detection of similar images.

  - Produce "web versions" for the image.  We always kept the original file,
    but to keep the design of the prototype simple there was an "as-is web
    version" that simply returned the same file as the input.

- A web application that communicates with the index and the catalogs.

- An FTP server that injects images to the queue using a FUSE mount point
  (drag-and-drop to the browser wasn't common yet).

That were the main components and all of them ran independently.  Of course
for some services to perform at 100%, they required others to be working.  The
web application would not be able to perform a search if the catalog was down,
or to upload new images if the queue was out of reach.


The principles stand
--------------------

Microservices are "a take" on the same old issue about software composition.
Conceptually Parnas_ still rules: must do modules.  Names have changed and
several rules to build better modules (components, services, etc) have been
provided.

Exposition of the modules as services have also been promoted.

In the web, the modules have drifted away from the server into the client.


Microservices and Pyxel
-----------------------

Pyxel was not actually a microservice architecture as it is understood now.
Deep down it used a central name-server that matched services names to network
endpoints.  We used Pyro_ for this prototype.

We did recognize that this was an *accidental* choice, a matter of convenience
to have the prototype working as soon as possible.

We chose Pyro to test our prototype not to keep it forever if it performed
poorly.  And though our first tests were positive there was some slowness.

To accommodate for a possible replacement of Pyro we chose to provide our own
"idiom" (in Python) to connect and communicate with services:

.. code-block:: python

  with service('pyxel.queue') as queue
      queue.method(*arguments)

That pattern was designed to have an appearance as simple as RPC.  Later we
found that `RPC was under fire`_, but the project was being shut down, so we
didn't fix that.

Under current views Pyxel needs several changes.  I can think of a couple:

- Probably exposing the queue to the client-side of the web application
  instead sending the images first to the server-side of the web application.

- Extract the user registration, authentication and authorization into a
  service.


Notes
-----

.. [#disagreement] Actually one of the main causes of Pyxel being a failure
   was I could not make all participants agreed on the requirements.


.. [#retina] Current retina displays would make that thumbnails look like
   icons and bandwidth is also more likely to allow very big pictures to be
   friendly.


.. _RPC was under fire: `RPC under fire`_
.. _Pyro: https://pypi.python.org/Pyro
.. _Parnas: https://www.cs.umd.edu/class/spring2003/cmsc838p/Design/criteria.pdf
.. _RPC under fire: http://steve.vinoski.net/pdf/IEEE-RPC_Under_Fire.pdf
