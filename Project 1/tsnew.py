import socket as mysoc
import sys
import threading


def createDICT(filenm):
    ts_file = open(filenm, "r")
    dns_table_ts = {}
    for line in ts_file:
        #print("line",line)
        line_split = line.split()
        dns_table_ts[line_split[0]] = (line_split[1], line_split[2])
    lower_dict = {}
    #print("dns table",dns_table_ts)
    for x in dns_table_ts:
        lower_dict[x.lower()] = (x, dns_table_ts.get(x)[0], dns_table_ts.get(x)[1])
    return lower_dict
    ts_file.close()


def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{}} \n'.format("socket open error ", err))
    tsListenPort = int(sys.argv[1])
    server_binding = ('', tsListenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)

    lower_dict = createDICT ('./PROJI-DNSTS.txt')
    print('lower_dict',lower_dict)
    hostNameMessage = ""
    while(hostNameMessage != "$END$"):
        csockid, addr = ss.accept()
        print("[TS]: Got a connection request from a client at", addr)

        retMessage = ""
        # get host name from client
        hostNameMessage = csockid.recv(250).decode('utf-8')
        hostNameMessage = str(hostNameMessage).replace("\r","").lower()
        print("[TS]: received host hostNameMessage", hostNameMessage)
        if (hostNameMessage != "$end$"):
            if hostNameMessage.lower() in lower_dict:
                value = lower_dict.get(hostNameMessage.lower())
                hostName = value[0]
                ip_add = value[1]
                flag = value[2]
                retMessage = hostName + " " + ip_add + " " + flag
            else:
                retMessage = hostNameMessage + " - Error:HOST NOT FOUND"
            print("retmessage",retMessage)
            csockid.send(retMessage.encode('utf-8'))
        else:
            retMessage == "terminated"
            print("HERE")
            csockid.send(retMessage.encode('utf-8'))
            break
    print("finished")



if (len(sys.argv) != 2):
    sys.exit("Improper number of arguments. Please try again with 1 argument.")

t1 = threading.Thread(name='server', target=server)
t1.start()
