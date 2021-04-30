import flask
from flask import jsonify, Flask
from xml.etree import cElementTree as ET
import xml_converter

import requests
from bs4 import BeautifulSoup
import urllib3

app = Flask(__name__)

@app.route('/covid19/srilanka/vaccines', methods=['GET'])
def vaccineStats():
    #Create list to insert into CSV
    vaccineList=[0]*3
    errorFag=0

    #Get the recently uploaded pdf url
    http = urllib3.PoolManager()
    url = "https://www.epid.gov.lk/web/index.php?option=com_content&view=article&id=231&lang=en"
    html = http.request('GET', url)
    soup = BeautifulSoup(html.data,features="html.parser")
    last_link = soup.find_all('a', href=True)[47]
    url = "https://www.epid.gov.lk"+last_link['href']
    print(url)
    #Create the xml file
    c=xml_converter.getXML(url,'vaccineStats.xml')
    if c=="error":
        errorFag=1     
    
    if(errorFag==0):
        tree = ET.parse('vaccineStats.xml')
        root = tree.getroot()
        vaccineFill(root[0],vaccineList)         #Get district data

    row = {'Covishield Vaccine First Dose': vaccineList[1], 'Sinopharm Vaccine First Dose': vaccineList[2], 'Covishield Vaccine Second Dose': vaccineList[3], 'Sinopharm Vaccine Second Dose': vaccineList[4]}
    print(row)
    return jsonify(row), 200

def vaccineFill(root,vaccineList): 
    fcovidShield=0
    fsinopharm=0
    scovidShield=0
    ssinopharm=0
    for i in range(len(root)):
        for j in range(len(root[i])):
            if root[i][j].text == "පළමු මාත්‍රාව - First Dose ":
                x=i+2
                for k in range(x,len(root),5):
                    if root[k].text is None:
                        break             
                    count1=root[k+1].text.strip().replace(',',"")
                    count2=root[k+3].text.strip().replace(',',"")
                    if(count1.isnumeric()):
                        vaccineList[1]=root[k+1].text.strip()
                    if(count2.isnumeric()):
                        vaccineList[2]=root[k+3].text.strip()     
            elif root[i][j].text == "වදවන මාත්‍රාව - Second Dose":
                x=i+3
                for k in range(x,len(root),5):
                    if root[k].text is None:
                        break           
                    count3=root[k+1].text.strip().replace(',',"")
                    count4=root[k+3].text.strip().replace(',',"")
                    if(count3.isnumeric()):
                        vaccineList[3]=root[k+1].text.strip()
                    if(count4.isnumeric()):
                        vaccineList[4]=root[k+3].text.strip() 

@app.route('/covid19/srilanka/districts', methods=['GET'])
def districtStats(chunk_size=None):
    #Create list to insert into CSV
    distList=[0]*27
    errorFag=0

    #Get the recently uploaded pdf url
    http = urllib3.PoolManager()
    url = "https://www.epid.gov.lk/web/index.php?option=com_content&view=article&id=225&lang=en"
    html = http.request('GET', url)
    soup = BeautifulSoup(html.data,features="html.parser")
    last_link = soup.find_all('a', href=True)[47]
    url = "https://www.epid.gov.lk"+last_link['href']
    print(url)
    #Create the xml file
    c=xml_converter.getXML(url,'districtStats.xml')
    if c=="error":
        errorFag=1     
    
    if(errorFag==0):
        tree = ET.parse('districtStats.xml')
        root = tree.getroot()
        districtFill(root[0],distList)         #Get district data

    row = {'GAMPAHA': distList[1], 'PUTTALAM': distList[2], 'KALUTARA': distList[3], 'ANURADHAPURA': distList[4], 'KANDY': distList[5], 'KURUNEGALA': distList[6], 'POLONNARUWA': distList[7], 'JAFFNA': distList[8], 'RATNAPURA': distList[9], 'KEGALLE': distList[10], 'MONERAGALA': distList[11], 'KALMUNAI': distList[12], 'MATALE': distList[13], 'GALLE': distList[14], 'AMPARA': distList[15], 'BADULLA': distList[16], 'MATARA': distList[17], 'BATTICOLOA': distList[18], 'HAMBANTOTA': distList[19], 'VAVUNIA': distList[20], 'TRINCOMALEE': distList[21], 'NUWARAELIYA': distList[22], 'KILINOCHCHI': distList[23], 'MANNAR': distList[24], 'MULLATIVU': distList[25], 'COLOMBO': distList[26]}
    print(row)    
    return jsonify(row), 200

def districtFill(root,distList): 
     for i in range(len(root)):
        for j in range(len(root[i])):
            dist=root[i][j].text.strip()
            if(dist=="GAMPAHA"):
                distList[1]=''.join((root[i+2].text).split())
            elif(dist=="PUTTALAM"):
                distList[2]=''.join((root[i+2].text).split())
            elif(dist=="KALUTARA"):
                distList[3]=''.join((root[i+2].text).split())
            elif(dist=="ANURADHAPURA"):
                distList[4]=''.join((root[i+1].text).split())
            elif(dist=="KANDY"):
                distList[5]=''.join((root[i+2].text).split())
            elif(dist=="KURUNEGALA"):
                distList[6]=''.join((root[i+1].text).split())
            elif(dist=="POLONNARUWA"):
                distList[7]=''.join((root[i+1].text).split())
            elif(dist=="JAFFNA"):
                distList[8]=''.join((root[i+2].text).split())
            elif(dist=="RATNAPURA"):
                distList[9]=''.join((root[i+2].text).split())
            elif(dist=="KEGALLE"):
                distList[10]=''.join((root[i+2].text).split())
            elif(dist=="MONERAGALA"):
                distList[11]=''.join((root[i+1].text).split())
            elif(dist=="KALMUNAI"):
                distList[12]=''.join((root[i+2].text).split())
            elif(dist=="MATALE"):
                distList[13]=''.join((root[i+1].text).split())
            elif(dist=="GALLE"):
                distList[14]=''.join((root[i+2].text).split())
            elif(dist=="AMPARA"):
                distList[15]=''.join((root[i+2].text).split())
            elif(dist=="BADULLA"):
                distList[16]=''.join((root[i+1].text).split())
            elif(dist=="MATARA"):
                distList[17]=''.join((root[i+2].text).split())
            elif(dist=="BATTICOLOA"):
                distList[18]=''.join((root[i+2].text).split())
            elif(dist=="HAMBANTOTA"):
                distList[19]=''.join((root[i+1].text).split())
            elif(dist=="VAVUNIA"):
                distList[20]=''.join((root[i+1].text).split())
            elif(dist=="TRINCOMALEE"):
                distList[21]=''.join((root[i+1].text).split())
            elif(dist=="NUWARAELIYA"):
                distList[22]=''.join((root[i+2].text).split())
            elif(dist=="KILINOCHCHI"):
                distList[23]=''.join((root[i+2].text).split())
            elif(dist=="MANNAR"):
                distList[24]=''.join((root[i+2].text).split())
            elif(dist=="MULLATIVU"):
                distList[25]=''.join((root[i+2].text).split())    
            elif(dist=="COLOMBO"):
                distList[26]=''.join((root[i+2].text).split())  

@app.route('/')
def index():
    return "<h1>COVID-19 STATS API!</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
