"""
py_seismic_v53.py
-----------------
Reference Python implementation of the v53 Multi-Physics Seismic Hazard Framework.
Fully closed-form, arithmetically verifiable calculation of Coulomb stress,
BPT recurrence, Phase Transition Index (PTI), integrated risk, and probability gain (G_EQ).
"""

import numpy as np
from scipy.stats import norm

class SeismicHazardModelV53:
    def __init__(
        self,
        tau_dot: float = 20.0,       # Tectonic loading rate (kPa/yr)
        r0: float = 10.0,            # Reference distance (km)
        dCFS0: float = 100.0,        # Reference stress (kPa)
        eta: float = 2.1,            # Attenuation exponent
        mu_T: float = 100.0,         # Mean recurrence (years)
        alpha: float = 0.30,         # Aperiodicity
        dt: float = 1/12,            # Time window (1 month = 1/12 yr)
        w_b: float = 0.40,           # b-value weight
        w_Rn: float = 0.30,          # Radon weight
        w_vTEC: float = 0.30,        # vTEC weight
        w_mod: float = 0.0020,       # PTI modulation weight
        P_baseline: float = 0.00020, # Baseline monthly rate (0.02%/mo)
        G_max: float = 45.0          # Probability gain cap
    ):
        self.tau_dot = tau_dot
        self.r0 = r0
        self.dCFS0 = dCFS0
        self.eta = eta
        self.mu_T = mu_T
        self.alpha = alpha
        self.dt = dt
        self.w_b = w_b
        self.w_Rn = w_Rn
        self.w_vTEC = w_vTEC
        self.w_mod = w_mod
        self.P_baseline = P_baseline
        self.G_max = G_max

    def compute_dCFS(self, Mw: float, r: float, d: float) -> float:
        """Compute attenuated Coulomb stress change dCFS (kPa)."""
        mag_factor = 10.0 ** (1.5 * (Mw - 6.0))
        dist_factor = ((r**2 + d**2) / (self.r0**2)) ** (self.eta / 2.0)
        return float(self.dCFS0 * mag_factor / dist_factor)

    def compute_bpt_prob(self, t: float) -> float:
        """Compute monthly rupture probability P_BPT(t)."""
        if t <= 0:
            return 0.0
        # Instantaneous rupture saturation for extreme stress shifts / mature faults (t >= 3.0 * mu_T)
        if t >= 3.0 * self.mu_T:
            return 1.00000
            
        gamma = (t / self.mu_T)
        z1 = (gamma - 1.0) / (self.alpha * np.sqrt(gamma))
        z2 = -(gamma + 1.0) / (self.alpha * np.sqrt(gamma))
        F_t = norm.cdf(z1) + np.exp(2.0 / (self.alpha**2)) * norm.cdf(z2)
        
        gamma_dt = ((t + self.dt) / self.mu_T)
        z1_dt = (gamma_dt - 1.0) / (self.alpha * np.sqrt(gamma_dt))
        z2_dt = -(gamma_dt + 1.0) / (self.alpha * np.sqrt(gamma_dt))
        F_tdt = norm.cdf(z1_dt) + np.exp(2.0 / (self.alpha**2)) * norm.cdf(z2_dt)
        
        if F_t >= 1.0:
            return 1.0
        P_bpt = (F_tdt - F_t) / (1.0 - F_t)
        return float(np.clip(P_bpt, 0.0, 1.0))

    def compute_sigmoids(self, b: float, z_Rn: float, z_vTEC: float):
        """Compute individual precursor sigmoid activations."""
        S_b = 1.0 / (1.0 + np.exp(10.0 * (b - 0.75)))
        S_Rn = 1.0 / (1.0 + np.exp(-2.0 * (z_Rn - 2.0)))
        S_vTEC = 1.0 / (1.0 + np.exp(-1.5 * (z_vTEC - 2.5)))
        return float(S_b), float(S_Rn), float(S_vTEC)

    def compute_pti(self, S_b: float, S_Rn: float, S_vTEC: float) -> float:
        """Compute explicit Phase Transition Index (PTI)."""
        pti_raw = self.w_b * S_b + self.w_Rn * S_Rn + self.w_vTEC * S_vTEC
        return float(min(1.0, pti_raw))

    def compute_integrated_risk(self, P_bpt_shifted: float, pti: float) -> float:
        """Compute integrated monthly rupture risk R_integrated."""
        if P_bpt_shifted >= 1.0:
            return 1.00000
        R_raw = P_bpt_shifted + (1.0 - P_bpt_shifted) * self.w_mod * pti
        return float(min(1.0, R_raw))

    def compute_gain(self, R_integrated: float) -> float:
        """Compute probability gain G_EQ."""
        G_raw = R_integrated / self.P_baseline
        return float(min(self.G_max, G_raw))

    def evaluate_event(
        self, Mw: float, r: float, d: float, t0_over_mu: float,
        b: float, z_Rn: float, z_vTEC: float
    ) -> dict:
        """Full end-to-end evaluation pipeline for a single event."""
        t0 = t0_over_mu * self.mu_T
        dCFS = self.compute_dCFS(Mw, r, d)
        dt_shift = dCFS / self.tau_dot
        t_prime = t0 + dt_shift
        
        P_bpt_unshifted = self.compute_bpt_prob(t0)
        P_bpt_shifted = self.compute_bpt_prob(t_prime)
        
        S_b, S_Rn, S_vTEC = self.compute_sigmoids(b, z_Rn, z_vTEC)
        pti = self.compute_pti(S_b, S_Rn, S_vTEC)
        
        R_integrated = self.compute_integrated_risk(P_bpt_shifted, pti)
        G_EQ = self.compute_gain(R_integrated)
        
        return {
            "dCFS": dCFS,
            "dt_shift": dt_shift,
            "t0": t0,
            "t_prime": t_prime,
            "P_bpt_unshifted": P_bpt_unshifted,
            "P_bpt_shifted": P_bpt_shifted,
            "S_b": S_b,
            "S_Rn": S_Rn,
            "S_vTEC": S_vTEC,
            "PTI": pti,
            "R_integrated": R_integrated,
            "G_EQ": G_EQ
        }
