from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import subprocess
from django.conf import settings
import os
from django.views.generic import base

ANDROID_ADB = getattr(settings, "ANDROID_ADB", None)
SDK_SIGNUP = getattr(settings, "SDK_SIGNUP", None)

RUTA_DESCARGA = getattr(settings, "RUTA_DESCARGA", None)

# Create your views here.
import json
from django.http import HttpResponse

class IndexView(base.View):

    def index(request):
        context = {}
        return render(request, 'index.html', context)

    def randomTesting( self ):
        rutas = os.walk('apk_finales')
        rutasFinales = []
        nombresLog = []

        for (dirpath, dirnames, filenames) in rutas:
            for file in filenames:
                filename, file_extension = os.path.splitext(file)
                if (file_extension == '.apk'):
                    nombreLog = str(os.path.basename(os.path.normpath(dirpath)))
                    apk = 'apk_finales/' + nombreLog + '/' + file
                    rutasFinales.append( apk )
                    nombresLog.append( nombreLog )
        i = 0
        apksUno = []
        apksDos = []
        apksTres = []
        apksCuatro = []
        apksCinco = []
        nombreLogUno = []
        nombreLogDos = []
        nombreLogTres = []
        nombreLogCuatro = []
        nombreLogCinco = []

        while i < len( nombresLog ) :
            if( i<600):
                apksUno.append( rutasFinales[i] )
                nombreLogUno.append( 'emulator-5554-' + nombresLog[i] )
            else:
                if (i >= 600 and i < 900 ):
                    apksDos.append(rutasFinales[i])
                    nombreLogDos.append('emulator-5556-' +nombresLog[i])
                else:
                    if (i >= 900 and i < 1200):
                        apksTres.append(rutasFinales[i])
                        nombreLogTres.append( 'emulator-5560-' +nombresLog[i])
                    else:
                        if (i >= 1200 and i <= 1500):
                            apksCuatro.append(rutasFinales[i])
                            nombreLogCuatro.append( 'emulator-5562-' + nombresLog[i])
            i = i + 1

        #Llamar los workers
        ejecutarMonkey( 'emulator-5554', '100', apksUno, nombreLogUno )

        print( apksUno )
        respuesta = True

        return HttpResponse(json.dumps(respuesta), content_type='application/json')


#Funcion principal para ejecutar el worker
def ejecutarMonkey( emulador, semilla, apks, nombresLog):
    i = 0
    while i < len(apks):
        print( apks[i] )
        # Firmar los apks para instalarlos
        comando = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore parcial.keystore -storepass 123456 " + apks[i] + " parcial"
        subprocess.call(comando, shell=False)

        # Instalar las apks para hacer monkey
        comando = "adb install " + apks[i]
        subprocess.call(comando, shell=False)

        #  Ejecutar monkeys con reporte de eventos
        comando = "adb shell  monkey -s "+semilla+" --ignore-crashes -p com.evancharlton.mileage -v 2000 --pct-syskeys 0 10"
        subprocess.call(comando, shell=False)

        # Ejecutar guardar solo errores
        comando = "adb shell logcat -d com.evancharlton.mileage:E *:E > /sdcard/logs/errors/" + nombresLog[i] + ".log "
        subprocess.call(comando, shell=False)
        # processDos = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE)
        # processDos.wait()

        # Descargar archivo de errores y reports en el local
        comando = "adb pull  /sdcard/logs/errors/" + nombresLog[i] + ".log " + RUTA_DESCARGA + "errors\\"
        subprocess.call(comando, shell=False)

        comando = "adb uninstall com.evancharlton.mileage "
        subprocess.call(comando, shell=False)

        # Limpiar logcat
        comando = "adb logcat -c "
        subprocess.call(comando, shell=False)
        i = i + 1
    respuesta = True