"""
test_v53_reproducibility.py
---------------------------
Automated test suite verifying py_seismic_v53 against Table 1a and Table 1b
from Zenodo Preprint v53.
"""

from py_seismic_v53 import SeismicHazardModelV53

# 12 Global Test Events from v53 Preprint
TEST_EVENTS = [
    {
        "name": "Flores Island Thrust, ID",
        "Mw": 7.8, "r": 26.8, "d": 15.0, "t0_mu": 0.92,
        "b": 0.50, "z_Rn": 3.4, "z_vTEC": 4.0,
        "target_dCFS": 4749.5, "target_PTI": 0.924, "target_GEQ": 45.0
    },
    {
        "name": "Chocó Fault Zone, CO",
        "Mw": 7.4, "r": 5.7, "d": 20.0, "t0_mu": 0.88,
        "b": 0.72, "z_Rn": 3.8, "z_vTEC": 2.8,
        "target_dCFS": 2705.4, "target_PTI": 0.705, "target_GEQ": 28.7
    },
    {
        "name": "Hokkaido Subduct., JP",
        "Mw": 6.0, "r": 37.2, "d": 22.0, "t0_mu": 0.96,
        "b": 0.76, "z_Rn": 0.7, "z_vTEC": 3.4,
        "target_dCFS": 4.6, "target_PTI": 0.449, "target_GEQ": 16.3
    },
    {
        "name": "Banten / Sunda Arc, ID",
        "Mw": 6.6, "r": 24.8, "d": 25.0, "t0_mu": 0.68,
        "b": 0.68, "z_Rn": 3.5, "z_vTEC": 0.9,
        "target_dCFS": 56.5, "target_PTI": 0.578, "target_GEQ": 11.4
    },
    {
        "name": "Ayacucho Subduct., PE",
        "Mw": 6.7, "r": 31.0, "d": 30.0, "t0_mu": 0.65,
        "b": 0.72, "z_Rn": 0.8, "z_vTEC": 3.5,
        "target_dCFS": 52.1, "target_PTI": 0.500, "target_GEQ": 9.8
    },
    {
        "name": "Port-Olry, Vanuatu Arc",
        "Mw": 6.1, "r": 24.7, "d": 40.0, "t0_mu": 0.58,
        "b": 0.54, "z_Rn": 0.9, "z_vTEC": 1.5,
        "target_dCFS": 5.5, "target_PTI": 0.441, "target_GEQ": 6.9
    },
    {
        "name": "South Sandwich Trench",
        "Mw": 6.2, "r": 16.1, "d": 20.0, "t0_mu": 0.55,
        "b": 0.66, "z_Rn": 2.1, "z_vTEC": 0.3,
        "target_dCFS": 27.5, "target_PTI": 0.460, "target_GEQ": 6.7
    },
    {
        "name": "Nikolski, Aleutian Arc, AK",
        "Mw": 6.3, "r": 13.7, "d": 18.0, "t0_mu": 0.52,
        "b": 1.02, "z_Rn": 2.2, "z_vTEC": 2.8,
        "target_dCFS": 50.8, "target_PTI": 0.388, "target_GEQ": 5.6
    },
    {
        "name": "Offshore Somalia (Aden)",
        "Mw": 6.0, "r": 24.4, "d": 10.0, "t0_mu": 0.48,
        "b": 0.58, "z_Rn": 0.5, "z_vTEC": 1.3,
        "target_dCFS": 13.1, "target_PTI": 0.395, "target_GEQ": 4.7
    },
    {
        "name": "Kermadec Trench, SW Pac.",
        "Mw": 6.3, "r": 24.2, "d": 35.0, "t0_mu": 0.35,
        "b": 0.80, "z_Rn": 0.4, "z_vTEC": 3.2,
        "target_dCFS": 13.5, "target_PTI": 0.385, "target_GEQ": 3.9
    },
    {
        "name": "Scotia Sea / S. Atlantic",
        "Mw": 6.2, "r": 15.5, "d": 15.0, "t0_mu": 0.42,
        "b": 0.76, "z_Rn": 1.6, "z_vTEC": 0.1,
        "target_dCFS": 39.7, "target_PTI": 0.291, "target_GEQ": 3.3
    },
    {
        "name": "Banda Sea / Weber Deep",
        "Mw": 6.0, "r": 22.2, "d": 50.0, "t0_mu": 0.40,
        "b": 0.88, "z_Rn": 2.2, "z_vTEC": 1.1,
        "target_dCFS": 2.8, "target_PTI": 0.298, "target_GEQ": 3.1
    }
]

def run_tests():
    m = SeismicHazardModelV53()
    print("=" * 90)
    print("RUNNING REPRODUCIBILITY VERIFICATION ON ALL 12 EVENTS (v53 PREPRINT)")
    print("=" * 90)
    all_passed = True
    for ev in TEST_EVENTS:
        res = m.evaluate_event(
            ev["Mw"], ev["r"], ev["d"], ev["t0_mu"],
            ev["b"], ev["z_Rn"], ev["z_vTEC"]
        )
        diff_dCFS = abs(res["dCFS"] - ev["target_dCFS"])
        diff_PTI = abs(res["PTI"] - ev["target_PTI"])
        diff_GEQ = abs(res["G_EQ"] - ev["target_GEQ"])
        passed = (diff_dCFS < 0.2) and (diff_PTI < 0.002) and (diff_GEQ < 0.1)
        if not passed:
            all_passed = False
        print(f"[{'PASS' if passed else 'FAIL'}] {ev['name']:27s} | dCFS: {res['dCFS']:6.1f} (tgt {ev['target_dCFS']:6.1f}) | PTI: {res['PTI']:.3f} (tgt {ev['target_PTI']:.3f}) | G_EQ: {res['G_EQ']:4.1f}x (tgt {ev['target_GEQ']:4.1f}x)")
    print("=" * 90)
    print(f"OVERALL VERIFICATION STATUS: {'ALL 12 TESTS PASSED PERFECTLY' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    if not success:
        exit(1)
