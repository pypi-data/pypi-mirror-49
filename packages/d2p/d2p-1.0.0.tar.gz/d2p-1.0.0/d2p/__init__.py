from bs4 import BeautifulSoup as S
from sys import argv
def d2p(xml, plaintext):
    soup = S(open(xml, encoding='utf-8').read(), features='lxml')
    pt = open(plaintext, encoding='utf-8', mode='w')
    for i in soup.find_all('d'):
        pt.write(i.text)
if len(argv) == 3:
    d2p(argv[1], argv[2])
