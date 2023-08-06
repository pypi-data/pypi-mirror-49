#!/usr/bin/env python
import ipaddress
import logging
from typing import Dict, Union, List, Tuple

from ..cloudformation.elements import CloudFormationResource
from ..core.base import ResourceProcessor

__author__ = "Giuseppe Chiesa"
__copyright__ = "Copyright 2017, Giuseppe Chiesa"
__credits__ = ["Giuseppe Chiesa"]
__license__ = "BSD"
__maintainer__ = "Giuseppe Chiesa"
__email__ = "mail@giuseppechiesa.it"
__status__ = "PerpetualBeta"


class Rule(object):
    def __init__(self, proto, cidr_or_sg, from_port, to_port):
        self.proto = proto
        self.cidr_or_sg = cidr_or_sg
        self.from_port = from_port
        self.to_port = to_port
        self._direction = None

    def is_cidr(self):
        try:
            ipaddress.ip_network(self.cidr_or_sg)
        except ValueError:
            return False
        return True

    def render_destination_group_id(self):
        """
        Rule cidr_or_sg support various formats


        :return:
        """
        if self.is_cidr():
            raise ValueError('Not a destination group id')

        if '.' in self.cidr_or_sg:
            fn_getatt_name, _, fn_getatt_attribute = self.cidr_or_sg.partition('.')
            return {'Fn::GetAtt': [fn_getatt_name, fn_getatt_attribute]}
        return self.cidr_or_sg

    @staticmethod
    def calculate_ports(port_or_port_range: str) -> Tuple[str, str]:
        def is_valid_port(data):
            if data == '-1':
                return True
            if data.isnumeric() and 1 <= int(data) <= 65535:
                return True
            return False

        if '-' in port_or_port_range:
            # then it's considered a port range
            from_port, to_port = port_or_port_range.split('-')
        elif port_or_port_range.upper() == 'ALL':
            # then it's considered all ports
            from_port = to_port = '-1'
        else:
            # otherwise we use that as a port
            from_port = to_port = port_or_port_range

        if not is_valid_port(from_port) or not is_valid_port(to_port):
            raise ValueError(f'Invalid port range: {port_or_port_range}')

        return from_port, to_port

    @staticmethod
    def calculate_cidr_or_sg(cidr_or_sg: str, template_parameters: dict) -> str:
        """
        implements the cidr_or_sg resolution when is not a cidr but it's in the form

        Parameters/<something>

        then we lookup the parameters and we use that value

        :param cidr_or_sg:
        :param template_parameters:
        :return:
        """
        result = cidr_or_sg
        if cidr_or_sg.lower().startswith('parameters/'):
            _, _, key = cidr_or_sg.partition('/')
            result = template_parameters.get(key, None)
        if not result:
            raise RuntimeError('Unable to resolve cidr_or_sg: {}'.format(cidr_or_sg))
        return result

    def __eq__(self, other):
        return (self.proto == other.proto and
                self.cidr_or_sg == other.cidr_or_sg and
                self.from_port == other.from_port and
                self.to_port == other.to_port)

    def __ne__(self, other):
        return not self.__eq__(other)


