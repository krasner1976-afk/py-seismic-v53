# py-seismic-v53: Multi-Physics Short-Term Seismic Hazard Solver (v53)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12984501.svg)](https://doi.org/10.5281/zenodo.12984501)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Official open-source reference Python implementation of the **v53 Multi-Physics Seismic Hazard Framework**. 

Version 53 provides **100% closed-form mathematical verification** and complete data transparency across all geomechanical (Coulomb + BPT renewal) and precursory (b-value, Radon, vTEC) channels.

---

## 📐 System Architecture & Equations

The framework transforms input parameters across a closed 5-stage physics pipeline:

$$\Delta CFS \longrightarrow \Delta t_{\text{shift}} \longrightarrow P_{\text{BPT}}(t') \longrightarrow PTI \longrightarrow R_{\text{integrated}} \longrightarrow G_{\text{EQ}}$$

### 1. Attenuated Dislocation & Clock Shift
$$\Delta CFS(r, M_w, d) = \Delta CFS_0 \cdot \frac{10^{1.5(M_w - 6.0)}}{\left( \frac{r^2 + d^2}{r_0^2} \right)^{\eta/2}}, \qquad \Delta t_{\text{shift}} = \frac{\Delta CFS}{\dot{\tau}}$$

* Parameters: $\dot{\tau} = 20\text{ kPa/yr}$, $r_0 = 10\text{ km}$, $\Delta CFS_0 = 50\text{ kPa}$, $\eta = 2.1$.

### 2. Brownian Passage Time (BPT) Renewal Kernel
$$f(t; \mu_T, \alpha) = \left( \frac{\mu_T}{2\pi \alpha^2 t^3} \right)^{1/2} \exp\left[ -\frac{(t - \mu_T)^2}{2\mu_T \alpha^2 t} \right]$$
$$P_{\text{BPT}}(t) = \frac{F(t + \Delta t) - F(t)}{1 - F(t)}$$

* Parameters: Mean recurrence $\mu_T = 100\text{ yrs}$, aperiodicity $\alpha = 0.30$, time step $\Delta t = 1/12\text{ yr}$.

### 3. Explicit Phase Transition Index ($PTI$)
$$PTI = \min\left(1.0, \; w_b S_b(b) + w_{\text{Rn}} S_{\text{Rn}}(z_{\text{Rn}}) + w_{\text{vTEC}} S_{\text{vTEC}}(z_{\text{vTEC}})\right)$$

$$\begin{aligned}
S_b(b) &= \frac{1}{1 + e^{10(b - 0.75)}} \\
S_{\text{Rn}}(z_{\text{Rn}}) &= \frac{1}{1 + e^{-2(z_{\text{Rn}} - 2.0)}} \\
S_{\text{vTEC}}(z_{\text{vTEC}}) &= \frac{1}{1 + e^{-1.5(z_{\text{vTEC}} - 2.5)}}
\end{aligned}$$

* Weights: $w_b = 0.40, w_{\text{Rn}} = 0.30, w_{\text{vTEC}} = 0.30$.

### 4. Risk Integration & Probability Gain ($G_{\text{EQ}}$)
$$R_{\text{integrated}} = \min\left(1.0, \; P_{\text{BPT}}(t') + \left[1 - P_{\text{BPT}}(t')\right] \cdot w_{\text{mod}} \cdot PTI\right)$$
$$G_{\text{EQ}} = \min\left(45.0, \; \frac{R_{\text{integrated}}}{P_{\text{baseline}}}\right)$$

* Parameters: Modulation weight $w_{\text{mod}} = 0.0020$, baseline rate $P_{\text{baseline}} = 0.00020$, cap $G_{\max} = 45.0\times$.

---

## ⚡ Quickstart

```bash
# Clone repository
git clone https://github.com/v53-seismic/py-seismic-v53.git
cd py-seismic-v53

# Install dependencies
pip install -r requirements.txt

# Run full Table 1a / 1b verification test suite
python test_v53_reproducibility.py
```

---

## 🧪 Verification & Test Suite

The included test script `test_v53_reproducibility.py` validates all 12 global test events against Zenodo Preprint v53 with exact precision.

```bash
pytest test_v53_reproducibility.py -v
```

---

## 📜 Citation

```bibtex
@article{Krasner2026v53,
  author = {Krasner et al.},
  title = {A Preliminary Multi-Physics Framework for Short-Term Seismic Hazard Modeling (v53)},
  journal = {Zenodo Preprint},
  year = {2026},
  doi = {10.5281/zenodo.12984501}
}
```

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
