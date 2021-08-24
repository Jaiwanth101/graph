# coding=utf-8

import json
import logging
import os
import sys
import xml.etree.ElementTree as ET

import requests

# import utils

# utils.setup_logging()
# _log = logging.getLogger(__name__)

verify = True
mni = 12000


# def set_mni(new_mni: int = 12000):
#     global mni
#     mni = new_mni


def set_verify_cert_flag(flag: bool = True):
    """
    verify server certificate, default is true.
    however, the dev server certificate is invalid, hence need to set it to
    false for dev server.
    HENCE: before calling any of the API in this lib, set the flag accordingly
    using, set_verify_cert_flag()
    """
    global verify
    verify = flag
    return


def create_ae(self, uri_cse, ae_name, ae_labels="", data_format="json",
              api=None, acpi=None):
    if acpi is None:
        raise Exception("acpi not valid!!!")

    """
        Method description:
        Create an application entity(AE) inside the OneM2M framework/tree
        under the specified CSE

        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        data_format : [str] payload format
    """
    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/{};ty=2; charset=utf-8'.format(
            data_format)}

    body = {
        "m2m:ae": {
            "rn": "{}".format(ae_name),
            "api": (
                api
                if api is not None
                else "acp_admin"
            ),
            "acpi": acpi,
            "rr": "true",  # resource reachable from CSE
            "lbl": ae_labels
        }
    }

    try:
        response = requests.post(uri_cse, json=body, headers=headers,
                                 verify=verify)
    except TypeError:
        response = requests.post(uri_cse, data=json.dumps(body),
                                 headers=headers, verify=verify)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    return


def delete_ae(self, uri, fmt_ex="json"):
    """
        Method description:
        Deletes/Unregisters an application entity(AE) from the OneM2M
        framework/tree under the specified CSE

        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        fmt_ex : [str] payload format
    """
    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/{}; charset=utf-8'.format(fmt_ex)}

    response = requests.delete(uri, headers=headers, verify=verify)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    return


def register_ae(self, uri_cse, ae_name, labels="", fmt_ex="json"):
    """
        Method description:
        Registers an application entity(AE) to the OneM2M framework/tree
        under the specified CSE

        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        labels : [str] labels for the AE
        fmt_ex : [str] payload format
    """

    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/{};ty=2; charset=utf-8'.format(fmt_ex)}

    payload = {
        "m2m:ae": {
            "rn": "{}".format(ae_name),
            "api": "tap",
            "rr": "true",
            "lbl": labels
        }
    }

    try:
        response = requests.post(uri_cse, json=payload, headers=headers,
                                 verify=verify)
    except TypeError:
        response = requests.post(uri_cse, data=json.dumps(payload),
                                 headers=headers, verify=verify)

    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    return


def create_cnt(self, uri_ae, cnt_name="", cnt_labels="", fmt_ex="json"):
    """
        Method description:
        Creates a container(CON) in the OneM2M framework/tree
        under the specified AE

        Parameters:
        uri_ae : [str] URI for the parent AE
        cnt_name : [str] name of the container (DESCRIPTOR/DATA)
        fmt_ex : [str] payload format
    """

    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/{};ty=3; charset=utf-8'.format(fmt_ex)}

    payload = {
        "m2m:cnt": {
            "rn": "{}".format(cnt_name),
            "mni": 12000,
            "lbl": cnt_labels,
        }
    }

    try:
        response = requests.post(uri_ae, json=payload, headers=headers,
                                 verify=verify)
    except TypeError:
        response = requests.post(uri_ae, data=json.dumps(payload),
                                 headers=headers, verify=verify)

    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    return


