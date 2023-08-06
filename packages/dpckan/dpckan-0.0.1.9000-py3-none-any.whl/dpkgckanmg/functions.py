import urllib
import json
import pprint
import os
import requests
import json
import sys
import shutil
import time
import json
import codecs
import importlib
import time
from urllib.parse import quote
from frictionless_ckan_mapper import ckan_to_frictionless as converter

separador = os.path.sep

def buscaListaDadosAbertos(authorizaton):
    request = urllib2.Request('https://homologa.cge.mg.gov.br/api/3/action/package_list')
    #request.add_header('Authorization', authorizaton)
    response_dict = json.loads(urllib2.urlopen(request, '{}').read())
    return response_dict['result']

def buscaDataSet(id,authorization):
        parametros = {
            'id': id
        }


        headers = {
    'Authorization': authorization
    }

        data_string = quote(json.dumps(parametros))
        request = urllib.request.Request('https://homologa.cge.mg.gov.br/api/3/action/package_show', data=data_string.encode('utf-8'), headers=headers)
        #request.add_header('Authorization', authorization)
        response_dict = json.loads(urllib.request.urlopen(request).read())
        #for i in range(len(response_dict['result']['resources']))
        if(response_dict['success'] == True and response_dict["result"]["resources"] != []):
            return response_dict['result']['resources']
        else:
            return response_dict['result']['id']

def buscaPastaArquivos(diretorio,separador):
    os.chdir(diretorio)
    listArquivos = []
    all_subdirs = [d for d in os.listdir(diretorio) if os.path.isdir(d)]
    #all_subdirs.remove('.cache')
    #pprint.pprint(all_subdirs)
    for dirs in all_subdirs:
        dir = os.path.join(diretorio, dirs)
        os.chdir(dir)
        current = os.getcwd()
        new = str(current).split(separador)[-1]
        listArquivos.append(new)
    return listArquivos

def buscaArquivos(diretorio,separador,isJson):
    #pprint.pprint(diretorio)
    os.listdir(diretorio)
    #pprint.pprint(os.listdir(diretorio))
    listArquivos = []
    all_subdirs = os.listdir(diretorio)#[d for d in os.listdir(diretorio) if os.path.isdir(d)]
    #all_subdirs.remove('.cache')
    for dirs in all_subdirs:
        #dir = os.path.join(diretorio, dirs)
        #os.chdir(dir)
        #current = os.getcwd()
        new = str(dirs)#.split(separador)[-1]

        if(not isJson and (new.find(".xls") > 0 or new.find(".csv") > 0)):
            listArquivos.append(new)
        elif(isJson and new.find(".json") > 0):
            listArquivos.append(new)

    #pprint.pprint(listArquivos)
    return listArquivos

def removePastaArquivos(diretorio,separador,comando,so,arquivo):
        os.chdir(diretorio)
        listArquivos = []
        #all_subdirs = [d for d in os.listdir(diretorio) if os.path.isdir(d)]
        #all_subdirs.remove('.cache')
        #pprint.pprint(os.path.isdir(diretorio))
        #for dirs in all_subdirs:
            #dir = os.path.join(diretorio, dirs)
        if os.path.isdir(diretorio):
            if(so == "WINDOWS"):
                arquivoDel = diretorio + separador + arquivo
                if(os.path.exists(arquivoDel)):
                    os.system(comando.replace('filename',arquivoDel))
                #time.sleep(20)
                #shutil.rmtree(diretorio)
            else:
                arquivoDel = diretorio + separador + arquivo
                comandoCompleto = comando + arquivoDel
                os.system(comandoCompleto)

def criarArquivo(authorization,package_id,caminhoCompleto,separador):
    format = caminhoCompleto.split(separador)[-1]
    formato = format.split('.')[1]
    nome = format
    #alterar os parametros passando somente id
    if(caminhoCompleto.find("http") > 0):
        saida = requests.post('https://homologa.cge.mg.gov.br/api/action/resource_create',
              data={"package_id":package_id,"name" : format,"url":caminhoCompleto},
              #data=dataset_dictAtual,
              headers={"Authorization": authorization})
    else:
        files = {'upload': (caminhoCompleto.split(separador)[-1], open(caminhoCompleto, 'rb'), 'text/' + formato)}
        saida = requests.post('https://homologa.cge.mg.gov.br/api/action/resource_create',
              data={"package_id":package_id,"name" : format},
              #data=dataset_dictAtual,
              headers={"Authorization": authorization},
              files = files)
    time.sleep(10)

