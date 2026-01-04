#!/usr/bin/env python3

import argparse
import math

# default amount of stations, can be setted by "--stations" argument
DEFAULT_STATIONS = 20

# default payload size
DEFAULT_PAYLOAD = 15000

SIFS = 10   # SIFS, in microseconds
DIFS = 50   # DIFS, in microseconds
SIGMA = 20  # slot time, in microseconds
DELTA = 0   # propagation time, typically very small

PHYH = 72 + 24      # Physical Header, in microseconds
MACH = 272 / 11     # MAC Header in IEEE 802.11, in microseconds

# ACK duration, in microseconds: 112 bits at 11Mbps + Physical Header duration
ACK = 112 / 11 + PHYH

# Equivalent duration of MAC header + PHY header
TotalH = PHYH + MACH


def Ts(x):
    """First equation (14)"""
    return TotalH + x / 11 + SIFS + DELTA + ACK + DIFS + DELTA

def Tc(x):
    """Second equation (14)"""
    return TotalH + x / 11 + DIFS + DELTA

def thau(x, sta):
    """Equation (28)"""
    return 1 / (sta * math.sqrt(Tc(x) / (2 * SIGMA)))

def ptr(x, sta):
    """Equation (10)"""
    return 1 - (1 - thau(x, sta)) ** sta

def ps(x, sta):
    """Equation (11)"""
    return sta * thau(x, sta) * (1 - thau(x, sta)) ** (sta - 1) / ptr(x, sta)

def efficiency(x, sta):
    """Equation (25). Computes the efficiency."""
    return (x / 11) / (Ts(x) - Tc(x) + (SIGMA * (1 - ptr(x, sta)) / ptr(x, sta) + Tc(x)) / ps(x, sta))


def efficiency_payload_range(args):
    """Compute and plot the efficiency range with a fixed station value"""
    import matplotlib.pyplot as plt
    import numpy as np

    if (args.p[0] >= args.p[1]):
        print("Error, payload start range must be lower that payload end")
        exit(1)

    x = np.arange(args.p[0], args.p[1])
    y = [efficiency(_, args.s) for _ in x]

    _, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title('Efficiency 802.11b')
    ax.set_title('Efficiency of a payload range ({stations} stations)'.format(stations=args.s))
    ax.set_xlabel('Payload range in bits')
    ax.set_ylabel('Efficiency')
    plt.plot(x, y, 'r')
    plt.grid()
    plt.show()


def efficiency_station_range(args):
    """Compute and plot the efficiency range with a fixed payload value"""
    import matplotlib.pyplot as plt
    import numpy as np

    if (args.s[0] >= args.s[1]):
        print("Error, station start range must be lower that station end")
        exit(1)

    x = np.arange(args.s[0], args.s[1])
    y = [efficiency(args.p, _) for _ in x]

    _, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title('Efficiency 802.11b')
    ax.set_title('Efficiency of a station range ({payload} payload in bits)'.format(payload=args.p))
    ax.set_xlabel('Station range')
    ax.set_ylabel('Efficiency')
    plt.plot(x, y, 'r')
    plt.grid()
    plt.show()


def efficiency_no_range(args):
    print("Stations: ", args.s, "\nPayload: ", args.p)
    print(efficiency(args.p, args.s))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, nargs='?', default=DEFAULT_PAYLOAD, help='payload size in bits')
    parser.add_argument('-s', type=int, nargs='?', default=DEFAULT_STATIONS, help='number of stations')
    parser.set_defaults(func=efficiency_no_range)

    subparsers = parser.add_subparsers(help='allow to configure ranges of stations or ranges of payloads')
    
    parser_payload_range = subparsers.add_parser('payload_range', help='allow to input a range of payloads [FROM] [TO]')
    parser_payload_range.add_argument('p', type=int, nargs=2, help='FROM and TO payload range')
    parser_payload_range.add_argument('-s', type=int, nargs='?', default=DEFAULT_STATIONS, help='number of stations, defaults to 20')
    parser_payload_range.set_defaults(func=efficiency_payload_range)

    parser_station_range = subparsers.add_parser('station_range', help='allow to input a range of stations [FROM] [TO]')
    parser_station_range.add_argument('-p', type=int, nargs='?', default=DEFAULT_PAYLOAD, help='payload size in bits')
    parser_station_range.add_argument('s', type=int, nargs=2, help='FROM and TO station range')
    parser_station_range.set_defaults(func=efficiency_station_range)

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
