import os, re, sys
from collections import defaultdict

bluecoat_ip_pat = re.compile(r'^199\.91\.13(2\.|5\.254)') #match
index_html_pat = re.compile(r'([0-9.]+).*GET / HTTP/1.1') #search
search_results_pat = re.compile(r'GET /search-results.png ') #search
favicon_pat = re.compile(r'GET /favicon.ico ') #search
track_pat = re.compile(r'GET /track\?url=(.*?) HTTP') #search
access_log_pat = re.compile(r'localhost_access_log.([-0-9]+)\.txt') #match

'''
213.128.218.38 - - [24/Feb/2016:05:52:46 +0000] "GET /right-corner.png HTTP/1.1" 200 3169
213.128.218.38 - - [24/Feb/2016:05:52:47 +0000] "GET /background.png HTTP/1.1" 200 178
213.128.218.38 - - [24/Feb/2016:05:52:47 +0000] "GET /search-results.png HTTP/1.1" 200 207620
213.128.218.38 - - [24/Feb/2016:05:52:47 +0000] "GET /favicon.ico HTTP/1.1" 200 5430
213.128.218.38 - - [24/Feb/2016:05:52:53 +0000] "GET /track?url=axtant HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:05:54:11 +0000] "GET / HTTP/1.1" 200 4621
213.128.218.38 - - [24/Feb/2016:05:54:11 +0000] "GET /right-corner.png HTTP/1.1" 200 3169
213.128.218.38 - - [24/Feb/2016:05:54:11 +0000] "GET /background.png HTTP/1.1" 200 178
213.128.218.38 - - [24/Feb/2016:05:54:11 +0000] "GET /search-results.png HTTP/1.1" 200 207620
213.128.218.38 - - [24/Feb/2016:05:54:12 +0000] "GET /favicon.ico HTTP/1.1" 200 5430
213.128.218.38 - - [24/Feb/2016:05:59:46 +0000] "GET /track?url=axtant HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:00:46 +0000] "GET /track?url=axtant HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:00:55 +0000] "GET /track?url=scip HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:01:35 +0000] "GET /track?url=text HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:01:41 +0000] "GET /track?url=oracle HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:14:43 +0000] "GET / HTTP/1.1" 200 4621
213.128.218.38 - - [24/Feb/2016:06:14:50 +0000] "GET /track?url=text HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:15:06 +0000] "GET /track?url=scip HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:28:49 +0000] "GET / HTTP/1.1" 304 -
213.128.218.38 - - [24/Feb/2016:06:28:49 +0000] "GET /search-results.png HTTP/1.1" 304 -
213.128.218.38 - - [24/Feb/2016:06:28:49 +0000] "GET /background.png HTTP/1.1" 304 -
213.128.218.38 - - [24/Feb/2016:06:28:49 +0000] "GET /right-corner.png HTTP/1.1" 304 -
213.128.218.38 - - [24/Feb/2016:06:28:49 +0000] "GET /favicon.ico HTTP/1.1" 304 -
213.128.218.38 - - [24/Feb/2016:06:28:56 +0000] "GET /track?url=bugtraq HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:29:04 +0000] "GET /track?url=oracle HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:30:20 +0000] "GET /track?url=text HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:30:25 +0000] "GET /track?url=google HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:33:15 +0000] "GET /track?url=google HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:33:30 +0000] "GET /track?url=text HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:41:46 +0000] "GET / HTTP/1.1" 200 4621
213.128.218.38 - - [24/Feb/2016:06:41:46 +0000] "GET /right-corner.png HTTP/1.1" 200 3169
213.128.218.38 - - [24/Feb/2016:06:41:47 +0000] "GET /background.png HTTP/1.1" 200 178
213.128.218.38 - - [24/Feb/2016:06:41:47 +0000] "GET /favicon.ico HTTP/1.1" 200 5430
213.128.218.38 - - [24/Feb/2016:06:41:47 +0000] "GET /search-results.png HTTP/1.1" 200 207620
213.128.218.38 - - [24/Feb/2016:06:42:01 +0000] "GET /track?url=oracle HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:42:44 +0000] "GET /track?url=bugtraq HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:43:00 +0000] "GET /track?url=scip HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:43:17 +0000] "GET /track?url=axtant HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:43:48 +0000] "GET /right-corner.png HTTP/1.1" 200 3169
213.128.218.38 - - [24/Feb/2016:06:43:48 +0000] "GET /background.png HTTP/1.1" 200 178
213.128.218.38 - - [24/Feb/2016:06:43:48 +0000] "GET /search-results.png HTTP/1.1" 200 207620
213.128.218.38 - - [24/Feb/2016:06:45:42 +0000] "GET /track?url=scip HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:45:58 +0000] "GET /track?url=secniche HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:46:51 +0000] "GET /track?url=axtant HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:51:36 +0000] "GET / HTTP/1.1" 200 4621
213.128.218.38 - - [24/Feb/2016:06:51:37 +0000] "GET /background.png HTTP/1.1" 200 178
213.128.218.38 - - [24/Feb/2016:06:51:37 +0000] "GET /right-corner.png HTTP/1.1" 200 3169
213.128.218.38 - - [24/Feb/2016:06:51:39 +0000] "GET /search-results.png HTTP/1.1" 200 207620
213.128.218.38 - - [24/Feb/2016:06:51:41 +0000] "GET /favicon.ico HTTP/1.1" 200 5430
213.128.218.38 - - [24/Feb/2016:06:51:52 +0000] "GET /track?url=bugtraq HTTP/1.1" 404 979
213.128.218.38 - - [24/Feb/2016:06:53:11 +0000] "GET /track?url=next HTTP/1.1" 404 979
'''

