# Organisation

## Raw
The folder "raw" contains files downloaded from the respective provider.
Thils folder exists only for provenance reasons and is probably not interesting for most users.

## Original
The folder "original" contains the extracted files from "raw" and is a starting point for all conversion efforts.

## Converted corpora

### SETH
```
SETH-master.zip
Corpus short name: SETH
Publication: Thomas, P., Rocktäschel, T., Hakenberg, J., Mayer, L., and Leser, U. (2016). SETH detects and normalizes genetic variants in text. Bioinformatics (2016)
URL: https://github.com/rockt/SETH
Downloaded: 12.2.2019 
Comments:
```

### Nagel

```NagelCorpus.tar.gz
Corpus short name: Nagel
Publication: Nagel K (2009) Automatic functional annotation of predicted active sites: combining PDB and literature mining. Cambridge, UK: University of Cambridge.
Nagel K (2009) Automatic functional annotation of predicted active sites: combining PDB and literature mining. Cambridge, UK: University of Cambridge.
Nagel K, Jimeno-Yepes A, Rebholz-Schuhmann D (2009) Annotation of protein residues based on a literature analysis: cross-validation against UniProtKb. BMC Bioinformatics 10 (Suppl 8): S4.
URL: http://sourceforge.net/projects/bionlp-corpora/files/ProteinResidue/NagelCorpus.tar.gz
Downloaded: 12.2.2019
Comments: 
```

### tmVar
```Corpus short name: tmVar 
Publication: Wei C-H, Harris BR, Kao H-Y, Lu Z (2013) tmVar: A text mining approach for extracting sequence variants in biomedical literature, Bioinformatics, 29(11) 1433-1439, doi:10.1093/bioinformatics/btt156. (link)
URL: https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/tmVar.html
Downloaded: 12.2.2019
Comments: tmVar norm contains dbSNP mentions; not sure how they were annotated
Also seperate sections for title and abstracts
```

### Variome

```Corpus short name: Variome
Publication: Verspoor K, Jimeno Yepes A, Cavedon L, McIntosh T, Herten-Crabb A, Thomas Z, Plazzer JP. (2013) Annotating the Biomedical Literature for the Human Variome. Database: The Journal of Biological Databases and Curation, 
URL: https://bitbucket.org/readbiomed/variome-corpus-data
Downloaded: 14.2.2019
Comments: Pubmed-central, many different entites
```



## Ignored corpora

### Mutationfinder
Ignored this corpus, as entities are not provided with offset information.

```MutationFinder-1.1.tar.gz
Corpus short name: Mutationfinder
Publication: J. Gregory Caporaso, William A. Baumgartner Jr., David A. Randolph, K. Bretonnel Cohen, and Lawrence Hunter; "MutationFinder: A high-performance system for extracting point mutation mentions from text" Bioinformatics, 2007 23(14):1862-1865; doi:10.1093/bioinformatics/btm235;
URL: http://mutationfinder.sourceforge.net/
Downloaded: 12.2.2019 
Comments: 
```

### Thomas2011
Ignored this corpus, as the goal was not to provide a full named-entity annotation but rather associate entities with dbSNP ids

```normalization-variation-corpus.tar.gz
Corpus short name: Thomas2011
Publication: P. Thomas and R. Klinger and L. Furlong and M. Hofmann-Apitius and C. Friedrich "Challenges in the Association of Human Single Nucleotide Polymorphism Mentions with Unique Database Identifiers" (2011)
URL: https://www.scai.fraunhofer.de/en/business-research-areas/bioinformatics/downloads/corpus-for-normalization-of-variation-mentions.html
Downloaded: 13.2.2019 
Comments: Annotates only mutations with dbSNP identifier; Provides no text corpus
```

### Verspoor
```ProteinResidueFullTextCorpus.tar.gz
Corpus short name: Verspoor 
Publication: Verspoor KM, Cohn JD, Ravikumar KE, Wall ME (Under Review) Text Mining Improves Prediction of Protein Functional Sites.
URL:
Downloaded: 12.2.2019 
Comments: Text is not provided due to licence issues
```

### Ravikumar

```
ProteinResidueRelationsSilverCorpus_A1.tar.gz
ProteinResidueRelationsSilverCorpus.tar.gz
Corpus short name: Ravikumar
Publication: Ravikumar K.E., Haibin, L., Cohn, JD, Wall, M.E., Verspoor, K.M. (2011) "Pattern Learning Through Distant Supervision for Extraction of Protein-Residue Associations in the Biomedical Literature".
URL: http://sourceforge.net/projects/bionlp-corpora/files/ProteinResidue/ProteinResidueRelationsSilverCorpus.tar.gz
URL: http://sourceforge.net/projects/bionlp-corpora/files/ProteinResidue/ProteinResidueRelationsSilverCorpus_A1.tar.gz
Downloaded: 12.2.2019
Comments: silver standard corpus 
```

