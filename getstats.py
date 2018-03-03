#!/usr/bin/python2

import pycurl

class Stats:
    def __init__(self, numc, tc, tp, tt):
        self.num_connects = numc
        self.time_connect = tc
        self.time_pretransfer = tp
        self.time_total = tt


if __name__ == "__main__":
    f = open("/dev/null", "w")
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://advnet.l8on.org')
    c.setopt(c.WRITEDATA, f)
    c.perform()

    item = Stats(
        c.getinfo(c.NUM_CONNECTS),
        c.getinfo(c.CONNECT_TIME),
        c.getinfo(c.PRETRANSFER_TIME),
        c.getinfo(c.TOTAL_TIME))

    f.close()
