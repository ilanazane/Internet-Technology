import socket as mysoc
import sys
import threading


outputStr = ""

def clientrs():
    global outputStr
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    rsPort = int(sys.argv[2])
    rsIP = mysoc.gethostbyname(sys.argv[1])

    # connect to the server on local machine
    rsServerBinding = (rsIP, rsPort)
    try:
        cs.connect(rsServerBinding)
    except:
        print("Invalid RS port number or hostname.")
        exit()
    with open("./PROJI-HNS.txt", "a") as myfile:
        myfile.write("STOP")

    # open file with hostnames to be queried
    inputFile = open('./PROJI-HNS.txt', "r")


    # send number of lines
    lineCount = len(inputFile.readlines())
    #
    # cs.send(str(lineCount).encode('utf-8'))
    # print("[C] client sent lineCount", lineCount)
    # # send hostnames to RS11
    inputFile.seek(0)
    tsHost = ""



    for queriedHostname in inputFile:
        print("host name", queriedHostname)
        cs.send(queriedHostname.encode('utf-8'))
        print("[C] client sent host name: ", queriedHostname)
        queriedHostname = queriedHostname[0:len(queriedHostname) - 1]
        # receive and use RS's response
        rsResponse = str(cs.recv(250).decode('utf-8'))
        print("[S]: response", rsResponse)
        rsResponseSplit = rsResponse.split(" ")
        if rsResponse == "terminated":
            break
        if (rsResponseSplit[2].rstrip() == "NS" and rsResponse!="terminated"):
            print("sent to TS")
            tsHost = rsResponseSplit[0].rstrip()
            tsThread = threading.Thread(
                name='clientts', target=clientts, args=(tsHost, queriedHostname))  # ts thread
            tsThread.start()
            tsThread.join()
        elif (rsResponseSplit[2].rstrip() == "A" and rsResponse != "terminated"):
            outputStr = outputStr + rsResponse + "\n"
        else:
            print("Invalid response from the RS server.")
        if queriedHostname == "STOP":
            break

# send fin message to ts server
    print("GOT OUT OF LOOP")
    tsThread = threading.Thread(
        name='clientts', target=clientts, args=(tsHost, "$END$"))  # ts thread
    tsThread.start()
    tsThread.join()

# write output
    outputFile = open("./RESOLVED.txt", "w")
    output = outputStr.rstrip()
    print("outputstring",output)
    outputFile.write(output)

# closing procedures
    outputFile.close()
    inputFile.close()
    cs.close()
    exit()


def clientts(tsHostname, queriedHostname):
    global outputStr
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

# Define the port on which you want to connect to the server
    tsPort = int(sys.argv[3])
    tsIP = mysoc.gethostbyname(tsHostname)

# connect to the server on local machine
    try:
        server_binding = (tsIP, tsPort)
        cs.connect(server_binding)
    except mysoc.error as error:
        print(error)
        exit()

# send queried hostname to TS server
    cs.send(queriedHostname.encode('utf-8'))
    print("END",queriedHostname)
# output message from TS to output file
    tsResponse = str(cs.recv(250).decode('utf-8'))
    print("[C]:tsResponse",tsResponse)
    #global outputStr
    if tsResponse != "terminated":
        outputStr += tsResponse + "\n"

# closing procedures
    cs.close()
    exit()

if (len(sys.argv) != 4):
    sys.exit("Improper number of arguments. Please try again with 3 arguments.")

rsThread = threading.Thread(name='clientrs', target=clientrs)  # rs thread
rsThread.start()

exit()
