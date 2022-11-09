import requests
import re
import sys
import json
from lxml import etree

url = 'https://www.jccal.org/elections/'

response = requests.get(url)
tree = etree.fromstring(response.text.replace('HTML', 'XML'))
pre = tree.xpath('//PRE/text()')
print('pre', pre)

lines = pre[0].split('\n\n')
total = {}

for l in lines[2:]:
    vote = l.split('\n')
    vote_name = vote[0].strip()
    total[vote_name] = {}

    for i, line in enumerate(vote):
        if i > 1 and ('(VOTE FOR)  1' not in line):
            count = re.split('(\. +){2,}', line.strip())

            if count[0]:
                candidate = count[0].strip()
                tallies = [f for f in re.split(' ', count[-1]) if f]

                if len(tallies) == 1:
                    tallies = [0, 0]

                total[vote_name].update(
                    {candidate: {'count': tallies[0], 'percentage': tallies[1]}}
                )

json.dump(total, sys.stdout, indent=4)
