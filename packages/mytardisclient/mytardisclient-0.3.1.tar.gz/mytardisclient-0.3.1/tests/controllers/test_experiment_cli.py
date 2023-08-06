"""
test_experiment_cli.py

Tests for querying the MyTardis REST API's experiment endpoints
via the command-line interface
"""
import json
import sys
import textwrap
from argparse import Namespace

import requests_mock

import mtclient.client
from mtclient.conf import config
from mtclient.controllers.experiment import ExperimentController


def test_experiment_list_cli_json(capfd):
    """
    Test listing experiments, requesting output in JSON format
    """
    mock_experiment_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 1
        },
        "objects": [
            {
                "id": 1,
                "title": "Test Experiment",
                "description": "exp description",
                "authors": [
                ],
                "created_by": "/api/v1/user/1/",
                "created_time": "2017-08-03T12:59:48.600082",
                "institution_name": "Monash University",
                "owner_ids": [
                    1,
                ],
                "parameter_sets": [
                ],
                "public_access": 1,
                "update_time": "2017-08-03T12:59:48.600106",
                "resource_uri": "/api/v1/experiment/1/",
            }
        ]
    }
    mock_experiment_list_response = json.dumps(mock_experiment_list)
    with requests_mock.Mocker() as mocker:
        experiment_list_url = "%s/api/v1/experiment/?format=json" % config.url
        mocker.get(experiment_list_url, text=mock_experiment_list_response)
        exp_controller = ExperimentController()
        args = Namespace(
            model='experiment', command='list', json=True, verbose=False,
            filter=None, limit=None, offset=None, order_by=None)

        exp_controller.list(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_experiment_list

        exp_controller.run_command(args)
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_experiment_list

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'experiment', 'list', '--json']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_experiment_list
        sys.argv = sys_argv


def test_experiment_list_cli_table(capfd):
    """
    Test listing experiment records, requesting output in ASCII table format
    """
    mock_experiment_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 1
        },
        "objects": [
            {
                "id": 1,
                "title": "Test Experiment",
                "description": "exp description",
                "authors": [
                ],
                "created_by": "/api/v1/user/1/",
                "created_time": "2017-08-03T12:59:48.600082",
                "institution_name": "Monash University",
                "owner_ids": [
                    1,
                ],
                "parameter_sets": [
                ],
                "public_access": 1,
                "update_time": "2017-08-03T12:59:48.600106",
                "resource_uri": "/api/v1/experiment/1/",
            }
        ]
    }
    mock_experiment_list_response = json.dumps(mock_experiment_list)
    expected = textwrap.dedent("""
        Model: Experiment
        Query: %s/api/v1/experiment/?format=json&order_by=-created_time
        Total Count: 1
        Limit: 20
        Offset: 0

        +----+-------------------+-----------------+
        | ID |    Institution    |      Title      |
        +====+===================+=================+
        |  1 | Monash University | Test Experiment |
        +----+-------------------+-----------------+
    """) % config.url
    with requests_mock.Mocker() as mocker:
        experiment_list_url = "%s/api/v1/experiment/?format=json" % config.url
        mocker.get(experiment_list_url, text=mock_experiment_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'experiment', 'list']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv


def test_experiment_get_cli_json(capfd):
    """
    Test looking up and displaying an experiment via the command-line interface
    """
    mock_experiment = {
        "id": 1,
        "title": "Test Experiment",
        "description": "exp description",
        "authors": [
        ],
        "created_by": "/api/v1/user/1/",
        "created_time": "2017-08-03T12:59:48.600082",
        "institution_name": "Monash University",
        "owner_ids": [
            1,
        ],
        "parameter_sets": [
        ],
        "public_access": 1,
        "update_time": "2017-08-03T12:59:48.600106",
        "resource_uri": "/api/v1/experiment/1/",
    }
    mock_experiment_get_response = json.dumps(mock_experiment)
    with requests_mock.Mocker() as mocker:
        get_experiment_url = "%s/api/v1/experiment/1/?format=json" % config.url
        mocker.get(get_experiment_url, text=mock_experiment_get_response)
        exp_controller = ExperimentController()
        args = Namespace(
            model='experiment', command='get', experiment_id=1, json=True,
            metadata=False, verbose=False)
        exp_controller.get(args, render_format="json")
        out, _ = capfd.readouterr()
        assert json.loads(out) == mock_experiment


