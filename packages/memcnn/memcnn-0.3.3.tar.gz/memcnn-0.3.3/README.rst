======
MemCNN
======

.. image:: https://img.shields.io/circleci/build/github/silvandeleemput/memcnn/master.svg        
        :alt: CircleCI - Status master branch
        :target: https://circleci.com/gh/silvandeleemput/memcnn/tree/master

.. image:: https://img.shields.io/docker/cloud/build/silvandeleemput/memcnn.svg
        :alt: Docker - Status
        :target: https://hub.docker.com/r/silvandeleemput/memcnn

.. image:: https://readthedocs.org/projects/memcnn/badge/?version=latest        
        :alt: Documentation - Status master branch
        :target: https://memcnn.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/codecov/c/gh/silvandeleemput/memcnn/master.svg   
        :alt: Codecov - Status master branch
        :target: https://codecov.io/gh/silvandeleemput/memcnn

.. image:: https://img.shields.io/pypi/v/memcnn.svg
        :alt: PyPI - Latest release
        :target: https://pypi.python.org/pypi/memcnn

.. image:: https://img.shields.io/pypi/implementation/memcnn.svg        
        :alt: PyPI - Implementation
        :target: https://pypi.python.org/pypi/memcnn

.. image:: https://img.shields.io/pypi/pyversions/memcnn.svg        
        :alt: PyPI - Python version
        :target: https://pypi.python.org/pypi/memcnn

.. image:: https://img.shields.io/github/license/silvandeleemput/memcnn.svg        
        :alt: GitHub - Repository license
        :target: https://github.com/silvandeleemput/memcnn/blob/master/LICENSE.txt

A `PyTorch <http://pytorch.org/>`__ framework for developing memory-efficient invertible neural networks.

* Free software: `MIT license <https://github.com/silvandeleemput/memcnn/blob/master/LICENSE.txt>`__ (please cite our work if you use it)
* Documentation: https://memcnn.readthedocs.io.
* Installation: https://memcnn.readthedocs.io/en/latest/installation.html

Features
--------

* Simple `ReversibleBlock` wrapper class to wrap and convert arbitrary PyTorch Modules into invertible versions.
* Simple switching between `additive` and `affine` invertible coupling schemes and different implementations.
* Simple toggling of memory saving by setting the `keep_input` property of the `ReversibleBlock`.
* Training and evaluation code for reproducing RevNet experiments using MemCNN.
* CI tests for Python v2.7 and v3.6 and torch v0.4, v1.0, and v1.1 with good code coverage.

Example usage: ReversibleBlock
------------------------------

