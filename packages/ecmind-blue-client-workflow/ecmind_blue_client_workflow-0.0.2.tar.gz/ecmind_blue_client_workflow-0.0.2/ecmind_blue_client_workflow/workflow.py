from ecmind_blue_client import Job
from ecmind_blue_client import Client
from XmlElement import XmlElement


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