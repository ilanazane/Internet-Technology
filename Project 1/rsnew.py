import socket as mysoc
import sys
import threading

def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    rsListenPort = int(sys.argv[1])
    server_binding = ('', rsListenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)

    # creating table data structure
    dns_table_rs = {}
    rs_file = open('./PROJI-DNSRS.txt', "r")

    TSHost = ""

    for line in rs_file:
        line_split = line.split()
        if (line_split[2] == "NS"):
            TSHost = line[0:len(line)-1].replace("\r","")
            print("TSHOST",TSHost)
        else:
            dns_table_rs[line_split[0]] = (line_split[1], line_split[2])

        # create lower-case dictionary, same tuple value
    lower_dict = {}
    for x in dns_table_rs:
        lower_dict[x.lower()] = (x, dns_table_rs.get(x)
                                 [0], dns_table_rs.get(x)[1])

    # number of strings received from client
    # numMessages = int(csockid.recv(6).decode('utf-8'))
    # retMessage = ""
    # print("[S]: Server received nummessages" ,numMessages)
    print("dict",lower_dict)
    hostNameMessage= ""
    while(hostNameMessage != "STOP"):
        hostNameMessage = csockid.recv(250).decode('utf-8')
        hostNameMessage = str(hostNameMessage).replace("\r\n","").lower()
        print("[S]: Server received hostname",hostNameMessage)
        temp=hostNameMessage
        #hostNameMessage = hostNameMessage[0:len(hostNameMessage) - 1]
        print("hostnameMessage2",hostNameMessage)
        if temp != "stop":
            if hostNameMessage in lower_dict:
                value = lower_dict.get(hostNameMessage)
                #print("HERE")
                hostName = value[0]
                ip_add = value[1]
                flag = value[2]
                retMessage = hostName + " " + ip_add + " " + flag
            else:
                # send TShostname + NS flag
                retMessage = TSHost
            #print(retMessage)
            print("[S]: Server sending message",retMessage)
            csockid.send(retMessage.encode('utf-8'))
        else:
            retMessage = "terminated"
            csockid.send(retMessage.encode('utf-8'))
            break
    print("RS LOOP FINISHED")
    rs_file.close()


if (len(sys.argv) != 2):
    sys.exit("Needs 2 args")

t1 = threading.Thread(name='server', target=server)
t1.start()
