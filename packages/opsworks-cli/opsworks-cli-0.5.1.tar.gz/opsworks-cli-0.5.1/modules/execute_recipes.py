#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# opsworks-cli for AWS OpsWorks Deployments

# execute recipes module

import boto3
import prettytable
import modules.common_functions


def test_output_summary(region, stack, layer, cookbook, custom_json):
    table = prettytable.PrettyTable()
    table.field_names = ["Region", "StackID", "LayerID", "Cookbook", "Custom_JSON"]
    table.add_row([str(region), str(stack), str(layer), str(cookbook), str(custom_json)])
    print(table.get_string(title="Test Input Summary"))


def run_recipes_with_layer(region, stack, layer, cookbook, custom_json=None):
    # adding new line to support the test functions
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print('run_recipes_with_layer sub function')
        test_output_summary(region, stack, layer, cookbook, custom_json)
    else:
        try:
            custom_json
        except NameError:
            custom_json = str({})
        if custom_json is None:
            custom_json = str({})
        # initiate boto3 client
        client = boto3.client('opsworks', region_name=region)
        # calling deployment to specified stack
        run_recipes = client.create_deployment(
            StackId=stack,
            Command={
                'Name': 'execute_recipes',
                'Args': {
                    'recipes': [
                        cookbook,
                    ]
                }
            },
            Comment='automated execute_recipes job with custom_json',
            CustomJson=custom_json
        )
        # calling aws api to get the instances within the Stack
        get_intance_count = client.describe_instances(
            LayerId=layer
        )
        all_instance_ids = []
        for instanceid in get_intance_count['Instances']:
            ec2id = instanceid['Ec2InstanceId']
            all_instance_ids.append(ec2id)
        instances = len(all_instance_ids)
        # deployment id
        deploymentid = run_recipes['DeploymentId']
        # sending describe command to get status"""  """
        modules.common_functions.get_status(deploymentid, region, instances)


def run_recipes_without_layer(region, stack, cookbook, custom_json=None):
    # adding new line to support the test functions
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print('run_recipes_without_layer sub function')
        layer = None
        test_output_summary(region, stack, layer, cookbook, custom_json=None)
    else:
        try:
            custom_json
        except NameError:
            custom_json = str({})
        if custom_json is None:
            custom_json = str({})
        # initiate boto3 client
        client = boto3.client('opsworks', region_name=region)
        # calling deployment to specified stack
        run_recipes = client.create_deployment(
            StackId=stack,
            Command={
                'Name': 'execute_recipes',
                'Args': {
                    'recipes': [
                        cookbook,
                    ]
                }
            },
            Comment='automated execute_recipes job without custom_json',
            CustomJson=custom_json
        )
        # calling aws api to get the instances within the Stack
        get_intance_count = client.describe_instances(
            StackId=stack
        )
        all_instance_ids = []
        for instanceid in get_intance_count['Instances']:
            ec2id = instanceid['Ec2InstanceId']
            all_instance_ids.append(ec2id)
        instances = len(all_instance_ids)
        # deployment id
        deploymentid = run_recipes['DeploymentId']
        # sending describe command to get status"""  """
        modules.common_functions.get_status(deploymentid, region, instances)


def execute_recipes(region, stack, cookbook, layer=None, custom_json=None):
    # adding new line to support the test functions
    if stack == '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0':
        print('execute_recipes main function testing')
        test_output_summary(region, stack, layer, cookbook, custom_json)
    else:
        # sending request to collect the stack and layer names
        modules.common_functions.get_names(stack, layer, region, "execute_recipe")
        if layer is None:
            run_recipes_without_layer(region, stack, cookbook, custom_json)
        else:
            run_recipes_with_layer(region, stack, layer, cookbook, custom_json)