def lerDadosJson(diretorio,nomeArquivo):
    with open(diretorio) as json_file:
        data = json.load(json_file)
        #pprint.pprint(data)
        tagsJson = {}
        tagsJson['tags'] = []
        for t in data['tags']:
            #pprint.pprint(t)
            tagsJson['tags'].append({'name': str(t)})

        #pprint.pprint(tagsJson['tags'])
        dataset_dict = [{
            'title': str(data['title']).replace('_',' ').upper(),
            'name':  nomeArquivo,
            'notes': str(data['notes']).replace('_',' '),
            'private': str(data['private']),
            #'author': data['author'].replace("\'u",''),
            'tags': tagsJson['tags'],
            'maintainer': str(data['maintainer']),
            'maintainer_email': str(data['maintainer_email']),
            #'type': data['type'].replace("\'u",''),
            'owner_org': 'controladoria-geral-do-estado',
            'url': str(data['url'])
        }]
    return dataset_dict

def lerDadosJsonResources(diretorio):
    with codecs.open(diretorio,'r', 'utf-8-sig') as json_file:
        data = json.load(json_file)
        dataset_dict = [{
            'resources': str(data['resources'])
        }]
    return dataset_dict

def lerCaminhoRelativo(diretorio):
    separador = os.path.sep
    with codecs.open(diretorio,'r', 'utf-8-sig') as json_file:
        data = json.load(json_file)
        for m in data.keys():
            if(m == 'resources'):
               for t in data[m]:
                   existe = 0
                   if(t['path'].find('http://') > 0):
                       existe = 1
                   if(t['path'].find('https://') > 0):
                       existe = 1

                   if(existe):
                     path = t['path'].replace(r'/',separador)
                     path = path.replace('\\',separador)
                     caminho = path.split(separador)[-1]
                     return path.split(separador)[0]
                   else:
                     return t['path']



def lerDadosJsonMapeado(diretorio,authorization,isUpdate,id):
    listaParametros = ["license_title","maintainer","relationships_as_object","private","maintainer_email","num_tags","id","metadata_created","metadata_modified","author_email","state","version","creator_user_id","type","num_resources","groups","license_id","relationships_as_subject","isopen","url","owner_org","extras","title","revision_id","update"]
    with codecs.open(diretorio,'r', 'utf-8-sig') as json_file:
        #pprint.pprint(json_file)
        data = json.load(json_file)
        #pprint.pprint(data)
        tagsJson = {}
        tagsJson['tags'] = []
        tagsDicionario = {}
        tagsDicionario['fields'] = []
        dataset_dict = {}
        #isUpdate = 'false'

        if(id == 'null'):
            id = 'null'

        for m in data.keys():
                #pprint.pprint(t)
                if(str(m) == 'keywords'):
                    for t in data[m]:
                        tagsJson['tags'].append({'name': t})
                    #pprint.pprint(tagsJson)
                    y = { 'tags' : tagsJson['tags'] }
                    dataset_dict.update(y)
                elif(str(m) == 'fields'):
                    for t in data[m]:
                        tagsDicionario['fields'].append({'id': t})
                    #pprint.pprint(tagsJson)
                    y = { 'fields' : tagsDicionario['fields'] }
                    dataset_dict.update(y)
                elif ((str(m) == 'resources')):
                    y = { str(m) : str(data[m]) }
                    #dataset_dict.update(y)
                elif (str(m) == 'name'):
                    y = { str(m) : str(data[m]) }
                    dataset_dict.update(y)
                elif (str(m) == 'description'):
                    y = { 'notes' : str(data[m]) }
                    dataset_dict.update(y)
                elif (str(m) == 'path'):
                    y = { 'url' : str(data[m]) }
                    dataset_dict.update(y)
                elif (str(m) == 'package_id'):
                    id = str(data[m])
                    y = { 'id' : id }
                    dataset_dict.update(y)
                elif (str(m) == 'update'):
                    isUpdate = 'true'
                elif (str(m) == 'contributors'):
                    for c in data[m]:
                        if(c['title']):
                            y = { "author" : c["title"] }
                            dataset_dict.update(y)
                        if(c['role'] == "publisher"):
                          y = { "owner_org" : c["organization"] }
                          dataset_dict.update(y)
                else:
                    if(str(m) in listaParametros):
                        y = { str(m) : str(data[m]) }
                        dataset_dict.update(y)

        if(isUpdate == 'true'):
            resources = buscaDataSet(id,authorization)
            y = { 'resources' : resources }
            dataset_dict.update(y)

        #encontrou = 'false'
        #for m in data.keys():
        #    if(str(m) == 'owner_org'):
        #        encontrou = 'true'

        #if(encontrou == 'false'):
        #    y = {'owner_org': 'controladoria-geral-do-estado-cge'}
        #    dataset_dict.update(y)

                #pprint.pprint(tagsJson['tags'])
                #dataset_dict = {
                #'title': str(data['title']).replace('_',' ').upper(),
                #'name': nomeArquivo,
                #'notes': str(data['notes']).replace('_',' '),
                #'private': str(data['private']),
                #'author': data['author'].replace("\'u",''),
                #'tags': tagsJson['tags'],
                #'maintainer': str(data['maintainer']),
                #'maintainer_email': str(data['maintainer_email']),
                #'type': data['type'].replace("\'u",''),
                #'owner_org': 'controladoria-geral-do-estado'
                #}
        #pprint.pprint(dataset_dict)
    dataset_dict = json.dumps(dataset_dict)
    return dataset_dict