## Unconverted corpora


#### Nala
```Corpus short name: Nala / tagtog_IDP4+
Publication:  Juan Miguel Cejuela, Aleksandar Bojchevski, Carsten Uhlig, Rustem Bekmukhametov, Sanjeev Kumar Karn, Shpend Mahmuti, Ashish Baghudana, Ankit Dubey, Venkata P Satagopam, Burkhard Rost; nala: text mining natural language mutation mentions, Bioinformatics, Volume 33, Issue 12, 15 June 2017, Pages 1852–1858
URL: https://www.tagtog.net/-corpora/IDP4+
Downloaded: 12.2.2019
Comments: 
```

### Osiris
```OSIRIScorpusv01.xml
Corpus short name: Osiris
Publication: Furlong LI, Dach H, Hofmann-Apitius M, Sanz F. OSIRISv1.2: a named entity recognition system for sequence variants of genes in biomedical literature. BMC Bioinformatics 2008, 9:84.
URL: https://sites.google.com/site/laurafurlongweb/databases-and-tools/corpora/
Downloaded: 12.2.2019 
Comments: 
```

### tmVarNorm
```Corpus short name: tmVarNorm 
Publication:tmVar 2.0: integrating genomic variant information from literature with dbSNP and ClinVar for precision medicine
Chih-Hsuan Wei, Lon Phan, Juliana Feltz, Rama Maiti, Tim Hefferon, and Zhiyong Lu
URL: https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/tmVar.html
Downloaded: 12.2.2019
Comments: 
```

### AMIA18
```
Corpus short name: amia18 
Publication: Antonio Jimeno Yepes, Andrew MacKinlay, Natalie Gunn, Christine Schieber, Noel Faux, Matthew Downton, Benjamin Goudey, Richard L. Martin, A hybrid approach for automated mutation annotation of the extended human mutation landscape in scientific literature, American Medical Informatics Association (AMIA) Symposium, 2018
URL:  https://github.com/ibm-aur-nlp/amia-18-mutation-corpus
Downloaded: 
Comments: Sets 00, 01, 02, 03 and 04 were used for training and sets 05, 06 and 07 were used as test sets in our study.
```




## Missing corpora

### Bronco
```
Corpus short name: Bronco
Publication: BRONCO: Biomedical entity Relation ONcology COrpus for extracting gene-variant-disease-drug relations DATABASE, 2016 Apr. 
URL:   http://infos.korea.ac.kr/bronco/
Downloaded: 
Comments: Broken URL
```

### Open Mutation Miner (OMM)

```
Corpus short name: OMM
Publications: Naderi, N., and R. Witte, "Automated extraction and semantic analysis of mutation impacts from the biomedical literature", BMC Genomics, vol. 13, no. Suppl 4, pp. S10, 06/2012.
Naderi, N., "Automated Extraction of Protein Mutation Impacts from the Biomedical Literature", Department of Computer Science and Software Engineering, M. Comp. Sc., Montreal : Concordia University, 09/2011.
Naderi, N., Mutation Impact Analysis System: Automated Extraction of Protein Mutation Impacts from the Biomedical Literature, LAP LAMBERT Academic Publishing, pp. 1-224, 2012.
Naderi, N., T. Kappler, C. J. O. Baker, and R. Witte, "OrganismTagger: Detection, normalization, and grounding of organism entities in biomedical documents", Bioinformatics, vol. 27, no. 19 Oxford University Press, pp. 2721--2729, August 9, 2011.
URL:  http://www.semanticsoftware.info/open-mutation-miner#OMM_Corpora
Comments: Download via Gate
```

### extractor of mutations (EMU)
```
EMU: Corpus unavailable?
Publication: Doughty E, Kertesz-Farkas A, Bodenreider O, Thompson G, Adadey A, Peterson T, Kann MG. Toward an automatic method for extracting cancer- and other disease-related point mutations from the biomedical literature. Bioinformatics. 2011 Feb 1;27(3):408-15. doi: 10.1093/bioinformatics/btq667. Epub 2010 Dec 7. PMID: 21138947; PMCID: PMC3031038.
URL: http://bioinf.umbc.edu/EMU/ftp
Comments: Broken URL
```

