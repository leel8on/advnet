#!/usr/bin/python2

import pycurl

# Object lists for text only site
text1 = []
text1tls = []
text2 = []

# Lists for single source image site
img1 = []
img1tls = []
img2 = []

# Lists for multi source image site
multi1 = []
multi1tls = []
multi2 = []

class Stats:
    def __init__(self, numc, tc, tp, tt):
        self.num_connects = numc
        self.time_connect = tc
        self.time_pretransfer = tp
        self.time_total = tt


def runstats(urlstr, version, lst):
    f = open("/dev/null", "w")
    a = pycurl.Curl()
    a.setopt(a.URL, urlstr)
    if version == 1:
        a.setopt(a.HTTP_VERSION, a.CURL_HTTP_VERSION_1_1)
    else:
        a.setopt(a.HTTP_VERSION, a.CURL_HTTP_VERSION_2_0)
    a.setopt(a.WRITEDATA, f)

    for i in range(100):
        a = pycurl.Curl()
        a.setopt(a.URL, urlstr)
        if version == 1:
            a.setopt(a.HTTP_VERSION, a.CURL_HTTP_VERSION_1_1)
        else:
            a.setopt(a.HTTP_VERSION, a.CURL_HTTP_VERSION_2_0)
        a.setopt(a.WRITEDATA, f)
        a.perform()
        lst.append(Stats(
            a.getinfo(a.NUM_CONNECTS),
            a.getinfo(a.CONNECT_TIME),
            a.getinfo(a.PRETRANSFER_TIME),
            a.getinfo(a.TOTAL_TIME)))
        a.close()
    f.close()


if __name__ == "__main__":

    # All the variations of the sites
    texturl = 'http://advnet.l8on.org'
    texturltls = 'https://advnet.l8on.org'
    imgurl = 'http://advnet.l8on.org:8080'
    imgurltls = 'https://advnet.l8on.org:8081'
    mimgurl = 'http://advnet.l8on.org:8082'
    mimgurltls = 'https://advnet.l8on.org:8083'

    # Text only sites
    runstats(texturl, 1, text1)
    runstats(texturltls, 1, text1tls)
    runstats(texturltls, 2, text2)

    # Single source image sites
    runstats(imgurl, 1, img1)
    runstats(imgurltls, 1, img1tls)
    runstats(imgurltls, 2, img2)
    
    # Multi source image sites
    runstats(mimgurl, 1, multi1)
    runstats(mimgurltls, 1, multi1tls)
    runstats(mimgurltls, 2, multi2)
 
    for i in range(len(text1)):
        print text1[i].num_connects
