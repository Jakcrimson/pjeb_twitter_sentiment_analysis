import csv

def exemple_data():
    data1 = "0","1467810369","Mon Apr 06 22:19:45 PDT 2023","NO_QUERY","_TheSpecialOne_","@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D"
    data2 = "0","1467810672","Mon Apr 06 22:19:49 PDT 2023","NO_QUERY","scotthamilton","is upset that he can't update his Facebook by texting it... and might cry as a result  School today also. Blah!"
    header = ["target","ids","date","flag","utilisateur","texte"]
    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(data1)
        writer.writerow(data2)

        
"""
test
"""

import pandas as pd

data = pd.read_csv('data.csv')
df = pd.DataFrame(data)