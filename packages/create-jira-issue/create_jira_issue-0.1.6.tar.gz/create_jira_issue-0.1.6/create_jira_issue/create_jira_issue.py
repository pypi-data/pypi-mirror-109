import requests
import argparse
import yaml
import json
import os
import sys
from urllib3.exceptions import InsecureRequestWarning
from url_normalize import url_normalize

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

DEFAULT_SETTINGS_NAME = "settings.yml"


def populate_with_args(parser):
    parser.add_argument("-s", help="issue summary", type=str, required=True)
    parser.add_argument("-d", help="issue description", type=str, default="")
    parser.add_argument("-n", help="path to settings file in yaml", type=str, default="settings.yml")
    parser.add_argument("--sprint", help="put issue in current sprint", action="store_true")
    return parser


def read_settings(settings_path=DEFAULT_SETTINGS_NAME):
    try:
        with open(settings_path, 'r') as settings_file:
            return yaml.full_load(settings_file)
    except IOError:
        sys.exit("error loading settings file!")


def get_create_issue_data(settings, summary, description):
    return {
        'fields': {
            'issuetype': {'id': str(settings['issuetype_id'])},
            'project': {'key': settings['project']},
            'summary': summary,
            'priority': {'id': str(settings['priority_id'])},
            'assignee': {'name': settings['assignee']},
            'reporter': {'name': settings['reporter']},
            'description': description,
            'labels': settings['labels']
        }
    }


def process_create_task_response(response, jira_url):
    if response.status_code != 201:
        print(f'error creating jira issue! Response is {response.json()} ({response.status_code})')
    else:
        body = response.json()
        issue_key = body['key']
        issue_jira_url = f"{jira_url}browse/{issue_key}"
        print(f"issue with key: {issue_key} has been created\n\n{issue_jira_url}\n\n")
        return issue_key


def get_active_sprint(settings):
    get_sprint_id_url = f"{settings['jira_url']}rest/agile/1.0/board/{settings['board_id']}/sprint?state=active"
    response = requests.get(url_normalize(get_sprint_id_url),
                            headers={'Content-Type': 'application/json'},
                            auth=(settings['login'], settings['password']),
                            verify=False)
    if response.status_code != 200:
        print(f'error getting active sprint! Response is {response.json()} ({response.status_code})')
    else:
        body = response.json()
        sprint_id = body['values'][0]['id']
        return sprint_id


def add_to_sprint(issue_key, settings):
    sprint_id = get_active_sprint(settings)
    add_to_sprint_url = f"{settings['jira_url']}/rest/agile/1.0/sprint/{sprint_id}/issue"
    data = {
        'issues': [issue_key]
    }
    response = requests.post(url_normalize(add_to_sprint_url),
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json'},
                             auth=(settings['login'], settings['password']),
                             verify=False)
    if response.status_code == 204:
        print(f"putting issue {issue_key} to sprint is successful!")
    else:
        print(f"putting issue {issue_key} to sprint is NOT successful!")


def create_jira_issue(summary, description, settings_path, to_sprint):
    settings = read_settings(settings_path)
    create_issue_url = f"{settings['jira_url']}/rest/api/2/issue"
    data = get_create_issue_data(settings, summary, description)
    jsoned_data = json.dumps(data)
    response = requests.post(url_normalize(create_issue_url),
                             data=jsoned_data,
                             headers={'Content-Type': 'application/json'},
                             auth=(settings['login'], settings['password']),
                             verify=False)
    issue_key = process_create_task_response(response, settings['jira_url'])
    if bool(issue_key) & to_sprint:
        add_to_sprint(issue_key, settings)


def validate_args(args):
    if not bool(args.n) and not os.path.exists(DEFAULT_SETTINGS_NAME):
        sys.exit("settings file not found!")


def main():
    parser = populate_with_args(argparse.ArgumentParser())
    args = parser.parse_args()
    validate_args(args)
    create_jira_issue(args.s, args.d, args.n, args.sprint)


if __name__ == '__main__':
    main()
