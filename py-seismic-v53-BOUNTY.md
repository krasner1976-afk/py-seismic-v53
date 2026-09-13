# Research Bounties & Open Validation Challenges

We invite open-source researchers, data scientists, geophysicists, and computational linguists to validate, extend, and benchmark the **py-seismic-v53** framework.

---

## 🟢 Open Bounties

### 1. Geosciences Bounty: CSEP N-test & L-test Validation
* **Task**: Perform formal CSEP (Center for the Study of Earthquake Predictability) spatial/temporal consistency tests ($N$-test, $L$-test) on independent earthquake catalogs (Japan JMA, USGS California, Indonesia BMKG) for 2024–2026.
* **Objective**: Evaluate whether the v53 integrated gain $G_{\text{EQ}}$ provides statistically significant information gain over spatial Poisson baselines.
* **Category**: `Geosciences / Seismology`

### 2. Data Science Bounty: GPU Acceleration of 3D Okada Dislocation
* **Task**: Accelerate the 3D Okada dislocation tensor calculation for 101,475 spatial nodes using PyTorch / CUDA / JAX.
* **Target Speedup**: Reduce full-globe calculation time from ~10 minutes to < 5 seconds.
* **Category**: `Data Science / HPC`

### 3. Computational Linguistics Bounty: Automated Precursor NLP Extractor
* **Task**: Build an NLP/LLM pipeline to automatically extract and normalize precursor observables ($b$-value, Radon flux $z$-score, ionospheric $vTEC$ anomaly) from historical geophysical reports (1900–2026).
* **Output Format**: Standard JSON/CSV output matching `py-seismic-v53` input schemas.
* **Category**: `Linguistics / Computational NLP`

---

## 🤝 Participation in External Benchmarks

We actively participate in:
* **SCEC/USGS SEAS (Sequences of Earthquakes and Aseismic Slip)** Benchmark Consortium.
* **NoisePy / MSNoise** Ambient Noise Cross-Correlation Monitoring.
* **ArXiv / Zenodo Open Science Data Curation**.

To submit a solution or claim a bounty, open a GitHub Issue or Pull Request with the tag `[BOUNTY-SUBMISSION]`.