def test_experiment_get_cli_table(capfd):
    """
    Test getting experiment record via the command-line interface,
    requesting output in ASCII table format
    """
    mock_experiment = {
        "id": 1,
        "title": "Test Experiment",
        "description": "exp description",
        "authors": [
        ],
        "created_by": "/api/v1/user/1/",
        "created_time": "2017-08-03T12:59:48.600082",
        "institution_name": "Monash University",
        "owner_ids": [
            1,
        ],
        "parameter_sets": [
            {
                "id": 1,
                "experiment": "/api/v1/experiment/1/",
                "schema": {
                    "id": 1,
                    "name": "Series Metadata",
                    "namespace": "http://schema/namespace",
                    "hidden": False,
                    "immutable": True,
                    "subtype": "",
                    "type": 1
                },
                "parameters": [
                    {
                        "id": 1,
                        "name": "/api/v1/parametername/1/",
                        "parameterset": "/api/v1/experimentparameter/1/",
                        "resource_uri": "/api/v1/experimentparameter/1/",
                        "string_value": "param value",
                        "numerical_value": None,
                        "datetime_value": None,
                        "link_id": None,
                        "value": None
                    }
                ]
            }
        ],
        "public_access": 1,
        "update_time": "2017-08-03T12:59:48.600106",
        "resource_uri": "/api/v1/experiment/1/",
    }
    mock_schema = {
        "hidden": False,
        "id": 1,
        "immutable": True,
        "name": "Schema Name",
        "namespace": "http://schema/namespace",
        "resource_uri": "/api/v1/schema/1/",
        "subtype": "",
        "type": 1
    }
    mock_schema_response = json.dumps(mock_schema)
    mock_pname = {
        "id": 1,
        "choices": "",
        "comparison_type": 1,
        "data_type": 2,
        "full_name": "Parameter Name",
        "immutable": True,
        "is_searchable": False,
        "name": "param name",
        "order": 1,
        "resource_uri": "/api/v1/parametername/1/",
        "schema": "/api/v1/schema/1/",
        "units": ""
    }
    mock_pname_response = json.dumps(mock_pname)
    mock_experiment_get_response = json.dumps(mock_experiment)
    mock_dataset_list = {
        "meta": {
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": 0
        },
        "objects": [
        ]
    }
    mock_ds_list_response = json.dumps(mock_dataset_list)
    expected = textwrap.dedent("""
        +------------------+-------------------+
        | Experiment field |       Value       |
        +==================+===================+
        | ID               | 1                 |
        +------------------+-------------------+
        | Institution      | Monash University |
        +------------------+-------------------+
        | Title            | Test Experiment   |
        +------------------+-------------------+
        | Description      | exp description   |
        +------------------+-------------------+
              
        +------------------------+-------------+----------------+--------------+-----------------+----------------+---------+
        | ExperimentParameter ID |   Schema    | Parameter Name | String Value | Numerical Value | Datetime Value | Link ID |
        +========================+=============+================+==============+=================+================+=========+
        |                      1 | Schema Name | param name     | param value  |                 |                |         |
        +------------------------+-------------+----------------+--------------+-----------------+----------------+---------+
    """)
    with requests_mock.Mocker() as mocker:
        get_experiment_url = "%s/api/v1/experiment/1/?format=json" % config.url
        mocker.get(get_experiment_url, text=mock_experiment_get_response)
        get_schema_url = "%s/api/v1/schema/1/?format=json" % config.url
        mocker.get(get_schema_url, text=mock_schema_response)
        get_pname_url = "%s/api/v1/parametername/1/?format=json" % config.url
        mocker.get(get_pname_url, text=mock_pname_response)
        ds_list_url = "%s/api/v1/dataset/?format=json&experiments__id=1" % config.url
        mocker.get(ds_list_url, text=mock_ds_list_response)

        sys_argv = sys.argv
        sys.argv = ['mytardis', 'experiment', 'get', '1', '--metadata']
        mtclient.client.run()
        out, _ = capfd.readouterr()
        assert out.strip() == expected.strip()
        sys.argv = sys_argv