def lerDadosJsonMapeadoResources(diretorio,authorization,isUpdate,id,separador):
    nome = diretorio.split(separador)[-1]
    dataset_dict = {}
    tagsDicionario['fields'] = []
    with codecs.open(diretorio,'r', 'utf-8-sig') as json_file:
       data = json.load(json_file)
       for m in data.keys():
           if ((str(m) == 'resources')):
               for r in data[m]:
                   if(r['name'] == nome):
                       for t in data[m]:
                           tagsDicionario['fields'].append({'id': t})
                           y = { 'fields' : tagsDicionario['fields'] }
                           dataset_dict.update(y)
    return dataset_dict


def importaDataSet(authorization,url,diretorio,format,privado,autor,type,tags,separador,caminhoPasta,comandoDelete,so, informed_environment='homologa'):
    try:
        url = environment(informed_environment)
        arquivosData = buscaArquivos(diretorio + separador + "data",separador,bool(False))

        #+ separador + url
        #caminhoCompletoJson = caminhoCompleto.replace(format,'json')
        caminhoCompletoJson = diretorio + separador + "datapackage" + '.json'
        #pprint.pprint(caminhoCompletoJson)
        #caminhoCompletoJson = local-onde-havia-caminho-maquina
        if(os.path.isfile(caminhoCompletoJson)):
            dataset_dict = lerDadosJsonMapeado(caminhoCompletoJson,authorization,'false','null')
        # Use the json module to dump the dictionary to a string for posting.

        arqPub = []
        with codecs.open(caminhoCompletoJson,'r', 'utf-8-sig') as json_file:
        #pprint.pprint(json_file)
            data = json.load(json_file)
            for j in data:
                if(j == 'resources'):
                    r = data[j]
                    for s in r:
                        arqPub.append(str(s['path']).split('/')[-1])

        data_string = quote(dataset_dict)

        headers = {
        'Authorization': authorization
        }

        # We'll use the package_create function to create a new dataset.
        request = urllib.request.Request(f'https://{url}/api/action/package_create', data=data_string.encode('utf-8'), headers=headers)

        # Creating a dataset requires an authorization header.
        # Replace *** with your API key, from your user account on the CKAN
        # site
        # that you're creating the dataset on.
        #request.add_header('Authorization', authorization)

        # Make the HTTP request.
        response = urllib.request.urlopen(request) #urllib.urlopen(request, data_string)
        assert response.code == 200

        # Use the json module to load CKAN's response into a dictionary.
        response_dict = json.loads(response.read())
        assert response_dict['success'] is True

        # package_create returns the created package as its result.
        created_package = response_dict['result']
        #pprint.pprint(created_package)
        if(created_package['id']):
            #caminhoCompleto = diretorio + '\\' + url + '\\' + url + '.' +
            #format
            id = str(created_package['id']).replace('u','')
        #pprint.pprint(arquivosData)

    except Exception as e:
        if(e.code == 409):
            print("O pacote de dados ja existe. Verifique as informacoes e tente novamente.")
        else:
            print("Nao foi possivel realizar a importacao do arquivo. Erro: " + e)

    try:
        arquivosDataJson = buscaArquivos(diretorio,separador,bool(True))
        for d in range(len(arquivosDataJson)):
            caminhoCompleto = diretorio + separador + arquivosDataJson[d]
            pprint.pprint("------------------------------------------------")
            pprint.pprint("Importacao de arquivo inicializada: " + arquivosDataJson[d])
            criarArquivo(authorization,id,caminhoCompleto,separador)
            pprint.pprint("Importacao de arquivo finalizada: " + arquivosDataJson[d])
            pprint.pprint("------------------------------------------------")
    except Exception as e:
        print("Nao foi possive importar o arquivo contendo os metadados. Erro: " + e)

    try:
        for d in range(len(arquivosData)):
            #pprint.pprint("Arquivolido")
            #pprint.pprint(arquivosData[d])
            caminhoCompleto = diretorio + separador + "data" + separador + arquivosData[d]
            #pprint.pprint(caminhoCompleto)
            existe = arquivosData[d] in arqPub
            if(os.path.isfile(caminhoCompleto) and existe):
                #pprint.pprint("CriaArquivo")
                #pprint.pprint(caminhoCompleto)
                pprint.pprint("------------------------------------------------")
                pprint.pprint("Importacao de arquivo inicializada: " + arquivosData[d])
                criarArquivo(authorization,id,caminhoCompleto,separador)
                pprint.pprint("Importacao de arquivo finalizada: " + arquivosData[d])
                pprint.pprint("------------------------------------------------")
    except Exception as e:
        print("Nao foi possivel realizar a importacao do arquivo de dados. Erro: " + e)

    try:
        resources = buscaDataSet(id,authorization)
        for d in resources:
            resource_id = d['id']
            name = str(d['name'])
            if(not name.find(".json") > 0):
                pprint.pprint("Atualizacao de dicionario de dados inicializada: " + name)
                atualizaDicionario(caminhoCompletoJson,resource_id,name,authorization,separador)
                pprint.pprint("Atualizacao de dicionario de dados finalizada: " + name)
    except Exception as e:
        print("Nao foi possivel atualizar o dicionario de dados. Erro: " + e)

    except Exception as e:
        if(e.code == 409):
            print("O pacote de dados ja existe. Verifique as informacoes e tente novamente.")
        else:
            print("Ocorreu um erro inesperado. Erro: " + e)


