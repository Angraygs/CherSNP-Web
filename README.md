# 410.712
Jack Yu - Final Project Proposal

	Introduction: 
		With the fast growth in DNA sequencing techniques, SNP (Single-nucleotide polymorphism) variants are more and more studied. However, sometimes, sequence of the variants may not be available directly. Variant might be simply annotated with allele change, like c.924G>A, or/and residue change, like p.Leu1517Phe, instead of having the whole sequence, which does make sense since SNP variants should only have 1 bp different with canonical sequence. But some researcher may still need the sequences for different reasons.

		My final project would be aiming to create a HTML page which could output both the RNA sequence and amino acid sequence of SNP variant in FASTA format based on user's input transcript level canonical sequence (mRNA for example) and allele change / residue change annotation. If the canonical transcript does have introns inside, user would need to provided the cutting sequence in snRNPs.

	Approach:
		Based on my imagination, this could be done in 3 general process:
			1. Having annotation and seqeunce passed to python script from HTML
			2. Having python script generate the desidred sequences:
				a. If annotation is allele change:
					Make the RNA sequence first, and then translate the sequence by cut out UTRs and introns
				b. If annotation is residue change:
					Try to translate the canonical sequence first, mark the position of CDSs, make the change based on annotation, and then get RNA sequence with the help of marks.

		Considering...:
			Maybe I could set up button tags asking user whether they are inputing RNA sequence or AA sequence and whether they want RNA sequence alone, AA sequence alone, or both?
