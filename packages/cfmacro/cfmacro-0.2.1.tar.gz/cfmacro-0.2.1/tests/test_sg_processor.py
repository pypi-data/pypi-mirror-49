#!/usr/bin/env python
import pytest

from cfmacro.cloudformation.elements import CloudFormationResource
from cfmacro.processors import SgProcessor
from cfmacro.processors.sg_processor import Rule

__author__ = "Giuseppe Chiesa"
__copyright__ = "Copyright 2017, Giuseppe Chiesa"
__credits__ = ["Giuseppe Chiesa"]
__license__ = "BSD"
__maintainer__ = "Giuseppe Chiesa"
__email__ = "mail@giuseppechiesa.it"
__status__ = "PerpetualBeta"


@pytest.mark.parametrize('target_group, expected_output', [
    ({'Ref': 'TestTargetGroup'}, 'TestTargetGroup'),
    ('TestTargetGroupString', 'TestTargetGroupString'),
    ({'Fn::GetAtt': ['TestTargetGroup', 'GroupId']}, 'TestTargetGroup')
])
def test_target_group_to_name(target_group, expected_output):
    assert SgProcessor.target_group_to_name(target_group) == expected_output


@pytest.mark.parametrize('bad_input', [
    (['TargetGroupName']),
    None,
    ({'Key': 'Value'}),
    ({'Fn::GetAttr': ['TestTargetGroup', 'VpcId']}, 'TestTargetGroup')
])
def test_target_group_to_name_wrong_input(bad_input):
    with pytest.raises(ValueError) as excinfo:
        SgProcessor.target_group_to_name(bad_input)
    assert 'Unable to calculate Sg key name' in str(excinfo.value)


@pytest.mark.parametrize('args, outcome', [
    # testing with simple cidr
    (dict(direction='ingress', target_group='TargetGroupString', label_from_to='TestLabel',
          rule=Rule(proto='tcp', cidr_or_sg='192.168.0.0/16', from_port='80', to_port='80'),
          rule_number=0),
     CloudFormationResource('TargetGroupStringFromTestLabelProtoTCPPort80To80Entry0', {
         'Type': 'AWS::EC2::SecurityGroupIngress',
         'Properties': {
             'GroupId': 'TargetGroupString',
             'Description': 'From TestLabel',
             'FromPort': '80',
             'ToPort': '80',
             'CidrIp': '192.168.0.0/16',
             'IpProtocol': 'tcp'
         }
     })),
    # testing with Fn::GetAtt for cidr that should be converted in DestinationGroupId
    (dict(direction='egress', target_group='SgVPC', label_from_to='SgTestLabel',
          rule=Rule(proto='tcp', cidr_or_sg='CustomResourceLambda.security_group_id',
                    from_port='80', to_port='80'),
          rule_number=1),
     CloudFormationResource('SgVPCToSgTestLabelProtoTCPPort80To80Entry1', {
         'Type': 'AWS::EC2::SecurityGroupEgress',
         'Properties': {
             'GroupId': 'SgVPC',
             'Description': 'To SgTestLabel',
             'FromPort': '80',
             'ToPort': '80',
             'DestinationSecurityGroupId': {'Fn::GetAtt': ["CustomResourceLambda", "security_group_id"]},
             'IpProtocol': 'tcp'
         }
     })),
    # testing with cidr is a security group (string) like sg-12345678
    (dict(direction='ingress', target_group='SgVPC', label_from_to='SgTestLabel',
          rule=Rule(proto='tcp', cidr_or_sg='CustomResourceLambda.security_group_id',
                    from_port='80', to_port='80'),
          rule_number=2),
     CloudFormationResource('SgVPCFromSgTestLabelProtoTCPPort80To80Entry2', {
         'Type': 'AWS::EC2::SecurityGroupIngress',
         'Properties': {
             'GroupId': 'SgVPC',
             'Description': 'From SgTestLabel',
             'FromPort': '80',
             'ToPort': '80',
             'SourceSecurityGroupId': {'Fn::GetAtt': ["CustomResourceLambda", "security_group_id"]},
             'IpProtocol': 'tcp'
         }
     })),
    # testing when target group is a ref to another group
    (dict(direction='egress', target_group={'Ref': 'SgVPC'}, label_from_to='SgTestLabel',
          rule=Rule(proto='tcp', cidr_or_sg='CustomResourceLambda.GroupId',
                    from_port='80', to_port='80'),
          rule_number=3),
     CloudFormationResource('SgVPCToSgTestLabelProtoTCPPort80To80Entry3', {
         'Type': 'AWS::EC2::SecurityGroupEgress',
         'Properties': {
             'GroupId': {'Ref': 'SgVPC'},
             'Description': 'To SgTestLabel',
             'FromPort': '80',
             'ToPort': '80',
             'DestinationSecurityGroupId': {'Fn::GetAtt': ["CustomResourceLambda", "GroupId"]},
             'IpProtocol': 'tcp'
         }
     })),
    # testing when label_from_to is empty then it's calculated based on the cidr_or_sg
    (dict(direction='egress', target_group={'Ref': 'SgVPC'}, label_from_to='',
          rule=Rule(proto='tcp', cidr_or_sg='CustomResourceLambda.GroupId',
                    from_port='80', to_port='80'),
          rule_number=3),
     CloudFormationResource('SgVPCToCustomResourceLambdaProtoTCPPort80To80Entry3', {
         'Type': 'AWS::EC2::SecurityGroupEgress',
         'Properties': {
             'GroupId': {'Ref': 'SgVPC'},
             'Description': 'To CustomResourceLambda',
             'FromPort': '80',
             'ToPort': '80',
             'DestinationSecurityGroupId': {'Fn::GetAtt': ["CustomResourceLambda", "GroupId"]},
             'IpProtocol': 'tcp'
         }
     })),
])
def test_sg_builder(args: dict, outcome: CloudFormationResource):
    processor = SgProcessor()
    resource = processor.sg_builder(**args)
    assert resource.name == outcome.name
    assert resource.node == outcome.node


