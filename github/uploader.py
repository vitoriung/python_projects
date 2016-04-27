GITHUB_API = 'https://api.github.com'

import argparse
import requests
import base64
import json
from urlparse import urljoin

# set command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--owner", help="repository owner")
parser.add_argument("-t", "--token", help="auth token")
parser.add_argument("-r", "--reponame", help="repository")
parser.add_argument("-f", "--filepath", help="path of the file")
parser.add_argument("-d", "--destination", help="location at the destination repository")
args = parser.parse_args()

# set variables
owner = args.owner
API_TOKEN = args.token
reponame = args.reponame
filepath = args.filepath
destination = args.destination

# function check whether repository exist already
def repo ():
    url = urljoin(GITHUB_API, 'user/repos')
    payload = {}
    res = requests.get(
        url,
        headers = {
        'Authorization': 'token %s' % API_TOKEN
        }
        )
    j = json.loads(res.text)
    REPOEXIST = ''
    print 'List of current repositories:'
    for i in range(0,len(j)):
      print (j[i]["name"])
      if (j[i]["name"]) == reponame:    
        REPOEXIST = 1
    if REPOEXIST == 1:
      filecommit()
    else:
      repocreate()
      filecommit()

# function create repository    
def repocreate ():
  url = urljoin(GITHUB_API, 'user/repos')
  payload = { "name": reponame }
  res = requests.post(
        url,
        headers = {
        'Authorization': 'token %s' % API_TOKEN
        },
        data = json.dumps(payload),
        )

#function commit the file
def filecommit ():
  print 'commiting ' + filepath + ' to the ' + reponame + ' repository'
  url=urljoin(GITHUB_API, 'repos/' + owner + '/' + reponame + '/contents/' + destination )
  res = requests.get(url,)
  with open(filepath) as f:
    encoded = base64.b64encode(f.read())
  if res.status_code == 200:
    print 'file already exist at the destination'
    filesha = json.loads(res.text)['sha']
    payload = { "message": "Commit from " + API_TOKEN, "path": filepath, "content": encoded, 'sha': filesha, }
  else:
    payload = { "message": "Commit from " + API_TOKEN, "path": filepath, "content": encoded, }
  res = requests.put(
        url,
        headers = {
        'Authorization': 'token %s' % API_TOKEN
        },
        data = json.dumps(payload),
        )
  s = json.loads(res.text)      
  sha = s['commit']['sha']
  print 'Sent commit ' + sha
    
if __name__ == '__main__':
    repo()