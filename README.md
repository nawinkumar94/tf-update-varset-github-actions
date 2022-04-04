# tf-update-varset-github-actions
Github actions to update terraform workspace variables

# About Project
This repository has github actions that will update the terraform workspace environment variables with temporary secrets which is created using assume role

Temporary credentials (AWSAccessKey, AWSSecretAccessKey and AWSSessionToken)are generated using assume role are valid for one hour since we are using oidc provider with github to assume role with web identity, these generated credentials will be updated in terraform workspace variable sets for every 50 minutes.

# update_varset.py
This will update the variable sets in every terraform organization for all environments, These varaiable sets are applied in all the workspaces. Used in github action workflow.

# create_varset.py
This will create variable sets in all terraform organization for all environments and will apply the variable sets to each workspaces in a organization. This is onetime process so not added in github action workflow.

# delete_var
This will delete the existing variables in terraform workspace, since we are having all common variables in variable sets, we should not have same varaibles in workspace varaibles also. This is onetime process so not added in github action workflow.
