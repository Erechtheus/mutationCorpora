The contents of this downloaded tarball includes annotations of protein-residue relations in 1520 PubMed abstracts. 
This corpus is considered to be a "silver standard" corpus rather than a gold standard as the annotations were automatically
generated and validated using physical information from the Protein Data Bank.

The corpus is available for download from: http://bionlp-corpora.sourceforge.net/proteinresidue/index.shtml

========
LICENSE
========
  Read license.txt before you utilize this corpus.

========
CONTENTS
========

1) The directory contains the following files:

     a) ProteinResidueRelationsSilverCorpus_TrainingSet.tsv -> Physically validated Protein-residue pair annotations of 904 abstracts (Training set).
     b) ProteinResidueRelationsSilverCorpus_DevSet.tsv -> Physically validated Protein-residue pair annotations of 243 abstracts (Development set).
     c) ProteinResidueRelationsSilverCorpus_TestSet.tsv -> Physically validated Protein-residue pair annotations of 243 abstracts (Test set).
     d) TrainingCorpusText/ -> Abstracts used for training
     e) DevelopmentCorpusText/ -> Abstracts used for development
     f) TestCorpusText/ -> Abstracts used for testing and evaluation


File format of the tsv files:
==============================

PDB_ID	PMID	AnnotationType	Span_start	Span_End	AminoAcid_WildType_3_Letter_Abbrev	Residue_Position	AminoAcid_MutatedType_3_Letter_Abbrev	Residue_mention_in_original_text
1lod	8144527	AminoAcidResidue	530	536	TYR	100	(null)	Tyr100
2cyk	8151703	Mutation	548	553	TYR	124	ASP	Y124D

The two valid Annotation Types are "Mutation" or "AminoAcidResidue". 
The AminoAcid_MutatedType_3_Letter_Abbrev column is empty or "(null)" in the case of an AminoAcidResidue.

==========
Reference                               
==========

Please cite: 

1) Ravikumar K.E., Haibin, L., Cohn, JD,  Wall, M.E., Verspoor, K.M. (2011) "Pattern Learning Through Distant Supervision for Extraction of Protein-Residue Associations in the Biomedical Literature". The Tenth International Conference on Machine Learning and Applications (ICMLA) 2011, Honolulu, Hawaii, USA, December, 2011.
2) Verspoor KM, Cohn JD, Ravikumar KE, Wall ME (Under Review) Text Mining Improves Prediction of Protein Functional Sites.
