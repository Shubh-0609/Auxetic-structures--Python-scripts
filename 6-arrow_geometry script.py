from sympy import *
import math
import numpy as np
from math import pi
from numpy import sin, cos, pi, linspace
import os
import pandas as pd
import time




def genAlines(h, l, theta, thick1, thick2, stars):
    phi = math.pi / stars
    lpoints = int((l) / (0.5 * thick1)) + 10
    hpoints = int((h) / (0.5 * thick2)) + 10
    t_h = 0.1 * h
    t_l = 0.1 * l
    alpha = math.pi / 2 - theta
    beta = theta - phi
    #     right down
    abx = np.linspace(0, l * (math.sin(theta)) - t_l * math.cos(alpha), lpoints)
    aby = np.linspace(l * ((math.sin(theta) / math.tan(phi)) - math.cos(theta)),
                      l * (math.sin(theta) / math.tan(phi)) - t_l * math.sin(alpha), lpoints)
    path = np.vstack((abx, aby))
    pts_ab = path.T

    #     right arc length
    t = t_l / math.cos(beta) - t_l * math.tan(beta)
    b1bx = np.linspace(l * (math.sin(theta)) - t * math.sin(phi), l * (math.sin(theta)) + thick1 * math.cos(phi),
                       3)
    b1by = np.linspace(l * (math.sin(theta) / math.tan(phi)) - t * math.cos(phi),
                       l * (math.sin(theta) / math.tan(phi)) + thick1 * math.sin(phi), 3)
    path = np.vstack((b1bx, b1by))
    pts_b1b = path.T

    #     right up
    cdx = np.linspace(l * (math.sin(theta)) - thick1 * math.sin(alpha), thick2 / 2 + t_h * math.cos(alpha), lpoints)
    cdy = np.linspace(l * (math.sin(theta) / math.tan(phi)) + thick1 * math.cos(alpha),
                      l * ((math.sin(theta) / math.tan(phi)) - math.cos(theta)) + thick2 * math.tan(
                          alpha) * 0.5 + thick1 / math.sin(theta) + t_h * math.sin(alpha), lpoints)
    path = np.vstack((cdx, cdy))
    pts_cd = path.T

    #     pointing point
    dex = np.linspace(thick2 / 2, thick2 / 2, hpoints)
    dey = np.linspace(
        l * ((math.sin(theta) / math.tan(phi)) - math.cos(theta)) + thick2 * math.tan(alpha) * 0.5 + thick1 / math.sin(
            theta) + t_h, h + l * (math.sin(theta) / math.tan(phi)) - l * math.cos(theta), hpoints)
    path = np.vstack((dex, dey))
    pts_de = path.T

    r1 = t_h * math.tan(theta / 2)
    stra = theta
    enda = pi
    numpt = int(abs((stra - enda) * 180 / (15 * pi)))
    angles1 = linspace(stra, enda, numpt)
    xs1 = t_h * math.tan(theta / 2) + thick2 / 2 + r1 * cos(angles1)
    ys1 = l * ((math.sin(theta) / math.tan(phi)) - math.cos(theta)) + thick2 * math.tan(
        alpha) * 0.5 + thick1 / math.sin(theta) + t_h - r1 * sin(angles1)
    path = np.vstack((xs1, ys1))
    arcpts1 = path.T

    r2 = t_l * math.tan(beta)
    stra = pi / 2 + phi - beta
    enda = pi / 2 - phi
    numpt = int(abs((phi - theta))*13)
    angles2 = linspace(stra, enda, numpt)
    xs2 = l * (math.sin(theta)) - t_l * (math.sin(phi) / math.cos(beta)) + r2 * cos(angles2)
    ys2 = l * (math.sin(theta) / math.tan(phi)) - t_l * (math.cos(phi) / math.cos(beta)) + r2 * sin(angles2)
    path = np.vstack((xs2, ys2))
    arcpts2 = path.T

    r3 = thick1
    stra = phi
    enda = pi / 2 + phi - beta
    numpt = int(abs((stra - enda) * 180 / (15 * pi)))
    angles3 = linspace(stra, enda, numpt)
    xs3 = l * (math.sin(theta)) + r3 * cos(angles3)
    ys3 = l * (math.sin(theta) / math.tan(phi)) + r3 * sin(angles3)
    path = np.vstack((xs3, ys3))
    arcpts3 = path.T

    pts11 = np.vstack((pts_ab, arcpts2, pts_b1b, arcpts3, pts_cd, arcpts1, pts_de))
    pts1 = np.array(pts11)

    mrr = np.array([[-1, 0], [0, 1]])
    arr1 = pts1.T
    rs1 = np.dot(mrr, arr1).T
    pts2 = rs1[::-1]

    pts = np.vstack((pts1, pts2))

    return pts

