from pyzbar import pyzbar
import argparse
import cv2
import serial
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())
import numpy as np
import cv2
import pymysql.cursors
import datetime
import sys

cap = cv2.VideoCapture(0)
ser = serial.Serial('COM10', 9600, timeout=1)
aux = ''

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='testpdf',
                             cursorclass=pymysql.cursors.DictCursor)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255, 0), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 0, 0), 2)
            #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
            #result = format(barcodeType, barcodeData)
            
            s = sys.getsizeof(barcodeData)
            #print(s)
            if s == 57:
                if barcodeData != aux:
                        print(barcodeData)
                        ser.write(barcodeData.encode("utf-8"))
                     #   with connection:
                        with connection.cursor() as cursor:
                                                #Create a new record    
                                                n_control = barcodeData
                                                ahora = datetime.datetime.now()
                                                sql = "INSERT INTO `ingresos` (`n_control`,`datime`) VALUES (%s,%s)"
                                                
                                                cursor.execute(sql, (n_control, ahora))
                                                print (ahora) #esto si quieres quitalo, solo era pa confirmar
                                        # connection is not autocommit by default. So you must commit to save your changes.
                        connection.commit()
                aux = barcodeData
                #rwString = ser.readlines()
                #print(rwString) 
            else: print("QR no valido")
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
ser.close()