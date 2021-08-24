## RUN THIS CODE BEFORE RUNNING dataStorageFlask.py because you need data before requesting for it.

from m2m import get_data,discovery,get_filtered_uri,get_group_data
import xml.etree.ElementTree as ET
import json
import ast
import datetime
from time import sleep
from plotly.offline import plot
import plotly.graph_objects as go

server = "https://onem2m.iiit.ac.in:443"

descriptor_inverter_0 = "/~/in-cse/in-name/AE-SL/SL-VN03-00/" #80K
descriptor_inverter_1 = "/~/in-cse/in-name/AE-SL/SL-VN02-00/" #25K
descriptor_inverter_2 = "/~/in-cse/in-name/AE-SL/SL-VN02-01/" #80K

def retrieveAllData(server,solar):
    uriso = server+ solar 
    returnCode , unfilteredData = get_group_data(uri = uriso)
    print(unfilteredData)
    return

def latestInstance(server,solar):
    # solar = "/~/in-cse/in-name/AE-SL/SL-VN03-00/Data/la/"
    uriso = server + solar
    returnCode, DescriptorData = get_data(uriso)
    # print(DescriptorData)
    return DescriptorData
    # Handle nan return
    # DescriptorData = DescriptorData.replace("nan", "-1.0")
    # return ast.literal_eval(DescriptorData)


def getDescriptorInfo(server,solar):
    # solar = "/~/in-cse/in-name/AE-SL/SL-VN03-00/Descriptor/la/"
    uriso = server + solar
    returnCode,DescriptorDataXML = get_data(uriso)
    tree = ET.fromstring(DescriptorDataXML)
    dataDescriptor = {}
    for child in tree:
        # print(f"{child.attrib['name']}:  {child.attrib['val']}")
        dataDescriptor[child.attrib["name"]] = child.attrib["val"]
    dataStringParams = dataDescriptor["Data String Parameters"]
    return ast.literal_eval(dataStringParams)
    
def getDataSolarInverter(descriptor_inverter):
    
    # desInfo = getDescriptorInfo(server,descriptor_inverter)    
    laData = latestInstance(server)
    timestamp = datetime.datetime.fromtimestamp(laData[0])
    # print(type(timestamp),timestamp)

# def main():
#     # store descriptor info for all inverters.
#     # 
#     from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
#     engine = create_engine('sqlite:///test.db', echo = True)


#     meta = MetaData()

#     desInfo = getDescriptorInfo(server,descriptor_inverter_0+"Descriptor/la")

#     heads = []
#     for i in range(3):
#         head = [Column('ID', Integer, primary_key=True, autoincrement='auto'), Column(desInfo[0], DateTime)]
#         for x in desInfo[1:]:
#             head.append(Column(x, Float))
#         heads.append(head)

#     # headsWeather = []

#     tables = [
#         Table(f'inverter_{i}', meta, *heads[i]) for i in range(3)
#     ]


#     meta.create_all(engine)

#     conn = engine.connect()
    

#     while(1):
#         # currentTime = datetime.datetime.now()

#         la_data = []
#         la_data.append(latestInstance(server,descriptor_inverter_0+"Data/la"))
#         la_data.append(latestInstance(server,descriptor_inverter_1+"Data/la"))
#         la_data.append(latestInstance(server,descriptor_inverter_2+"Data/la"))
#         # print(la_data)
#         store = {}
#         for i in range(3):
#             la_data[i][0] = datetime.datetime.fromtimestamp(la_data[i][0])
#             del la_data[i][6]
#             for k in range(len(la_data[i])):
#                 store[desInfo[k]] = la_data[i][k]
#             ins = tables[i].insert().values(store)
#             res = conn.execute(ins)
#         # Sel
#         sleep(60)
        
def timePlot(laVal):
    x = []
    y = []
    a = -1
    for ct,i in enumerate(laVal['m2m:cin']):
        temp = []
        temp = (i['con'].split(','))
        
        temp[0] = temp[0][1:len(temp)]
        temp[-1] = (temp[-1][:-1])
        stamp = datetime.datetime.fromtimestamp(int(temp[0]))
        if(stamp not in x):
            x.append(stamp)
            y.append(float(temp[1]))
    return x,y
def Cmain():

    server = "https://onem2m.iiit.ac.in:443"
    descriptor_inverter = []
    descriptor_inverter.append("/~/in-cse/in-name/AE-SL/SL-VN03-00") #80K
    descriptor_inverter.append("/~/in-cse/in-name/AE-SL/SL-VN02-00") #25K
    descriptor_inverter.append("/~/in-cse/in-name/AE-SL/SL-VN02-01") #80K
    

    # speak_output = "Latest instance for inverter_0 : \n"
    # desInfo = getDescriptorInfo(server,descriptor_inverter[0]+"/Descriptor/la")
    laVal =[]
    laVal= [(latestInstance(server,k+"/Data?rcn=4"))for k in descriptor_inverter]
    # print(type(laVal),laVal.keys())
    # print(len(laVal['m2m:cin']))
    
    x1,y1 = timePlot(laVal[0])
    x2,y2 = timePlot(laVal[2])
    fig = go.Figure([go.Scatter(x = x1,y = y1,mode = 'lines',name = "Energy_PV0")])
    fig.add_trace(go.Scatter(x = x2,y = y2,name = "Energy_PV1"))
    name = "PV1vsPV2.jpeg"
    # fig.show()
    fig.write_image("images/"+name)
    return name,fig
 
def checkIfDuplicates_1(listOfElems):
    ''' Check if given list contains any duplicates '''
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True



def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time