def savearray(parameter):
    # h,l,theta,thick1,thick2,stars=6.5,3,math.pi/4.5,0.25,0.5,6
    parameter=[ h,l,theta,thick1,thick2,stars]
    phi=math.pi/stars

    arrow_1=genAlines(h,l, theta, thick1,thick2, stars)
    arrow_1=np.array(arrow_1)
    np.save('arrow_1.npy', arrow_1)
    np.save('parameter.npy', parameter)


    sci = np.deg2rad(60)
    rotmat = np.array([[cos(sci), -sin(sci)], [sin(sci), cos(sci)]])
    arrow_2=np.dot(rotmat,arrow_1.T).T
    arrow_2=np.array(arrow_2)
    arrow_2 = arrow_2.astype('float64')
    np.save('arrow_2.npy', arrow_2)

    sci = np.deg2rad(120)
    rotmat = np.array([[cos(sci), -sin(sci)], [sin(sci), cos(sci)]])
    arrow_3=np.dot(rotmat,arrow_1.T).T
    arrow_3=np.array(arrow_3)
    arrow_3 = arrow_3.astype('float64')
    np.save('arrow_3.npy', arrow_3)

    sci = np.deg2rad(180)
    rotmat = np.array([[cos(sci), -sin(sci)], [sin(sci), cos(sci)]])
    arrow_4=np.dot(rotmat,arrow_1.T).T
    arrow_4=np.array(arrow_4)
    arrow_4 = arrow_4.astype('float64')
    np.save('arrow_4.npy', arrow_4)

    sci = np.deg2rad(240)
    rotmat = np.array([[cos(sci), -sin(sci)], [sin(sci), cos(sci)]])
    arrow_5=np.dot(rotmat,arrow_1.T).T
    arrow_5=np.array(arrow_5)
    arrow_5 = arrow_5.astype('float64')
    np.save('arrow_5.npy', arrow_5)

    sci = np.deg2rad(300)
    rotmat = np.array([[cos(sci), -sin(sci)], [sin(sci), cos(sci)]])
    arrow_6=np.dot(rotmat,arrow_1.T).T
    arrow_6=np.array(arrow_6)
    arrow_6 = arrow_6.astype('float64')
    np.save('arrow_6.npy', arrow_6)

    x=thick2
    y=h + l * (math.sin(theta) / math.tan(phi)) - l * math.cos(theta)
    anglecos=math.cos(math.pi/6)
    anglesin=math.sin(math.pi/6)
    angletan=math.tan(math.pi/3)

    cut_1=np.array([[x*anglecos+thick2/2,y+x*anglesin-thick2],[x*anglecos+thick2/2,x+thick2/angletan+y+x*anglesin],[-thick2-x*anglecos,y+x*anglesin],[-thick2-x*anglecos,y-thick2/angletan-x*anglesin-thick2],[x*anglecos+thick2/2,y+x*anglesin-thick2]])
    cut_1 = cut_1.astype('float64')
    np.save('cut_1.npy', cut_1)

    cut_2=np.array([[x*anglecos+thick2/2,-y+x*anglesin-thick2],[x*anglecos+thick2/2,x+thick2/angletan-y+x*anglesin],[-thick2-x*anglecos,-y+x*anglesin],[-thick2-x*anglecos,-y-thick2/angletan-x*anglesin-thick2],[x*anglecos+thick2/2,-y+x*anglesin-thick2]])
    cut_2 = cut_2.astype('float64')
    np.save('cut_2.npy', cut_2)
    return None

for h in range(3, 5, 1):
    for l in range(2, 4, 1):
        for theta in np.arange(math.pi / 3.5, math.pi / 2.5, math.pi / 18):
            for thick1 in np.arange(0.25, 0.75, 0.25):
                for thick2 in np.arange(0.25, 0.75, 0.25):
                    for stars in range(6, 7):
                        try:
                            t = time.localtime()
                            current_time = time.strftime("%H:%M:%S", t)
                            print(current_time)

                            parameter = [h, l, theta, thick1, thick2, stars]
                            savearray(parameter)
                            abaq='abaqus cae script=6_arrow_cae.py'
                            # abaq = 'abaqus cae noGUI=6_arrow_cae.py'
                            d = os.system(abaq)
                            print(d)
                            print(parameter)
                            # t = time.localtime()
                            # current_time = time.strftime("%H:%M:%S", t)
                            # print(current_time)
                            Parameters = str(parameter)
                            text_file_Parameters = open("Study" + "Parameters" + ".txt", "a")
                            text_file_Parameters.write(Parameters + '\n')
                            text_file_Parameters.close()
                            name = ''
                            for i in parameter:
                                name = name + str(i) + '-'
                            df = pd.read_csv('resulttry.csv')
                            df.columns = df.columns.str.replace(' ', '')
                            df['Frame'] = df['Frame'].str.replace('Increment', '')
                            df['Frame'] = df['Frame'].str.replace('Step Time', '')
                            df['Frame'] = df['Frame'].str.replace(' ', '')
                            df['Frame'] = df['Frame'].str.replace('=', '')
                            df['Frame'] = df['Frame'].str.replace(':', ',')
                            df['PartInstanceName'] = df['PartInstanceName'].str.replace('VIRTPOINTINST_', '')
                            df['PartInstanceName'] = df['PartInstanceName'].str.replace('MERGED-', '')
                            dfnew = df[
                                ['Frame', 'PartInstanceName', 'NodeLabel', 'X', 'Y', 'RF-RF1', 'RF-RF2', 'U-U1', 'U-U2',
                                 'S-S11', 'S-S22', 'S-S12']].copy()
                            dfnew.to_csv(name + 'sd.csv', index=False)
                            os.remove('resulttry.csv')
                            t = time.localtime()
                            current_time = time.strftime("%H:%M:%S", t)
                            print(current_time)

                        except:
                            print([h, l, theta, thick1, thick2, stars])
                            np.save(str(h) + str(l) + str(theta) + str(thick1) + str(thick2) + str(stars) + 'error.npy',
                                    np.array([h, l, theta, thick1, thick2, stars]))
                            t = time.localtime()
                            current_time = time.strftime("%H:%M:%S", t)
                            print(current_time)