==========
SLL plugin
==========

Scipion plugin for CryoEM tools developed at `SciLifeLab <https://www.scilifelab.se/>`_.

Installation
____________

You will need to use `Scipion 2.0 <https://github.com/I2PC/scipion/releases/tag/v2.0>`_ to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

   .. code-block:: bash

      scipion installp -p scipion-em-sll

b) Developer's version

   * download repository

   .. code-block:: bash

      git clone https://github.com/scipion-em/scipion-em-sll.git

   * install

   .. code-block:: bash

      scipion installp -p path_to_scipion-em-sll --devel

To check the installation, simply run one of the following Scipion tests:

.. code-block:: bash

   scipion test gctf.tests.test_protocols_gctf.TestGctfRefine
   scipion test gctf.tests.test_protocols_gctf.TestGctf


Protocols
_________

.. csv-table::
   :header: "Protocol", "Description"
   :widths: 30, 70

   "filter classes CC", "Simple protocol to select 'good' classes based on cross-correlation and the number of particles assigned."
   "filter CTF", "If we took the bones out, it wouldn't be crunchy, now would it?"



References
__________

* None yet
