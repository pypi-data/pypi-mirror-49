.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

The following sections detail a variety of ways to contribute, as well as how to get started.

Types of Contributions
----------------------

Write Documentation
~~~~~~~~~~~~~~~~~~~

``pyjanitor`` could always use more documentation, whether as part of the
official pyjanitor docs, in docstrings, or the examples gallery.

During sprints, we require newcomers to the project to first contribute a
documentation fix before contributing a code fix. Doing so has numerous benefits:

1. You become familiar with the project by first reading through the docs.
2. Your documentation contribution will be a pain point that you have full context on.
3. Your contribution will be impactful because documentation is the project's front-facing interface.
4. Your first contribution will be simpler, because you won't have to wrestle with build systems.
5. You can choose between getting set up locally first (recommended), or instead directly making edits on the GitHub web UI (also not a problem).
6. Every newcomer is equal in our eyes, and it's the most egalitarian way to get started (regardless of experience).

Remote contributors outside of sprints and prior contributors who are joining
us at the sprints need not adhere to this rule, as a good prior
assumption is that you are a motivated user of the library already. If you have
made a prior pull request to the library, we would like to encourage you to mentor newcomers
in lieu of coding contributions.

Documentation can come in many forms. For example, you might want to contribute:

- Fixes for a typographical, grammatical, or spelling error.
- Changes for a docstring that was unclear.
- Clarifications for installation/setup instructions that are unclear.
- Corrections to a sentence/phrase/word choice that didn't make sense.
- New example/tutorial notebooks using the library.
- Edits to existing tutorial notebooks with better code style.

In particular, contributing new tutorial notebooks and improving the clarity of existing ones
are great ways to get familiar with the library and find pain points that you can
propose as fixes or enhancements to the library.

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/ericmjl/pyjanitor/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with ``bug``
and ``available to hack on`` is open to whoever wants to implement it.

Do be sure to claim the issue for yourself by indicating, "I would like to
work on this issue." If you would like to discuss it further before going forward,
you are more than welcome to discuss on the GitHub issue tracker.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with ``enhancement``
and ``available to hack on`` are open to whoever wants to implement it.

Implementing a feature generally means writing a function that has the
following form:

