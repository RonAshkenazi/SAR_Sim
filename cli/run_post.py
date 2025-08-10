"""Offline post-processing using Gaussian Process Regression."""
import argparse
import json
import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from io.config import load_config
from visualize.heatmap import save_heatmap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    csv_path = cfg["io"]["out_csv"]
    data = pd.read_csv(csv_path)
    xs = data['x'].values
    ys = data['y'].values
    rssi = data['rssi'].values
    X = np.column_stack((xs, ys))
    kernel = RBF(length_scale=cfg["algos"]["gp"].get("length_scale",10.0)) + WhiteKernel(noise_level=cfg["algos"]["gp"].get("noise",1.0))
    gp = GaussianProcessRegressor(kernel=kernel)
    gp.fit(X, rssi)

    env = cfg['space']
    grid_res = cfg['algos']['pf'].get('grid_res', 2.0)
    gx = np.arange(0, env['x']+grid_res, grid_res)
    gy = np.arange(0, env['y']+grid_res, grid_res)
    xx, yy = np.meshgrid(gx, gy)
    Xpred = np.column_stack((xx.ravel(), yy.ravel()))
    mean, std = gp.predict(Xpred, return_std=True)
    mean = mean.reshape(xx.shape)
    std = std.reshape(xx.shape)
    out_dir = cfg['io'].get('out_dir','runs')
    save_heatmap(xx, yy, mean, f"{out_dir}/heatmap.png")
    save_heatmap(xx, yy, std, f"{out_dir}/uncertainty.png")
    idx = np.unravel_index(np.argmax(mean), mean.shape)
    peak = {"x": float(xx[idx]), "y": float(yy[idx]), "rssi": float(mean[idx])}
    with open(f"{out_dir}/peak.json", 'w') as f:
        json.dump(peak, f)

if __name__ == '__main__':
    main()
