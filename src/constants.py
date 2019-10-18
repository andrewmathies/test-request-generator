repo_id_dict = {
    'cooking.advantium-lcd-ui': '118932734',
    'cooking.avenger_rc17': '98896708',
    'cooking.avenger_ui': '98896683',
    'cooking.cap-sense-ui': '145855732',
    'cooking.common': '98896675',
    'cooking.dorado-bsp': '116300020',
    'cooking.ParametricCommon': '98896701',
    'cooking.precision_cook_parametric': '105667303',
    'cooking.rc17-boot-loader': '98896710',
    'cooking.safety-touch-ui': '95908726',
    'cooking.wall-oven-lcd-ui': '92404662'
}

zenhub_url = 'https://api.zenhub.io/p1/'
github_url = 'https://api.github.com/repos/geappliances/'
confluence_url = 'https://geappliances.atlassian.net/wiki/rest/api/content/'

zenhub_kwargs = {
    'headers': {
        'Content-Type': 'application/json',
        'X-Authentication-Token': ''
    }
}

github_kwargs = {
    'headers': {
        'Content-Type': 'application/vnd.github.v3.raw+json',
        'User-Agent': 'Report-Generater',
        'Authorization': ''
    }
}

confluence_kwargs = {
    'headers': {
        'Content-Type': 'application/json',
        'Authorization': ''
    },
    'json': {
        "type": "page",
        "title": "",
        "space": {
            "key": ""
        },
        "ancestors": [
            {
                "id": ""
            }
        ],
        "body": {
            "storage": {
                "value": "",
                "representation": "storage"
            }
        }
    }
}

template_end = '<p class="auto-cursor-target"><br /></p>'