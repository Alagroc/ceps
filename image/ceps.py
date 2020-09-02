#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import time
import sys
import signal
import re
import requests
import ConfigParser

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

#our sighandler on kill
def sig_handler(signum, frame):
    restlog.info("recieved a SIGTERM, exiting now!")
    sys.exit(0)

#if we recieve a SIGTERM, call our handler
signal.signal(signal.SIGTERM, sig_handler)

# Our regexs #
pattern={}
sections=['cert','pass','email','card']
for section in sections:
    pattern[section] = {} 

pattern['cert'][0]='BEGIN RSA PRIVATE KEY';
pattern['pass'][0]='[pP][aA][sS][sS][wW][oO][rR][dD][^(?\.)|(?\`)|(?\&)|(?\\)(?\>)|(?sS)|(?\w)|(?\[)|(?\])|(?\')|(?\_)|(?\-)|(?\,)][\w\W\s]{1,3}[^(?\n)|(\t)|(\s)]{7,25}';
pattern['email'][0]='[\w]{1,25}@[\w]{3,25}[?\.\w]{2,3}[?\.][?\w]{2,3}'
pattern['card'][0]='(4[0-9]{3}(?:[\s*\S]){0,3}[0-9]{4}(?:[\s*\S]){0,3}[0-9]{4}(?:[\s*\S]){0,3}[0-9]{4}(?:[0-9]{3})?[\s\S]{0,1}$|5[1-5](?:[\s*\S]){0,3}[0-9]{4}(?:[\s*\   S]){0,3}[0-9]{4}(?:[\s*\S]){0,3}[0-9]{4}(?:[0-9]{3})?[\s\S]{0,1}$)'

# Our functions #
def searchrgx(text,explainrgx=False,type=None):
    if type is None:
        for item in sections:
            i=0
            while i<len(pattern[item]):
                ret = re.search(str(pattern[item][i]),text)
                if ret:
                    try:
                        if explainrgx is not False:
                            ret=givemethergx(text,item,i)
                            return ret
                    except:
                        print "Issues trying to check the exact value of the regex explainrgx"
                        return True
                    return "found" 
                i+=1
        return
    else:
        #"Not implemented yet"
        return False

def givemethergx(text,item,index):
    print "In search of the truth!"
    ret = re.search(str(pattern[item][index]),text)
    if ret:
        print "Regex found: %s" % ret.group(0)
        return ret.group(0)
    else:
        print "Error ahoy"

def showhelp():
    msg =  "No given text. Need a post field 'text' with the text you want to check\n \
\ni.e., with curl it would be: \
\n\n\t$ curl -d \"text=my password is 123456789\" https://endpoint/checkrgx/\n"
    return make_response(msg, 400)
   
# Begining of API #
@app.route('/checkrgx/', methods=['GET', 'POST'])
def index():
    # we expect these parameters
    required_params = [ 'text', 'explainrgx' ]

    if len(request.form) < 1:
        return showhelp()
    else:
        try:
            text = request.form['text']
        except:
            return showhelp()

    explainrgx = request.args.get('explainrgx')

    #validate basic params
    if not text:
        return showhelp()

    if not explainrgx or explainrgx != "True":
        explainrgx = False

    #return make_response(text, 200) 
    ret=searchrgx(text,explainrgx)
    if ret:
        code=200
        msg=ret
    if ret is None:
        #No regex found
        msg=""
        code=200
    # missing here a check if the comparison went well, returning a 50X if not...
    return make_response(msg, code)

@app.route('/', methods=['GET', 'POST'])
def barra():
    msg="\n\
¯\_(ツ)_/¯\n\
\n\
Try one of the following endpoints: \n\
\n\
\t/searchrgx/   =>  Search for sensitive data in a text you can post using the post id 'text' \n\
\n\
\t<TBC>\n\
\n\
"
    return make_response(msg, 200)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

