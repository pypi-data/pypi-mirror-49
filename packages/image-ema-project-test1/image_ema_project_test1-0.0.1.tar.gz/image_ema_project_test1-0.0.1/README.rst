Image-EMA IDI Project
---------------------

A simple example project for the 2019 High-speed Image Based Experimental Modal Analysis & Open Source Tools Summer School.


Quickstart
----------

At the end of the summer school, the image-ema-project will be available on PyPI and can be installed with `pip <https://pip.pypa.io>`_.

.. code-block:: console

    $ pip install image_ema_project

After installing image-ema-project you can use it like any other Python module.

Here is a simple example:

.. code-block:: python

    import image_ema_project as iep
    import numpy as np
    import matplotlib.pyplot as plt

    video = np.load('examples/speckle.npy', mmap_mode='r')
    results = iep.get_displacements(video, point=[5, 5], roi_size=[7, 7])

    plt.figure()
    plt.plot(results[0], label='x [px]')
    plt.plot(results[1], label='y [px]')
    plt.legend()
    plt.show()

You can also run this basic example by running the following commain in the project base direcotry:

.. code-block:: console

    $ python -m examples.basic_example

The `Read the Docs page <http://image_ema_project.readthedocs.io>`_ provides the project documentation.