def create_desc_cin(self, uri_desc_cnt, node_description, desc_cin_labels="",
                    data_format="json"):
    """
        Method description:
        Creates a descriptor content instance(desc_CIN) in the OneM2M framework/tree
        under the specified DESCRIPTOR CON

        This holds the detailed description for an specific AE

        Parameters:
        uri_desc_cnt : [str] URI for the parent DESCRIPTOR CON
        data_format : [str] payload format
    """

    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/{};ty=4; charset=utf-8'.format(
            data_format)}

    body = {
        "m2m:cin": {
            "cnf": "application/json",
            "con": node_description,
            "lbl": desc_cin_labels,
        }
    }

    print("header: {}, body: {}".format(headers, body))

    try:
        response = requests.post(uri_desc_cnt, json=body, headers=headers,
                                 verify=verify)
    except TypeError:
        response = requests.post(uri_desc_cnt, data=json.dumps(body),
                                 headers=headers, verify=verify)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    return


def create_data_cin(self, uri_cnt, value, cin_labels="", fmt_ex="json"):
    """
        Method description:
        Creates a data content instance(data_CIN) in the OneM2M framework/tree
        under the specified DATA CON

        Parameters:
        uri_cnt : [str] URI for the parent DATA CON
        fmt_ex : [str] payload format (json/XML)
    """

    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/{};ty=4; charset=utf-8'.format(fmt_ex)
    }

    payload = {
        "m2m:cin": {
            "con": "{}".format(value),
            # "con": (
            #     json.dumps(value)
            #     if fmt_ex == 'json'
            #     else "{}".format(value)
            # ),
            "lbl": cin_labels,
            "cnf": "text"
        }
    }

    print(
        'uri_cnt: {}'.format(uri_cnt)
        + ', headers: {}'.format(headers)
        + ', payload: {}'.format(payload)
    )

    try:
        response = requests.post(uri_cnt, json=payload, headers=headers,
                                 verify=verify)
    except TypeError:
        response = requests.post(uri_cnt, data=json.dumps(payload),
                                 headers=headers, verify=verify)
    cin = None
    success = False
    if response.ok:
        cin = json.loads(response.content)['m2m:cin']['rn']
        success = True

    # print('Return code : {}'.format(response.status_code))
    # print('Return Content : {}'.format(response.text))
    return success, response.status_code, cin


def create_group(self, uri_cse, group_name, uri_list):
    """
        Method description:
        Creates an AE that groups various other specifies AEs in the OneM2M framework/tree
        under the specified DATA CON

        Parameters:
        uri : [str] URI for the parent DATA CON appended by "la" or "ol"
        fmt_ex : [str] payload format (json/XML)
    """

    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/json;ty=9; charset=utf-8'
    }

    payload = {
        "m2m:grp":
            {
                "rn": group_name,
                "mt": 3,
                "mid": uri_list,
                "mnm": 10
            }
    }

    verify = os.getenv('VERIFY_CERT', True)
    try:
        response = requests.post(uri_cse, json=payload, headers=headers,
                                 verify=verify)
    except TypeError:
        response = requests.post(uri_cse, data=json.dumps(payload),
                                 headers=headers, verify=verify)

    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    return


def get_data(uri, fmt_ex="json"):
    """
        Method description:
        Gets data from the specified container(data_CIN)
        in the OneM2M framework/tree

        Parameters:
        uri : [str] URI for the parent DATA CON appended by "la" or "ol"
        fmt_ex : [str] payload format (json/XML)
    """
    headers = {
        # 'X-M2M-Origin': '{}:{}'.format(
        #     os.getenv('OM2M_UN', 'guest'),
        #     os.getenv('OM2M_PD', 'guest')
        # ),
        'X-M2M-Origin': '{}:{}'.format("guest","guest"),
        'Content-type': 'application/{}; charset=utf-8'.format(fmt_ex)}

    response = requests.get(uri, headers=headers, verify=verify)
    # print('Return code : {}'.format(response.status_code))
    # print('Return Content : {}'.format(response.text))
    # print(response.text)
    _resp = json.loads(response.text)
    return response.status_code, _resp["m2m:cnt"]
    # return response.status_code, _resp["m2m:cin"]["con"]


