import datetime
from enum import Enum

from ecmind_blue_client import Job
from ecmind_blue_client import Client
from XmlElement import XmlElement

class State(Enum):
    INIT = 1
    RUNNING = 2
    SUSPENDED = 4
    ACTIVE = 8
    TERMINATED = 16
    COMPLETED = 32
    SYSSUSPENDED = 64


def get_organisations(client:Client, only_active:bool=True):
    result_get_organisations = client.execute(Job(jobname='wfm.GetOrganisations'))
    if not result_get_organisations.return_code == 0:
        raise RuntimeError(result_get_organisations.error_message)

    organisations = XmlElement.from_string(result_get_organisations.values['Organisations']).to_dict()['Organisation']

    if not isinstance(organisations, list):
        organisations = [ organisations ]

    if only_active:
        return { o['@Id']: o['@Name'] for o in organisations if o['@Active'] == 1 }
    else:
        return { o['@Id']: o['@Name'] for o in organisations }


def admin_get_workflow_list(client: Client, organisation_id: str) -> dict[str, dict[str, object]]:
    job = Job('wfm.AdminGetWorkflowList', OrganisationId=organisation_id)
    
    get_workflow_list = client.execute(job)
    if not get_workflow_list.return_code == 0:
        raise RuntimeError(get_workflow_list.error_message)
    
    workflows = XmlElement.from_string(get_workflow_list.values['Workflows']).to_dict()['Workflow']
    workflows = [workflows] if type(workflows) is dict else workflows

    return { w['@Id']: {'name': w['@Name'], 'process_count': w['@ProcessCount']} for w in workflows }


def admin_get_process_list(client: Client, organisation_id: str, workflow_id: str) -> dict[str, dict[str, object]]:
    job = Job('wfm.AdminGetProcessList', OrganisationId=organisation_id, WorkflowId=workflow_id)
    
    admin_get_process_list_result = client.execute(job)
    if not admin_get_process_list_result.return_code == 0:
        raise RuntimeError(admin_get_process_list_result.error_message)
    
    processes = XmlElement.from_string(admin_get_process_list_result.values['Processes']).to_dict()['Process']
    processes = [processes] if type(processes) is dict else processes

    return { 
        p['@Id']: {
            'name': p['@Name'], 
            'subject': p['@Subject'],
            'state': State(int(p['@State'])),
            'suspended_activity': p['@SuspendedActivity'],
            'creation':{
                'user_id': p['Creation']['@UserId'],
                'user_name': p['Creation']['@UserName'],
                'time': datetime.datetime.fromtimestamp(p['Creation']['@Time']),
            },
            'last_activity':{
                'id': p['LastActivity']['@Id'],
                'name': p['LastActivity']['@Name'],
                'user_id': p['LastActivity']['@UserId'],
                'user_name': p['LastActivity']['@UserName'],
                'exec_time': datetime.datetime.fromtimestamp(p['LastActivity']['@ExecTime']),
            }
        } for p in processes 
    }


def get_roles(client:Client, organisation_id:str):
    result_get_organisations_objects = client.execute(Job(
        jobname='wfm.GetOrganisationObjects',
        OrganisationId=organisation_id,
        RequestType=4,
        ObjectIds='',
        ObjectName='',
        ClassIds='',
        ClassName='Rolle',
        AttributeId='',
        AttributeValue='',
        RequestData=1
    ))
    if not result_get_organisations_objects.return_code == 0:
        raise RuntimeError(result_get_organisations_objects.error_message)

    roles = XmlElement.from_string(
            result_get_organisations_objects.values['Objects']
        ).to_dict()['Object']

    if not isinstance(roles, list):
        roles = [ roles ]

    return {r['@Id']: r['@Name'] for r in roles }