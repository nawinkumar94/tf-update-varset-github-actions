import requests

headers = {"Authorization": f"Bearer {TF_TOKEN}",
           "Content-Type": "application/vnd.api+json"}

def get_org_data():
    tf_org_endpoint = "https://app.terraform.io/api/v2/organizations"
    org_data = requests.get(tf_org_endpoint, headers=headers).json()
    org_details = [element['attributes'] for element in org_data['data']]
    org_name = [element['name'] for element in org_details]
    return org_name

def setup_org_workspace_details():
    for org_name in get_org_data():
        workspace_list_endpoint = f"https://app.terraform.io/api/v2/organizations/{org_name}" \
                                  f"/workspaces?page%5Bnumber%5D=1&page%5Bsize%5D=100"
        workspace_data = requests.get(workspace_list_endpoint, headers=headers).json()
        workspace_details = [element['attributes'] for element in workspace_data['data']]
        workspace_names = [element['name'] for element in workspace_details]
        for workspace_name in workspace_names:
            org_workspace_dict = {'org_name': org_name, 'workspace_name': workspace_name}
            list_vars(org_name,workspace_name)


def list_vars(org_name, workspace_name):
        list_vars_endpoint = f"https://app.terraform.io/api/v2/vars?filter%5Borganization%5D%5Bname%5D={org_name}&filter%5Bworkspace%5D%5Bname%5D={workspace_name}"
        list_vars_response = requests.get(list_vars_endpoint, headers=headers).json()
        if list_vars_response:
            list_vars_details = dict((element['attributes']['key'] , element['id']) for element in list_vars_response['data'])
            for variable_name,variable_id in list_vars_details.items():
                if variable_name == 'AWS_ACCESS_KEY_ID':
                    delete_vars(variable_id)
                if variable_name == 'AWS_SECRET_ACCESS_KEY':
                    delete_vars(variable_id)
                if variable_name == 'allowed_account_ids':
                    delete_vars(variable_id)
                if variable_name == 'account_role':
                    delete_vars(variable_id)
                if variable_name == 'external_id':
                    delete_vars(variable_id)

def delete_vars(variable_id):
    delete_vars_endpoint = f"https://app.terraform.io/api/v2/vars/{variable_id}"
    delete_vars_response = requests.delete(delete_vars_endpoint, headers=headers)

def main():
    setup_org_workspace_details()



if __name__ == '__main__':
    main()