def get_group_data(uri, data_format="json"):
    """
        Method description:
        Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
        under the specified CSE

        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        fmt_ex : [str] payload format
    """
    headers = {
        # 'X-M2M-Origin': '{}:{}'.format(
        #     os.getenv('OM2M_UN', 'admin'),
        #     os.getenv('OM2M_PD', 'admin')
        # ),
                'X-M2M-Origin': '{}:{}'.format(
                "guest", "guest"
        ),
        'Content-type': 'application/{}; charset=utf-8'.format(data_format)}

    response = requests.get(uri, headers=headers, verify=verify)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    _resp = json.loads(response.text)
    return (
        response.status_code,
        _resp["m2m:grp"]["lt"]  # To get latest (entered data) instance
    )


def get_filtered_uri(self, uri, filter=""):
    """
        Method description:
        Splits the string into a list of URIs

        Parameters:
        uri : [str] URI for the parent DATA CON appended by "la" or "ol"
        fmt_ex : [str] payload format (json/XML)
    """
    _, filtered_uri = discovery(self, uri)
    filtered_uri_list = filtered_uri.split(" ")
    print(filtered_uri_list)
    return filtered_uri_list


def delete(self, uri, data_format="json"):
    """
        Method description:
        Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
        under the specified CSE

        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        fmt_ex : [str] payload format
    """
    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/{}; charset=utf-8'.format(data_format)}

    response = requests.delete(uri, headers=headers, verify=verify)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    return


def discovery(self, uri, fmt_ex="json"):
    """
        Method description:
        Returns a string of URIs separated by space
        from the OneM2M framework/tree

        Parameters:
        uri : [str] URI for the server appended by filter parameters
        fmt_ex : [str] payload format (json/XML)
    """
    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/{}; charset=utf-8'.format(fmt_ex)}

    response = requests.get(uri, headers=headers, verify=verify)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    _resp = json.loads(response.text)
    return response.status_code, _resp["m2m:uril"]


def create_group_ae(self, cse_uri, group_name, uri_list):
    """
        Method description:
        Creates an AE that groups various other specifies AEs in the OneM2M
        framework/tree under the specified DATA CON

        Parameters:
        uri : [str] URI for the parent DATA CON appended by "la" or "ol"
        fmt_ex : [str] payload format (json/XML)
    """

    headers = {
        'X-M2M-Origin': '{}:{}'.format(
            os.getenv('OM2M_UN', 'admin'),
            os.getenv('OM2M_PD', 'admin')
        ),
        'Content-type': 'application/json;ty=9; charset=utf-8'
    }

    payload = {
        "m2m:grp":
            {
                "rn": group_name,
                "mt": 3,
                "mid": uri_list,
                "mnm": 10
            }
    }

    try:
        response = requests.post(cse_uri, json=payload, headers=headers,
                                 verify=verify)
    except TypeError:
        response = requests.post(cse_uri, data=json.dumps(payload),
                                 headers=headers, verify=verify)

    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    return


# def main(argv=None):
#     if argv is None:
#         argv = sys.argv
#     print('main(), argv: {}'.format(argv))

#     server = "http://onem2m.iiit.ac.in:443"
#     # solar = "/~/in-cse/cin-988318778"
#     solar = "/~/in-cse/in-name/AE-SL/SL-VN03-00/Descriptor/la/"
#     uriso = server + solar
#     returnCode,DescriptorDataXML = get_data(uriso)
#     tree = ET.fromstring(DescriptorDataXML)
#     print(tree)
#     # root = tree.getroot()
#     dataDescriptor = {}
#     for child in tree:
#         # print(child.attrib)
#         dataDescriptor[child.attrib["name"]] = child.attrib["val"]
#     # print(dataDescriptor.keys())
#     dataStringParams = dataDescriptor["Data String Parameters"]
#     print(len(dataStringParams))

#     # latestInstance(server)


#     return



# if __name__ == '__main__':
#     try:
#         sys.exit(main(sys.argv[1:]))
#     except KeyboardInterrupt:
#         pass
