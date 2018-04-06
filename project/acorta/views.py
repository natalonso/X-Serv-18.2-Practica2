from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import Pagina

@csrf_exempt
def principal(request):

    if request.method == 'GET':

        lista = Pagina.objects.all()
        salida = "<ul>"

        for url in lista:
            salida += '<li><a href="' + str(url.id) + '">' + url.url + '</a>'
        salida += "</ul>"

        return HttpResponse("""
                            <form action="" method="POST">
                            Servidor acortador de urls:<br>
                            <input type="text" name="url" placeholder="google.es"><br>
                            <input type="submit" value="Enviar">
                            </form>""" + "Las paginas disponibles hasta el momento son: \n" + salida)

    if request.method == 'POST':
        try:
            nuevapagina = Pagina(url=request.POST['url'])
            try:
                Pagina.objects.get(url=nuevapagina)
                return HttpResponse('Ya existia en nuestra BD')

            except Pagina.DoesNotExist:
                nuevapagina.save()
                return HttpResponse("<html><body><h1>URL ORIGINAL y URL ACORTADA: <br> URL ORIGINAL: " +
                        "<a href='https://" + str(nuevapagina) + "'>"+ str(nuevapagina)+ "</a><br> URL ACORTADA: " +
                        "<a href='https://" + str(nuevapagina) + "'>"+ str(nuevapagina.id)+ "</a></h1></body></html>")
        except KeyError:
                return HttpResponse("Debe rellenar el formulario")

def redireccion(request, identificador):
    print("identificador: " + str(identificador))
    #busco en la base de datos a ver si esta por el identificador
    try:
        redireccion = Pagina.objects.get(id=int(identificador))
        print("redireccion: " + str(redireccion))
        return HttpResponse("<html><meta http-equiv="+'refresh'+ " content="+'1'+";url=" + 'https://'
                            + str(redireccion) + "/></html>")
    except Pagina.DoesNotExist:
    #si no esta envio mensaje de error
        return HttpResponse("NO TENEMOS ESE IDENTIFICADOR")
