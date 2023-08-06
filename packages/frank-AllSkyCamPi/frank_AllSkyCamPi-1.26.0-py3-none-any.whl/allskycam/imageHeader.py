import datetime
import time
import traceback
from datetime import datetime, timedelta
from allskycam import suncalc2
from pytz import timezone
import pytz
import sys
import math
import os
from importlib import resources  # Python 3.7+
from configparser import ConfigParser

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '', 'config.txt'))
latitude  = float(config['site']['latitude'])
longitude = float(config['site']['longitude'])
timeZone = str(config['site']['time_zone'])
full_moon_reduc = float(config['moon']['full_moon_reduc'])
ms_offset = float(config['moon']['ms_offset'])
ms_duration = float(config['moon']['ms_duration'])
mr_offset = float(config['moon']['mr_offset'])
mr_duration = float(config['moon']['mr_duration'])

dd_offset_dawn = float(config['offset']['dawn'])
dd_offset_dusk = float(config['offset']['dusk'])

def getHeader(datacalcolo):
    isDebug= True          # True will stampa debug info. False, not
    logLevel = 0           # 0 = basic, 1= full
    isLinear= False        # True: linear variation of exposure; False:quadratic
    # end of parameters
    # do not touch below

    isTimeLapse =  True
    sun_factor = 1
    riduzione_lineare = 0
    riduzione_quadratica = 0
    zona = "***"
    try:
       valori=["",0,False,""]

       tz = timezone(timeZone)
       stampa("Orario attuale = "+str(datacalcolo), isDebug, logLevel, 0)

       # get sun information
       sc = suncalc2.getTimes(datacalcolo, latitude, longitude)
       

       s_set  = datetime.strptime(sc["sunset"],"%Y-%m-%d %H:%M:%S")
       dusk_ = datetime.strptime(sc["dusk"],"%Y-%m-%d %H:%M:%S")
       night_ = datetime.strptime(sc["night"],"%Y-%m-%d %H:%M:%S")
       nightEnd_ = datetime.strptime(sc["nightEnd"],"%Y-%m-%d %H:%M:%S")
       dawn_ = datetime.strptime(sc["dawn"],"%Y-%m-%d %H:%M:%S")
       s_rise = datetime.strptime(sc["sunrise"],"%Y-%m-%d %H:%M:%S")

       dawn = dawn_.astimezone(tz)
       srise  = s_rise.astimezone(tz)
       sset   = s_set.astimezone(tz)
       dusk = dusk_.astimezone(tz)
       night = night_.astimezone(tz)
       nightEnd = nightEnd_.astimezone(tz)

       # calcolo corretto di nightEnd per header
       if datacalcolo > nightEnd:
          sc2 = suncalc2.getTimes(datacalcolo+timedelta(days=1), latitude, longitude)
          nightEndH_ = datetime.strptime(sc2["nightEnd"],"%Y-%m-%d %H:%M:%S")
          nightEndHeader = nightEndH_.astimezone(tz)
       else:
          nightEndHeader = nightEnd_.astimezone(tz)


       NS = str(night)[11:16]
       NE = str(nightEndHeader)[11:16]

       # Get Moon Rise/Set/Fraction/Phase/exposure reduction
       moonValues = getMoon(datacalcolo,isDebug, logLevel)
       moon_rise = moonValues[0]
       moon_set = moonValues[1]
       fr = moonValues[2]
       ph = moonValues[3]
       moon_reduction = moonValues[4]

       stampa("suncalc2= "+str(sc), isDebug, logLevel, 1)
       sep = " | "
       stringa = datacalcolo.strftime("%d/%m/%Y %H:%M") + sep + "NS=" + NS + sep
       stringa += "NE=" + NE + sep+ "MR=" + moon_rise + sep + "MS=" + moon_set + sep + str(int(round(fr*100,0))) + "% | " + ph

       stampa(stringa, isDebug, logLevel, 0)

       # offset dawn e dusk 
       dawn = dawn+timedelta(minutes= + dd_offset_dawn)
       dusk = dusk+timedelta(minutes= + dd_offset_dusk)

       if (datacalcolo >= night and datacalcolo <= nightEnd) or (datacalcolo >=nightEnd and datacalcolo>=night) or (datacalcolo <nightEnd and datacalcolo<night):
          # prendo il tempo di posa notturno
          zona = "notte"
          riduzione_lineare = 1
          riduzione_quadratica = 1

       elif datacalcolo < srise  and datacalcolo > dawn:
          zona="pre_alba"

       elif datacalcolo > nightEnd and datacalcolo < dawn:
          #transizione alba
          zona = "alba"
          delta = datacalcolo - nightEnd
          totale = dawn  - nightEnd
          deltaminuti = int(delta.total_seconds() / 60)
          durata = int(totale.total_seconds() / 60)
          riduzione_lineare =  round(1-(deltaminuti/durata),3)
          riduzione_quadratica = riduzioneQuadratica(deltaminuti,durata)
       elif (datacalcolo < dusk and datacalcolo >  sset):
          #prima del tramonto
          zona="pre_tramonto"

       elif (datacalcolo >= dusk and datacalcolo < night):
          #transizione tramonto
          zona="tramonto"
          delta = datacalcolo - dusk
          totale = night -dusk
          deltaminuti = int(delta.total_seconds() / 60)
          durata = int(totale.total_seconds() / 60)
          riduzione_lineare = round(deltaminuti/durata,3)
          riduzione_quadratica = round(1-riduzioneQuadratica(deltaminuti, durata),4)
       else:
          # automatico
          zona="giorno"
          isTimeLapse = False

       if isLinear==True:
          riduzione = riduzione_lineare
       else:
          riduzione = riduzione_quadratica

       if riduzione < 0 or riduzione >1 :
          riduzione = 0


       stampa("Rid. Alba/Tram = "+str(riduzione), isDebug, logLevel, 0)
       stampa("dawn           = "+str(dawn), isDebug, logLevel, 0)
       stampa("dusk           = "+str(dusk), isDebug, logLevel, 0)
       stampa("night          = "+str(night), isDebug, logLevel, 0)
       stampa("nightEnd       = "+str(nightEnd), isDebug, logLevel, 0)
       stampa("nightEndHeader = "+str(nightEndHeader), isDebug, logLevel, 0)

       if zona!="notte":
          # moon_reduction only at night
          moon_reduction=1

       riduzione_totale = round(riduzione * moon_reduction,3)
       stampa("zona = " + zona + " -> RL="+ str(riduzione_lineare) + " -> RQ=" + str(riduzione_quadratica) + " | Riduz.Tot. = " + str(round(riduzione_totale,3)), isDebug, logLevel, 0)

