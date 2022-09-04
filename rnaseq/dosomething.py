import sys,gzip
par = sys.argv
with gzip.open(par[1]) as IN:
    for li in IN:
        print(li.strip())
