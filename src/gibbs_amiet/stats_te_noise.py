import os

import numpy as np
import scipy.signal as sg

import matplotlib.pyplot as plt
# Matplotlib global settings
plt.style.use('../../style.mplstyle')

if __name__ == "__main__":
    
    import utils
    import filter
    import stats

    data_dir = "../../../data/"
    fig_dir = '../../../figures/'
    mesh_file = os.path.join(data_dir, "SherFWHsolid1_grid.h5")
    data_file = os.path.join(data_dir, "SherFWHsolid1_p_raw_data_250.h5")

    info_dict = utils.get_data_info(data_file, verbose=False)
    p_te = utils.extract_pressure_te(data_file, 100, 2**12, False)

    # ==============================================
    #    De-normalize the data
    # ==============================================
    rho_ref = 1.225     # experiments density [kg/m^3]
    U_ref = 16          # experiments velocity [m/s]
    cref = 0.1356       # airfoil chord [m]
    p_dyn = rho_ref*U_ref**2 # dynamic pressure [Pa]
    p_ref = 2e-5        # Reference pressure in Pa

    p_te *= p_dyn
    info_dict['T_s'] *= cref / U_ref
    info_dict['f_s'] *= U_ref / cref

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

    fig, ax = plt.subplots(figsize=(8,2))
    X , Y = np.meshgrid( t, z)
    c = ax.pcolormesh(X,Y,p_te.T,shading='nearest', cmap='berlin')
    fig.colorbar(c, ax=ax, orientation='vertical', fraction=.1, label=r'$p-\langle p\rangle$')
    ax.set_xlabel('$t$')
    ax.set_ylabel('$z$ index')


    # ==============================================
    #    Pressure spectrum at trailing edge
    # ==============================================
    fig, ax = plt.subplots()
    xf_w, spp = stats.spectrum(p_te, fs=fs, nperseg=nperseg, noverlap=noverlap, window=window, axis=0)

    ax.plot(xf_w, 10*np.log10(spp/p_ref**2))

    ax.set_xscale('log')
    ax.set_xlim([100, 0.5/T])
    ax.set_xlabel('$f$ [Hz]')
    ax.set_ylabel(r'$10\log(\Phi_{pp}/p_{\mathrm{ref}}^2)$ [dB/Hz]')
    ax.grid(which='minor', linestyle='--', linewidth=0.5)
    ax.grid(which='major', linestyle='-', linewidth=0.5)
    plt.savefig(os.path.join(fig_dir, 'spectrum_te.pdf'), bbox_inches='tight', transparent=True)

    # ==============================================
    #    Coherence length
    # ==============================================
    f, gamma = stats.coherence_function(
        p_te,
        ref_index=n_sens//2,  # Midspan sensor
        filter=True,
        flims=(1600, 8000),
        fs=fs,
        nperseg=nperseg,
        noverlap=noverlap,
        window=window
    )

    X, Y = np.meshgrid(f, z)
    
    fig, ax = plt.subplots(figsize=(8, 3))
    c = ax.pcolormesh(X,Y, gamma,shading='nearest', cmap='bone', vmax=1.0)
    fig.colorbar(c, ax=ax, label='$\gamma^2$ [-]')
    ax.grid(which='major', linewidth=0.5, color='white', alpha=0.5)
    ax.set_xlabel('$f$ [Hz]')
    ax.set_ylabel('$z/c$ [-]')
    plt.savefig(os.path.join(fig_dir, 'coherence_funct_te.png'), bbox_inches='tight', transparent=True, dpi=300)

    f, lz = stats.coherence_length(
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

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(f, lz)
    ax.set_xscale('log')
    ax.set_xlabel('$f$ [Hz]')
    ax.set_ylabel(r'$\ell_z/c$ [-]')
    ax.grid(which='minor', linestyle='--', linewidth=0.5)
    ax.grid(which='major', linestyle='-', linewidth=0.5)
    ax.set_xlim([f[1], f[-1]])
    plt.savefig(os.path.join(fig_dir, 'coherence_length_te.pdf'), bbox_inches='tight', transparent=True)

    plt.show()