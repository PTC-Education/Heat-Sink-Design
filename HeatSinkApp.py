from flask import Flask, render_template, request, redirect, url_for 
import json
import numpy as np 
import os 

from onshape_client.client import Client
from onshape_client.oas import BTFeatureScriptEvalCall2377
from onshape_client.onshape_url import OnshapeElement
from onshape_client.utility import parse_quantity


app = Flask(__name__)

appkey = ''
secretkey = ''
DID = ''
WID = '' 
EID = ''


# Search and check if a file named "OnshapeAPIKey.py" exists in the folder 
for _, _, files in os.walk('.'): 
    if "OnshapeAPIKey.py" in files: 
        exec(open('OnshapeAPIKey.py').read())
        appkey = access
        secretkey = secret
        break 


@app.route('/')
def index():
    return redirect(url_for("login"))


@app.route('/login')
def login():
    global appkey
    global secretkey
    global DID
    global WID
    global EID

    if appkey: 
        APPKEY = appkey 
    else: 
        APPKEY = None 
    if secretkey: 
        SECRETKEY = secretkey
    else: 
        SECRETKEY = None 
        
    DID = request.args.get('documentId')
    WID = request.args.get('workspaceId')
    EID = request.args.get('elementId')
    return render_template('login.html', APPKEY=APPKEY, SECRETKEY=SECRETKEY, DID=DID, WID=WID, EID=EID)


@app.route('/config')
def config():
    global appkey
    global secretkey
    global DID
    global WID
    global EID
    
    if not appkey or not secretkey: 
        appkey = request.args.get('appkey')
        secretkey = request.args.get('secretkey')
    if not DID or not WID or not EID: 
        DID = request.args.get('did') 
        WID = request.args.get('wid')
        EID = request.args.get('eid')

    return render_template('config.html', return1=configure_onshape_client(appkey, secretkey, DID, WID, EID))


# ################# Helper functions ####################################################################
def configure_onshape_client(access, secret, did, wid, eid):
    base = 'https://cad.onshape.com'
    client = Client(configuration={"base_url": base,
                                   "access_key": access,
                                   "secret_key": secret})
    try:
        return heat_transfer(client, did, wid, eid)
    except:
        return "Client not configured"


# Heat transfer calculation related
def heat_transfer(client, did, wid, eid):
    url = 'https://cad.onshape.com/documents/{}/w/{}/e/{}'.format(str(did), str(wid), str(eid))
    base = 'https://cad.onshape.com'
    fixed_url = '/api/partstudios/d/did/w/wid/e/eid/massproperties'

    method = 'GET'
    params = {'partId': "JHD"}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
               'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)
    fixed_url = fixed_url.replace('eid', eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
    parsed = json.loads(response.data)

    # Heat transfer calculation
    surface_area = np.mean(parsed["bodies"]["-all-"]["periphery"])
    area_unfin = float(get_variable_value(client, url, "", "Area_Unfin").split("*")[0])
    area_fin = surface_area - area_unfin - 0.0104
    FW = float(get_variable_value(client, url, "", "Fin_Width").split("*")[0])

    # The command below prints the entire JSON response from Onshape
    return "Total Heat Transfer: " + str(500 * (area_unfin + calc_efficiency(FW) * area_fin)) + "W."


def calc_efficiency(FW): 
    m = np.sqrt(8000/3 * (0.001+FW)/FW)
    Lc = 0.03 + FW/2000 / (0.001+FW)
    eff = np.tanh(m * Lc) / (m * Lc)
    return eff


# Helper functions to get the value of a variable 
script = r'''
    function(context, queries) {
            return getAllVariables(context);
        }
    '''


def get_variable_value(client, url, configuration, var_name):
    variables = get_variables(client, url, configuration)
    for x in variables:
        if var_name in x:
            return x[var_name]


def get_variables(client, url, configuration):
    element = OnshapeElement(url)
    script_call = BTFeatureScriptEvalCall2377(script=script)
    response = client.part_studios_api.eval_feature_script(
        element.did,
        element.wvm,
        element.wvmid,
        element.eid,
        bt_feature_script_eval_call_2377=script_call,
        _preload_content=False,
        configuration=configuration
    )
    measurements = json.loads(response.data.decode("utf-8"))["result"]["message"]["value"]
    parsed_measurements = parse_variables_from_map(measurements)
    variables = []
    for name, val in parsed_measurements.items():
        variables.append({name: val})
    return variables


def parse_variables_from_map(unparsed):
    parsed_variables = {}
    value = None
    for to_parse in unparsed:
        if is_fs_type(to_parse, "BTFSValueMapEntry"):
            key = to_parse["message"]["key"]["message"]["value"]
            candidate_message = to_parse["message"]["value"]
            if is_fs_type(candidate_message, ["BTFSValueMap", "BTFSValueArray"]):
                value = parse_variables_from_map(candidate_message["message"]["value"])
            elif is_fs_type(candidate_message, "BTFSValueWithUnits"):
                value = parse_quantity(candidate_message["message"])
            parsed_variables[key] = value
    return parsed_variables


def is_fs_type(candidate, type_name):
    result = False
    try:
        if isinstance(type_name, str):
            result = type_name == candidate["typeName"]
        elif isinstance(type_name, list):
            result = any(
                [type_name_one == candidate["typeName"] for type_name_one in type_name]
            )
    except:
        result = False
    return result
