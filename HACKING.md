Shredder Code Style Commandments
================================

- Step 1: Read http://www.python.org/dev/peps/pep-0008/
- Step 2: Read http://www.python.org/dev/peps/pep-0008/ again
- Step 3: Read on

General
-------

- Put two newlines between top-level code (funcs, classes, etc)
- Put one newline between methods in classes and anywhere else
- Long lines should be wrapped in parentheses
  in preference to using a backslash for line continuation.
- Do not write "except:", use "except Exception:" at the very least
- Include your name with TODOs as in "#TODO(Your Name Here)"
- Do not shadow a built-in or reserved word. Example::

    def list():
        return [1, 2, 3]

    mylist = list() # BAD, shadows `list` built-in

    class Foo(object):
        def list(self):
            return [1, 2, 3]

    mylist = Foo().list() # OKAY, does not shadow built-in

Imports
-------

- Do not import more than one module per line (*)
- Do not make relative imports
- Order your imports by the full module path
- Organize your imports according to the following template

Example::

    # vim: tabstop=4 shiftwidth=4 softtabstop=4
    {{stdlib imports in human alphabetical order}}
    \n
    {{third-party lib imports in human alphabetical order}}
    \n
    {{treasury imports in human alphabetical order}}
    \n
    \n
    {{begin your code}}

Human Alphabetical Order Examples
---------------------------------

Example::

    import httplib
    import logging
    import random
    import StringIO
    import time
    import unittest
    import workflows

    import shredder.apps.question.models

Docstrings
----------

Example::

    '''A one line docstring looks like this and ends in a period.'''

    '''A multi line docstring has a one-line summary, less than 80 characters.

    Then a new paragraph after a newline that explains in more detail any
    general information about the function, class or method. Example usages
    are also great to have here if it is a complex class for function.

    When writing the docstring for a class, an extra line should be placed
    after the closing quotations. For more in-depth explanations for these
    decisions see http://www.python.org/dev/peps/pep-0257/

    If you are going to describe parameters and return values, use Sphinx, the
    appropriate syntax is as follows.

    :param foo: the foo parameter
    :param bar: the bar parameter
    :returns: return_type -- description of the return value
    :returns: description of the return value
    :raises: AttributeError, KeyError
    '''

Dictionaries/Lists
------------------

If a dictionary (dict) or list object is longer than 80 characters, its items
should be split with newlines. Embedded iterables should have their items
indented. Additionally, the last item in the dictionary should have a trailing
comma. This increases readability and simplifies future diffs.

Example::

  my_dictionary = {
      "data": {
          "name": "jack",
          "age": 27,
          "properties": {
               "user_id": 12,
          },
          "status": "ACTIVE",
      },
  }

Calling Methods
---------------

Calls to methods 80 characters or longer should format each argument with
newlines. This is not a requirement, but a guideline::

    unnecessarily_long_function_name('string one',
                                     'string two',
                                     kwarg1=constants.ACTIVE,
                                     kwarg2=['a', 'b', 'c'])

Rather than constructing parameters inline, it is better to break things up::

    list_of_strings = [
        'what_a_long_string',
        'not as long',
    ]

    dict_of_numbers = {
        'one': 1,
        'two': 2,
        'twenty four': 24,
    }

    object_one.call_a_method('string three',
                             'string four',
                             kwarg1=list_of_strings,
                             kwarg2=dict_of_numbers)

Design
------

Experiences are needed to actually understand how these design principles would
affect how the code would run and evolute, because sometimes the consequences
are subtle.

- Small is beautiful. A function is too long when it reaches over 30 lines, becomes difficult to understand and reuse.
- Use decorators or metaclasses when you want to modify the behavior of a function or class. Decorators and metaclasses are executed at compiling time, it's fast.
- Try not to violate DRY, thought it might still be exceptional. sometimes. Repeating too much would eventually lead to bad design.
- Use builtin types in preferences to self-made types or third-party types. 'collections', 'itertools', and 'functools' are places to look at when you want data-oriented utilities.
- Callables with over 6 parameters would be enough. Too many arguments is an indication that the callable is having too many responsibilities, thus becomes difficult to maintain.
- When you are writing data-iterating processes, always consider iterators or generators. Iterators and generators not only beats loops in performance, but reduces complexities.

Creating Unit Tests
-------------------

For every new feature, unit tests should be created that both test and
(implicitly) document the usage of said feature. If submitting a patch for a
bug that had no unit test, a new passing unit test should be added. If a
submitted bug fix does have a unit test, be sure to add a new one that fails
without the patch and passes with the patch.

Commit Messages
---------------

Using a common format for commit messages will help keep our git history
readable. Follow these guidelines:

- Prefix your commits. Prefixes are used to classify your commits. This is helpful when inspecting git history using 'git log'. Available prefixes,

    REV
        All changes that bring in new features, enhancements to the original implementations, or other forward code evolutions should fall into this category.
    FIX
        A change that is meant to fix a bug should fall into this category.
    FMT
        A change that is meant to improve the code style, or format of the original code. e.g., Remove the trailing space, replacing the tabs using spaces, etc.
    ADD
        Added a new file.
    DEL
        Deleted a file.

  An example of the prefixed commit message would look like this,

    - REV: Made the transition available under a centralized name.
    - REV: Added a unittest for budget request approval.
    - FIX: Fixed the treasury user email unset problem.
    - FMT: Inserted a new line into the code and import lines.
    - ADD: Added a new js file containing all event listeners.
    - DEL: Deleted the deprecated template.

- Provide a brief summary (it is recommended to keep the commit title
  under 50 chars).
- The first line of the commit message should provide an accurate
  description of the change, not just a reference to a bug or
  blueprint. It must be followed by a single blank line.
- Following your brief summary, provide a more detailed description of
  the patch, manually wrapping the text at 72 characters. This
  description should provide enough detail that one does not have to
  refer to external resources to determine its high-level functionality.
- Once you use 'git review', two lines will be appended to the commit
  message: a blank line followed by a 'Change-Id'. This is important
  to correlate this commit with a specific review in Gerrit, and it
  should not be modified.

Templates
---------

- There should be no inline CSS and Javascript at all.
  Attribute 'id' and 'class' should be
  the only dependencies between page and scripts.
- Using template tag 'include' to separate the shared HTML snippets.
- Keep same indentation as the outer HTML outside if and for tag block

Javascript
----------

- Indent using 4 spaces.
- Always use semicolon ';'.
- Placing all script tag only at the bottom of the HTML. In order to
  enable this to work without problem, make sure the interactions on
  the browser side can be delayed when the page completes rendering itself.
- Name 'shredder' is the only allowed global name. All names should
  go under this name using the dot syntax.

Example::

    shredder.binders = {
        'home': function() { // note the space in between
            // binding event listeners
        }
    }

- Using camel naming convention for functions, variables, and objects.

Example::

    getRequestId()

- When binding event listeners, always use live() or on().
- For a more detailed library oriented best practice guidelines, go read
  http://docs.jquery.com
