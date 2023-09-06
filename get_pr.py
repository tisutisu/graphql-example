import os
import requests


owner = "tisutisu"
repo = "demo-pac"
token = os.environ["GITHUB_TOKEN"]

headers = {"Authorization": f"Bearer {token}"}

def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

      
query = """
{
  repository(owner:"tisutisu", name:"demo-pac") {
    pullRequests(last: 5) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
}
"""

result = run_query(query)
all_edges = result["data"]["repository"]["pullRequests"]["edges"]
for edge in all_edges:
    print(edge["node"]["id"], edge["node"]["title"])

