#!/usr/bin/python2

import pycurl
import numpy
import math
import matplotlib.pyplot as plt

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

# Total Sample Mean 
text1_sm = []
text1tls_sm = []
text2_sm = []

img1_sm = []
img1tls_sm = []
img2_sm = []

multi1_sm = []
multi1tls_sm = []
multi2_sm = []

#simulation runs
text1_n = 0
text1tls_n = 0
text2_n = 0

img1_n = 0
img1tls_n = 0
img2_n = 0

multi1_n = 0
multi1tls_n = 0
multi2_n = 0

# Stats Class 
class Stats:
    def __init__(self, numc, tc, tp, tt):
        self.num_connects = numc
        self.time_connect = tc
        self.time_pretransfer = tp
        self.time_total = tt

    def __str__(self):
    	print("Stats ID:" + str(id(self)))
    	return ' #_conn: %d\n t_conn: %f\n t_prtf: %f\n t_totl: %f' % (
    		self.num_connects, 
    		self.time_connect, 
    		self.time_pretransfer, 
    		self.time_total);

# Sample Mean 
def SampleMean(ls):
	conn_sum = 0.0
	time_sum = 0.0
	prtm_sum = 0.0
	totm_sum = 0.0
	for l in ls:
		conn_sum += l.num_connects 
		time_sum += l.time_connect
		prtm_sum += l.time_pretransfer
		totm_sum += l.time_total

	return Stats(conn_sum / len(ls), 
				 time_sum / len(ls), 
				 prtm_sum / len(ls), 
				 totm_sum / len(ls))

# runstats
def runstats(urlstr, version, lst, sm_lst, n):
    f = open("/dev/null", "w")
    
    a = pycurl.Curl()
    a.setopt(a.URL, urlstr)
    if version == 1:
        a.setopt(a.HTTP_VERSION, a.CURL_HTTP_VERSION_1_1)
    else:
        a.setopt(a.HTTP_VERSION, a.CURL_HTTP_VERSION_2_0)
    a.setopt(a.WRITEDATA, f)

    # getting a baseline
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

        sm_lst.append(SampleMean(lst));

        a.close()

    # for l in lst:
    # 	print(l)

    # get to a init confidence interval
    total_time = []
    for l in lst:
    	total_time.append(l.time_total)

    # for l in total_time:
    #  	print(l)

    vari = numpy.var(total_time);
    #print(vari)

    z_val = 1.645

    conf = (2 * math.sqrt(vari) * z_val) / (math.sqrt(len(total_time)));
    #print(str(conf) + " > " + str(numpy.float(sm_lst[-1].time_total * .1)))

    #while(numpy.float64(sm_lst[-1].time_total * .1) <= conf):
    while (conf > .0015):
    	#print(str(conf) + " > " + str(.0015))
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

        sm_lst.append(SampleMean(lst));
        total_time.append(lst[-1].time_total);
        conf = (2 * math.sqrt(numpy.var(total_time)) * 1.645) / (math.sqrt(len(total_time)));
       # print(str(conf) + " > " + str(numpy.float64(sm_lst[-1].time_total * .1)))

    print("took: " + str(len(total_time)));
    n = len(total_time);
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
    print("\ntext only")

    print("--text1")
    runstats(texturl, 1, text1, text1_sm, text1_n)
    print("Runs: " + str(text1_n))
    print("Sample Mean: " + str(SampleMean(text1)));
    
    print("--texturltls")
    runstats(texturltls, 1, text1tls, text1tls_sm, text1tls_n)
    print("Runs: " + str(text1tls_n))
    print("Sample Mean: " + str(SampleMean(text1tls)));
    
    print("--texturltls 2")
    runstats(texturltls, 2, text2, text2_sm, text2_n)
    print("Runs: " + str(text2_n))
    print("Sample Mean: " + str(SampleMean(text2)));

    # Single source image sites
    print("\nimages from 1 source")

    print("--imgurl")
    runstats(imgurl, 1, img1, img1_sm, img1_n)
    print("Runs: " + str(img1_n))
    print("Sample Mean: " + str(SampleMean(img1)));
    
    print("--imgurltls")
    runstats(imgurltls, 1, img1tls, img1_sm, img1_n)
    print("Runs: " + str(img1_n))
    print("Sample Mean: " + str(SampleMean(img1tls)));
    
    print("--imgurltls 2")
    runstats(imgurltls, 2, img2, img2_sm, img2_n)
    print("Runs: " + str(img2_n))
    print("Sample Mean: " + str(SampleMean(img2)));

    # Multi source image sites
    print("\nimages from 1 source")
    
    print("--mimgurl")
    runstats(mimgurl, 1, multi1, multi1_sm, multi1_n)
    print("Runs: " + str(multi1_n))
    print("Sample Mean: " + str(SampleMean(multi1)));
    
    print("--mimgurltls")
    runstats(mimgurltls, 1, multi1tls, multi1tls_sm, multi1tls_n)
    print("Runs: " + str(multi1tls_n))
    print("Sample Mean: " + str(SampleMean(multi1tls)));
    
    print("--mimgurltls 2")
    runstats(mimgurltls, 2, multi2, multi2_sm, multi2_n)
    print("Runs: " + str(multi2_n))
    print("Sample Mean: " + str(SampleMean(multi2)));
 
    print("\nDONE!")
