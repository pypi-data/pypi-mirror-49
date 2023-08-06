# from urllib.parse import unquote, quote
#
# url = 'https://ip.ihuan.me/?page='+quote(str(2))
# print(unquote(url))
import re
str = 'http://			27.195.216.54		:			8118	'
a = re.sub('[ \n\t]', '', str)
print(a)