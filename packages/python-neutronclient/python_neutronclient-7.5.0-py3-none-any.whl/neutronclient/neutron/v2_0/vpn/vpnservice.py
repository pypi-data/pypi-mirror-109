#    (c) Copyright 2013 Hewlett-Packard Development Company, L.P.
#    All Rights Reserved.
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

from neutronclient._i18n import _
from neutronclient.common import utils
from neutronclient.neutron import v2_0 as neutronv20


def add_common_args(parser):
    parser.add_argument(
        '--name',
        help=_('Name for the VPN service.'))
    parser.add_argument(
        '--description',
        help=_('Description for the VPN service.'))


def common_args2body(parsed_args, body):
    neutronv20.update_dict(parsed_args, body,
                           ['name', 'description'])


class ListVPNService(neutronv20.ListCommand):
    """List VPN service configurations that belong to a given tenant."""

    resource = 'vpnservice'
    list_columns = [
        'id', 'name', 'router_id', 'status'
    ]
    _formatters = {}
    pagination_support = True
    sorting_support = True


class ShowVPNService(neutronv20.ShowCommand):
    """Show information of a given VPN service."""

    resource = 'vpnservice'
    help_resource = 'VPN service'


class CreateVPNService(neutronv20.CreateCommand):
    """Create a VPN service."""
    resource = 'vpnservice'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false.'))
        parser.add_argument(
            'router', metavar='ROUTER',
            help=_('Router unique identifier for the VPN service.'))
        parser.add_argument(
            'subnet', nargs='?', metavar='SUBNET',
            help=_('[DEPRECATED in Mitaka] Unique identifier for the local '
                   'private subnet.'))
        add_common_args(parser)

    def args2body(self, parsed_args):
        if parsed_args.subnet:
            _subnet_id = neutronv20.find_resourceid_by_name_or_id(
                self.get_client(), 'subnet', parsed_args.subnet)
        else:
            _subnet_id = None
        _router_id = neutronv20.find_resourceid_by_name_or_id(
            self.get_client(), 'router',
            parsed_args.router)

        body = {'subnet_id': _subnet_id,
                'router_id': _router_id,
                'admin_state_up': parsed_args.admin_state}
        neutronv20.update_dict(parsed_args, body,
                               ['tenant_id'])
        common_args2body(parsed_args, body)
        return {self.resource: body}


class UpdateVPNService(neutronv20.UpdateCommand):
    """Update a given VPN service."""

    resource = 'vpnservice'
    help_resource = 'VPN service'

    def add_known_arguments(self, parser):
        add_common_args(parser)
        utils.add_boolean_argument(
            parser, '--admin-state-up',
            help=_('Update the admin state for the VPN Service.'
                   '(True means UP)'))

    def args2body(self, parsed_args):
        body = {}
        common_args2body(parsed_args, body)
        neutronv20.update_dict(parsed_args, body,
                               ['admin_state_up'])
        return {self.resource: body}


class DeleteVPNService(neutronv20.DeleteCommand):
    """Delete a given VPN service."""

    resource = 'vpnservice'
    help_resource = 'VPN service'
