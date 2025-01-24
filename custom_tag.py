#Custom Tagger for AppDynamics by Ryan Plummer (rp93@cisco.com)
#Last Updated 1-24-2025 


import sys,json, requests;

#Enter Credentials Here
controllerurl = ""
accountname   = ""
apiclientname = ""
apisecret     = ""

headers    = {"Content-Type" : "application/x-www-form-urlencoded"}
auth       = (apiclientname, apisecret)
payload    = "grant_type=client_credentials&client_id="+str(apiclientname)+"@"+str(accountname)+"&client_secret="+str(apisecret)

#The type of the entity. The values can be APPLICATION, APPLICATION_COMPONENT,APPLICATION_COMPONENT_NODE, SIM_MACHINE, BASE_PAGE, BUSINESS_TRANSACTION
# Only Application Works at this time.
entityType = 'APPLICATION'

#List of entities. You can either use this or the command line.
entityGroup = ["Ryan_Test_Application_1","Ryan_Test_Application_2"]

#API or CMDB
source = "API"

#Enter List of key/value pairs You can either use this or the command line.
taglist = '[ {"key" : "vendor", "value" : "Ryantheon" } , {"key" : "user", "value" : "RyanGroup" }]'


#Gets the Token using the api user
def getAPIToken():
    #Get API Token
    apirequest = requests.post("https://"+str(controllerurl)+"/controller/api/oauth/access_token",headers=headers, auth=auth,data=payload)
    apidata    = json.loads(apirequest.text)
    token      = apidata["access_token"]
    print("Got Token!")
    return token

#Gets ApplicationID from EntityList (if entityType is 'Application')
def getApplicationID(applications,token):
    application_api_url = "/controller/rest/applications"
    headers    = {"Content-Type" : "application/x-www-form-urlencoded", "Authorization" : "Bearer "+str(token)}

    apirequest = requests.get("https://"+str(controllerurl) + str(application_api_url) + "?output=json",headers=headers)
    applist = []
    apitext = json.loads(apirequest.text)
    for app in apitext:
        for entity in applications:     
            if entity == app['name']:
                applist.append((entity,app['id']))
                break
    return applist

def createTagPayload(applist):
    entityPayload = '['
    appPayload = ''
    counter = 0
    for app in applist:
        if counter != 0:
            appPayload += ','
        appPayload += '{ "entityName" : "' + str(app[0]) + '", "entityId" : "' + str(app[1]) + '", "tags": ' + str(taglist) + '}'
        counter += 1
    entityPayload += str(appPayload) + ']'
    payload = '{"entityType" : "' + str(entityType) + '", "source" : "' + str(source) + '", "entities" : ' + str(entityPayload) + '}'
    return payload

def tagEntities(tagPayload):
    tag_api_url = "/controller/restui/tags/tagEntitiesInBatch"
    headers    = {"Content-Type" : "application/json", "Authorization" : "Bearer "+str(token)}
    apirequest = requests.post("https://"+str(controllerurl) + str(tag_api_url),data=tagPayload,headers=headers)
    print("Tagged Applications")
    print(apirequest.text)

def deleteTagsBatch(ids):
    delete_tag_url = "/controller/restui/tags/removeAllTagsOnEntitiesInBatch"
    headers    = {"Content-Type" : "application/json", "Authorization" : "Bearer "+str(token)}
    idlist = []
    for app in ids:
        idlist.append(app[1])

    payload = '{"entityType": "APPLICATION", "entityIds" : ' + str(idlist) + '}'
    apirequest = requests.post("https://"+str(controllerurl) + str(delete_tag_url),data=payload,headers=headers)
    print("Deleted Tags...")
    print(apirequest.text)


#Start
if len(sys.argv) == 1 or (sys.argv[1] != '-d' and sys.argv[1] != '-t'):
    print("No arguments or wrong arguments given. Use either '-t' (to tag) or '-d' (to delete)")
else:

    #Assign Arguments if any
    if len(sys.argv) >= 3:
        tester = sys.argv[2]
    #Check Type in EntityGroup (Should be list)
    try:
        if type(eval(tester)) is not list:
            raise TypeError("Format of Entity Group ( "+str(entityGroup)+" ) is not valid. This needs to be a list like ['Ryan_Test_Application_1','Ryan_Test_Application_2'] surrounded by double quotes")
    except Exception as e:
        print("Format of Entity Group ( "+str(entityGroup)+" ) is not valid. This needs to be a list like ['Ryan_Test_Application_1','Ryan_Test_Application_2'] surrounded by double quotes")

    entityGroup = eval(tester) 

    if sys.argv[1] == '-t':
        if len(sys.argv) == 4:
            taglist = str(sys.argv[3])

        #Check Type in TagList (Should be dict)
        try:
            if type(eval(taglist)[0]) is not dict:
                raise TypeError("Format of Tag List ( "+str(taglist)+" ) is not valid. This needs to be a list with a dictionaty like [{\"key\" : \"cheese\", \"value\" : \"Swiss\" }] surrounded by single quotes")
        except Exception as e:
            print("Format of Tag List ( "+str(taglist)+" ) is not valid. This needs to be a list with a dictionaty like [{\"key\" : \"cheese\", \"value\" : \"Swiss\" }] surrounded by single quotes")
    
    try:
        print('Getting Token...')
        token = getAPIToken()
        applist = getApplicationID(entityGroup,token)
        if sys.argv[1] == '-d':
            deleteTagsBatch(applist)
        elif sys.argv[1] == '-t':
            tagPayload = createTagPayload(applist)
            tagEntities(tagPayload)
        
    except TypeError as te:
        print
    except Exception as e:
        print('Something Broke...')
        print(e)