def comparaDataSet(dataset_dict,resources):
    dataset_dictNovo = {}

    for m in resources.keys():
        if(dataset_dict.has_key(m) and (str(resources[m]) != str(dataset_dict[m]))):
            #pprint.pprint("Escopo1")
            #pprint.pprint(str(m))
            #pprint.pprint(str(resources[m]))
            #pprint.pprint(str(dataset_dict[m]))
            #pprint.pprint("Escopo2")
            y = { str(m) : str(dataset_dict[m]) }
            resources[m] = str(dataset_dict[m])
            dataset_dictNovo.update(y)

    return resources

def atualizaMeta():
    dataset_dict = {
    'title': "teste",
    'name':  "teste4554",
    'notes': "nota",
    'private': 'false',
    'author': "fulano de tal",
    'type': "text/csv",
    'tags': [{"name": "my_tag"}, {"name": "my-other-tag"}],
    'owner_org': 'controladoria-geral-do-estado',
    'id': 'local-onde-havia-chave-acesso'
    }

    #pprint.pprint(dataset_dict)
    # Use the json module to dump the dictionary to a string for posting.
    data_string = quote(json.dumps(dataset_dict))

    headers = {
    'Authorization': authorization
    }

    # We'll use the package_create function to create a new dataset.
    request = urllib.request.Request('https://homologa.cge.mg.gov.br/api/action/package_update', data=data_string.encode('utf-8'), headers=headers)

    # Creating a dataset requires an authorization header.
    # Replace *** with your API key, from your user account on the CKAN site
    # that you're creating the dataset on.
    #request.add_header('Authorization',
    #'local-onde-havia-chave-acesso')

    # Make the HTTP request.
    response = urllib.request.urlopen(request)
    assert response.code == 200

    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read())
    assert response_dict['success'] is True

    # package_create returns the created package as its result.
    created_package = response_dict['result']

    return created_package