class SgProcessor(ResourceProcessor):
    """
    Security Group Macro Processor
    """
    tag = 'Custom::SgProcessorV1'

    def __init__(self):
        """
        This core support cloudformation elements like the following::

            "SgTestEgressRules": {
              "Type": "Custom::SgProcessorV1",
              "Properties": {
                "ServiceToken": "",
                "Direction": "Egress",
                "Rules": { "Ref": "WhitelistTest" },
                "FromTo": "TestLabel",
                "TargetGroup": {"Ref": "SgTest"}
              }
            }

        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self._template_params = None

    @staticmethod
    def target_group_to_name(tg):
        """ calculate the name from a target group node """
        if isinstance(tg, dict) and tg.get('Ref', None):
            name = tg['Ref']
        elif isinstance(tg, dict) and tg.get('Fn::GetAtt', None):
            name = tg['Fn::GetAtt'][0] if tg['Fn::GetAtt'][1] == 'GroupId' else None
        elif isinstance(tg, dict) and tg.get('Fn::GetAtt', None):
            name = tg['Fn::GetAtt'][0] if tg['Fn::GetAtt'][1] == 'security_group_id' else None
        elif isinstance(tg, str):
            name = tg
        else:
            name = None
        if not name:
            raise ValueError('Unable to calculate Sg key name')
        return name

    def _calculate_descriptive_labels(self, direction: str, label_from_to: str, rule: Rule) -> Tuple[str, str]:
        result_label = label_from_to
        if not result_label:
            # use the cidr_or_sg
            result_label = (rule.cidr_or_sg if rule.is_cidr()
                            else rule.calculate_cidr_or_sg(rule.cidr_or_sg, self._template_params).partition('.')[0])
        if direction == 'ingress':
            description = f'From {result_label}'
            key_label = f'From{result_label}'
        else:
            description = f'To {result_label}'
            key_label = f'To{result_label}'
        return description, key_label

    def sg_builder(self, direction: str, target_group: Union[str, dict], label_from_to: str,
                   rule: Rule, rule_number: int) -> CloudFormationResource:
        """
        Builds a security group cloudformation object

        :param direction:
        :param target_group:
        :param label_from_to:
        :param rule:
        :param rule_number:
        :return:
        """
        # calculate the resource name
        resource_name = SgProcessor.target_group_to_name(target_group)
        # calculate the labels
        description, key_label = self._calculate_descriptive_labels(direction, label_from_to, rule)

        sg_key = (f"{resource_name}{key_label}"
                  f"Proto{rule.proto.upper()}Port{rule.from_port}To{rule.to_port}"
                  f"Entry{rule_number}")
        sg_value = {
            'Type': f'AWS::EC2::SecurityGroup{direction.title()}',
            'Properties': {
                'GroupId': target_group,
                'Description': description,
                'FromPort': rule.from_port,
                'ToPort': rule.to_port,
                'IpProtocol': rule.proto.lower()
            }
        }

        # add CidrIp or DestinationSecurityGroupId depending if it's a valid cidr or a security group
        if rule.is_cidr():
            sg_value['Properties']['CidrIp'] = rule.cidr_or_sg
        else:
            if direction.lower() == 'ingress':
                sg_value['Properties']['SourceSecurityGroupId'] = rule.render_destination_group_id()
            else:
                sg_value['Properties']['DestinationSecurityGroupId'] = rule.render_destination_group_id()

        return CloudFormationResource(sg_key, sg_value)

    def _resolve_rules(self, rules_node: Union[dict, str]) -> list:
        """
        Takes the rule node and verify if it's a reference to parameters and if it's a plain string or a list of strings
        :param rules_node:
        :return:
        """
        # verify whether the node is a string or a ref to a parameter
        if isinstance(rules_node, dict) and rules_node.get('Ref', None):
            # it's a ref then we lookup the info from the parameters
            data = self._template_params.get(rules_node['Ref'], None)
        elif isinstance(rules_node, str):
            data = rules_node
        elif isinstance(rules_node, list):
            data = rules_node
        else:
            raise ValueError(f'Not a valid value for Rules: {rules_node}')

        # if the data is a plan string we split it as comma separated
        if isinstance(data, str):
            rules = [elem.strip() for elem in data.split(',')]
        elif isinstance(data, list):
            rules = data
        else:
            raise ValueError(f'Unsupported data in rules. Data: {data}')
        return rules

    def _parse_rules(self, node: dict) -> List[Rule]:
        """
        parse a rule line. Rule is a string that represent the security group information.

        The format of the string is the following:

        <proto>:<cidr_or_sg>:<port_or_port_range>

        examples:

        1. multiple rules comma separated as string::

            'tcp:10.0.0.1/32:80, tcp:10.0.0.1/32:21-22'

        2. multiple rules as list of strings::

            [ 'tcp:10.0.0.1/32:80', 'tcp:10.0.0.1/32:21-22' ]

        3. multiple rules with cidrs and security groups::

            'tcp:10.0.0.1/32:80, tcp:DestinationSg.GroupId:21-22'

        4. multiple rules not in-line but with a ref to a parameter::

            { "Ref": "SomeParameter" }
            (in this case we are going to resolve the data from the parameter)

        :param node:
        :return:
        """
        # check if the rules are a reference to parameter and resolve them
        rules = self._resolve_rules(rules_node=node['Properties']['Rules'])

        rule_set = []
        # for each rule entry we parse it as per format
        for rule in rules:
            proto, cidr_or_sg, port_or_port_range = rule.strip().split(':')
            from_port, to_port = Rule.calculate_ports(port_or_port_range)
            rule_set.append(Rule(proto=proto.lower(),
                                 cidr_or_sg=Rule.calculate_cidr_or_sg(cidr_or_sg, self._template_params),
                                 from_port=from_port,
                                 to_port=to_port))
        return rule_set

    def process(self, resource: CloudFormationResource, params: dict) -> Dict[str, dict]:
        self._template_params = params
        rule_set = self._parse_rules(resource.node)

        # if there are not rules we return back the node unparsed
        if not rule_set:
            return {resource.name: resource.node}

        result = {}
        for rule_id, rule in enumerate(rule_set):
            sg = self.sg_builder(resource.properties['Direction'],
                                 resource.properties['TargetGroup'],
                                 resource.properties['FromTo'],
                                 rule, rule_id)
            result[sg.name] = sg.node
        return result
