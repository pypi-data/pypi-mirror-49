DesktopScoreViewer
==================
The DesktopScoreViewer program does exactly as
its name implies: it gathers game scores and
data and displays them live on a mini GUI on the
top right corner of your screen. This allows the
user to casually follow games without it being
too intrusive or distracting.

Installation
------------
You can press the git clone button on the top
right or type this on your terminal:

::

    git clone https://github.com/JosephJ12/DesktopScoreViewer

You can also install using pip:

::

    pip install DesktopScoreViewer

Program also requires firefox webdriver,
geckodriver which must be installed separately.
Install at this link:
https://www.guru99.com/gecko-marionette-driver-selenium.html

Usage
-----
Running the __main__.py of package will open
up the GUI.

.. code-block:: python

    from DesktopScoreViewer import __main__

    #call DesktopScoreViewer package's main
    __main__.main()

License
--------
`MIT
<https://choosealicense.com/licenses/mit/>`_
