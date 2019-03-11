#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 01:24:07 2017

@author: cheeyau
"""

from __future__ import print_function
from flask import Flask,request,Response
from flask_cors import CORS,cross_origin
from PIL import Image
import sys
import math
import numpy as np
import logging
from logging.handlers import RotatingFileHandler
import json
from math import sqrt,pow
from operator import itemgetter

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app,resources={r"/*": {"origins": "*"}},allow_headers='*')

print("initiated the app! With a name of:", __name__)

def facecontour_matching(face_contour):
    
    dia = [[0,0],[1.51716999085015,12.9474086514029],[3.96139987005405,25.6666706709765],[6.70663872007039,38.3608554211184],[11.6563782164204,49.8980599778561],[19.5628614970209,59.8332884924484],[29.3921843878919,68.2822414153031],[40.1619682121802,75.9436444866468],[52.0149209047062,77.8872396465118],[63.8915168023067,75.4346042341768],[74.4701375365298,67.2722965992063],[83.9187841412503,57.9945575796437],[91.4481053741481,47.4859805453282],[95.6264389577863,35.3762363707676],[97.7540765632307,22.2633669087530],[99.3228335491292,9.20579745664388],[100,-4.11012258917420]];
    sq = [[0,0],[1.02689584392100,13.4027550574357],[2.77988462768204,26.2964593367449],[4.59647610637228,39.5718167145022],[8.27625026150635,51.6637850887671],[15.7806608219281,61.5761651262436],[26.1815424355842,69.1907693706475],[37.8786009900340,75.9159544745278],[50.5921598613041,77.7526794281395],[63.2468949747256,75.7533047843493],[74.9206735039913,68.5791091112831],[85.2573070595986,60.5084935392779],[92.6148941233108,50.1528189549801],[95.8443729732081,37.4659783813210],[97.2819491105112,23.9806478852246],[99.1503635886345,10.7488962973929],[100,-3.03544357353187]];
    ov = [[0,0],[1.22485359113485,14.6966589775273],[4.07328660319787,29.0057593127686],[7.01862704660618,43.0847025858252],[11.9337845434218,56.3588194422575],[19.0735838784343,67.9980716552758],[27.9909970958415,78.2288212426777],[38.0778732117101,86.7468957846491],[49.8723326548973,89.1647145796864],[61.7753942282507,86.7452072426038],[72.5515804999418,78.2365955105947],[82.2221994254788,68.1973828741376],[89.8541913066374,56.3806048914355],[94.4092331194439,42.6411465641712],[97.0203142056501,27.7653383873112],[99.0836623470592,12.9869927265807],[100,-2.08985275011253]];
    ro = [[0,0],[1.29533872710868,13.1630224466070],[3.46324450855438,26.2589069122142],[6.12059180545315,39.2616729485647],[10.3424004087097,50.8622626509690],[18.3322186012974,60.7935820023330],[27.8956920151952,68.7549230461903],[38.4654868151612,75.9190391630759],[50.0904965419855,77.6636516414815],[61.7801475493361,75.2154542956292],[72.5036449347747,66.8959828595264],[82.4726353498213,58.2447761258034],[90.3805575902598,47.9420753429314],[94.8786541255628,36.1455867287432],[97.2602351206837,23.0003405840276],[98.8893377075678,9.89526220346810],[100,-3.27898272024635]];
    he = [[0,0],[1.29438412225297,14.1028946766652],[3.61980460341116,27.9773141248551],[6.13762527696954,41.6485108698223],[10.3002507510704,54.6001190673322],[17.9333538349932,65.4523770097541],[27.7018822100790,74.9712779630813],[38.6955424660343,83.1431015857246],[50.9985096870343,85.0769995032290],[63.4205245270819,82.2087581513811],[74.6780253747467,73.7735867653901],[84.7012671602836,64.1522563653711],[92.5890836546574,52.8146807655005],[96.4792341841522,39.2317594366775],[98.2207319092565,24.8318469629945],[99.3977637420261,10.6152075004534],[100,-4.18032786885245]];

    #dia = [[0,0],[17,142],[42,277],[66,414],[112,535],[187,644],[283,737],[393,824],[520,851],[648,831],[760,748],[858,652],[934,541],[979,416],[1002,280],[1027,144],[1043,-2]]
    #scale = dia[-1][0]/100;
    #dia = np.divide(dia,scale)
    #sq = [[0,0],[7,68],[18,136],[31,204],[55,268],[92,323],[136,372],[188,415],[247,426],[305,414],[356,369],[400,319],[435,264],[458,201],[471,133],[483,65],[489,-3]]
    #scale = sq[-1][0]/100;
    #sq = np.divide(sq,scale)
    #ov = [[0,0],[0,15],[3,31],[5,46],[9,60],[17,71],[28,81],[40,89],[53,91],[66,89],[76,80],[85,71],[92,60],[97,48],[100,34],[102,21],[103,7]]
    #scale = ov[-1][0]/100;
    #ov = np.divide(ov,scale)
    #ro = [[0,0],[1,31],[5,62],[8,92],[15,122],[30,148],[52,170],[77,187],[105,194],[136,192],[166,179],[194,161],[214,138],[225,109],[233,78],[241,47],[246,13]]
    #scale = ro[-1][0]/100;
    #ro = np.divide(ro,scale)
    #he = [[0,0],[6,49],[16,97],[26,143],[44,185],[73,220],[109,251],[147,280],[188,290],[231,282],[272,254],[312,224],[342,188],[360,144],[370,96],[378,46],[384,-7]]
    #scale = he[-1][0]/100;
    #he = np.divide(he,scale)
    #re = [[0,0],[7,68],[18,136],[31,204],[55,268],[92,323],[136,372],[188,415],[247,426],[305,414],[356,369],[400,319],[435,264],[458,201],[471,133],[483,65],[489,-3]]
    #scale = re[-1][0]/100;
    #re = np.divide(re,scale)

    im_cnt = np.subtract(face_contour[:],face_contour[0])
    scale = im_cnt[-1][0]/100;
    im_cnt = np.divide(im_cnt,scale)

    sqrt(np.sum(np.power(np.subtract(im_cnt,dia),2)))
    contour_type = ["diamond.png","square.png","oval.png","round.png","heart.png"]
    rank = enumerate([sqrt(np.sum(np.power(np.subtract(im_cnt,dia),2))),sqrt(np.sum(np.power(np.subtract(im_cnt,sq),2))),sqrt(np.sum(np.power(np.subtract(im_cnt,ov),2))),sqrt(np.sum(np.power(np.subtract(im_cnt,ro),2))),sqrt(np.sum(np.power(np.subtract(im_cnt,he),2)))])
    rrank = {"diamond":sqrt(np.sum(np.power(np.subtract(im_cnt,dia),2))),
             "square":sqrt(np.sum(np.power(np.subtract(im_cnt,sq),2))),
             "oval":sqrt(np.sum(np.power(np.subtract(im_cnt,ov),2))),
             "round":sqrt(np.sum(np.power(np.subtract(im_cnt,ro),2))),
            "heart":sqrt(np.sum(np.power(np.subtract(im_cnt,he),2)))}
    i, value = min(rank, key=itemgetter(1))
    styles = []
    if i ==1:
        styles.append('')
    return rrank,contour_type[i]

def process_json(content):

    feature_dictionary = {}
    json_result = json.loads(content)
    analysis = []

    feature_dictionary['eyebrowLeft2'] = json_result['objects'][1]['landmarks']['eyebrowLeft'][2]
    feature_dictionary['eyebrowRight2'] = json_result['objects'][1]['landmarks']['eyebrowRight'][2]
    feature_dictionary['eyeLeftAvg'] = np.divide(np.sum([json_result['objects'][1]['landmarks']['eyeLeft'][1],json_result['objects'][1]['landmarks']['eyeLeft'][2]],axis=0),2)
    feature_dictionary['eyeRightAvg'] = np.divide(np.sum([json_result['objects'][1]['landmarks']['eyeRight'][1],json_result['objects'][1]['landmarks']['eyeRight'][2]],axis=0),2)
    feature_dictionary['eyeRight3'] = json_result['objects'][1]['landmarks']['eyeRight'][3]
    feature_dictionary['eyeRight0'] = json_result['objects'][1]['landmarks']['eyeRight'][0]
    feature_dictionary['eyeLeft3'] = json_result['objects'][1]['landmarks']['eyeLeft'][3]
    feature_dictionary['eyeLeft0'] = json_result['objects'][1]['landmarks']['eyeLeft'][0]
    feature_dictionary['eyeLeftC'] = np.divide(np.sum([json_result['objects'][1]['landmarks']['eyeLeft'][4],json_result['objects'][1]['landmarks']['eyeLeft'][5]],axis=0),2)
    feature_dictionary['eyeRightC'] = np.divide(np.sum([json_result['objects'][1]['landmarks']['eyeRight'][4],json_result['objects'][1]['landmarks']['eyeRight'][5]],axis=0),2)
    feature_dictionary['faceContour2'] = json_result['objects'][1]['landmarks']['faceContour'][2]
    feature_dictionary['noseBall0']=json_result['objects'][1]['landmarks']['noseBall'][0]
    feature_dictionary['noseBall2'] = json_result['objects'][1]['landmarks']['noseBall'][2]
    feature_dictionary['noseBall4'] = json_result['objects'][1]['landmarks']['noseBall'][4]
    feature_dictionary['faceContour14'] = json_result['objects'][1]['landmarks']['faceContour'][14]
    feature_dictionary['mouthOuter2'] = json_result['objects'][1]['landmarks']['mouthOuter'][2]
    feature_dictionary['mouthOuter3'] = json_result['objects'][1]['landmarks']['mouthOuter'][3]
    feature_dictionary['mouthOuter4'] = json_result['objects'][1]['landmarks']['mouthOuter'][4]
    feature_dictionary['mouthOuter0'] = json_result['objects'][1]['landmarks']['mouthOuter'][0]
    feature_dictionary['mouthInnerAvg'] = np.divide(np.sum([json_result['objects'][1]['landmarks']['mouthInner'][2],json_result['objects'][1]['landmarks']['mouthInner'][6]],axis=0),2)
    feature_dictionary['mouthInner2'] = json_result['objects'][1]['landmarks']['mouthInner'][2]
    feature_dictionary['mouthInner6'] = json_result['objects'][1]['landmarks']['mouthInner'][6]
    feature_dictionary['mouthOuter6'] = json_result['objects'][1]['landmarks']['mouthOuter'][6]
    feature_dictionary['mouthOuter9'] = json_result['objects'][1]['landmarks']['mouthOuter'][9]
    feature_dictionary['faceContour8'] = json_result['objects'][1]['landmarks']['faceContour'][8]
    feature_dictionary['nosebridge3'] = json_result['objects'][1]['landmarks']['noseBridge'][3]

    # alternative for nose
    little_shait = 1.3;
    total_dist = math.ceil((feature_dictionary['noseBall4'][0] - feature_dictionary['noseBall0'][0])*little_shait);
    dist_ratio = (feature_dictionary['noseBall4'][0] - feature_dictionary['nosebridge3'][0])/(feature_dictionary['noseBall4'][0] - feature_dictionary['noseBall0'][0]);
    feature_dictionary['noseBall4'][0] = feature_dictionary['nosebridge3'][0] + math.ceil(dist_ratio*total_dist);
    feature_dictionary['noseBall0'][0] = feature_dictionary['noseBall4'][0] - total_dist;
    
    #wide mouth
    smile_adj = abs( feature_dictionary['mouthInner6'][1]-feature_dictionary['mouthInner2'][1]);
                   
    canon_5 = abs(np.divide(float(np.subtract(feature_dictionary['eyeRight0'][0],feature_dictionary['eyeLeft3'][0])),float(np.subtract(feature_dictionary['noseBall4'][0],feature_dictionary['noseBall0'][0]))))
    canon_6 = abs(np.divide(float(np.subtract(feature_dictionary['eyeRight0'][0],feature_dictionary['eyeLeft3'][0])),float(np.subtract(feature_dictionary['eyeLeft3'][0],feature_dictionary['eyeLeft0'][0]))))
    canon_8 = abs(np.divide(float(np.subtract(feature_dictionary['faceContour14'][0],feature_dictionary['faceContour2'][0])),float(np.multiply(np.subtract(feature_dictionary['noseBall4'][0],feature_dictionary['noseBall0'][0]),4))))

    golden_5 = abs(np.divide(np.subtract(feature_dictionary['mouthOuter6'][0],feature_dictionary['mouthOuter0'][0]),np.multiply(np.subtract(feature_dictionary['eyeRight0'][0],feature_dictionary['eyeLeft3'][0]),1.5)))
    golden_6 = abs(np.divide(np.subtract(feature_dictionary['mouthOuter3'][1],feature_dictionary['faceContour8'][1])-smile_adj,np.multiply(np.subtract(feature_dictionary['eyeRight0'][0],feature_dictionary['eyeLeft3'][0]),1.4)))
    golden_7 = abs(np.divide(np.subtract(feature_dictionary['mouthOuter3'][1],feature_dictionary['faceContour8'][1])- smile_adj,np.multiply(np.subtract(feature_dictionary['noseBall4'][0],feature_dictionary['noseBall0'][0]),1.5)))
    golden_17 = abs(np.divide(np.subtract(feature_dictionary['mouthOuter6'][0],feature_dictionary['mouthOuter0'][0]),np.multiply(np.subtract(feature_dictionary['noseBall4'][0],feature_dictionary['noseBall0'][0]),1.5)))

    symm_1 = abs(np.divide(float(np.subtract(feature_dictionary['noseBall2'][0],feature_dictionary['mouthOuter2'][0])),float(np.subtract(feature_dictionary['eyeLeft0'][0],feature_dictionary['noseBall2'][0]))))
     
    if symm_1> 1:
        analysis.append({"recommendation":"Top lip not symmetric, left side longer than right side","description":"Apply lip liner on the inside of the left lip and outside of the right lip. Add more lipstick to the inner part of the lip.",
                   "pname":" Lip liner","productImage":"https://www.nyxcosmetics.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-cpd-nyxusa-master-catalog/default/dwbbca9dd2/ProductImages/Lips/Slim_Lip_Pencil/Slim_Lip_Pencil/slimlippencil_main.jpg?sw=600&sh=600&sm=fit"})
    elif symm_1 < 1:
        analysis.append({"recommendation":"Top lip not symmetric, left side shorter than right side","description":"Apply lip liner on the outside of the left lip and inside of the right lip. Add more lipstick to the inner part of the lip.",
                   "pname":"Lip liner","productImage":"https://www.nyxcosmetics.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-cpd-nyxusa-master-catalog/default/dwbbca9dd2/ProductImages/Lips/Slim_Lip_Pencil/Slim_Lip_Pencil/slimlippencil_main.jpg?sw=600&sh=600&sm=fit"})
    else:
        analysis.append({"recommendation":"Lips symmetric","description":"N/A",
                   "pname":"N/A","productImage":"N/A"})
    #Nose width
    if canon_8 < 1:
        analysis.append({"recommendation":"Nose width large","description":"Perform nose contouring",
                   "pname":" Countouring powder","productImage":"http://www.wisebread.com/files/fruganomics/u5171/city%20color.jpg"})
    elif canon_8 > 1:
        analysis.append({"recommendation":"Nose width small","description":"Contour sides of the nose bridge",
                   "pname":" Countouring powder","productImage":"http://www.wisebread.com/files/fruganomics/u5171/city%20color.jpg"})
    else:
        analysis.append({"recommendation":"Perfect Nose width","description":"N/A",
                   "pname":"N/A","productImage":"N/A"})
    #Distance between eyes   
    if canon_6 > 1:
        analysis.append({"recommendation":"Eyes far apart","description":"Use darker eye shadow in the inner corner of the eyes and use dark brow highlights",
                   "pname":"Eye shadow and highlighter","productImage":"https://images-na.ssl-images-amazon.com/images/I/71ov2tyvmQL._SL1300_.jpg"})
    elif canon_6 < 1:
        analysis.append({"recommendation":"Eyes closely set","description":"Use lighter eye shadow in the inner corner of the eyes and use light brow highlights",
                   "pname":"Eye shadow and highlighter","productImage":"https://images-na.ssl-images-amazon.com/images/I/71ov2tyvmQL._SL1300_.jpg"})
    else:
        analysis.append({"recommendation":"Perfect eye spacing","description":"N/A",
                   "pname":"N/A","productImage":"N/A"})

    #Distance between eyes
    if golden_5 > 1:
        analysis.append({"recommendation":"Wide lips","description":"Use lip liner inside the lips with mat lipstick",
                   "pname":"Matte lipstick","productImage":"https://www.nyxcosmetics.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-cpd-nyxusa-master-catalog/default/dw190a6040/ProductImages/2016/Lips/Matte_Lipstick_Extension/mattelipstick_main.jpg?sw=600&sh=600&sm=fit"})
    elif golden_5 <1: 
        analysis.append({"recommendation":"Narrow lips","description":"Use lip liner outside the lips with bright lipstick",
                   "pname":"Bright lipstick","productImage":"https://darklipstips.com/wp-content/uploads/2015/08/Revlon-Super-Lustrous-Lipstick-Creme-Love-Bright-Red.jpg"})
    else :
        analysis.append({"recommendation":"Perfect lips","description":"N/A",
                   "pname":"N/A","productImage":"N/A"})

    # Mouth width 
    #if canon_6 - canon_8 > 0:
    #    if golden_7 > 1:
    #        analysis.append({"recommendation":"Chin too long","description":"Perform chin contouring",
    #               "pname":"Countouring powder","productImage":"https://media.allure.com/photos/581a4de84e15a10a15009790/master/pass/Countour-compilation.jpg"})
    #    else: 
    #        analysis.append({"recommendation":"Perfect Chin","description":"N/A",
    #               "pname":"N/A","productImage":"N/A"})
    #else :
    if golden_6 > 1:
        analysis.append({"recommendation":"Long Chin","description":"Perform chin contouring",
                    "pname":"Countouring powder","productImage":"https://media.allure.com/photos/581a4de84e15a10a15009790/master/pass/Countour-compilation.jpg"})
    else :
        analysis.append({"recommendation":"Perfect Chin","description":"N/A",
                    "pname":"N/A","productImage":"N/A"})
    facerank,facecontour_analysis = facecontour_matching(json_result['objects'][1]['landmarks']['faceContour'])
    return analysis,facerank,facecontour_analysis

@app.route('/')
def index():

    app.logger.info('Test')
    return "Hello, World!"

app = Flask(__name__)


@app.route("/img", methods=["POST"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def home():
    content = request.get_json()
    #img = Image.open(request.files['file'])
    # print(content,sys.stdout)
    # sys.stdout.flush()
    analyzed_json,facerank,facecontour_analysis = process_json(content)
    json_return = {"data":analyzed_json,"facecountour":facecontour_analysis,"facerank":facerank}
    js = json.dumps(json_return)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(debug = True)

