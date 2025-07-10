.. gibbs_amiet documentation master file, created by
   sphinx-quickstart on Tue Jul  8 21:22:03 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

gibbs_amiet documentation
=========================

:code:`gibbs_amiet` is a Python package developed to compute the trailing-edge noise of isolated airfoils using the Amiet model with synthetic input data. The turbulent fluctuations are sampled from a Gibbs distribution, and then processed inside the package to compute the noise.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Usage example
-------------

.. code-block:: python

   data_dir = "../data/"
   fig_dir = '../figures/'
   data_file = os.path.join(data_dir, "SherFWHsolid1_p_raw_data_250.h5")

   info_dict = ga.utils.get_data_info(data_file, verbose=False)
   p_te = ga.utils.extract_pressure_te(data_file, 100, 2**12, False)
   

   # ==============================================
   #    Basic information
   # ==============================================
   N = p_te.shape[0]       # Number of sample points
   T = info_dict['T_s']    # sample spacing
   fs = info_dict['f_s']   # Sampling frequency
   n_sens = p_te.shape[1]  # Number of sensors
   nperseg = N//8
   noverlap = nperseg//2
   window = 'hann'

   z = np.linspace(0.0,1.0,n_sens)*2.0  # Sensor indices
   t = np.arange(N)*T

   # ==============================================
   #    Pressure spectrum at trailing edge
   # ==============================================
   xf_w, spp = ga.stats.spectrum(
      p_te,
      fs=fs,
      nperseg=nperseg,
      noverlap=noverlap,
      window=window,
      axis=0)

   # ==============================================
   #    Coherence length
   # ==============================================
   f, gamma = ga.stats.coherence_function(
      p_te,
      ref_index=n_sens//2,  # Midspan sensor
      filter=True,
      flims=(1600, 8000),
      fs=fs,
      nperseg=nperseg,
      noverlap=noverlap,
      window=window
   )

   f, lz = ga.stats.coherence_length(
      p_te,
      z=z,
      ref_index=n_sens//2,  # Midspan sensor
      filter=True,
      flims=(1600, 8000),
      fs=fs,
      nperseg=nperseg,
      noverlap=noverlap,
      window=window
   )


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`