def updateMetaData(caminhoCompleto,separador,url,authorization):
    caminhoCompletoJson = caminhoCompleto + separador + 'datapackage.json'

    #pprint.pprint(caminhoCompletoJson)
        #caminhoCompletoJson = local-onde-havia-caminho-maquina
    if(os.path.isfile(caminhoCompletoJson)):
        dataset_dict = lerDadosJsonMapeado(caminhoCompletoJson,url,authorization,'null')
        #pprint.pprint(dataset_dict)
    else:
        #pprint.pprint(caminhoCompletoJson)
        # Put the details of the dataset we're going to create into a dict.
        dataset_dict = {
            'title': str(url).replace('_',' ').upper(),
            'name':  str(url),
            'notes': str(url).replace('_',' '),
            'private': privado,
            'author':autor,
            'type': type,
            'tags': [{"name": "my_tag"}, {"name": "my-other-tag"}],
            'owner_org': 'controladoria-geral-do-estado'
        }

    # Use the json module to dump the dictionary to a string for posting.
    data_string = quote(json.dumps(dataset_dict))


    headers = {
    'Authorization': authorization
    }

    # We'll use the package_create function to create a new dataset.
    request = urllib.request.Request('https://homologa.cge.mg.gov.br/api/action/package_update', data=data_string.encode('utf-8'), headers=headers)

    # Creating a dataset requires an authorization header.
    # Replace *** with your API key, from your user account on the CKAN site
    # that you're creating the dataset on.
    #request.add_header('Authorization', authorizaton)

    # Make the HTTP request.
    response = urllib.request.urlopen(request)
    assert response.code == 200

    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read())
    assert response_dict['success'] is True

    # package_create returns the created package as its result.
    update_package = response_dict['result']
    #pprint.pprint(response_dict['result'])

def atualizaDicionario(datapackage,resource_id,resource,authorization,separador):
    with codecs.open(datapackage,'r', 'utf-8-sig') as json_file:
        data = json.load(json_file)
        ckan_dict = data
        dataset_dict = {}
        for m in data.keys():
            if(str(m) == 'resources'):
                        for n in data[m]:
                            name = str(n['path']).split('/')[-1]
                            if(name == resource):
                                schema = n['schema']
                                fieldsList = n['schema']['fields']
                                resource_id = { "resource_id" : resource_id }
                                dataset_dict.update(resource_id)
                                force = { "force" : "True" }
                                dataset_dict.update(force)
                                fields = []
                                #fields['fields'] = []
                                for p in fieldsList:
                                    if 'type_override' in p.keys():
                                        metaInfo = {"label": p["title"], "notes" : p["description"] , "type_override" : p["type_override"] }
                                    else:
                                        metaInfo = { "label": p["title"], "notes" : p["description"] }
                                    if p["type"] == "string":
                                        tipo = "text"
                                    else:
                                        tipo = p["type"]

                                    field = { "type" : tipo, "id" : p["name"] , "info" : metaInfo }

                                    fields.append(field)
                                #pprint.pprint(fields)
                                fieldsFull = { "fields" : fields}
                                dataset_dict.update(fieldsFull)

    frictionless_package = converter.dataset(dataset_dict)
    frictionless_package = json.dumps(frictionless_package)

    #return
    #requests.post('https://homologa.cge.mg.gov.br/api/action/datastore_create',
    #              data=frictionless_package,
    #              headers={"Authorization": authorization})

     # Use the json module to dump the dictionary to a string for posting.
    #data_string = quote(frictionless_package)

    headers = {
    'Authorization': authorization
    }
    #data = urllib.parse.urlencode(frictionless_package)
    # We'll use the package_create function to create a new dataset.
    request = urllib.request.Request('https://homologa.cge.mg.gov.br/api/action/datastore_create', data=frictionless_package.encode('utf-8'), headers=headers)

    # Creating a dataset requires an authorization header.
    # Replace *** with your API key, from your user account on the CKAN site
    # that you're creating the dataset on.
    #request.add_header('Authorization', authorization)

    # Make the HTTP request.
    response = urllib.request.urlopen(request)
    assert response.code == 200
    time.sleep(10)
    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read())
    assert response_dict['success'] is True

def environment(informed_environment):
  url = ''
  if informed_environment == 'homologa':
    url = 'homologa.cge.mg.gov.br'
  elif informed_environment == 'portal':
    url = 'https://dados.mg.gov.br/'
  else:
    url = 'homologa.cge.mg.gov.br'
  return url
