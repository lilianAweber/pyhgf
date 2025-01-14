.. _api_ref:

.. currentmodule:: pyhgf


.. contents:: Table of Contents
   :depth: 2

API
+++

Binary
------

Core functionnalities to update *binary* node structures.

.. currentmodule:: pyhgf.binary

.. autosummary::
   :toctree: generated/pyhgf.binary

    binary_node_update
    binary_input_update
    gaussian_density
    sgm
    binary_surprise
    loop_binary_inputs


Continuous
----------

Core functionnalities to update *continuous* node structures.

.. currentmodule:: pyhgf.continuous

.. autosummary::
   :toctree: generated/pyhgf.continuous

    continuous_node_update
    continuous_input_update
    gaussian_surprise
    loop_continuous_inputs

Distribution
------------

The Herarchical Gaussian Filter as a PyMC distribution. This distribution can be
embedded in a PyMC model (pymc>=5.0.0).

.. currentmodule:: pyhgf.distribution

.. autosummary::
   :toctree: generated/pyhgf.distribution

   hgf_logp
   HGFLogpGradOp
   HGFDistribution

Model
-----

The main class used to create a standard Hierarchical Gaussian Filter for binary or
continuous inputs, with two or three levels. This class wraps the previous JAX modules
and create a standard node structure for these models.

.. currentmodule:: pyhgf.model

.. autosummary::
   :toctree: generated/pyhgf.model

   HGF

Plots
-----

Plotting functionnalities to visualize parameters trajectories and correlations after
observing new data.

.. currentmodule:: pyhgf.plots

.. autosummary::
   :toctree: generated/pyhgf.plots

   plot_trajectories
   plot_correlations

Response
--------

A collection of responses functions. A response function is simply a callable taking at
least the HGF instance as input after observation and returning surprise.

.. currentmodule:: pyhgf.response

.. autosummary::
   :toctree: generated/pyhgf.response

   total_gaussian_surprise
   total_binary_surprise

Structure
---------

Utilities for testing and manipulating node structures.

.. currentmodule:: pyhgf.structure

.. autosummary::
   :toctree: generated/pyhgf.structure

   structure_as_dict
   structure_validation
