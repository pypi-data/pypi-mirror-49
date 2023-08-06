OrcaSong 2
==========

OrcaSong 2 is an alternative to orcasong, with (hopefully) more
accessible features.
It has a slightly reduced functionality (no plots), but apart from that
does the same job as orcasong.

Basic Use
---------

Import the main class, the FileBinner (see
:py:class:`orcasong_2.core.FileBinner`),
like this:

.. code-block:: python

    from orcasong_2.core import FileBinner

The FileBinner allows to make nd histograms ("images") from calibrated and
h5-converted root files.
To do this, you can pass a list defining the binning. E.g., the following would
set up the file binner to generate zt data:

.. code-block:: python

    bin_edges_list = [
        ["pos_z", np.linspace(0, 10, 11)],
        ["time", np.linspace(-50, 550, 101)],
    ]

    fb = FileBinner(bin_edges_list)

Calling the object like this will show you the binning:

.. code-block:: python

    >>> fb
    <FileBinner: ('pos_z', 'time') (10, 100)>

As you can see, the FileBinner will produce zt data, with 10 and 100 bins,
respectively.
Convert a file like this:

.. code-block:: python

    fb.run(infile, outfile)

Or event this for multiple files, which will all be saved in the given folder:

.. code-block:: python

    fb.run_multi(infiles, outfolder)

Adding mc_info
--------------

To add info from the mc_tracks (or from wherever), you can define some
function `my_mcinfo_extractor` which takes as an input a km3pipe blob,
and outputs a dict mapping str to float.

This will be saved as a numpy structured array "y" in the output file, with
the str being the dtype names. Set up like follows:

.. code-block:: python

    fb = FileBinner(bin_edges_list, mc_info_extr=my_mcinfo_extractor)