looking_for_landing = 1
looking_for_browser_evidence = 2
looking_for_clicks = 3

def count_phish_in_file(f, tallies, day):
    with open(f, 'r') as x:
        lines = x.readlines()
    ip = None
    state = looking_for_landing
    evidence = 0
    line_num = 0
    for line in lines:
        line_num += 1
        if bluecoat_ip_pat.match(line):
            state = looking_for_landing
            ip = None
            evidence = 0
            continue
        m = index_html_pat.search(line)
        if m:
            state = looking_for_browser_evidence
            evidence = 0
            ip = m.group(1)
        elif favicon_pat.search(line) or search_results_pat.search(line):
            evidence += 1
            if evidence >= 2:
                state = looking_for_clicks
                tallies['day=' + day + ', unique visits'] += 1
                tallies['ip=' + ip + ', unique visits'] += 1
                tallies['overall, unique visits'] += 1
        else:
            m = track_pat.search(line)
            if m:
                if state != looking_for_clicks:
                    print("Line " + str(line_num) + ": Found clicks but no prior fetch of / + favicon.ico and search-results.png:\n" + line)
                    continue
                tgt = m.group(1)
                tallies['day=' + day + ', total clicks'] += 1
                tallies['day=' + day + 'tgt=' + tgt + ', total clicks'] += 1
                tallies['ip=' + ip + ', total clicks'] += 1
                tallies['ip=' + ip + 'tgt=' + tgt + ', total clicks'] += 1
                tallies['overall, total clicks'] += 1
                tallies['tgt=' + tgt + ', total clicks'] += 1
                if evidence >= 2:
                    evidence = 0
                    tallies['day=' + day + ', at least 1 click'] += 1
                    tallies['day=' + day + 'tgt=' + tgt + ', at least 1 click'] += 1
                    tallies['ip=' + ip + ', at least 1 click'] += 1
                    tallies['ip=' + ip + 'tgt=' + tgt + ', at least 1 click'] += 1
                    tallies['overall, at least 1 click'] += 1


def summarize(tallies):
    keys = sorted(tallies.keys())
    for key in keys:
        print('%s: %s' % (key, tallies[key]))


def count_phish(folder):
    tallies = defaultdict(int)
    for fname in os.listdir(folder):
        m = access_log_pat.match(fname)
        if m:
            day = m.group(1)
            count_phish_in_file(os.path.join(folder, fname), tallies, day)
    summarize(tallies)
    

if __name__ == '__main__':
    folder = '.'
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    count_phish(folder)