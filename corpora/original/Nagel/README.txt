The contents of this downloaded tarball consist of a version of the Nagel corpus. The original release consists 
of a single file which contains 100 abstracts and the annotations that accompany it as part of the corpus.
An alternative with the text files and a separate list of the annotations in stand-off representation are also provided.

The corpus is available for download from: http://bionlp-corpora.sourceforge.net/proteinresidue/index.shtml

========
LICENSE
========
  Read license.txt before you utilize this corpus.

========
CONTENTS
========

1) The directory contains the following files:

     a) Nagel_GC.xml -> Original XML annotations from Kevin Nagel (Nagel 2009)
     b) Nagel_GC.standoff.txt -> Annotations with Normalized Residue annotations along with their text spans

2) The directory contains the following subdirectory:
     a) NagelCorpusText -> The set of PubMed abstracts annotated in Nagel_GC.standoff.txt

In-line XML annotation format for Nagel's original annotations (Nagel_GC.xml):
============================================================

    1) Protein-organism-residue triplet relations
		a) XML Tag : <rel> </rel>
    			eg: <rel>O:SaccharomycesP:Vps4p (End13p), AAA-family ATPase;R:Vps4p-(K179A);A:ATP binding</rel>
			Entity Identifiers = O: Organism, P: Protein, R: Residue, A: Catalytic triad

    2) Instances of Protein name annotation in abstracts
		a) XML Tag : <p> </p>
			e.g. <p>vasopressin-neurophysin</p>
    3) Instances of Residue annotation in abstracts
		a) XML Tag : <r type="site"> </r> -> Residue with position
			e.g. <r type="site">Gly17</r>
		b) XML Tag : <r type="name"> </r> -> Only residue name without position
			e.g. <r type="name">valine residue</r>
    4) Instances of Organism name annotation in abstracts
		a) XML Tag : <o> </o>
			e.g. <o>Escherichia coli</o>
    5) Instances of catalytic triad annotation
		a) <a> </a> - > catalytic triad
			e.g. <a>redox-active</a>

Standoff file format of Nagel_GC.standoff.txt
===============================================

PMID	AnnotationType	Span_start	Span_End	AminoAcid_WildType_3_Letter_Abbrev	Residue_Position	AminoAcid_MutatedType_3_Letter_Abbrev	Residue_mention_in_original_text
10089511	Mutation	4	8	Glu	92	Lys	E92K
10366507	AminoAcidResidue	4	10	Lys	301		Lys301

The two valid Annotation Types are "Mutation" or "AminoAcidResidue". 
The AminoAcid_MutatedType_3_Letter_Abbrev column is empty in the case of an AminoAcidResidue.

===========
References
===========

  Please cite: 

Nagel K (2009) Automatic functional annotation of predicted active sites: combining PDB and literature mining. Cambridge, UK: University of Cambridge.

Nagel K, Jimeno-Yepes A, Rebholz-Schuhmann D (2009) Annotation of protein residues based on a literature analysis: cross-validation against UniProtKb. BMC Bioinformatics 10 (Suppl 8): S4.


