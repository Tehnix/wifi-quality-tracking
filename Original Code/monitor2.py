##############Modules################
import time
import csv
from pythonwifi.iwlibs import Wireless
from datetime import datetime
from subprocess import call
from subprocess import check_output
import pyping
from collections import Counter
############Modules end##############

#change the value of "filename" to the file name/path you want it to save as on Dropbox
filename= "test2.csv"



########Dont change anything below this line########

time.sleep(30) #sleeping so it won't measure before having Internet connection
wifi=Wireless('wlan0')
while(True):
    #getting the date and time
    kl=str(datetime.now())
    channels={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0} #dictionary with channels
    try:
        signal= wifi.getStatistics()[1].getSignallevel() #signallevel
        stoj= wifi.getStatistics()[1].getNoiselevel() #noiselevel
        freq = wifi.getFrequency() #getting frequency being used
        num, rates=wifi.getChannelInfo() #getting frequencies available
        channel=rates.index(freq)+1 #getting the channel number
    except:
        signal=0
        stoj=0
        channel=-1
    #Getting the channels in use nearby
    try:
        scan=check_output(["iwlist", "wlan0", "scan"]) #Use the iwlist command
        scan=scan.decode()
        sscan=scan.split("Frequency:") #splits the output after the word frequency
        for i in range(1,len(sscan)):
            sscan[i]=sscan[i][:9] #getting the first 9 characters after the word frequency
            sscan[i]=rates.index(sscan[i])+1 #getting the channel number from the frequency
        sscan= sscan[1:] #saving all except the first
        sscan=sorted(sscan) #sorting
        countscan=Counter(sscan) #counting the amount on each channel
        channels.update(countscan) #updating the channel dictionary
        channels[channel]=channels[channel]-1 #not counting the AP connected to
    except:
        channels=channels  
    #pinging different locations and getting rtt
    try:
        cn=pyping.ping('campusnet.dtu.dk')
        goo=pyping.ping('google.dk')
        rttcn=float(cn.avg_rtt)
        rttgoo=float(goo.avg_rtt)
    except:
        rttcn=-1
        rttgoo=-1
    #speedtesting
    try:
        speed=check_output(["speedtest-cli","--simple"])
        speed=speed.decode()
        sspeed=speed.split(" ")
        download=float(sspeed[3])
        upload=float(sspeed[5])
    except:
        download=-1
        upload=-1
    #Changing the csv file
    with open('/home/pi/Desktop/testRpi.csv', 'a') as fp:
        a=csv.writer(fp,delimiter=',')
        data=[kl,signal,stoj,rttcn,rttgoo,download,upload,channel,channels[1],channels[2],channels[3],channels[4],channels[5],channels[6], \
              channels[7],channels[8],channels[9],channels[10],channels[11],channels[12],channels[13]]
        a.writerow(data)
    print data
    #Sending the csv file
    path = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Desktop/testRpi.csv " + filename
    call ([path], shell=True)

    time.sleep(300)
