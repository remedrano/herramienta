var express = require('express');
var app = express();


function comparacionImagenes(pathInicio, pathFin , nombreFinal) {

    var resemble = require('node-resemble-js');

    var fs = require('fs');
    var img1 = fs.readFileSync(pathInicio );
    var img2 = fs.readFileSync(pathFin);

    console.log(pathInicio);
    console.log(pathFin);
    console.log(nombreFinal);


    var comparacion = resemble(img1).compareTo(img2).onComplete(function (data) {
        data.getDiffImage().pack().pipe(fs.createWriteStream(nombreFinal));
        console.log("Comaparacion realizada");
    });



}


app.listen(3000, function () {
    console.log('Example app listening on port 3000!');


    var fs = require('fs');
    var path = require('path')
    const resultadosCalabash = '../../../../calabash/resultados_small/';
    const resultadosCalabashDiff = '../../../../vrt/screenshots_resultados/'
    var directorios = fs.readdirSync(resultadosCalabash);
    var directoriosComparar = fs.readdirSync(resultadosCalabash);
    var comparados = [];

    var cantidadTotal = 0;
    directorios.forEach(directorio => {


        var rutaInicial = resultadosCalabash + directorio
        var primerArchivoComparar = null;

        fs.readdirSync(rutaInicial).forEach(primerArchivo => {
            var ext = path.extname(primerArchivo);
            if ((ext !== '.html')) { //Comparar imagenes
                primerArchivoComparar = primerArchivo;
                var arreglo = primerArchivoComparar.split("_")[1];
                var numero = arreglo.split(".")[0];

                directoriosComparar.forEach(directoriosComparar => {

                    if (!comparados.includes(directoriosComparar)) {
                        if (directoriosComparar === directorio) {
                            return true;
                        } else {
                            var ruta = resultadosCalabash + directoriosComparar
                            fs.readdirSync(ruta).forEach(fileFinal => {
                                if (path.extname(ruta + "/" + fileFinal) !== '.html') {
                                    if (fileFinal === "screenshot_" + numero + ".png") {

                                        var dir = resultadosCalabashDiff + directorio
                                        //var img1 = fs.readFileSync(ruta + "/" + fileFinal);
                                        //var img2 = fs.readFileSync(rutaInicial + "/" + primerArchivoComparar);

                                        if (!fs.existsSync(dir)) {
                                            fs.mkdirSync(dir);
                                        }

                                        const options = {
                                            misMatchPercentage: 100, // %
                                            isSameDimensions: true, // or false
                                            dimensionDifference: {width: 0, height: -1}, // defined if dimensions are not the same
                                        };

                                        //console.log(  dir+ "/"+fileFinal )

                                        comparacionImagenes( ruta + "/" + fileFinal , rutaInicial + "/" + primerArchivoComparar, dir+ "/"+fileFinal );
                                        //cantidadTotal ++; //comparacionImagenes('diff_paleta' + numero + '.png');


                                    }
                                    else {
                                        return true;
                                    }
                                }
                                else {
                                    return true;
                                }
                            })
                        }
                    }
                });
            } else {
                return true;
            }
        });

        comparados.push(directorio);

    })

    for (var i = 0; i < cantidadTotal; i++) {
        comparacionImagenes('diff_paleta' + i + '.png');
    }
});