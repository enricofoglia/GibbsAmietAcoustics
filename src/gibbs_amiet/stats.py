import numpy as np
import scipy.signal as sg

from .filter import butter_bandpass_filter


def spectrum(
        data,
        filter: bool = False,
        flims: tuple = (0.0, 1.0),
        fs: float = 1.0,
        order: int = 2,
        **kwargs
):
    '''
    Compute the power spectral density (PSD) of the input data.

    Parameters
    ----------
    data : np.ndarray
        Input data to compute the spectrum.
    filter : bool, optional
        If True, apply a bandpass filter to the data before computing the
         spectrum. Default is False.
    flims : tuple, optional
        Frequency limits for the bandpass filter (low, high) in Hz. Default is
         (0.0, 1.0).
    fs : float, optional
        Sampling frequency in Hz. Default is 1.0.
    order : int, optional
        Order of the Butterworth filter. Default is 2.
    **kwargs : dict, optional
        Additional keyword arguments passed to `scipy.signal.welch`.

    Returns
    -------
    f : np.ndarray
        Frequencies at which the PSD is computed.
    spp : np.ndarray
        Power spectral density of the input data.
    '''
    if filter:
        filtered_data = butter_bandpass_filter(
            data, flims[0], flims[1], fs, order=order)
    else:
        filtered_data = data

    f, spp = sg.welch(filtered_data, fs=fs, **kwargs)
    spp = np.mean(spp, axis=1)

    return f, spp


def coherence_function(
    data: np.ndarray,
    ref_index: int = 0,
    filter: bool = False,
    flims: tuple = (0.0, 1.0),
    fs: float = 1.0,
    order: int = 2,
    **kwargs
):
    '''
    Compute the coherence function for the input data.

    Parameters
    ----------
    data : np.ndarray
        Input data array where each column represents a sensor.
    ref_index : int, optional
        Index of the reference sensor in the data array. Default is 0.
    filter : bool, optional
        If True, apply a bandpass filter to the data before computing the
          coherence. Default is False.
    flims : tuple, optional
        Frequency limits for the bandpass filter (low, high) in Hz. Default is
          (0.0, 1.0).
    fs : float, optional
        Sampling frequency in Hz. Default is 1.0.
    order : int, optional
        Order of the Butterworth filter. Default is 2.
    **kwargs : dict, optional
        Additional keyword arguments passed to `scipy.signal.coherence`.

    Returns
    -------
    f : np.ndarray
        Frequencies at which the coherence is computed.
    gamma : np.ndarray
        Coherence values for each sensor with respect to the reference sensor.
    '''

    reference = data[:, ref_index]  # Reference sensor (midspan)
    if filter:
        reference = butter_bandpass_filter(
            reference, flims[0], flims[1], fs, order=order)

    gamma = []

    for i in range(data.shape[1]):
        fi = data[:, i]  # Current sensor data
        if filter:
            fi = butter_bandpass_filter(
                fi, flims[0], flims[1], fs, order=order)
        f, coh = sg.coherence(reference, fi, fs=fs, **kwargs)
        gamma.append(coh)

    gamma = np.array(gamma)

    return f, gamma


def coherence_length(
    data: np.ndarray,
    z: np.ndarray,
    ref_index: int = 0,
    filter: bool = False,
    flims: tuple = (0.0, 1.0),
    fs: float = 1.0,
    order: int = 2,
    **kwargs
):
    '''
    Compute the coherence function for the input data.

    Parameters
    ----------
    data : np.ndarray
        Input data array where each column represents a sensor.
    z : np.ndarray
        Array of sensor indices or positions corresponding to the data columns.
    ref_index : int, optional
        Index of the reference sensor in the data array. Default is 0.
    filter : bool, optional
        If True, apply a bandpass filter to the data before computing the
           coherence. Default is False.
    flims : tuple, optional
        Frequency limits for the bandpass filter (low, high) in Hz. Default is
           (0.0, 1.0).
    fs : float, optional
        Sampling frequency in Hz. Default is 1.0.
    order : int, optional
        Order of the Butterworth filter. Default is 2.
    **kwargs : dict, optional
        Additional keyword arguments passed to `scipy.signal.coherence`.

    Returns
    -------
    f : np.ndarray
        Frequencies at which the coherence is computed.
    lz : np.ndarray
        Coherence length at all frequencies.
    '''
    f, gamma = coherence_function(
        data,
        ref_index=ref_index,
        filter=filter,
        flims=flims,
        fs=fs,
        order=order,
        **kwargs
    )

    lz = np.trapz(np.sqrt(gamma), x=z, axis=0)  # Coherence length
    return f, lz
