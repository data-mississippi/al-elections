import requests
import re
import sys
import json
from lxml import etree

url = 'https://www.jccal.org/elections/'

response = requests.get(url)
t = re.subn(r'<(script).*?<\/\1>(?s)', '', response.text)[0]
print(t)
tree = etree.fromstring(re.subn(r'<(script).*?<\/\1>(?s)', '', response.text)[0])
# response.text.replace('HTML', 'XML').replace(
#         '<script async type=\"text/javascript\" src=\"/_Incapsula_Resource?SWJIYLWA=719d34d31c8e3a6e6fffd425f7e032f3&ns=1&cb=1635945332\"></script>',
#         '',
#     )
pre = tree.xpath('//PRE/text()')
# print('pre', pre)

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