@pytest.mark.parametrize('rules, ruleset, params', [
    # test : rules as string with single entry
    (
            'tcp:192.168.0.0/24:80',
            [Rule(proto='tcp',
                  cidr_or_sg='192.168.0.0/24',
                  from_port='80',
                  to_port='80')],
            {}
    ),
    # test : rules as string with single entry
    (
            'icmp:192.168.1.0/24:ALL',
            [Rule(proto='icmp',
                  cidr_or_sg='192.168.1.0/24',
                  from_port='-1',
                  to_port='-1')],
            {}
    ),
    # test : rules as string with multiple comma separated entries
    (
            'tcp:192.168.1.1/32:80, tcp:192.168.1.2/32:80, udp:10.10.10.10/32:20-21',
            [Rule(proto='tcp',
                  cidr_or_sg='192.168.1.1/32',
                  from_port='80',
                  to_port='80'),
             Rule(proto='tcp',
                  cidr_or_sg='192.168.1.2/32',
                  from_port='80',
                  to_port='80'),
             Rule(proto='udp',
                  cidr_or_sg='10.10.10.10/32',
                  from_port='20',
                  to_port='21')
             ],
            {}
    ),
    # test : rules as list of strings
    (
            ['tcp:192.168.1.1/32:80', 'tcp:192.168.1.2/32:80', 'udp:10.10.10.10/32:20-21'],
            [Rule(proto='tcp',
                  cidr_or_sg='192.168.1.1/32',
                  from_port='80',
                  to_port='80'),
             Rule(proto='tcp',
                  cidr_or_sg='192.168.1.2/32',
                  from_port='80',
                  to_port='80'),
             Rule(proto='udp',
                  cidr_or_sg='10.10.10.10/32',
                  from_port='20',
                  to_port='21')
             ],
            {}
    ),
    # test : rules in parameters as list of strings
    (
            {'Ref': 'testRules'},
            [Rule(proto='tcp',
                  cidr_or_sg='192.168.1.1/32',
                  from_port='80',
                  to_port='80'),
             Rule(proto='tcp',
                  cidr_or_sg='192.168.1.2/32',
                  from_port='80',
                  to_port='80'),
             Rule(proto='udp',
                  cidr_or_sg='10.10.10.10/32',
                  from_port='20',
                  to_port='21')
             ],
            {'testRules': ['tcp:192.168.1.1/32:80', 'tcp:192.168.1.2/32:80', 'udp:10.10.10.10/32:20-21']}
    ),
    # test : rules as string with destinationGroupIds instead cidrs
    (
            'tcp:sg-12345678:80, tcp:SgTest.GroupId:80, udp:CustomResourceLambda.security_group_id:20-21',
            [Rule(proto='tcp',
                  cidr_or_sg='sg-12345678',
                  from_port='80',
                  to_port='80'),
             Rule(proto='tcp',
                  cidr_or_sg='SgTest.GroupId',
                  from_port='80',
                  to_port='80'),
             Rule(proto='udp',
                  cidr_or_sg='CustomResourceLambda.security_group_id',
                  from_port='20',
                  to_port='21')
             ],
            {}
    ),
    # test : rules as string with cidr_or_sg that refers to a parameter
    (
            'tcp:sg-12345678:80, tcp:Parameters/SgTest:80, udp:CustomResourceLambda.security_group_id:20-21',
            [Rule(proto='tcp',
                  cidr_or_sg='sg-12345678',
                  from_port='80',
                  to_port='80'),
             Rule(proto='tcp',
                  cidr_or_sg='sg-87654321',
                  from_port='80',
                  to_port='80'),
             Rule(proto='udp',
                  cidr_or_sg='CustomResourceLambda.security_group_id',
                  from_port='20',
                  to_port='21')
             ],
            {'SgTest': 'sg-87654321'}
    ),
    # test : rules as string with port range and custom resource to lookup
    (
            'tcp:CustomResourceLambda.security_group_id:1024-65535',
            [Rule(proto='tcp',
                  cidr_or_sg='CustomResourceLambda.security_group_id',
                  from_port='1024',
                  to_port='65535')
             ],
            {}
    ),

])
def test_parse_rules(rules, ruleset, params):
    node = {
        'Properties': {
            'Rules': rules
        }
    }
    sgp = SgProcessor()
    sgp._template_params = params
    processed_rules = sgp._parse_rules(node)

    assert processed_rules == ruleset
