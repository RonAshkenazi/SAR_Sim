from algos.rssi import RSSIModel


def test_rssi_inversion():
    model = RSSIModel(pl0_db=40, n=2, d0_m=1.0, min_d_m=0.5, max_d_m=150)
    d = model.to_distance(-30, -70)
    assert abs(d - 1.0) < 1e-6
