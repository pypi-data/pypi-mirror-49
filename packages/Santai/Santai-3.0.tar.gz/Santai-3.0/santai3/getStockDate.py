__author__ = 'Administrator'  # !/usr/bin/python

import easyquotation

quotation = easyquotation.use('sina')
print(quotation.stocks('000002'))
print(quotation.stocks(['000001', '000002']))

quotation = easyquotation.use('lf')  # ['leverfun', 'lf']
#print(quotation.stocks('000002'))
#print(quotation.stocks(['000001', '000002']))
