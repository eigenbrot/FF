#!/usr/bin/python
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot_total_hist(outputfile):

    data = np.loadtxt('data.txt')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('N')
    ax.set_xlabel('FF4 Bus Number')
    ax.set_xlim(3600,3680)
    bins = np.arange(3600,3700)
    ax.hist(data, bins=bins, histtype='stepfilled')
    fig.savefig(outputfile)
    plt.close('all')

def update_hist(i, ax, data, bins):
    print(i+1)
    ax.clear()
    ax.set_ylabel('N')
    ax.set_xlabel('FF4 Bus Number')
    try:
        ax.set_xlim(3600,np.max(data[:i+1])+1)
        ax.hist(data[:i + 1], bins=bins, histtype='stepfilled')
    except IndexError:
        ax.hist(data, bins=bins, histtype='stepfilled')

def plot_animation(outputfile):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    data = np.loadtxt('data.txt')
    bins = np.arange(3600,3700)

    random.seed(42)
    predate_idx = random.sample(range(103), k=103)
    data[:103] = data[:103][predate_idx]

    anihist = animation.FuncAnimation(fig, update_hist, data.size+10, fargs=(ax, data, bins))

    ffWriter = animation.writers['ffmpeg']
    writer = ffWriter(fps=6)

    anihist.save(outputfile, writer=writer)

if __name__ == '__main__':
    plot_animation('FF_buses.mp4')