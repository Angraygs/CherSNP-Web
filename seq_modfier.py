import json
import re

DNA_AA = {
	'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
	'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
	'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
	'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
	'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
	'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
	'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
	'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
	'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
	'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
	'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
	'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
	'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
	'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
	'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
	'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}

AA_DNA = {
	'A':['GCA','GCC','GCG','GCT'],
	'R':['CGA','CGC','CGG','CGT','AGA','AGG'],
	'N':['AAC','AAT'],
	'D':['GAC','GAT'],
	'C':['TGC','TGT'],
	'E':['GAA','GAG'],
	'Q':['CAA','CAG'],
	'G':['GGA','GGC','GGG','GGT'],
	'H':['CAC', 'CAT'],
	'I':['ATA','ATC','ATT'],
	'L':['CTA','CTC','CTG','CTT','TTA','TTG'],
	'K':['AAA','AAG'],
	'M':['ATG'],
	'F':['TTC','TTT'],
	'P':['CCA','CCC','CCG','CCT'],
	'S':['TCA','TCC','TCG','TCT','AGC','AGT'],
	'T':['ACA','ACC','ACG','ACT'],
	'W':['TGG'],
	'Y':['TAC','TAT'],
	'V':['GTA','GTC','GTG','GTT']
}

AA_simp = {
	'Ala':'A',
	'Arg':'R',
	'Asn':'N',
	'Asp':'D',
	'Cys':'C',
	'Glu':'E',
	'Gln':'Q',
	'Gly':'G',
	'His':'H',
	'Ile':'I',
	'Leu':'L',
	'Lys':'K',
	'Met':'M',
	'Phe':'F',
	'Pro':'P',
	'Ser':'S',
	'Thr':'T',
	'Trp':'W',
	'Tyr':'Y',
	'Val':'V',
}

def aa_modfier(seq = 'MMAAA', mark = 'p.Met2Ala'):
	# If mark is not for protein...
	if re.search(r'p.', mark) is None:
		return -1
	#Else we can go further
	else:
		#First, get all info from the mark
		info = mark.split('p.')[1]
		ori = info[:3]
		tar = info[-3:]
		info = info.split(ori)[1]
		pos = int(info.split(tar)[0])-1
		ori = AA_simp[ori]
		tar = AA_simp[tar]
	
		#Then check ref seq
		#If reference doesn't match, something is wrong
		if seq[pos] != ori:
			return -2
		#Else do the modification
		else:
			ans = seq[:pos] + tar + seq[pos+1:]
			return ans

def xna_modfier(seq = 'AGCCCT', mark = 'c.2G>A'):
	# Not supporting genomic mark
	if re.search(r'g.', mark) is not None:
		return -1

	# Only process when mark in acceptable types
	elif re.search(r'r.', mark) is not None or re.search(r'c.', mark) is not None:
		#First, get all info from the mark
		typ = mark.split('.')[0]
		info = mark.split('.')[1]
		ori = info[-3]
		tar = info[-1]
		pos = int(info.split(info[-3:])[0])-1
		#Format check + Ref seq matching
		if info[-2] == '>' and seq[pos] == ori:
			ans = seq[:pos] + tar + seq[pos+1:]
			return ans
		else:
			return -2
	
# def translater 

print(aa_modfier())
print(xna_modfier())