# Copyright 2013 Big Switch Networks Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import sys
from unittest import mock


from neutronclient.neutron.v2_0.fw import firewallpolicy
from neutronclient import shell
from neutronclient.tests.unit import test_cli20


class CLITestV20FirewallPolicyJSON(test_cli20.CLITestV20Base):
    def setUp(self):
        super(CLITestV20FirewallPolicyJSON, self).setUp()

    def test_create_firewall_policy_with_mandatory_params(self):
        # firewall-policy-create with mandatory (none) params only.
        resource = 'firewall_policy'
        cmd = firewallpolicy.CreateFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                  None)
        tenant_id = 'my-tenant'
        name = 'my-name'
        my_id = 'myid'
        args = ['--tenant-id', tenant_id,
                '--admin-state_up',
                name, ]
        position_names = ['name', ]
        position_values = [name, ]
        self._test_create_resource(resource, cmd, name, my_id, args,
                                   position_names, position_values,
                                   admin_state_up=True, tenant_id=tenant_id)

    def test_create_firewall_policy_with_all_params(self):
        # firewall-policy-create with rule param of misc format.
        resource = 'firewall_policy'
        cmd = firewallpolicy.CreateFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                  None)
        name = 'my-name'
        description = 'my-desc'
        firewall_rules_res = ['rule_id1', 'rule_id2']
        tenant_id = 'my-tenant'
        my_id = 'myid'
        position_names = ['name', ]
        position_values = [name, ]

        # check for both str and unicode format firewall_rules_arg
        for firewall_rules_arg in ['rule_id1 rule_id2', u'rule_id1 rule_id2']:
            args = ['--description', description,
                    '--shared',
                    '--firewall-rules', firewall_rules_arg,
                    '--audited',
                    '--tenant-id', tenant_id,
                    '--admin-state_up',
                    name]
            self._test_create_resource(resource, cmd, name, my_id, args,
                                       position_names, position_values,
                                       description=description, shared=True,
                                       firewall_rules=firewall_rules_res,
                                       audited=True, admin_state_up=True,
                                       tenant_id=tenant_id)

    def test_list_firewall_policies(self):
        # firewall-policy-list.
        resources = "firewall_policies"
        cmd = firewallpolicy.ListFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                None)
        self._test_list_resources(resources, cmd, True)

    def test_list_firewall_policies_pagination(self):
        # firewall-policy-list."""
        resources = "firewall_policies"
        cmd = firewallpolicy.ListFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                None)
        self._test_list_resources_with_pagination(resources, cmd)

    def test_list_firewall_policies_sort(self):
        # sorted list: firewall-policy-list --sort-key name --sort-key id
        # --sort-key asc --sort-key desc
        resources = "firewall_policies"
        cmd = firewallpolicy.ListFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                None)
        self._test_list_resources(resources, cmd,
                                  sort_key=["name", "id"],
                                  sort_dir=["asc", "desc"])

    def test_list_firewall_policies_limit(self):
        # size (1000) limited list: firewall-policy-list -P.
        resources = "firewall_policies"
        cmd = firewallpolicy.ListFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                None)
        self._test_list_resources(resources, cmd, page_size=1000)

    def test_show_firewall_policy_id(self):
        # firewall-policy-show test_id.
        resource = 'firewall_policy'
        cmd = firewallpolicy.ShowFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                None)
        args = ['--fields', 'id', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id, args, ['id'])

    def test_show_firewall_policy_id_name(self):
        # firewall-policy-show.
        resource = 'firewall_policy'
        cmd = firewallpolicy.ShowFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                None)
        args = ['--fields', 'id', '--fields', 'name', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id,
                                 args, ['id', 'name'])

    def test_update_firewall_policy(self):
        # firewall-policy-update myid --name newname.
        resource = 'firewall_policy'
        cmd = firewallpolicy.UpdateFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                  None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['myid', '--name', 'newname'],
                                   {'name': 'newname', })

    def test_update_firewall_policy_with_rules(self):
        # firewall-policy-update myid --firewall-rules "rule1 rule2".
        resource = 'firewall_policy'
        cmd = firewallpolicy.UpdateFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                  None)
        firewall_rules_arg = u'rule_id3 rule_id4'
        firewall_rules_res = ['rule_id3', 'rule_id4']
        self._test_update_resource(
            resource, cmd, 'myid',
            ['myid', '--firewall-rules', firewall_rules_arg],
            {'firewall_rules': firewall_rules_res, })

    def test_delete_firewall_policy(self):
        # firewall-policy-delete my-id.
        resource = 'firewall_policy'
        cmd = firewallpolicy.DeleteFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                  None)
        my_id = 'myid1'
        args = [my_id]
        self._test_delete_resource(resource, cmd, my_id, args)

    def test_insert_firewall_rule(self):
        # firewall-policy-insert-rule myid newruleid --insert-before ruleAid
        # --insert-after ruleBid
        resource = 'firewall_policy'
        cmd = firewallpolicy.FirewallPolicyInsertRule(
            test_cli20.MyApp(sys.stdout),
            None)
        myid = 'myid'
        args = ['myid', 'newrule',
                '--insert-before', 'rule2',
                '--insert-after', 'rule1']
        extrafields = {'firewall_rule_id': 'newrule',
                       'insert_before': 'rule2',
                       'insert_after': 'rule1'}

        body = extrafields
        path = getattr(self.client, resource + "_insert_path")
        cmd_parser = cmd.get_parser(resource + "_insert_rule")
        resp = (test_cli20.MyResp(204), None)

        with mock.patch.object(cmd, "get_client",
                               return_value=self.client) as mock_get_client, \
                mock.patch.object(self.client.httpclient, "request",
                                  return_value=resp) as mock_request:
            shell.run_command(cmd, cmd_parser, args)
        self.assert_mock_multiple_calls_with_same_arguments(
            mock_get_client, mock.call(), 4)
        mock_request.assert_called_once_with(
            test_cli20.MyUrlComparator(
                test_cli20.end_url(path % myid),
                self.client),
            'PUT', body=test_cli20.MyComparator(body, self.client),
            headers=test_cli20.ContainsKeyValue(
                {'X-Auth-Token': test_cli20.TOKEN}))

    def test_remove_firewall_rule(self):
        # firewall-policy-remove-rule myid ruleid
        resource = 'firewall_policy'
        cmd = firewallpolicy.FirewallPolicyRemoveRule(
            test_cli20.MyApp(sys.stdout),
            None)
        myid = 'myid'
        args = ['myid', 'removerule']
        extrafields = {'firewall_rule_id': 'removerule', }

        body = extrafields
        path = getattr(self.client, resource + "_remove_path")
        cmd_parser = cmd.get_parser(resource + "_remove_rule")
        resp = (test_cli20.MyResp(204), None)

        with mock.patch.object(cmd, "get_client",
                               return_value=self.client) as mock_get_client, \
                mock.patch.object(self.client.httpclient, "request",
                                  return_value=resp) as mock_request:
            shell.run_command(cmd, cmd_parser, args)
        self.assert_mock_multiple_calls_with_same_arguments(
            mock_get_client, mock.call(), 2)
        mock_request.assert_called_once_with(
            test_cli20.MyUrlComparator(
                test_cli20.end_url(path % myid),
                self.client),
            'PUT', body=test_cli20.MyComparator(body, self.client),
            headers=test_cli20.ContainsKeyValue(
                {'X-Auth-Token': test_cli20.TOKEN}))

    def test_update_firewall_policy_name_shared_audited(self):
        # firewall-policy-update myid --name newname2 --shared --audited
        resource = 'firewall_policy'
        cmd = firewallpolicy.UpdateFirewallPolicy(test_cli20.MyApp(sys.stdout),
                                                  None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['myid', '--name', 'newname2',
                                    '--shared', 'True', '--audited', 'True'],
                                   {'name': 'newname2',
                                    'shared': 'True', 'audited': 'True'})
