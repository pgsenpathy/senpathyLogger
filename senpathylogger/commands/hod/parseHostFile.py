def parseHostFile(hostFileName):
    hosts = {}
    with open(hostFileName) as f:
        for line in f:
            print line
            a = line.split()
            dept = a[0]
            hostname = a[1]
            hosts[a[1]] = a[0]
    return hosts