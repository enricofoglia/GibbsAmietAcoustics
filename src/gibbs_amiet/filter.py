import scipy.signal as sg

def _butter_bandpass(lowcut, highcut, fs, order=5):
    # Butterworth bandpass filter design
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sg.butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    '''
    Filter the data using a Butterworth bandpass filter.
    
    Parameters
    ----------
    data : np.ndarray
        Input data to be filtered.
    lowcut : float
        Low cutoff frequency in Hz.
    highcut : float
        High cutoff frequency in Hz.
    fs : float
        Sampling frequency in Hz.
    order : int, optional
        Order of the filter. Default is 2.

    Returns
    -------
    np.ndarray
        Filtered data.
    '''
    b, a = _butter_bandpass(lowcut, highcut, fs, order=order)
    y = sg.lfilter(b, a, data)
    return y
