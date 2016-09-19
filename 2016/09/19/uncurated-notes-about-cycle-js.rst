==================================
 Non-curated notes about Cycle.js
==================================

In the past few days I have been reading about Reactive Programming.  Mostly
about how it's done with `cycle.js`_.  As the title attempts to suggest, this
post is by no means an account of well thought ideas, but my first ideas and
notes while reading about it.

`Cycle.js`_ is attractive, and its appeal spans from two key properties in my
opinion:

- There's a single type of connector between the components: the streams.

  .. note:: Both ``sources`` and ``sinks`` return streams.

- There are two distinct type of computational components: the drivers and the
  the ``main(sources)`` function.

  .. note:: Intent, view and model functions may be regarded as internal
	    structure of ``main()``.

This is appealing because the architecture is simple.  You may understand the
main points of this architecture in about an hour.  You may recall this is
actually an evolution (or instance) of the producer-consumer pattern.

There's a third element in `cycle.js`_: the cycle itself.  Which is based on
the 'dialog abstraction'.  Actually, this is what caught my attention in the
first place.  It goes like: your program outputs are the input to an external
(possibly human) entity which, in turn, may react and produce more events in
your program's source streams.

Architecturally this is simple and good.


Components
==========

   Any Cycle.js app can be reused as a component in a larger Cycle.js app.

   -- From the Cycle.js documentation

When it comes to designing an application or component you have to decide
about the type of events your application may receive and the expected output
events it may produce in response.

The previous statement is only true in two cases:

- Your 'smaller' Cycle.js application does not need to interact with other
  parts of your 'larger' application.

- Your 'smaller' Cycle.js exposes its model; or you have "model drivers".

I think this becomes rather obvious in the 16th part of the Egghead's video
series on Cycle.js.  The one when they make the slider component and they need
to expose the stream of 'values' from the slider.

.. note:: Actually the documentation states that components expose, somehow,
   its state.


Streams to the extreme (and localization)
-----------------------------------------

The Egghead's series exposes how Cycle.js became to be and you can, therefore,
see the evolution it is.  Is a short video series worth watching: right to the
point without many detours.

There's a video when they needed to make a component out of the Height and
Weight sliders, and they needed to pass parameters like the label, min value
and max value. I thought they were going to use old plain closures::

  function Slider(sources, props) {
      const label = props.label;
      // etc...
      return main(sources);
  }

It came as a surprise that they put those parameters into a ``props``
**source** to the ``main()`` function of the component.

At first I thought that was really far fetched, but after thinking about it a
bit more I think is can be really useful.

I started to think about an application with just a slider and a language
selector::


   Height: 6 feet   <-----o-->

   Choose language: [ENG]


The slider component is the one we see in the video series.  The language
selector is a selection component and the expected behavior is that when I
change the language the *entire application* changes to the new language.

My first thought is that the language selector gets is value from a driver
(which I don't know if it already exists) that deals with localization.  Let's
say you can obtain such a driver like this::

  cycle.run(main, {
     // etc...
     locale: makeLocaleDriver({languages: ['en_US', 'es_ES'], ...})
  })


The driver would let you respond to changes in translations::

  const label$ = sources.locale.select('Height');


Or combining with another mapping from another stream so that the ``props``
stream remains almost unchanged::

  const label$ = props$.map(p => sources.locale.select(p.label));


However, after revisiting that last idea, I noticed that it doesn't work.  A
change in in the locale does not trigger any event in the ``props$`` stream.
Assuming that ``locale.current$`` is a stream of localization object, this may
work::

  const label$ = props$.combine(sources.locale.current$)
                       .map((label, locale) => locale.gettext(label));


The thing gets a little bit more tricky when it comes to changing the units:
feet vs meter, etc...  I've been thinking about it for a bit.  The most
problematic issue is that state is not clearly owned unless we introduce a
kind of *quantity* for which the unit of measure is explicit::

  run(main, {
      props: xs.of({
         value: new Quantity(175, Unit.Length.cm),
      })
  })


However this may seem a bit overreaching for a single *value* that only needs
to be in between two boundaries (slider).

This is, IMO the breaking point: If I really need to manage units on my
application and those need to be fully localized, my components might be
regarded as over-engineered for other apps.  My only hope is that a simple
slider, without any knowledge of units, might be wrapped inside a
`FullyLocalizedSlider` for that purpose.


Open questions
==============

Most of the ideas exposed above are not battle tested.  I happen to be
evaluating whether I could use `Cycle.js`_ inside Odoo to develop some widgets
that require almost real-times updates, and the stream interface is thus quite
natural.

There are challenges about integrating my components with the rest of the
application, and being an application that must display at least three
languages I need to think on advance about the problems I would face.


.. categories:: Programming
.. tags:: UI, Thought


.. _cycle.js: http://cycle.js.org/
