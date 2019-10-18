# Generate test request docker action
This action will read release notes and existing issues for a given release. It will then create a test request page on Confluence, and email a list of recipients to notify them of the test request.

Github actions use yaml files to specify input and output. See [example](https://help.github.com/en/articles/creating-a-docker-container-action#example-using-a-public-action)

## TODO
1. test with an action automating the process
1. figure out how to get repo name in docker to pass to python (might have to be an argument manually configured in yaml)
1. get name of Confluence page from release notes json
1. add other columns from template to BBT and existing issues tables
1. trim crap from front of release notes (ex. - or dot from dotted list)
1. generate a TR email too, and email it to a list of recipients


## Inputs
### `confluence-space`
**Required** The key for the space in Confluence where the test request page will be created. See [space key](https://confluence.atlassian.com/doc/space-keys-829076188.html). Default `"VFJXJ"`.

### `confluence-parent-id`
**Required** The ID of the page in Confluence that will be the parent of the test request page being created. See [page id](https://confluence.atlassian.com/confkb/how-to-get-confluence-page-id-648380445.html).

### `github-key`
**Required** Personal access token that will act as an API key for github. See [creating a personal access token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line).

### `zenhub-key`
**Required** Zenhub API key. See [Zenhub authentication](https://github.com/ZenHubIO/API#authentication).

### `confluence-key`
**Required** Confluence API key. See [creating a Confluence key](https://id.atlassian.com/manage/api-tokens).

## Outputs
### `page-id`
The ID of the test request Confluence page this action will create. If this is empty then the action failed to make a page.

## Example usage
??