"""Plotting utilities."""
import matplotlib.pyplot as plt
import numpy as np


def save_heatmap(xx, yy, zz, path: str):
    plt.figure()
    plt.pcolormesh(xx, yy, zz, shading='auto')
    plt.colorbar(label='RSSI')
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.savefig(path)
    plt.close()
