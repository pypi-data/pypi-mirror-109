import os
import sys
import datetime
from fractions import Fraction
import time
from pytz import timezone
from importlib import resources  # Python 3.7+
from configparser import ConfigParser
from allskycam import imageHeader, fileManager

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '', 'config.txt'))
time_zone = str(config['site']['time_zone'])

outputFolder = str(config['system']['otuputFolder'])
outputLocalWebFile = str(config['system']['outputLocalWebFile'])
horiz = str(config['resolution']['horiz'])
vert = str(config['resolution']['vert'])
picture_rotation = str(config['resolution']['picture_rotation'])

font_size = str(config['font']['font_size'])
esp_secs = float(config['exposure']['esp_secs'])
esp_dawn_dusk = float(config['exposure']['esp_dawn_dusk'])

isFTP = str(config['ftp']['isFTP'])=='True'
FTP_server = str(config['ftp']['FTP_server'])
FTP_login = str(config['ftp']['FTP_login'])
FTP_pass = str(config['ftp']['FTP_pass'])
FTP_uploadFolder = str(config['ftp']['FTP_uploadFolder'])
FTP_fileNameAllSkyImg = str(config['ftp']['FTP_fileNameAllSkyImgJPG'])
FTP_fileName = FTP_uploadFolder + "/" + FTP_fileNameAllSkyImg
tz = timezone(time_zone)
x = datetime.datetime.now(tz)

def main():

    print("Execution started at: " +str(x))
    s = imageHeader.getHeader(x)

    header = str(s[0])
    isNotte = s[1]
    isTimeLapse = s[2]
    zona = s[3]
    esposizione = 0
    if zona == "notte":
       esposizione = int(esp_secs * 1000000 * isNotte)
    elif zona == "alba" or zona == "tramonto":
       esposizione = int(esp_dawn_dusk * 1000000 * isNotte)
    else:
       esposizione = 0

    header += " " + str(round(esposizione / 1000000,3))

    nomefile = fileManager.getOutputFileName(outputFolder, x)
    if isTimeLapse:
       nomefile = nomefile + "TL"

    nomefile = nomefile + ".jpg"
    print("executing capture:")
    comando = "raspistill -n -md 2  -o " + nomefile
    comando += " -e jpg -w " + str(horiz) + " -h "+ str(vert)
    comando += " -rot " + str(picture_rotation)
    comando += " -a 1024  -ae "+ str(font_size) + " -a '"+ header +"'"
    if esposizione >0:
       comando +=" -ag 16 -bm -st -ex off -drc high -t 1  -ss " + str(esposizione)
    else:
       comando +=" -ex auto -awb auto "  #-br 45 -co 5"

    if zona == "giorno":
      comando +=" -ev -2"

    try:
       # ensure no raspistill is operating
       killcmd = "ps -ef|grep raspistill| grep -v color|awk '{print $2}'|xargs kill -9 1> /dev/null 2>&1"
       os.system(killcmd)

       print(comando)
       os.system(comando)
       pass
    except:
       print("ERROR: " + str(sys.exc_info()[0]))
       pass
       return
    finally:
       z=datetime.datetime.now(tz)
       print("Execution time: " + str(abs(z-x).seconds) +" secs")

    time.sleep(2)
    fileManager.saveToWEB(nomefile, outputLocalWebFile)
    fileManager.saveToFTP(isFTP, nomefile,FTP_server,FTP_login,FTP_pass,FTP_fileName+".jpg")

    print("AllSkyCam is done.")
    return


if __name__ == "__main__":
    main()

def outputDailyFolder():
   return outF