.. code:: python

    import torch
    import torch.nn as nn
    import memcnn


    # define a new torch Module with a sequence of operations: Relu o BatchNorm2d o Conv2d
    class ExampleOperation(nn.Module):
        def __init__(self, channels):
            super(ExampleOperation, self).__init__()
            self.seq = nn.Sequential(
                                        nn.Conv2d(in_channels=channels, out_channels=channels,
                                                  kernel_size=(3, 3), padding=1),
                                        nn.BatchNorm2d(num_features=channels),
                                        nn.ReLU(inplace=True)
                                    )

        def forward(self, x):
            return self.seq(x)

    # generate some random input data (batch_size, num_channels, y_elements, x_elements)
    X = torch.rand(2, 10, 8, 8)

    # application of the operation(s) the normal way
    model_normal = ExampleOperation(channels=10)
    Y = model_normal(X)

    # application of the operation(s) turned invertible using the reversible block
    F = ExampleOperation(channels=10 // 2)
    model_invertible = memcnn.ReversibleBlock(F, coupling='additive', keep_input=True, keep_input_inverse=True)
    Y2 = model_invertible(X)

    # The input (X) can be approximated (X2) by applying the inverse method of the reversible block on Y2
    X2 = model_invertible.inverse(Y2)

Run PyTorch Experiments
-----------------------

After installing MemCNN run:

.. code:: bash

    python -m memcnn.train [MODEL] [DATASET] [--fresh] [--no-cuda]

* Available values for ``DATASET`` are ``cifar10`` and ``cifar100``.
* Available values for ``MODEL`` are ``resnet32``, ``resnet110``, ``resnet164``, ``revnet38``, ``revnet110``, ``revnet164``
* Use the ``--fresh`` flag to remove earlier experiment results.
* Use the ``--no-cuda`` flag to train on the CPU rather than the GPU through CUDA.

Datasets are automatically downloaded if they are not available.

When using Python 3.* replace the ``python`` directive with the appropriate Python 3 directive. For example when using the MemCNN docker image use ``python3.6``.


Results
-------

TensorFlow results were obtained from `the reversible residual
network <https://arxiv.org/abs/1707.04585>`__ running the code from
their `GitHub <https://github.com/renmengye/revnet-public>`__.

+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+
|            |               Tensorflow                          |               PyTorch                       |
+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+
|            |    Cifar-10            |      Cifar-100           |      Cifar-10        |     Cifar-100        |
+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+
| Model      | acc.     | time        | acc.      | time         | acc.     | time      | acc.      | time     |
+============+==========+=============+===========+==============+==========+===========+===========+==========+
| resnet-32  |  92.74   |  2:04       |  69.10    |      1:58    |  92.86   |  1:51     |  69.81    |  1:51    |
+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+
| resnet-110 |  93.99   |  4:11       |  73.30    |      6:44    |  93.55   |  2:51     |  72.40    |  2:39    |
+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+
| resnet-164 |  94.57   | 11:05       |  76.79    |  10:59       |  94.80   |  4:59     |  76.47    |  3:45    |
+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+
| revnet-38  |  93.14   |  2:17       |  71.17    |      2:20    |  92.80   |  2:09     |  69.90    |  2:16    |
+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+
| revnet-110 |  94.02   |  6:59       |  74.00    |      7:03    |  94.10   |  3:42     |  73.30    |  3:50    |
+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+
| revnet-164 |  94.56   | 13:09       |  76.39    |  13:12       |  94.90   |  7:21     |  76.90    |  7:17    |
+------------+----------+-------------+-----------+--------------+----------+-----------+-----------+----------+


The PyTorch results listed were recomputed on June 11th 2018, and differ
from the results in the ICLR paper. The Tensorflow results are still the
same.

Memory consumption of model training in PyTorch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

============= =============
 Model        GPU VRAM (MB)
============= =============
resnet-32      766
resnet-110     1357
resnet-164     3083
revnet-38      677
revnet-110     706
revnet-164     1226
============= =============

Works using MemCNN
------------------

* `MemCNN: a Framework for Developing Memory Efficient Deep Invertible Networks <https://openreview.net/forum?id=r1KzqK1wz>`__ by Sil C. van de Leemput et al.
* `Reversible GANs for Memory-efficient Image-to-Image Translation <https://arxiv.org/abs/1902.02729>`__ by Tycho van der Ouderaa et al.
* `Chest CT Super-resolution and Domain-adaptation using Memory-efficient 3D Reversible GANs <https://openreview.net/forum?id=SkxueFsiFV>`__ by Tycho van der Ouderaa et al.

Citation
--------

Reference: Sil C. van de Leemput, Jonas Teuwen, Rashindra Manniesing.
`MemCNN: a Framework for Developing Memory Efficient Deep Invertible
Networks <https://openreview.net/forum?id=r1KzqK1wz>`__. *International
Conference on Learning Representations (ICLR) 2018 Workshop Track.
(https://iclr.cc/)*

If you use our code, please cite:

.. code:: bibtex

    @inproceedings{
      leemput2018memcnn,
      title={MemCNN: a Framework for Developing Memory Efficient Deep Invertible Networks},
      author={Sil C. van de Leemput, Jonas Teuwen, Rashindra Manniesing},
      booktitle={ICLR 2018 Workshop Track},
      year={2018},
      url={https://openreview.net/forum?id=r1KzqK1wz},
    }
