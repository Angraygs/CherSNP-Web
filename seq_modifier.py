import json
import re

# All three dicts below could be put into a seperate JSON for reuse
# But I think it may not be necessary for this project since would need to read them in anyway

Ambig_nuc = {
	'R':['A','G'],
	'Y':['C','T'],
	'S':['C','G'],
	'W':['A','T'],
	'K':['G','T'],
	'M':['A','C'],
	'B':['C','G','T'],
	'V':['A','G','C'],
	'D':['A','G','T'],
	'H':['A','C','T']
}

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

def cds_reader(cdss):
	ans = []
	regions = cdss.split(',')
	for ele in regions:
		if len(ele) > 0:
			nods = ele.split('..')
			ans.append([int(nods[0]), int(nods[1])])
	return ans

# Extract information from AA mark
# Original AA, position, Changed AA
def aa_mark_decode(mark):
	info = mark.split('p.')[1]
	ori = info[:3]
	tar = info[-3:]
	info = info.split(ori)[1]
	pos = int(info.split(tar)[0])-1
	ori = AA_simp[ori]
	tar = AA_simp[tar]
	return pos, ori, tar
	
# Modify AA seq based on mark
def aa_modfier(seq = 'MMAAA', mark = 'p.Met2Ala'):
	# If mark is not for protein...
	if re.search(r'p.', mark) is None:
		return -1
	#Else we can go further
	else:
		#First, get all info from the mark
		pos, ori, tar = aa_mark_decode(mark)

		#Then check ref seq
		#If reference doesn't match, something is wrong
		if seq[pos] != ori:
			return -2
		#Else do the modification
		else:
			ans = seq[:pos] + tar + seq[pos+1:]
			return ans

# Modify DNA/RNA seq based on mark
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


# Convert DNA to RNA
def D2RNA(seq):
	return seq.replace('T', 'U')

# Convert RNA to DNA
def R2DNA(seq):
	return seq.replace('U', 'T')

# This would generate AA sequence based on information
def translater(seq, CDSs=None, AAmark = None):
	# Just covert it to DNA first
	seq = R2DNA(seq)
	used_rem = 0
	# Preset some variables 
	ans = []
	DNA_ans = ''
	remain = ''

	# Get AA mark information if necessary 
	if AAmark is not None:
		if re.search(r'p.', AAmark) is None:
			return -1
		else:
			pos, ori, tar = aa_mark_decode(AAmark)

	# if no CDSs specified, will assume how seq is one
	if CDSs is None: CDSs = [[1,len(seq)]]

	# Iterate through every CDS
	for p in range(len(CDSs)):
		part = CDSs[p]
		start = part[0]-1
		end = part[1]

		i = start

		# While staying in the CDS
		while i < end:
			if i+3 <= end:
				if len(remain) > 0:
					read = remain + seq[i:i+3-len(remain)]
					i -= len(remain)
					used_rem = len(remain)
					remain = ''
				else:
					read = seq[i:i+3]


				# We hit on a coding codon
				if DNA_AA[read] != '_':
					ans.append(DNA_AA[read])

					if AAmark is not None and len(ans) == pos+1:
						if DNA_AA[read] == ori:
							ans[-1] = tar

							# Get var's DNA seq
							cod = AA_DNA[tar]
							tempans = cod[0]
							opt = 0
							for c in cod:
								count = 0
								for a in range(3):
									if c[a] == read[a]: count += 1
								if count > opt:
									tempans = c
									opt = count
							# Easy pissy if not involving 2 CDSs
							if not used_rem:
								DNA_ans = seq[:i] + tempans + seq[i+3:]
							# But things can go complicated
							else:
								pre_end = CDSs[p-1][1]
								DNA_ans = seq[:pre_end-used_rem] + tempans[:used_rem] + seq[pre_end:start] + tempans[used_rem:] + seq[start+3-used_rem:] 
								used_rem = 0
						else:
							print('Error: Hit variant pos but something wrong')
							return 'Error: Hit variant pos but something wrong', 'Error: Hit variant pos but something wrong'
					i+=3

				# Or we hit on stop codon 
				else: 
					if(i+3 == CDSs[-1][1]):
						ans = ''.join(ans)
						return ans, DNA_ans
					else:
						print('Error: Hit stop codon before use all seqs')
						return 'Error: Hit stop codon before use all seqs', 'Error: Hit stop codon before use all seqs'

			# If some nucleotides are still left pass them to next cds
			else:
				remain = seq[i:end]
				break
