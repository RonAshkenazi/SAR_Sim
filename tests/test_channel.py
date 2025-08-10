from channel.models import LogDistanceChannel


def test_path_loss_no_noise():
    ch = LogDistanceChannel(pl0_db=40, n=2, shadow_sigma_db=0, awgn_sigma_db=0)
    rssi = ch.rssi((0,0,0),(1,0,0), -30)
    assert abs(rssi + 70) < 1e-6
