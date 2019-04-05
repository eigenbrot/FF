#!/usr/bin/python
import os
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

DATA_FILE = '/home/ade/PycharmProjects/FF/data.txt'

def plot_total_hist(outputfile):

    data = np.loadtxt(DATA_FILE)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('N')
    ax.set_xlabel('FF4 Bus Number')
    ax.set_xlim(np.min(data) - 1, np.max(data) + 1)
    bins = np.arange(3600,3700) - 0.5

    colors = ['#a6cee3','#1f78b4','#b2df8a']
    ax.hist(data, bins=bins, histtype='stepfilled', label='All', color=colors[-1])
    ax.hist(data[-120:], bins=bins, histtype='stepfilled', color=colors[-2], label='Last 120 rides')
    ax.hist(data[-30:], bins=bins, histtype='stepfilled', color=colors[0], label='Last 30 rides')
    ax.legend(loc=0, frameon=False)
    fig.savefig(outputfile)
    plt.close('all')

def update_hist(i, ax, data, bins, cols, numframes):
    print('\r[{{:<{}}}]'.format(cols).format('='*int(cols*(i+1)/numframes)),end='')
    ax.clear()
    ax.set_ylabel('N')
    ax.set_xlabel('FF4 Bus Number')
    try:
        ax.set_xlim(3600 - 0.5,np.max(data[:i+1])+0.5)
        ax.hist(data[:i + 1], bins=bins, histtype='stepfilled')
    except IndexError:
        ax.hist(data, bins=bins, histtype='stepfilled')
    try:
        ax.axvline(x=data[i], color='r', lw='0.7')
    except IndexError:
        ax.axvline(x=data[-1], color='r', lw='0.7')

def plot_animation(outputfile, fps=12):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    data = np.loadtxt(DATA_FILE)
    bins = np.arange(3600,3700) - 0.5

    random.seed(42)
    predate_idx = random.sample(range(103), k=103)
    data[:103] = data[:103][predate_idx]

    rows, cols = os.popen('stty size','r').read().split()
    cols = int(cols) - 2
    numframes = data.size + fps * 2
    anihist = animation.FuncAnimation(fig, update_hist, numframes, fargs=(ax, data, bins, cols, numframes))

    ffWriter = animation.writers['ffmpeg']
    writer = ffWriter(fps=fps)

    print('Making movie...')
    anihist.save(outputfile, writer=writer)

def print_stats():

    data = np.loadtxt(DATA_FILE)

    buses = []
    hists = []
    for lookback in [-30, -120, 0]:
        hist, be = np.histogram(data[lookback:], bins=np.arange(3600,3700))
        be = be[:-1]
        nzid = np.where(hist > 0)
        maxbus = np.max(be[nzid])
        minbus = np.min(be[nzid])

        sortid = np.argsort(hist)[::-1]
        buses.append(be[sortid])
        hists.append(hist[sortid])

    print('Top 3 buses:')
    print('{:20}{:20}{:20}'.format('last 30 rides', 'last 120 rides', 'all time'))
    for i in range(3):
        str = ''
        for j in range(3):
            str += '{:20}'.format('{} - {}'.format(buses[j][i], hists[j][i]))
        print(str)

    missingid = np.where((be >= minbus) & (be <= maxbus) & (hist == 0))[0]
    print('Missing buses:')
    for i in missingid:
        print('\t{}'.format(be[i]))

    return

def print_bus(bus):

    data = np.loadtxt(DATA_FILE)
    idx = np.where(data == bus)[0]

    print('bus {} has been ridden {} times'.format(bus, idx.size))

    return

def compute_run_prob(bus, run_length, N=10000, flat_prob=False):

    data = np.loadtxt(DATA_FILE)
    numrides = data.shape[0]
    buses, nums = np.unique(data, return_counts=True)
    probs = nums/np.sum(nums)
    if flat_prob:
        probs = probs * 0 + 1./buses.size

    seq_count = 0
    for i in range(N):

        all_rides = np.random.choice(buses, size=numrides, p=probs)
        for j in range(numrides - run_length):
            if np.array_equal(all_rides[j:j+run_length], np.array([bus] * run_length)):
                seq_count += 1
                break

    return seq_count / N

if __name__ == '__main__':

    try:
        if sys.argv[1] == '-m':
            try:
                fps = int(sys.argv[2])
            except:
                fps = 12
            plot_animation('/home/ade/PycharmProjects/FF/FF_buses.mp4', fps)
        elif sys.argv[1] == '-b':
            print_bus(int(sys.argv[2]))
        elif sys.argv[1] == '-p':
            plot_total_hist('/home/ade/PycharmProjects/FF/FF_hist.png')
            os.system('feh /home/ade/PycharmProjects/FF/FF_hist.png &')
        else:
            print_stats()
    except IndexError:
        print_stats()