#       stampa("Total Reduction= " + str(round(riduzione_totale,3)), isDebug, logLevel, 0)

       valori[0] = stringa
       valori[1] = riduzione_totale
       valori[2] = isTimeLapse
       valori[3] = zona
    except Exception as e:
       stampa("type error: " + str(e), isDebug, logLevel, 0)
       stampa(traceback.format_exc(), isDebug, logLevel, 0)
       valori[0] = ""
       valori[1] = 0
    return valori
	
def getMoon(datacalcolo, isDebug, logLevel):
   moon_factor = 1
   #Get moon illumination information
   sm = suncalc2.getMoonIllumination(datacalcolo)
   mf = (sm["phase"])
   an = (sm["angle"])
   fr = float((str(sm["fraction"]))[0:4])

   moon_phase=str(mf)[0:5]
   luna_sorta = False
   luna_tramontata = False

   stampa("Moon phase     = " + str(mf) + " | Moon angle     = " + str(an) + " | Moon fraction  = " + str(fr), isDebug, logLevel, 1)

   # Get moonrise/moonset times
   tz = timezone(timeZone)
   smt = suncalc2.getMoonTimes(datacalcolo, latitude, longitude)
   stampa(str(smt), isDebug, logLevel,1)
   try:
      mrise= smt["rise"].astimezone(tz)
      moon_rise = str(mrise)[11:16]
      stampa("Moon rise      = " + str(mrise), isDebug, logLevel, 0)
   except:
      mrise="--"
      moon_rise="--"

   try:
      mset= smt["set"].astimezone(tz)
      moon_set = str(mset)[11:16]
      stampa("Moon set       = " + str(mset), isDebug, logLevel, 0)
   except:
      mset="--"
      moon_set="--"



   # ricalcolo luna pre e post:
   smt_prima = suncalc2.getMoonTimes(datacalcolo+timedelta(days=-1), latitude, longitude)
   smt_dopo  = suncalc2.getMoonTimes(datacalcolo+timedelta(days=1), latitude, longitude)

   if moon_rise!="--" and moon_set!="--":
      if mrise > mset:
         if datacalcolo <=mset:
            # mrise del giorno prima
            mrise= "--"
            moon_rise = "--"
         elif (datacalcolo > mset and datacalcolo < mrise) or (datacalcolo >=mrise):
            # mset del giorno dopo
            mset= "--"
            moon_set="--"

   stampa("NEW Moon Rise  = " + str(mrise), isDebug, logLevel, 0)
   stampa("NEW Moon Set   = " + str(mset), isDebug, logLevel, 0)

   luna_sorta= False
   if moon_rise == "--":
      luna_sorta = True
   else:
      if datacalcolo > mrise:
         luna_sorta = True

   luna_tramontata = True
   if moon_set == "--":
      luna_tramontata = False
   else:
      if datacalcolo < mset:
         luna_tramontata = False

   #calculating phase
   ph = ""
   if mf>=0.86 or  mf<0.12:
      ph = "New"
   elif mf>=0.12  and mf<0.21:
        ph = "WaxCr"
   elif mf>=0.21  and mf<0.32:
        ph = "1st Q"
   elif mf>=0.32  and mf<0.39:
        ph = "WaxGib"
   elif mf>=0.37  and mf<0.62:
        ph = "Full"
   elif mf>=0.62  and mf<0.69:
        ph = "WanGib"
   elif mf>=0.69 and mf<0.78:
        ph = "LastQ"
   elif mf>=0.78 and mf<=0.88:
        ph = "WanCr"

    #Gestione Riduzione esposizione luna
   try:
      moonRise_factor = 1
      # calcolo riduzione presenza luna
      if moon_rise == "--":
         # applicare la riduzione
         luna_sorta = True
      else:
         #esiste un orario in cui la luna sorge
         dmr = datacalcolo - (mrise+timedelta(minutes= -mr_offset))
         deltamoonrise = int(dmr.total_seconds() / 60)
         if deltamoonrise > 0:
            luna_sorta = True
            if deltamoonrise >= 0 and deltamoonrise < mr_duration:
               # la luna è sorta ed è nel transitorio
               moonRise_factor = round(deltamoonrise/mr_duration,3)
         else:
            #la luna non è ancora sorta
            luna_sorta = False
            moonRise_factor=0
   except Exception as e:
      stampa("errore nel moonRise", isDebug, logLevel, 0)
      stampa("type error: " + str(e), isDebug, logLevel, 0)
      stampa(traceback.format_exc(), isDebug, logLevel, 0)

   try:
      moonSet_factor = 1
      if moon_set =="--":
         # applicare la riduzione
         luna_tramontata = False
      else:
         #esiste una orario di tramonto luna.
         dms = (mset+timedelta(minutes=+ms_offset)) - datacalcolo
         deltamoonset = int(dms.total_seconds() / 60)
         if deltamoonset > 0:
            luna_tramontata = False
            if deltamoonset >= 0 and deltamoonset < ms_duration:
               # la luna tramonta ed è nel transitorio
               moonSet_factor = round((deltamoonset/ms_duration),3)
         else:
            luna_tramontata = True
            moonSet_factor = 0
   except Exception as e:
      stampa("errore nel moonSet", isDebug, logLevel, 0)
      stampa("type error: " + str(e), isDebug, logLevel, 0)
      stampa(traceback.format_exc(), isDebug, logLevel, 0)

   stampa("Moon is rise   = "+str(luna_sorta), isDebug, logLevel, 0)
   stampa("Moon is set    = "+str(luna_tramontata), isDebug, logLevel, 0)

   if luna_sorta == True and luna_tramontata == False:
     stampa("full moon red  = "+str(full_moon_reduc), isDebug,logLevel,0)
     stampa("moon fraction  = "+str(fr), isDebug,logLevel,0)
     stampa("moonSet  factor= "+str(moonSet_factor), isDebug,logLevel,0)
     stampa("moonRise factor= "+str(moonRise_factor), isDebug,logLevel,0)
     moon_factor = round(1-(full_moon_reduc * fr * moonSet_factor * moonRise_factor),3)

     # | coeff | frazione | moon_rise | moon_set | tot     | esp
     # |  0.7  |   0,01   |     1     |     1    |  0.007  | 55 *(1-0.007)= 54.61
     # |  0.7  |   0,10   |     1     |     1    |  0.07   | 55 *(1-0.070)= 51.10
     # |  0.7  |   0,30   |     1     |     1    |  0.21   | 55 *(1-0.210)= 43.45
     # |  0.7  |   0,70   |     1     |     1    |  0.49   | 55 *(1-0.490)= 28.05
     # |  0.7  |   1,00   |     1     |     1    |  0.7    | 55 *(1-0.700)= 16.50
     # |  0.7  |   0,30   |     1     |     0,9  |  0.19   | 55 *(1-0.700)= 16.50
     # |  0.7  |   1,00   |     1     |     1    |  0.7    | 55 *(1-0.700)= 16.50
   else:
     # moon not visible, so no reduction
     moon_factor = 1

   stampa("Total Moon red (1=no reduction)= "+str(moon_factor), isDebug, logLevel, 0)
 
   valori=["","",0,"",0]
   valori[0] = moon_rise
   valori[1] = moon_set
   valori[2] = fr
   valori[3] = ph
   valori[4] = moon_factor
   return valori


def riduzioneQuadratica(deltaminuti, durata):
    #riduzione_quadratica = round(math.exp(-(deltaminuti**2)/(2*(durata/3)**2))  ,4)
    rid =  math.exp(-(deltaminuti**2)/(2*(durata/3)**2))
    return rid

def stampa(stringa, isDebug, logLevel, logActual):
    if isDebug==False:
        return
    if logLevel>=logActual:
        print("   " + stringa)
    return



