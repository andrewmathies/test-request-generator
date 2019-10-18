import requests
import json
import sys
import re

from constants import *
from util import encode_key, build_table

issue_dict = {}

def get_name(session, repo, issue_number):
    url = 'https://api.github.com/repos/geappliances/' + repo + '/issues/' + issue_number
    
    resp = session.get(url, **github_kwargs)
    issue_json = resp.json()

    if 'state' not in issue_json or 'title' not in issue_json:
        print(issue_json)
        raise SystemExit('get_name failed, bad response from github issue request')

    state = issue_json['state']
    if state != "open":
        return ''

    name = issue_json['title']
    name = name.replace('[', r'\[')
    name = name.replace(']', r'\]')

    return name

def get_pipeline(session, repo_id, issue_number):
    resp = session.get(zenhub_url + 'repositories/' + repo_id + '/issues/' + issue_number, **zenhub_kwargs)
    json = resp.json()

    if 'pipeline' in json:
        return json['pipeline']['name']
    elif 'message' in json:
        print(json['message'])
        raise SystemExit('get_pipeline failed with issue number: ' + issue_number + ' and repo id: ' + repo_id)
    else:
        #print('issue ' + issue_number + ' is closed')
        return 'Closed'

def get_notes(session, repo):
    global release_json

    resp = session.get(github_url + repo + '/releases/latest', **github_kwargs)
    release_json = resp.json()

    if 'body' in release_json:
        release_notes = release_json['body']
    else:
        print(release_json)
        raise SystemExit('get_notes failed, body not found in response for releases/latest request')
    
    links = []
    pipelines = []

    for line in release_notes.splitlines():
        # every time we see #n where n is any number of digits > 1, add the number those digits form to a list then return the list
        idList = [titleID[1:] for titleID in re.findall(r'#\d+', line.strip())]
        if len(idList):
            links.append('<a href="https://github.com/geappliances/' + repo + '/issues/' + idList[0] + '">' + line.strip() + '</a>')
            pipeline = get_pipeline(session, repo_id_dict[repo], idList[0])
            pipelines.append(pipeline)

    return links, pipelines

def get_relevant_reports(session, repo):
    if 'name' in release_json:
        release_title = release_json['name']
    else:
        raise SystemExit('get_existing_issues failed, name not found in response for releases/latest request')

    release_title = release_title.replace('-', '')
    release_title = release_title.replace('+', '')
    search_candidates = release_title.split()

    release_reports = session.get(zenhub_url + 'repositories/' + repo_id_dict[repo] + '/reports/releases', **zenhub_kwargs)
    release_reports_json = release_reports.json()
    if 'message' in release_reports_json:
            print(release_reports_json)
            raise SystemExit('get_existing_issues failed, bad response for zenhub reports/releases request')
    report_data = [(report['title'], report['state'], report['release_id']) for report in release_reports_json]

    valuable_reports = set()

    for title, state, id in report_data:
        if state == 'open':
            for candidate in search_candidates:
                matches = re.findall('\\b' + candidate + '\\b', title)
                if len(matches):
                    valuable_reports.add((id, title))

    return list(valuable_reports)

def get_existing_issues(session, repo, release):
    resp = session.get(zenhub_url + 'reports/release/' + release[0] + '/issues', **zenhub_kwargs)
    release_issues = resp.json()

    if 'message' in release_issues:
        print(json)
        raise SystemExit('get_existing_issues failed, bad response for zenhub reports/release/issues request')

    links = []
    pipelines = []

    for issue in release_issues:
        issue_repo_id = str(issue['repo_id'])
        issue_number = str(issue['issue_number'])
        key = issue_repo_id + issue_number

        # no need to include duplicate tickets
        if key in issue_dict:
            continue

        issue_dict[key] = True
        name = get_name(session, repo, issue_number)
        
        # no need to include tickets that are closed
        if not name:
            continue

        links.append('<a href="https://github.com/geappliances/' + repo + '/issues/' + issue_number + '">' + name + ' #' + issue_number + '</a>')
        pipeline = get_pipeline(session, repo_id_dict[repo], issue_number)
        pipelines.append(pipeline)
    
    return links, pipelines

def publish_page(session, html):
    confluence_kwargs['headers']['Authorization'] = encode_key(CONFLUENCE_EMAIL, CONFLUENCE_KEY)
    confluence_kwargs['json']['title'] = 'test'
    confluence_kwargs['json']['ancestors'][0]['id'] = PARENT_ID
    confluence_kwargs['json']['space']['key'] = SPACE_KEY
    confluence_kwargs['json']['body']['storage']['value'] = html

    resp = session.post(confluence_url, **confluence_kwargs)

    try:
        json = resp.json()
    except ValueError:
        raise SystemExit('publish_page failed. likely an authentication issue')

    if 'id' in json:
        print('Successfully published test request page')
        return
    else:
        print(json)
        raise SystemExit('publish_page failed, bad response for create page request')

def init_headers():
    zenhub_kwargs['headers']['X-Authentication-Token'] = ZENHUB_KEY
    github_kwargs['headers']['Authorization'] = 'token ' + GITHUB_KEY

def main():
    session = requests.Session()
    
    with open('/test-request-generator/html_templates/template_beginning.html', 'r') as f:
        page_html = f.read()

    links, pipelines = get_notes(session, REPO)
    bbt_table = build_table(['Issues', 'Pipelines'], links, pipelines)
    page_html += bbt_table

    with open('/test-request-generator/html_templates/template_middle.html', 'r') as f:
        page_html += f.read()

    reports = get_relevant_reports(session, REPO)
    for report in reports:
        links, pipelines = get_existing_issues(session, REPO, report)
        existing_issue_table = build_table(['Issues', 'Pipelines'], links, pipelines)
        if existing_issue_table:
            page_html += '<p>' + report[1] + '</p>'
            page_html += existing_issue_table

    page_html += template_end
    publish_page(session, page_html)

if __name__ == '__main__':
    global CONFLUENCE_EMAIL, SPACE_KEY, PARENT_ID, GITHUB_KEY, ZENHUB_KEY, CONFLUENCE_KEY, REPO

    CONFLUENCE_EMAIL = sys.argv[1]
    SPACE_KEY = sys.argv[2]
    PARENT_ID = sys.argv[3]
    GITHUB_KEY = sys.argv[4]
    ZENHUB_KEY = sys.argv[5]
    CONFLUENCE_KEY = sys.argv[6]
    REPO = sys.argv[7]
    
    init_headers()
    main()
