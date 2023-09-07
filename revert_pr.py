import os
import requests


token = os.environ["GITHUB_TOKEN"]
headers = {"Authorization": f"Bearer {token}"}

def run_query(query, variables):
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

get_pr_id_query_variables = {
  "owner": "tisutisu",
  "repo": "demo-pac",
  "pr_number": 5
}
get_pr_id_query = """
query GetPullRequestID($owner:String!, $repo:String!, $pr_number:Int!) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number: $pr_number) {
      id
    }
  }
}
"""

result = run_query(get_pr_id_query, get_pr_id_query_variables)
pr_id = result["data"]["repository"]["pullRequest"]["id"]
print(pr_id)

revert_pr_varaibles = {
    "pullrequest_id": str(pr_id),
    "title": "Reverting PR #5",
    "body" : "Reverting pull request #5",
    "draft": False,
}
revert_pr_mutation = """
mutation RevertPullRequest($pullrequest_id:ID!, $title:String!, $body:String!, $draft:Boolean!) {
  revertPullRequest(input:{pullRequestId: $pullrequest_id, title: $title, body: $body, draft: $draft}) {
    clientMutationId
    pullRequest {
      id
    }
    revertPullRequest {
      id
    }
  }
}
"""

result = run_query(revert_pr_mutation, revert_pr_varaibles)
if "errors" in result.keys():
    for error in result["errors"]:
        print("ERROR: {0}".format(error["message"]))
else:
    print("SUCCESS: Reverted PR id {0}".format(result["data"]["revertPullRequest"]["revertPullRequest"]["id"]))
