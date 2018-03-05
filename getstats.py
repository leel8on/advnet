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

    def __str__(self):
    	print("Stats ID:" + str(id(self)))
    	return ' #_conn: %d\n t_conn: %f\n t_prtf: %f\n t_totl: %f' % (
    		self.num_connects, 
    		self.time_connect, 
    		self.time_pretransfer, 
    		self.time_total);

    

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
        a.perform()
        lst.append(Stats(
            a.getinfo(a.NUM_CONNECTS),
            a.getinfo(a.CONNECT_TIME),
            a.getinfo(a.PRETRANSFER_TIME),
            a.getinfo(a.TOTAL_TIME)))

    f.close()

if __name__ == "__main__":

    # All the variations of the sites
    texturl = 'http://advnet.l8on.org'
    texturltls = 'https://advnet.l8on.org'
    imgurl = 'http://advnet.l8on.org:8080'
    imgurltls = 'https://advnet.l8on.org:8081'
    mimgurl = 'http://advnet.l8on.org:8082'
    mimgurltls = 'https://advnet.l8on.org:8083'


    runstats(texturl, 1, text1)
    runstats(texturltls, 1, text1tls)
    runstats(texturltls, 2, text2)

    print(SampleMean(text1));
    print(SampleMean(img1));
    print(SampleMean(multi1));

    for i in range(len(text1)):
        print text1[i].time_total
