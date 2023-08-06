Rituals
=======

Common tasks for `Invoke <http://www.pyinvoke.org/>`__ that are needed
again and again.

|GINOSAJI| … and again and again.

 |Groups|  |Travis CI|  |Coveralls|  |GitHub Issues|  |License|
 |Development Status|  |Latest Version|

Overview
--------

“Rituals” is a task library for `Invoke <http://www.pyinvoke.org/>`__
that keeps the most common tasks you always need out of your project,
and makes them centrally maintained. This leaves your ``tasks.py`` small
and to the point, with only things specific to the project at hand. The
following lists the common task implementations that the
``rituals.easy`` module offers. See the `full
docs <https://rituals.readthedocs.io/en/latest/usage.html#adding-rituals-to-your-project>`__
on how to integrate them into your ``tasks.py``.

-  ``help`` – Default task, when invoked with no task names.
-  ``clean`` – Perform house-cleaning.
-  ``build`` – Build the project.
-  ``test`` – Perform standard unittests.
-  ``check`` – Perform source code checks.
-  ``release.bump`` – Bump a development version.
-  ``release.dist`` – Distribute the project.
-  ``release.prep`` – Prepare for a release (perform QA checks, and
   switch to non-dev versioning).
-  … and *many* more, see ``inv -l`` for a complete list.

The guiding principle for these tasks is to strictly separate low-level
tasks for building and installing (via ``setup.py``) from high-level
convenience tasks a developer uses (via ``invoke``). Invoke tasks can
use Setuptools ones as building blocks, but never the other way 'round –
this avoids any bootstrapping headaches during package installations.

Use ``inv -h ‹task›`` as usual to get details on the options of these
tasks. Look at the modules in
`acts <https://github.com/jhermann/rituals/blob/master/src/rituals/acts>`__
if you want to know what these tasks do exactly. Also consult the `full
documentation <https://rituals.readthedocs.io/>`__ for a complete
reference.

:bulb: \| The easiest way to get a working project using ``rituals`` is
the
`py-generic-project <https://github.com/Springerle/py-generic-project>`__
cookiecutter archetype. That way you have a working project skeleton
within minutes that is fully equipped, with all aspects of building,
testing, quality checks, continuous integration, documentation, and
releasing covered. ---- \| :----

Some Practical Examples
-----------------------

The following table shows a selection of typical use-cases and how to
carry them out in projects that include *Rituals* in their ``tasks.py``
(e.g. this one).

+--------+--------+
| Comman | Descri |
| d      | ption  |
+========+========+
| ``inv  | Start  |
| docs - | a      |
| w -b`` | ``sphi |
|        | nx-aut |
|        | obuild |
|        | ``     |
|        | watchd |
|        | og     |
|        | and    |
|        | open   |
|        | the    |
|        | result |
|        | ing    |
|        | live-r |
|        | eload  |
|        | previe |
|        | w      |
|        | in     |
|        | your   |
|        | browse |
|        | r.     |
+--------+--------+
| ``inv  | Run    |
| test.t | ``tox` |
| ox --c | `      |
| lean - | for    |
| e py34 | Python |
| ``     | 3.4    |
|        | with a |
|        | clean  |
|        | status |
|        | ,      |
|        | i.e.   |
|        | an     |
|        | empty  |
|        | ``.tox |
|        | ``     |
|        | direct |
|        | ory.   |
+--------+--------+
| ``inv  | Set    |
| releas | the    |
| e.bump | ``tag_ |
| ``     | build` |
|        | `      |
|        | value  |
|        | in     |
|        | ``setu |
|        | p.cfg` |
|        | `      |
|        | to     |
|        | someth |
|        | ing    |
|        | like   |
|        | ``0.3. |
|        | 0.dev1 |
|        | 17+0.2 |
|        | .0.g99 |
|        | 3edd3. |
|        | 201504 |
|        | 08t174 |
|        | 7``,   |
|        | unique |
|        | ly     |
|        | identi |
|        | fying  |
|        | dev    |
|        | builds |
|        | ,      |
|        | even   |
|        | in     |
|        | dirty  |
|        | workin |
|        | g      |
|        | direct |
|        | ories. |
+--------+--------+

See the `full documentation <https://rituals.readthedocs.io/>`__ for
more examples and a complete reference.

Contributing
------------

To create a working directory for this project, call these commands:

.. code:: sh

    git clone "https://github.com/jhermann/rituals.git"
    cd rituals
    command . .env --yes --develop  # add '--virtualenv /usr/bin/virtualenv' for Python2
    invoke build --docs test check

To use the source in this working directory within another project,
change your current directory to *this* project, then call ``bin/pip``
from *that* project's virtualenv like so:

::

    …/.venv/…/bin/pip install -e .

See
`CONTRIBUTING <https://github.com/jhermann/rituals/blob/master/CONTRIBUTING.md>`__
for more.

|Throughput Graph|

Releasing
---------

This is the process of releasing ``rituals`` itself, projects that use
it will have an identical to very similar sequence of commands.

.. code:: sh

    inv release.prep
    inv release.dist --devpi # local release + tox testing

    git push && git push --tags # … and wait for Travis CI to do its thing

    twine upload -r pypi dist/*

If you have any pending changes, staged or unstaged, you'll get an error
like this:

.. figure:: https://raw.githubusercontent.com/jhermann/rituals/master/docs/_static/img/invoke-release-prep-changes.png
   :alt: uncommitted changes

   uncommitted changes

Related Projects
----------------

-  `Springerle/py-generic-project <https://github.com/Springerle/py-generic-project>`__
   – Cookiecutter template that creates a basic Python project, which
   can be later on augmented with various optional accessories.
-  `pyinvoke/invoke <https://github.com/pyinvoke/invoke>`__ – Task
   execution tool & library.
-  `pyinvoke/invocations <https://github.com/pyinvoke/invocations>`__ –
   A collection of reusable Invoke tasks and task modules.

Acknowledgements
----------------

-  Logo elements from `clker.com Free
   Clipart <http://www.clker.com/>`__.
-  In case you wonder about the logo, `watch
   this <http://youtu.be/9VDvgL58h_Y>`__.

.. |GINOSAJI| image:: https://raw.githubusercontent.com/jhermann/rituals/master/docs/_static/img/symbol-200.png
.. |Groups| image:: https://img.shields.io/badge/Google_groups-rituals--dev-orange.svg
   :target: https://groups.google.com/forum/#!forum/rituals-dev
.. |Travis CI| image:: https://api.travis-ci.org/jhermann/rituals.svg
   :target: https://travis-ci.org/jhermann/rituals
.. |Coveralls| image:: https://img.shields.io/coveralls/jhermann/rituals.svg
   :target: https://coveralls.io/r/jhermann/rituals
.. |GitHub Issues| image:: https://img.shields.io/github/issues/jhermann/rituals.svg
   :target: https://github.com/jhermann/rituals/issues
.. |License| image:: https://img.shields.io/pypi/l/rituals.svg
   :target: https://github.com/jhermann/rituals/blob/master/LICENSE
.. |Development Status| image:: https://img.shields.io/pypi/status/rituals.svg
   :target: https://pypi.python.org/pypi/rituals/
.. |Latest Version| image:: https://img.shields.io/pypi/v/rituals.svg
   :target: https://pypi.python.org/pypi/rituals/
.. |Throughput Graph| image:: https://graphs.waffle.io/jhermann/rituals/throughput.svg
   :target: https://waffle.io/jhermann/rituals/metrics
