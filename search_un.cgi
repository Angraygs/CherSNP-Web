#!/usr/bin/env python3
import cgi
import jinja2
import re
import mysql.connector



form = cgi.FieldStorage()
temp = form.getvalue('term')
# temp = 'bifunctional'
term = '%' + str(temp) + '%'






templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('u6temp.html')

print("Content-Type: text/html\n\n")
print(template.render(results = term))
