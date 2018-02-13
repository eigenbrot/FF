#!/usr/bin/python
import sys
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
        ax.set_xlim(3600 - 0.5,np.max(data[:i+1])+0.5)
        ax.hist(data[:i + 1], bins=bins, histtype='stepfilled')
    except IndexError:
        ax.hist(data, bins=bins, histtype='stepfilled')
    try:
        ax.axvline(x=data[i], color='r', lw='0.7')
    except IndexError:
        ax.axvline(x=data[-1], color='r', lw='0.7')

def plot_animation(outputfile):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    data = np.loadtxt('data.txt')
    bins = np.arange(3600,3700) - 0.5

    random.seed(42)
    predate_idx = random.sample(range(103), k=103)
    data[:103] = data[:103][predate_idx]

    anihist = animation.FuncAnimation(fig, update_hist, data.size+10, fargs=(ax, data, bins))

    ffWriter = animation.writers['ffmpeg']
    writer = ffWriter(fps=6)

    anihist.save(outputfile, writer=writer)

def print_stats():

    data = np.loadtxt('data.txt')

    hist, be = np.histogram(data, bins=np.arange(3600,3700))
    be = be[:-1]
    nzid = np.where(hist > 0)
    maxbus = np.max(be[nzid])
    minbus = np.min(be[nzid])

    sortid = np.argsort(hist)[::-1]
    sorted_bus = be[sortid]
    sorted_hist = hist[sortid]
    print('Top 3 buses:')
    for i in range(3):
        print('\t{} - {}'.format(sorted_bus[i], sorted_hist[i]))

    missingid = np.where((be >= minbus) & (be <= maxbus) & (hist == 0))[0]
    print('Missing buses:')
    for i in missingid:
        print('\t{}'.format(be[i]))

    return

def print_bus(bus):

    data = np.loadtxt('data.txt')
    idx = np.where(data == bus)[0]

    print('bus {} has been ridden {} times'.format(bus, idx.size))

    return

if __name__ == '__main__':

    try:
        if sys.argv[1] == '-m':
            plot_animation('FF_buses.mp4')
        elif sys.argv[1] == '-b':
            print_bus(int(sys.argv[2]))
        else:
            print_stats()
    except IndexError:
        print_stats()
