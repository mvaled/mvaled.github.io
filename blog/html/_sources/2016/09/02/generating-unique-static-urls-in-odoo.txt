=======================================
 Generating unique static URLs in Odoo
=======================================

.. categories:: Programming
.. tags:: Odoo


By default Odoo bundles static assets (JS and CSS) within a couple of
files: All CSS files are bundled into a single big CSS file.  The same
happens for JS files.

The URLs of those bundles vary with any change within any of the
included files.  But those files are big.  Therefore changing assets
put some stress in the network and diminish the usefulness of caches.

Since Sep 19th, 2015 we introduced a `patch <merchise-8.0-spdy_>`__ in
Odoo to avoid bundling of static assets when using a SPDY or HTTP/2
proxy like Nginx.

Reportedly, this has worked very good in our case where some users
have slow connections.  However, measuring the logs of a week we see
that about 21% of GET request are assets::

  $ egrep 'GET .*(\.|/)(css|js).* HTTP/' /var/log/nginx/o.access.log.1 | wc -l
  10554

  $ egrep 'GET .* HTTP' /var/log/nginx/o.access.log.1 | wc -l
  50216

Odoo's default cache expiration time is seven days.  This is
considerably low taking into account that bundle's URLs change when
the content does.

Another issue is that assets that change can be served staled from the
caches for seven days.

We're taking the path to produce unique URLs for static assets.  Our
current work can be seen in our `merchise-unique-static-urls`_
branch.  In our development/deployment scenarios these simple changes
would suffice for JS and CSS.  There's still work to do regarding
invalidation of static images in our templates.


.. _merchise-8.0-spdy: https://github.com/merchise-autrement/odoo/commit/03741a2cb81907b4b67ca8437f260b073689d212
.. _merchise-unique-static-urls: https://github.com/merchise-autrement/odoo/tree/merchise-unique-static-urls
