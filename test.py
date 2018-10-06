from scapy.all import *
import time

# target = ["10.2.10.2"]
    
# t, unans = traceroute(target,l4=UDP(sport=1234), dport=1234)


from scapy.all import *
import sys
host_ip = "10.2.10.2"

paths = {
    (22,80): ["l1", "s1", "c2", "s4", "l3"],
    (123,123): ["l1", "s1", "c1", "s3", "l3"],
    (22,22): ["l1", "s2", "c1", "s3", "l3"],
    (80,80): ["l1", "s2", "c2", "s3", "l3"],
    (443,443): ["l1", "s2", "c1", "s4", "l3"],
    (61477,32126): ["l1", "s1", "c1", "s4", "l3"]
}

def test_4_ports(sport, dport, timeout=2):
    path = []
    for i in range(1, 28):
        pkt = IP(dst=host_ip, ttl=i) / UDP(sport=sport, dport=dport)
        # Send the packet and get a reply
        reply = sr1(pkt, verbose=0, timeout=timeout)
        if reply is None:
            break
        elif reply.type == 3:
            # We've reached our destination
            break
        else:
            # We're in the middle somewhere
            path.append(reply.src);

    return path

def calculatePaths():
    global paths
    paths = {}
    while len(links.keys()) < 8:
        sport = RandShort()
        dport = RandShort()
        print(sport, dport)
        path = test_4_ports(sport, dport)
        if path not in links.values():
            paths[(int(sport), int(dport))] = path


#calculateLinks()
#for ports, link in paths.items():
#    print(ports, ":",link)

def path_is_up(ports):
    for _ in range(5):
        sport, dport = ports
        pkt = IP(dst=host_ip) / UDP(sport=sport, dport=dport)
        reply = sr1(pkt, verbose=0, timeout=1)
        if reply is not None:
            print(sport, dport)
            return True

    return False

def get_links(path):
    links = []
    for i in range(len(path)-1):
        links.append((path[i], path[i+1]))
    return links

while(True):
    time.sleep(1)
    paths_status = [(ports, path, path_is_up(ports)) for ports, path in paths.items()]
    print(paths_status)

    links = {}

    for port, path, is_up in paths_status:
        print("Path:", port, is_up, path)
        #print("Links:", get_links(path))
        if is_up:
            for link in get_links(path):
                links[link] = True
        else:
            for link in get_links(path):
                if link not in links:
                    links[link] = False
        # print("After adding:", links)

    print(links)
    with open("ajax_info.txt", "w") as f:
        output = '\n'.join(["%s-%s" % link for link, up in links.items() if not up])

        f.write(output)
        print(output)
            
