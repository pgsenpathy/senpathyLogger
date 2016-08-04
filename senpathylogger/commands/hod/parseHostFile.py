import sys

def parseHostFile(hostFileName):
    hosts = {}
    with open(hostFileName) as f:
        for line in f:
            a = line.split()
            try:
                dept = a[0]
                hostname = a[1]
            except IndexError as e:
                sys.exit("Note: Your hostnames file has some issues\n" + \
                         "\t\tThis could be possible due to empty lines\n" + \
                         "\t\tOr due to missing hostname or departname")
            hosts[hostname] = dept
    return hosts