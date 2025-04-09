import requests
import dbtools
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bs4 import BeautifulSoup

# TODO: extend this to allow checking for different versions of the IPT as the forms may change?
# Functional for IPT 2.6.3

def open_ipt_session(ipt_auth, ipt_url):
    """
    Begin a session with the target IPT
    Author: Jon Pye
    :param ipt_auth: Authentication details for the ipt, of the form {'email': 'email@mailserver.com', 'password':'cleartextPassword'}
    :param ipt_url: URL of the IPT we are authenticating with.
    :return: None
    """
    
    # relative path to IPT login form
    login_url = server_root + 'login.do'
    
    s = requests.Session()  # open a session
    
    # retrieve the login form
    resp = session.get(login_url)
    
    # login forms generate a CSRF token that we have to persist in our response  
    soup = BeautifulSoup(resp.text, 'lxml')
    
    # Add it to our credentials dictionary
    ipt_auth['csrfToken'] = soup.find("input", {"name":"csrfToken"})['value']
    login = session.post(login_url, data=ipt_auth)
    
    if login.status_code != '200':
        print("Login failed, status code {}".format(login.status_code))
        return None
    else:
        return s

def create_new_ipt_project(projname:str, filepath:str, ipt_url:str, ipt_session):
    
    """
    Create a new project on the given IPT using an existing DwC archive zip
    Author: Jon Pye
    :param projname: the project name as given by get_obis_shortname()
    :param filepath: payload resource filepath
    :param ipt_url: URL of the IPT to publish to
    :param ipt_session: authenticated requests session for the IPT
    :return: URL of the resource
    """
    
    path, filename = os.path.split(filepath)
    
    if not filename:  # if the filepath has no name in it
        print('no file specified in filepath, aborting')
        return None
    
    # if there IS a file and it is not a valid DwC Archive, do we want to do anything here? The IPT runs its own checks...
    
    values = MultipartEncoder(fields={'create':'Create', # hidden form fields with values
                                      'shortname':projname,
                                      'resourceType':'samplingevent',
                                      '__checkbox_importDwca': 'true',
                                      'importDwca': 'true',
                                      'file': (filename, open(filepath, 'rb'),
                                                      'application/x-zip-compressed'),
                                     }
                             )
    create_dataset = ipt_session.post(ipt_url + 'manage/create.do',
                                      data=values,
                                      headers={'Content-Type':values.content_type}
                                     )
    return

    
def refresh_ipt_project_files(projname:str, filepath:str, ipt_url:str, ipt_session):
    """
    Update data for a project on the given IPT using an existing DwC archive zip
    Author: Jon Pye
    :param projname: the project name as given by get_obis_shortname()
    :param filepath: payload resource filepath
    :param ipt_url: URL of the IPT to publish to
    :param ipt_session: authenticated requests session for the IPT
    :return: URL of the resource
    """
    
    path, filename = os.path.split(filepath)
    
    if not filename:  # if the filepath has no name in it
        print('no file specified in filepath, aborting')
        return None
    
    values = MultipartEncoder(fields={'add':'Add',
              'r':projname,
              'sourceType':'source-file',
              'validate':'false', 
              'file': (filename,
               open(filepath, 'rb'),
               'application/x-zip-compressed'),
              })
    
    update_dataset = ipt_session.post(ipt_url + 'manage/addsource.do',
                                      data=values, 
                                      headers = {'Content-Type':values.content_type}
                                     )
    return

def refresh_ipt_project_metadata(projname:str, filepath:str, ipt_url:str, ipt_session):
    """
    Update metadata for a project on the given IPT using an existing eml.xml file
    Author: Jon Pye
    :param projname: the project name as given by get_obis_shortname()
    :param filepath: payload resource filepath
    :param ipt_url: URL of the IPT to publish to
    :param ipt_session: authenticated requests session for the IPT
    :return: URL of the resource
    """
    
    path, filename = os.path.split(filepath)
    
    if not filename:  # if the filepath has no name in it
        print('no file specified in filepath, aborting')
        return None
    
    values = MultipartEncoder(fields={'emlReplace':'Replace',
              'r':projname,
              'sourceType':'source-file',
              'validateEml':'true',
              '__checkbox_validateEml': 'true',
              'emlFile': (filename,
               open(filepath, 'rb'),
               'application/xml'),
              })

    update_metadata = ipt_session.post(ipt.url + 'manage/replace-eml.do',
                                       data=values, 
                                       headers = {'Content-Type':values.content_type}
                                      )
    return

def make_public_ipt_project(projname:str, filepath:str, ipt_url:str, ipt_session):
    """
    Update metadata for a project on the given IPT using an existing eml.xml file
    Author: Jon Pye
    :param projname: the project name as given by get_obis_shortname()
    :param ipt_url: URL of the IPT to publish to
    :param ipt_session: authenticated requests session for the IPT
    :return: URL of the resource
    """
    pub_params = {'r' : projname,          # resource = dataset name
                  'makePrivate': 'Public'
                 }
    
    contents = ipt_session.post(ipt_url + 'manage/resource-makePublic.do', data = pub_params)
    return

def publish_ipt_project(projname:str, filepath:str, ipt_url:str, ipt_session, publishing_notes:str=""):
    """
    Update metadata for a project on the given IPT using an existing eml.xml file
    Author: Jon Pye
    :param projname: the project name as given by get_obis_shortname()
    :param ipt_url: URL of the IPT to publish to
    :param ipt_session: authenticated requests session for the IPT
    :param publishing_notes: optional message to publish this version with
    :return: URL of the resource
    """
    
    pub_params = {'r' : projname,      # resource = dataset name
                  'autopublish': '',
                  'currPubMode' : 'AUTO_PUBLISH_OFF',
                  'pubMode': '',
                  'currPubFreq': '',
                  'pubFreq': '',
                  'publish': 'Publish',
                  'summary': publishing_notes
             }
    contents = ipt_session.post(ipt_url + 'manage/publish.do', data = pub_params)
    return
    
