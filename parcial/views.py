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

    #Agrega el permiso de internet a todas las apks antes de ejecutar calabash
    def agregarPermisoInternetApks(self):

        rutas = os.walk('apks/originales')
        rutaJar = 'apks/apktool_2.3.4.jar'
        rutasDestino = 'apks/conpermiso'
        rutasDescomprimido = 'apks/descomprimidos'

        for (dirpath, dirnames, filenames) in rutas:
            for file in filenames:
                filename, file_extension = os.path.splitext(file)
                if (file_extension == '.apk'):
                    nombreLog = str(os.path.basename(os.path.normpath(dirpath)))
                    apk = 'apks/originales/' + nombreLog + '/' + file

                    #  Descrompimir
                    comando = "java -jar "+rutaJar+" d -f "+apk+" -o "+rutasDescomprimido+"/"+nombreLog
                    subprocess.call(comando, shell=True)

                    #Editar archivo
                    archivo = open(rutasDescomprimido +"/"+nombreLog + "/AndroidManifest.xml",'r')
                    data = archivo.readlines()
                    data[3] = data[3] + '\n\t<uses-permission android:name="android.permission.INTERNET" />\n'

                    with open(rutasDescomprimido +"/"+nombreLog + "/AndroidManifest.xml",'w') as file:
                        file.writelines(data)
                    archivo.close()

                    #  Comprimir
                    comando = "java -jar " + rutaJar + " b -f " + (rutasDescomprimido + "/" + nombreLog) + " -o " + (rutasDestino+"/"+nombreLog+"/"+"com.evancharlton.mileage_3110.apk")
                    subprocess.call(comando, shell=True)

        respuesta = True

        return HttpResponse(json.dumps(respuesta), content_type='application/json')


    #Ejecuta los escenarios de calabash
    def ejecutarCalabash(self):

        rutas = os.walk('apks/conpermiso')
        rutasDestino = 'calabash/resultados/'

        for (dirpath, dirnames, filenames) in rutas:
            for file in filenames:
                filename, file_extension = os.path.splitext(file)
                if (file_extension == '.apk'):
                    nombreLog = str(os.path.basename(os.path.normpath(dirpath)))
                    apk = '../apks/conpermiso/' + nombreLog + '/' + file

                    #  Firmar app calabash
                    comando = "calabash-android resign "+apk
                    subprocess.call(comando, shell=True, cwd='calabash/')

                    #  Crear carpeta de resultados
                    comando = "mkdir resultados/" + nombreLog+"/"
                    subprocess.call(comando, shell=True, cwd='calabash/')

                    #  Crear permisos
                    comando = "chmod  777 -R resultados/" + nombreLog + "/"
                    subprocess.call(comando, shell=True, cwd='calabash/')

                    #  Correr calabash en app
                    comando = "SCREENSHOT_PATH=resultados/"+nombreLog+"/ calabash-android run " + apk+" --format html --out resultados/"+nombreLog+"/reports.html "
                    subprocess.call(comando, shell=True, cwd='calabash/')

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