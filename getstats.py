#!/usr/bin/python2

import pycurl

# HTTP 1.1 No TLS
alist = []

# HTTP 1.1 With TLS
blist = []

# HTTP 2 With TLS
clist = []





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
		print(l)
		conn_sum += l.num_connects 
		time_sum += l.time_connect
		prtm_sum += l.time_pretransfer
		totm_sum += l.time_total

	return Stats(conn_sum / len(ls), 
				 time_sum / len(ls), 
				 prtm_sum / len(ls), 
				 totm_sum / len(ls))

if __name__ == "__main__":
    f = open("/dev/null", "w")

    # HTTP 1.1 No TLS
    a = pycurl.Curl()
    a.setopt(a.URL, 'http://advnet.l8on.org')
    a.setopt(a.HTTP_VERSION, a.CURL_HTTP_VERSION_1_1)
    a.setopt(a.WRITEDATA, f)

    # HTTP 1.1 With TLS
    b = pycurl.Curl()
    b.setopt(b.URL, 'https://advnet.l8on.org')
    b.setopt(b.HTTP_VERSION, b.CURL_HTTP_VERSION_1_1)
    b.setopt(b.WRITEDATA, f)

    # HTTP 2 With TLS
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://advnet.l8on.org')
    c.setopt(c.HTTP_VERSION, c.CURL_HTTP_VERSION_2_0)
    c.setopt(c.WRITEDATA, f)

    for i in range(100):
        a.perform()
        alist.append(Stats(
            a.getinfo(a.NUM_CONNECTS),
            a.getinfo(a.CONNECT_TIME),
            a.getinfo(a.PRETRANSFER_TIME),
            a.getinfo(a.TOTAL_TIME)))

    for i in range(100):
        b.perform()
        blist.append(Stats(
            b.getinfo(b.NUM_CONNECTS),
            b.getinfo(b.CONNECT_TIME),
            b.getinfo(b.PRETRANSFER_TIME),
            b.getinfo(b.TOTAL_TIME)))

    for i in range(100):
        c.perform()
        clist.append(Stats(
            c.getinfo(c.NUM_CONNECTS),
            c.getinfo(c.CONNECT_TIME),
            c.getinfo(c.PRETRANSFER_TIME),
            c.getinfo(c.TOTAL_TIME)))

    print(SampleMean(alist));
    print(SampleMean(blist));
    print(SampleMean(clist));

    f.close()
