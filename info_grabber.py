link_list = []
with open('output.txt', 'r') as file:
    for line in file:
        link_list.append('https://github.com'+line.rstrip('\n'))

print(link_list)

from github import Github
# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("access_token")

# First create a Github instance:

# Public Web Github
g = Github(auth=auth)

# Github Enterprise with custom hostname
g = Github(base_url="https://{hostname}/api/v3", auth=auth)

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)

# To close connections after use
g.close()