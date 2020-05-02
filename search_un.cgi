#!/usr/bin/env python3
import cgi
import jinja2
import re
import seq_modifier

templateLoader = jinja2.FileSystemLoader(searchpath="./templates" )
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('temp.html')

form = cgi.FieldStorage()

mark = form.getvalue('mark')
cds = form.getvalue('cds')
seq = form.getvalue('seq')
out = form.getvalue('out')
inf = form.getvalue('inf')

# seq = 'ATGACGACGACGACGACGACGACGACGACGACGACGACGACGGGGGGGGGGTTTTAG'
# cds = '1..41,51..57'
# mark = 'p.Thr14Ala'

temp = seq.split()
rseq = ''
for ele in temp:
	if re.search(r'>', ele): 
		header = ele + ': ' + mark + ', ' + out
	else:
		rseq += str(ele)
cdss = seq_modifier.cds_reader(cds)

if inf == 'AA' and out == 'AA':
	if mark.split('.')[0] == 'p':
		anseq = seq_modifier. aa_modfier(rseq, mark)
	else:
		print("Content-Type: text/html\n\n")
		print(template.render(ans = ['Error','Error: Protein input can only go with Protein mark']))
elif inf == 'AA' and out != 'AA':
	print("Content-Type: text/html\n\n")
	print(template.render(ans = ['Error','Error: Protein input can only go with Protein output']))

elif mark.split('.')[0] == 'p':
	ansp, ansd = seq_modifier.translater(rseq, cdss, mark)
	if out == 'AA': anseq = ansp
	elif out == 'DNA':anseq = ansd
	else: anseq = seq_modifier.D2RNA(ansd)

else:
	if inf == 'RNA':
		if mark.split('.')[0] == 'c':
			temp = seq_modifier.R2DNA(rseq)
			anseq = seq_modifier.xna_modfier(temp, mark)
		elif mark.split('.')[0] == 'r':
			anseq = seq_modifier.xna_modfier(rseq, mark)


	elif inf == 'DNA':
		if mark.split('.')[0] == 'c':
			anseq = seq_modifier.xna_modfier(rseq, mark)
		elif mark.split('.')[0] == 'r':
			temp = seq_modifier.D2RNA(rseq)
			anseq = seq_modifier.xna_modfier(temp, mark)

	else:
		print("Content-Type: text/html\n\n")
		print(template.render(ans = ['Error','Error: Something is wrong...']))

	if out == 'AA': anseq,temp = seq_modifier.translater(anseq, cdss)
	elif out == 'DNA':anseq = seq_modifier.R2DNA(anseq)
	else: anseq = seq_modifier.D2RNA(anseq)




ans = [header, anseq]
print("Content-Type: text/html\n\n")
print(template.render(ans = ans))
