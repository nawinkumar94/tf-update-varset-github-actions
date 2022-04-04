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
        stg_org_workspaces = []
        uat_org_workspaces = []
        prd_org_workspaces = []
        sec_org_workspaces = []
        dat_org_workspaces = []
        it_org_workspaces = []
        net_org_workspaces = []
        workspace_list_endpoint = f"https://app.terraform.io/api/v2/organizations/{org_name}" \
                                  f"/workspaces?page%5Bnumber%5D=1&page%5Bsize%5D=100"
        workspace_data = requests.get(workspace_list_endpoint, headers=headers).json()
        workspace_details = dict((element['attributes']['name'] , element['id']) for element in workspace_data['data'])
        for workspace_name,workspace_id in workspace_details.items():
            org_workspace_dict = {'org_name': org_name, 'workspace_id': workspace_id}
            if workspace_name.endswith('-stg'):
                stg_org_workspaces.append(workspace_id)
            if workspace_name.endswith('-uat'):
                uat_org_workspaces.append(workspace_id)
            if workspace_name.endswith('-prd'):
                prd_org_workspaces.append(workspace_id)
            if workspace_name.endswith('-sec'):
                sec_org_workspaces.append(workspace_id)
            if workspace_name.endswith('-dat'):
                dat_org_workspaces.append(workspace_id)
            if workspace_name.endswith('-it'):
                it_org_workspaces.append(workspace_id)
            if workspace_name.endswith('-net'):
                net_org_workspaces.append(workspace_id)
        create_varset(org_name,stg_org_workspaces,'stg-aws-access-credentials')
        create_varset(org_name,uat_org_workspaces,'uat-aws-access-credentials')
        create_varset(org_name,prd_org_workspaces,'prd-aws-access-credentials')
        create_varset(org_name,sec_org_workspaces,'sec-aws-access-credentials')
        create_varset(org_name,dat_org_workspaces,'dat-aws-access-credentials')
        create_varset(org_name,it_org_workspaces,'it-aws-access-credentials')
        create_varset(org_name,net_org_workspaces,'net-aws-access-credentials')

def create_varset(org_name, workspaces, varset_name):
    data = {"data": {"type":"varsets","attributes": {"name":varset_name,"description":'',"is-global": False},
            "relationships": { "workspaces": { "data": [ {"id": id ,"type": "workspaces"} for id in workspaces]},
            "vars": { "data": [ {"type": "vars","attributes": {"key":'AWS_ACCESS_KEY_ID',"value":'AWS_ACCESS_KEY_ID',"category": "env"}},
            {"type": "vars","attributes": {"key":'AWS_SECRET_ACCESS_KEY',"value":'AWS_SECRET_ACCESS_KEY',"category": "env"}},
            {"type": "vars","attributes": {"key":'AWS_SESSION_TOKEN',"value":'AWS_SESSION_TOKEN',"category": "env"}},
            {"type": "vars","attributes": {"key":'allowed_account_ids',"value":'["664398042318"]',"category": "terraform"}},
            {"type": "vars","attributes": {"key":'account_role',"value":'arn:aws:iam::664398042318:role/DeployProd',"category": "terraform"}},
            {"type": "vars","attributes": {"key":'external_id',"value":'957e0aec-a6ca-4a6b-a2dd-96f2e913e56c-67ue0aclw-16f2a613e86c',"category": "terraform"}}
            ]}}}}
    create_varset_endpoint = f"https://app.terraform.io/api/v2/organizations/{org_name}/varsets"
    create_varset_response = requests.post(create_varset_endpoint, headers=headers, json=data)

def main():
    setup_org_workspace_details()

if __name__ == '__main__':
    main()
