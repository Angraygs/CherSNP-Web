
	Introduction: 
		With the fast growth in DNA sequencing techniques, SNP (Single-nucleotide polymorphism) variants are more and more studied. However, sometimes, sequence of the variants may not be available directly. Variant might be simply annotated with allele change in HGVS format, like c.924G>A, or/and residue change, like p.Leu1517Phe, instead of having the whole sequence, which does make sense since SNP variants should only have 1 bp different with canonical sequence. But some researcher may still need the sequences for different reasons.

		Intoductions about HGVS annotation can be found here: https://www.hgvs.org/mutnomen/recs-DNA.html

		This project is aiming to create a HTML page which could output the DNA, RNA, or amino acid sequence of SNP variant in FASTA format based on user's input canonical sequence, which also could be in DNA, RNA, or AA types, CDS coordinates, and allele change / residue change annotation. However, if user selected to input AA sequence as reference sequence, both SNP annotation type and output type are restricted to AA type. 

	Requirment:
		HTML5 browser and accessibility to bfx3.aap.jhu

	Useage:
		1. Input HGVS format SNP annotation in first box
		2. Please choose correspond type of refernce sequence in first select box
		3. If you believe translation process would be needed, please indicate CDS regions in second box. However, if you don't think so or there are no introns in sequence, please feel free to leave it blank
		4. Please input reference sequence in third box
		5. Please indicate desired output type


	Approach:
		Based on my imagination, this could be done in 3 general process:
			1. Having SNP annotation, source seqeunce, CDS coordinates, and desired output type passed to python script from HTML
			2. Having python script generate the desidred sequences with following basic principal: 
				a. Convert input sequence into same type with annotation (DNA, RNA or Protein) if they are in different type.
				b. Make change based on annotation to consisting sequence.
				c. Convert changed sequence into desired output type. 

				Note: 
					If translation process would be needed in either a or c part, users' input CDS regions will be used for process.

					If input type is Amino Acid (Protein), this application would only accept consisting SNP annotation and AA output type because, without information about regions like UTRs and introns, neither DNA nor RNA sequence could be gained purely based on AA sequnece.

					The convertion between DNA and RNA is simply substitute U to T or T to U, which is stimulating transcription process.

	Test:
		My test seqeunce is an arbitray short sequence which could be processed even manually and makes debug much more doable.
		seq = 'ATGACGACGACGACGACGACGACGACGACGACGACGACGACGGGGGGGGGGTTTTAG'
		or correspond protein sequence:
		seq = 'MTTTTTTTTTTTTTF'


		Basically, two types of situation would be faced:
			1. Translation required: 
				This would be little bit complicated espeically considering the codon of AA influenced by SNP could be in 2 seperate CDS. One of the relatively comprehensive test I came out with is using DNA seq + annotation being p.Thr14Ala and set output sequence as RNA. CDS is 1..41,51..57
				In this case, to make changes on reference sequence, translation process would be tested as the same time with testing ability to mark allele changes on reference DNA seq when AA change influences 2 CDSs. Then, to make output RNA type, the DNA RNA conversion ability is also tested.
			2. Translation not required: 
				This type is realatively easy and could be tested with either DNA seq + annotation being r.4A>U + output being back into DNA
				Or using AA seq with annotation p.Thr14Ala and output being AA

	Discussion:
		One thing bothers me the most was thinking about 'What users could wrongly input'. This could be not only simple error like input annotation in wrong format, CDS regions in unsupported format, but also be complicate errors like CDS regions are not consisting with input sequence (like stop codon comes earlier than CDS ends). Certainly I have tried to deal with some, but I am pretty sure there are more things could be done espeicially if this is not just a single demo project but something really goes online. As we should known, users could always make some 'incredible' mistakes which are corner cases we just failed to realized.

	URL: http://bfx3.aap.jhu.edu/gyu17/final/search.html
	Source codes can be found on server: /var/www/html/gyu17/final or on blackboard as I submitted or on GitHub

