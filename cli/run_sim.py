"""Run signal scanning simulation."""
import argparse
import random
import numpy as np
from core.environment import Environment
from core.time import TimeConfig
from channel.models import LogDistanceChannel
from actors.emitter import Emitter
from actors.scanner import Scanner
from actors.motion import LawnMower, RandomWalk, WaypointPath
from io.config import load_config
from io.csv_writer import write_csv
from algos.rssi import RSSIModel
from algos.multilateration import Multilateration


def create_motion(cfg, env):
    model = cfg["model"]
    speed = cfg.get("speed", 1.0)
    if model == "lawnmower":
        return LawnMower(env, speed, cfg.get("lane_spacing", 10.0), cfg.get("altitude", 5.0))
    elif model == "random_walk":
        return RandomWalk(env, speed, cfg.get("altitude", 5.0))
    elif model == "waypoint":
        return WaypointPath(env, speed, cfg.get("waypoints", []))
    else:
        raise ValueError(f"Unknown motion model {model}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    random.seed(cfg.get("seed", 0))
    np.random.seed(cfg.get("seed", 0))

    env = Environment(**cfg["space"])
    time_cfg = TimeConfig(**cfg["time"])
    channel_cfg = cfg["channel"]
    channel = LogDistanceChannel(pl0_db=channel_cfg["pl0_db"], n=channel_cfg["n"],
                                 shadow_sigma_db=channel_cfg.get("shadow_sigma_db",0),
                                 awgn_sigma_db=channel_cfg.get("awgn_sigma_db",0))

    emitters = []
    for e_cfg in cfg.get("emitters", []):
        pos = e_cfg.get("pos")
        if pos == "random":
            pos = (random.uniform(0, env.x), random.uniform(0, env.y), random.uniform(0, env.z))
        emitters.append(Emitter.create(e_cfg["id"], e_cfg["proto"], e_cfg["tx_dbm"], pos))

    sc_cfg = cfg["scanner"]
    start = sc_cfg.get("start")
    if start == "random":
        start = (random.uniform(0, env.x), random.uniform(0, env.y), sc_cfg.get("motion",{}).get("altitude",5.0))
    motion = create_motion(sc_cfg["motion"], env)
    scanner = Scanner(id=sc_cfg["id"], position=start, motion=motion, channel=channel,
                      sample_rate_hz=sc_cfg.get("sample_rate_hz",1.0))

    rssi_model = RSSIModel(pl0_db=channel_cfg["pl0_db"], n=channel_cfg["n"], d0_m=1.0,
                           min_d_m=cfg["algos"]["rssi2d"]["min_d_m"],
                           max_d_m=cfg["algos"]["rssi2d"]["max_d_m"])
    multilateration = Multilateration(**cfg["algos"]["multilateration"])
    positions = []
    distances = []

    for t in time_cfg.timeline():
        scanner.step(t, emitters)
        last = scanner.history[-len(emitters):]
        for row, e in zip(last, emitters):
            d = rssi_model.to_distance(e.tx_dbm, row["rssi"])
            positions.append((row["x"], row["y"], row["z"]))
            distances.append(d)
        if len(positions) >= 4:
            est = multilateration.estimate(positions[-10:], distances[-10:])
            if est is not None:
                scanner.log(t, est_x=est[0], est_y=est[1], est_z=est[2])

    out_csv = cfg["io"]["out_csv"]
    write_csv(out_csv, scanner.history)

if __name__ == '__main__':
    main()
