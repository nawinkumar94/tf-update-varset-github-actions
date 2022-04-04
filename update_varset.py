import requests
import os

TF_TOKEN = os.environ['TF_TOKEN']
STG_ACCESS_KEY = os.environ['STG_ACCESS_KEY']
STG_SECRET_KEY = os.environ['STG_SECRET_KEY']
STG_SESSION_TOKEN = os.environ['STG_SESSION_TOKEN']
UAT_ACCESS_KEY = os.environ['UAT_ACCESS_KEY']
UAT_SECRET_KEY = os.environ['UAT_SECRET_KEY']
UAT_SESSION_TOKEN = os.environ['UAT_SESSION_TOKEN']
SEC_ACCESS_KEY = os.environ['SEC_ACCESS_KEY']
SEC_SECRET_KEY = os.environ['SEC_SECRET_KEY']
SEC_SESSION_TOKEN = os.environ['SEC_SESSION_TOKEN']
DAT_ACCESS_KEY = os.environ['DAT_ACCESS_KEY']
DAT_SECRET_KEY = os.environ['DAT_SECRET_KEY']
DAT_SESSION_TOKEN = os.environ['DAT_SESSION_TOKEN']
PRD_ACCESS_KEY = os.environ['PRD_ACCESS_KEY']
PRD_SECRET_KEY = os.environ['PRD_SECRET_KEY']
PRD_SESSION_TOKEN = os.environ['PRD_SESSION_TOKEN']
NET_ACCESS_KEY = os.environ['NET_ACCESS_KEY']
NET_SECRET_KEY = os.environ['NET_SECRET_KEY']
NET_SESSION_TOKEN = os.environ['NET_SESSION_TOKEN']
IT_ACCESS_KEY = os.environ['IT_ACCESS_KEY']
IT_SECRET_KEY = os.environ['IT_SECRET_KEY']
IT_SESSION_TOKEN = os.environ['IT_SESSION_TOKEN']

headers = {"Authorization": f"Bearer {TF_TOKEN}",
           "Content-Type": "application/vnd.api+json"}

def get_org_data():
    tf_org_endpoint = "https://app.terraform.io/api/v2/organizations"
    org_data = requests.get(tf_org_endpoint, headers=headers).json()
    org_details = [element['attributes'] for element in org_data['data']]
    org_name = [element['name'] for element in org_details]
    return org_name

def get_variable_sets():
    for org_name in get_org_data():
        # List Variable Set
        org_varset_endpoint = f"https://app.terraform.io/api/v2/organizations/{org_name}/varsets"
        org_varset_data = requests.get(org_varset_endpoint, headers=headers).json()
        org_varset_ids = [element['id'] for element in org_varset_data['data']]
        org_varset_details = dict((element['attributes']['name'] , element['id']) for element in org_varset_data['data'])
        if org_varset_ids: # If Variable Set is not empty
            for varset_name,varset_id in org_varset_details.items():
                get_variable(varset_name,varset_id)

def get_variable(varset_name,varset_id):
    org_var_details = {}
    org_var_endpoint = f"https://app.terraform.io/api/v2/varsets/{varset_id}/relationships/vars"
    org_var_data = requests.get(org_var_endpoint, headers=headers).json()
    # Variable name and Variable id as key value pair
    org_var_details = dict((element['attributes']['key'] , element['id']) for element in org_var_data['data'])
    for var_name,var_id in org_var_details.items():
        hcl = False
        category = 'env'
        var_value = ''
        if varset_name == 'stg-aws-access-credentials':
            if var_name == 'AWS_ACCESS_KEY_ID':
                sensitive = False
                var_value = STG_ACCESS_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SECRET_ACCESS_KEY':
                sensitive = True
                var_value = STG_SECRET_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SESSION_TOKEN':
                sensitive = True
                var_value = STG_SESSION_TOKEN
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
        elif varset_name == 'uat-aws-access-credentials':
            if var_name == 'AWS_ACCESS_KEY_ID':
                sensitive = False
                var_value = UAT_ACCESS_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SECRET_ACCESS_KEY':
                sensitive = True
                var_value = UAT_SECRET_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SESSION_TOKEN':
                sensitive = True
                var_value = UAT_SESSION_TOKEN
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
        elif varset_name == 'prd-aws-access-credentials':
            if var_name == 'AWS_ACCESS_KEY_ID':
                sensitive = False
                var_value = PRD_ACCESS_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SECRET_ACCESS_KEY':
                sensitive = True
                var_value = PRD_SECRET_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SESSION_TOKEN':
                sensitive = True
                var_value = PRD_SESSION_TOKEN
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
        elif varset_name == 'sec-aws-access-credentials':
            if var_name == 'AWS_ACCESS_KEY_ID':
                sensitive = False
                var_value = SEC_ACCESS_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SECRET_ACCESS_KEY':
                sensitive = True
                var_value = SEC_SECRET_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SESSION_TOKEN':
                sensitive = True
                var_value = SEC_SESSION_TOKEN
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
        elif varset_name == 'dat-aws-access-credentials':
            if var_name == 'AWS_ACCESS_KEY_ID':
                sensitive = False
                var_value = DAT_ACCESS_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SECRET_ACCESS_KEY':
                sensitive = True
                var_value = DAT_SECRET_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SESSION_TOKEN':
                sensitive = True
                var_value = DAT_SESSION_TOKEN
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
        elif varset_name == 'net-aws-access-credentials':
            if var_name == 'AWS_ACCESS_KEY_ID':
                sensitive = False
                var_value = NET_ACCESS_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SECRET_ACCESS_KEY':
                sensitive = True
                var_value = NET_SECRET_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SESSION_TOKEN':
                sensitive = True
                var_value = NET_SESSION_TOKEN
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
        elif varset_name == 'it-aws-access-credentials':
            if var_name == 'AWS_ACCESS_KEY_ID':
                sensitive = False
                var_value = IT_ACCESS_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SECRET_ACCESS_KEY':
                sensitive = True
                var_value = IT_SECRET_KEY
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)
            if var_name == 'AWS_SESSION_TOKEN':
                sensitive = True
                var_value = IT_SESSION_TOKEN
                update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category)

def update_workspace_vars(var_name,var_value,var_id,varset_id,sensitive,hcl,category):
    data = {"data": {"attributes": {"key":var_name,"value":var_value,"description": var_name,
                     "category":category,"hcl": hcl,"sensitive": sensitive},"type":"vars"}}
    var_update_endpoint = f"https://app.terraform.io/api/v2/varsets/{varset_id}/relationships/vars/{var_id}"
    var_update_response = requests.patch(var_update_endpoint, headers=headers, json=data)


def main():
    get_variable_sets()

if __name__ == '__main__':
    main()
