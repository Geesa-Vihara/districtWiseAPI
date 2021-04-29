import requests
import re
import random
import string
import json
import time

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)).lower()


def getXML(url, file, manualMode = False):
    session = requests.Session()

    pageLoad = session.get('https://www.freefileconvert.com')
    searchObj = re.search( r'( <meta name="csrf-token" content=")(\w{2,})(">)', str(pageLoad.content))

    accessToken = ""
    if searchObj:
       accessToken = searchObj.group()[34:-2]
    else:
       raise Exception('Unable to fetch the access token.')

    headers = {
        "Origin":"https://www.freefileconvert.com",
        "Accept-Encoding":"gzip, deflate, br",
        "X-CSRF-TOKEN":accessToken,
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Referer":"https://www.freefileconvert.com/",
        "X-Requested-With":"XMLHttpRequest",
        "Connection":"keep-alive"
    }
    progressKey = id_generator()
    payload = {
        "_token":accessToken,
        "url":url,
        "output_format":"xml",
        "progress_key":progressKey,
        }
    xmlRequest = session.post('https://www.freefileconvert.com/file/url', data=payload, headers=headers)
    parsedJSON = json.loads("" + xmlRequest.content.strip().decode('utf-8'))
    if (parsedJSON['status'] == "success"):
        fileURL = 'https://www.freefileconvert.com/file/' + parsedJSON['id'] + '/download'
        """ logger.info("Reading XML: " + fileURL)
        logger.info("Waiting for the PDF -> XML conversion to finish") """
        while True:
            statusResp = session.get("https://www.freefileconvert.com/file/"+parsedJSON['id']+"/status", headers=headers)
            if "Success" in statusResp.content.strip().decode('utf-8'):
                break
            #time.sleep(1)
        xml = session.get(fileURL, headers=headers)
        open(file, 'wb').write(xml.content)
        return xml.content.strip().decode('utf-8')
    else:
        #raise Exception("Error occured: " + parsedJSON['error'])
        return "error"