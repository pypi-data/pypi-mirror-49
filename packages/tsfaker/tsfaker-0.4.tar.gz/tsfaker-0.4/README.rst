==================
Table Schema Faker
==================

Generate tabular fake data conforming to a `Table Schema <https://frictionlessdata.io/specs/table-schema/>`_

Usage
=====

.. code:: bash

    # Installation
    $ pip3 install tsfaker

    # Usage
    $ tsfaker https://gitlab.com/healthdatahub/tsfaker/raw/master/tests/schemas/implemented_types.json  --nrows 3 --pretty
                    string              number      integer        date             datetime  year yearmonth
    0           QZluRNRoaJ   8524064526.189381   5603365028  1918-06-09  1963-02-25T15:27:14  1927   1968-03
    1    OAXCFryYDVMWmRTnP   8084094810.096195  -9782888534  1995-06-06  1924-06-14T07:41:59  1928   1929-02
    2                        -6416720321.04726  -1060427558  2006-12-11  2002-12-25T07:41:47  1999   1914-11


Goals
=====

We aim to generate fake data conforming to a *schema*.

We do not aim to generate realistic data with statistical information (see related work).

Implementation steps
--------------------

- Generate data conforming to types
- Generate data conforming to formats and constraints, such as min/max, enum, missing values, unique, length, and regex
- Generate multiple tables conforming to foreign key references, with optional tables' data provided through csv

API
---

- We want to provide both a Python API and a command line API

Development methodology
-----------------------

We will conform to Test Driven Development methodology, hence writing test before writing implementation.

We want generated data to be valid when using `goodtables <https://pypi.org/project/goodtables/>`_.

We could go by conforming to more and more `content checks <https://github.com/frictionlessdata/goodtables-py#content-checks>`_, which are included in table-schema specification.

Related Python libraries
========================

We may use directly or get inspiration from the following libraries

Simple data Generators
----------------------

- `numpy <https://github.com/numpy/numpy>`_ comes with many functions to generate random data.

- `rstr <https://pypi.org/project/rstr/>`_ and `exrex <https://github.com/asciimoo/exrex>`_ generate random string following regular expressions.

- `Faker <https://github.com/joke2k/faker>`_ and `Mimesis <https://mimesis.readthedocs.io/index.html>`_ allow to generate fake data. They both focus on generating high level data, such as names, email or addresses, which does not seem necessary for us.

- `DataScienceFaker <https://github.com/EDS-APHP/dsfaker>`_ generate synthetic data conforming to statistical distributions. It is based on numpy and rstr.

Table generator
---------------

- `pydbgen <https://github.com/tirthajyoti/pydbgen>`_ is a shallow wrapper around Faker to generate tables as pandas dataframe, sqlite table or Excel files.

- `pySyntheticDatasetGenerator <https://github.com/EDS-APHP/pySyntheticDatasetGenerator>`_ is a wrapper around dsfaker, that generate tables with their relations as described in yaml configuration files.

- `datafiller <https://github.com/memsql/datafiller>`_ generate random data from database schema. API could be interesting.

- `plaitpy <https://github.com/plaitpy/plaitpy>`_ is a fake table generator from a yaml configuration file.


Realistic data
--------------

Generating realistic data - ie data carrying statistical information -  could mean different things in different contexts :

- realistic statistical distribution on single columns,
- realistic temporal dynamics,
- realistic correlations between pairs of columns,
- realistic correlations between pairs of columns from different (joinable) tables,
- etc.

Hence there is no universal way to generate realistic data. Most approaches follow two steps :

1. learn a statistical model from the real data,
2. generate data using this model.

The statistical model depends of the context, and is usually not expressed in the form of a generic schema, such as table-schema.
However, a schema of your data will be often be necessary to *configure* this kind of libraries.

This topic is an active research area, with many articles but few production implementations :

- `DataSynthesizer <https://github.com/DataResponsibly/DataSynthesizer>`_ (`article <https://arxiv.org/abs/1710.08874>`__) learn a diferentially private Bayesian network capturing the correlation structure between attributes
- `SDV <https://github.com/HDI-Project/SDV>`_ (`article <https://dai.lids.mit.edu/wp-content/uploads/2018/03/SDV.pdf>`__) Generative modeling for relational databases.
- `medGAN <https://github.com/mp2893/medgan>`_ (`article <https://arxiv.org/abs/1703.06490>`__) Generative adversarial network for generating electronic health records.
- `dpgan <https://github.com/alps-lab/dpgan>`_ (`article <https://arxiv.org/pdf/1801.01594.pdf>`__) Differentially Private Releasing via Deep Generative Model.

The statistical model may convey sensitive information and personnal data. 
It is important fact to bear in mind, as protecting sensitive information is a common reason to generate fake data in the first place.

Some tools offer ways to mitigate the risk from personal data leakage, with no formal guarantees.
Other tools offer formal privacy guarantees through `differential privacy <https://en.wikipedia.org/wiki/Differential_privacy>`_.

An active line of work is to use Generative Adversial Network to generate realistic data.
When using Neural Network, one can use TensorFlow's `specific library <https://medium.com/tensorflow/introducing-tensorflow-privacy-learning-with-differential-privacy-for-training-data-b143c5e801b6>`_.
`PySyft project <https://github.com/OpenMined/PySyft>`_ aims to provide a generic implementation for PyTorch.