.. code-block:: python

    @pf.register_dataframe_method
    def function(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        """
        Very detailed docstring here. Look to other functions for examples.
        """
        # stuff done here
        return df

The function signature should take a pandas ``DataFrame`` as the input and return
a pandas ``DataFrame`` as the output. Any manipulation to the dataframe should be
implemented inside the function. The standard functionality of ``pyjanitor`` methods that we're moving towards is to not modify the input ``DataFrame``.

This function should be implemented in ``functions.py``, and it should have a test
accompanying it in ``tests/functions/test_<function_name_here>.py``.

When writing a test, the minimum acceptable test is an "example-based test."
Under ``tests/conf.py`` you will find a suite of example dataframes that can be
imported and used in the test.

If you are more experienced with testing, you can use `Hypothesis <https://hypothesis.readthedocs.io/en/latest/>`_ to
automatically generate example dataframes. We provide a number of
dataframe-generating strategies in ``janitor.testing_utils.strategies``.

We may go back-and-forth a few times on the docstring. The docstring is a very
important part of developer documentation; therefore, we may want much more detail than
you are used to providing. This is for maintenance purposes: Contributions from new contributors
frequently end up being maintained by the maintainers, and hence we would err on the side of
providing more contextual information than less, especially regarding design choices.

If you're wondering why we don't have to implement the method chaining
portion, it's because we use the ``register_dataframe_method`` from ``pandas-flavor``,
which registers the function as a pandas dataframe method.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/ericmjl/pyjanitor/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to setup ``pyjanitor`` for local development.

1. Fork the ``pyjanitor`` repo on GitHub: https://github.com/ericmjl/pyjanitor.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pyjanitor.git

3. Install your local copy into a conda environment. Assuming you have conda installed, this is how you set up your fork for local development::

    $ cd pyjanitor/
    $ make install

This also installs your new conda environment as a Jupyter-accessible kernel. To run correctly inside the environment, make sure you select the correct kernel from the top right corner of JupyterLab!

If you are on Windows, you likely need to install ``make`` before you can run the install. You can get it from ``conda-forge``::

    $ conda install -c defaults -c conda-forge make

4. You should also be able to build the docs locally. To do this, from the main ``pyjanitor`` directory::

    $ make docs

The above command allows you to view the documentation locally in your browser. `Sphinx (a python documentation generator) <http://www.sphinx-doc.org/en/stable/usage/quickstart.html>`_ builds and renders the html for you, and you can find the html files by navigating to ``pyjanitor/docs/_build``, and then you can find the correct html file. To see the main pyjanitor page, open the ``index.html`` file.

Sphinx uses `rst files (restructured text) <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ as its markdown language. To edit documentation, go to the rst file that corresponds to the html file you would like to edit. Make the changes directly in the rst file with the correct markup. Save the file, and rebuild the html pages using the same commands as above to see what your changes look like in html.

5. Submit an issue to the ``pyjanitor`` GitHub issue tracker describing your planned changes: https://github.com/ericmjl/pyjanitor/issues

This helps us keep track of who is working on what.

6. Create a branch for local development:

New features added to ``pyjanitor`` should be done in a new branch you have based off of the latest version of the ``dev`` branch. The protocol for ``pyjanitor`` branches for new development is that the ``master`` branch mirrors the current version of ``pyjanitor`` on PyPI, whereas the ``dev`` branch is for additional features for an eventual new official version of the package which might be deemed slightly less stable. Once more confident in the reliability/suitability for introducing a batch of changes into the official version, the ``dev`` branch is then merged into ``master`` and the PyPI package is subsequently updated.

To base a branch directly off of ``dev`` instead of ``master``, create a new one as follows::

    $ git checkout -b name-of-your-bugfix-or-feature dev

Now you can make your changes locally.

7. When you're done making changes, check that your changes are properly formatted and that all tests still pass::

    $ make check

If any of the checks fail, you can apply any of them individually (to save time):

* Automated code formatting: ``make style``
* Code styling problems check: ``make lint``
* Code unit testing: ``make test``

Styling problems must be resolved before the pull request can be accepted.

``make test`` runs all of ``pyjanitor``'s unit tests to probe for whether changes to the source code have potentially introduced bugs. These tests must also pass before the pull request is accepted.

All of these commands are available when you create the development environment.

When you run the test locally, the tests in ``chemistry.py`` & ``biology.py`` are automatically skipped if you don't have the optional dependencies (e.g. ``rdkit``) installed.

7. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website. When you are picking out which branch to merge into, be sure to select ``dev`` (not ``master``).


PyCharm Users
~~~~~~~~~~~~~

Currently, PyCharm doesn't support the generation of Conda environments via a
YAML file as prescribed above. To get around this issue, you need to setup
your environment as described above, and then within PyCharm point your interpreter
to the predefined conda environment.

1. Complete steps 1-3 under the Getting Started section.
2. Determine the location of the newly-created conda environment::

    conda info --env

3. Open up the location of the cloned pyjanitor directory in PyCharm.
4. Navigate to the Preferences location.

    .. image:: /images/preferences.png

5. Navigate to the Project Interpreter tab.

    .. image:: /images/project_interpreter.png

6. Click the cog at the top right and select Add.

    .. image:: /images/click_add.png

7. Select Conda Environment on the left and then select existing environment. Click
on the three dots, copy the location of your newly-created conda environment,
and append bin/python to the end of the path.

    .. image:: /images/add_env.png

Click OK and you should be good to go!


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.

Tips
----

To run a subset of tests::

    $ py.test tests.test_functions
