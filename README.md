# rdmo-ansible
ansible playbooks for rdmo deployment

**Do not use this in production! Expect breaking changes in the behaviour of these playbooks!**

This is still a work in progress. Expect breaking changes, so don't use this to deploy production instances.

To run this playbook, execute:
```shell
ansible-playbook -i  ./hosts/staging ./rdmo.yml -v
```
