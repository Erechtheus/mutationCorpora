# Organisation

## Original
The folder "original" contains the downloaded and potentially extracted files and is a starting point for all conversion efforts.

## Converted NER-corpora
You can find corpora converted into the JSON format in folder "json". 
In the following we provide a short overview of corpora.

### AMIA18
Conversion looks fine
```
Corpus short name: amia18 
Publication: Antonio Jimeno Yepes, Andrew MacKinlay, Natalie Gunn, Christine Schieber, Noel Faux, Matthew Downton, Benjamin Goudey, Richard L. Martin, A hybrid approach for automated mutation annotation of the extended human mutation landscape in scientific literature, American Medical Informatics Association (AMIA) Symposium, 2018
URL:  https://github.com/ibm-aur-nlp/amia-18-mutation-corpus
Downloaded: 
Comments: Sets 00, 01, 02, 03 and 04 were used for training and sets 05, 06 and 07 were used as test sets in our study.
```

#### Overview of corpus 'amia-train'
```
100 documents
	Offseterrors=0
	mostCommonTokens=[('mutations', 115), ('mutation', 94), ('BRAF', 53), ('p53', 50), ('APC', 36), ('MSI', 29), ('microsatellite instability', 28), ('K-ras', 26), ('SNPs', 23), ('methylation', 20)]
1831 entities
	Entity-types=Counter({'Gene_protein': 825, 'DNA_Mutation': 592, 'locus': 187, 'Protein_Mutation': 64, 'Mutation': 60, 'DNA_modification': 43, 'dbSNP': 37, 'RNA': 18, 'RNA_Mutation': 5})
	Unique dbSNP Mentions:0
	mostCommonRSIDs=[]
	uniqueRSIDs=0
	For 0 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: set()
618 relations
	types=Counter({'Has_Mutation': 520, 'Component_of': 63, 'Has_Modification': 35})
```

#### Overview of corpus 'amia-test'
```
45 documents
	Offseterrors=0
	mostCommonTokens=[('mutations', 54), ('mutation', 49), ('MSI', 32), ('p53', 17), ('mutant', 14), ('KRAS', 13), ('SNPs', 12), ('PIK3CA', 12), ('polymorphisms', 11), ('APC', 10)]
763 entities
	Entity-types=Counter({'DNA_Mutation': 338, 'Gene_protein': 280, 'locus': 92, 'Protein_Mutation': 26, 'RNA_Mutation': 16, 'RNA': 5, 'dbSNP': 3, 'Mutation': 2, 'DNA_modification': 1})
	Unique dbSNP Mentions:0
	mostCommonRSIDs=[]
	uniqueRSIDs=0
	For 0 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: set()
227 relations
	types=Counter({'Has_Mutation': 211, 'Component_of': 15, 'Has_Modification': 1})
```



### SETH
```
SETH-master.zip
Corpus short name: SETH
Publication: Thomas, P., Rocktäschel, T., Hakenberg, J., Mayer, L., and Leser, U. (2016). SETH detects and normalizes genetic variants in text. Bioinformatics (2016)
URL: https://github.com/rockt/SETH
Downloaded: 12.2.2019 
Comments:
```

#### Overview of corpus 'SETH'
```
630 documents
	Offseterrors=0
	mostCommonTokens=[('MEN1', 30), ('BRCA1', 29), ('NF1', 24), ('TP53', 19), ('PTEN', 18), ('CFTR', 18), ('p53', 16), ('BRCA2', 16), ('SOX9', 14), ('TSC1', 13)]
3219 entities
	Entity-types=Counter({'Gene': 2315, 'SNP': 895, 'RS': 9})
	Unique dbSNP Mentions:0
	mostCommonRSIDs=[]
	uniqueRSIDs=0
	For 0 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: set()
593 relations
	types=Counter({'AssociatedTo': 384, 'Equals': 209})
```


### tmVar
```Corpus short name: tmVar 
Publication: Wei C-H, Harris BR, Kao H-Y, Lu Z (2013) tmVar: A text mining approach for extracting sequence variants in biomedical literature, Bioinformatics, 29(11) 1433-1439, doi:10.1093/bioinformatics/btt156. (link)
URL: https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/tmVar.html
Downloaded: 12.2.2019
Comments: tmVar norm contains dbSNP mentions; not sure how they were annotated
Also seperate sections for title and abstracts
```

#### Overview of corpus 'tmvar-train'
```
334 documents
	Offseterrors=0
	mostCommonTokens=[('Delta32', 13), ('R114H', 13), ('G-395A', 8), ('Met326Ile', 8), ('Cys 23 Ser', 8), ('G/C', 7), ('rs6232', 7), ('G/A', 6), ('E333D', 6), ('F826Y', 6)]
967 entities
	Entity-types=Counter({'ProteinMutation': 440, 'DNAMutation': 431, 'SNP': 96})
	Unique dbSNP Mentions:0
	mostCommonRSIDs=[]
	uniqueRSIDs=0
	For 0 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: set()
0 relations
	types=Counter()
```

#### Overview of corpus 'tmvar-test'
```
166 documents
	Offseterrors=0
	mostCommonTokens=[('Delta30', 9), ('Val175Met', 7), ('Arg399Gln', 5), ('V175M', 5), ('6bINS', 5), ('A467T', 5), ('N372H', 5), ('c.399_402delAGAG', 5), ('3020insC', 5), ('L1503R', 4)]
464 entities
	Entity-types=Counter({'DNAMutation': 220, 'ProteinMutation': 205, 'SNP': 39})
	Unique dbSNP Mentions:0
	mostCommonRSIDs=[]
	uniqueRSIDs=0
	For 0 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: set()
0 relations
	types=Counter()
```

### Variome

```Corpus short name: Variome
Publication: Verspoor K, Jimeno Yepes A, Cavedon L, McIntosh T, Herten-Crabb A, Thomas Z, Plazzer JP. (2013) Annotating the Biomedical Literature for the Human Variome. Database: The Journal of Biological Databases and Curation, 
URL: https://bitbucket.org/readbiomed/variome-corpus-data
Downloaded: 14.2.2019
Comments: Pubmed-central, many different entites
```

Please note that the offset-errors are due to some encoding issues which pose no problem.
For instance, in '1619718-05-Discussion-p01' the text '> 60 years' != '> 60 years', as the one uses a regular space and the other a hairspace.



#### Overview of corpus 'Variome'
```
120 documents
	Offseterrors=10
	mostCommonTokens=[('patients', 229), ('colorectal', 194), ('APC', 191), ('cancer', 180), ('mutation', 154), ('cancers', 137), ('CRC', 129), ('MLH1', 128), ('polyps', 126), ('BRAF', 117)]
6991 entities
	Entity-types=Counter({'disease': 1700, 'cohort-patient': 1272, 'gene': 1086, 'size': 675, 'mutation': 598, 'body-part': 465, 'Concepts_Ideas': 359, 'Disorder': 353, 'Physiology': 252, 'age': 85, 'gender': 62, 'ethnicity': 62, 'Phenomena': 22})
	Unique dbSNP Mentions:0
	mostCommonRSIDs=[]
	uniqueRSIDs=0
	For 0 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: set()
4650 relations
	types=Counter({'has': 4007, 'relatedTo': 643})
```


### Variome 120

```Corpus short name: Variome
Publication: https://pubmed.ncbi.nlm.nih.gov/25285203/
URL: https://github.com/Rostlab/nala/tree/develop/resources/corpora/variome_120
Downloaded: 12.11.2021
Comments: In Nala, the authors used Variome120, which is more specific in terms of "position specific variants", and if I understand correctly varopme is the same dataset as in the F1000 paper.
```


#### Overview of corpus 'Variome120'
```
120 documents
	Offseterrors=0
	mostCommonTokens=[('p.Lys618Ala', 39), ('V600E', 11), ('c.1852_1853AA>GC', 7), ('c.5465A > T', 4), ('c.70C > T', 3), ('c.834G > C', 3), ('c.835-7T > G', 3), ('c.3927_3931del AAAGA', 2), ('p.Pro622Thr', 2), ('proline 622 to threonine (p.Pro622Thr) amino acid substitution', 2)]
120 entities
	Entity-types=Counter({'mutation': 120})
	Unique dbSNP Mentions:0
	mostCommonRSIDs=[]
	uniqueRSIDs=0
	For 0 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: set()
0 relations
	types=Counter()
```


## Converted linking corpora

### Osiris
```OSIRIScorpusv01.xml
Corpus short name: Osiris
Publication: Furlong LI, Dach H, Hofmann-Apitius M, Sanz F. OSIRISv1.2: a named entity recognition system for sequence variants of genes in biomedical literature. BMC Bioinformatics 2008, 9:84.
URL: https://sites.google.com/site/laurafurlongweb/databases-and-tools/corpora/
Downloaded: 12.2.2019 
Comments: 
```

#### Overview of corpus 'osiris'
```
105 documents
	Offseterrors=0
	mostCommonTokens=[('insulin', 26), ('UCP2', 21), ('TNF-beta', 13), ('adiponectin', 10), ('p53', 10), ('APOE', 9), ('BDNF', 9), ('HbE', 9), ('FCGR2B', 8), ('BRCA1', 8)]
1220 entities
	Entity-types=Counter({'gene': 689, 'variant': 531})
	Unique dbSNP Mentions:242
	mostCommonRSIDs=[(1061622, 11), (747302, 9), (1801282, 8), (1799983, 7), (1050501, 6), (1009382, 6), (2245220, 6), (1805123, 6), (1861972, 6), (1861973, 6)]
	uniqueRSIDs=105
	For 0 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: set()
0 relations
	types=Counter()
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

#### Overview of corpus 'thomas'
```
296 documents
	Offseterrors=0
	mostCommonTokens=[('Val158Met', 12), ('Val66Met', 9), ('Pro12Ala', 6), ('Y402H', 5), ('V103I', 3), ('Leu72Met', 3), ('K121Q', 3), ('Gly482Ser', 3), ('T300A', 3), ('-174G>C', 3)]
527 entities
	Entity-types=Counter({'PSM': 283, 'NSM': 244})
	Unique dbSNP Mentions:527
	mostCommonRSIDs=[(4680, 14), (1061170, 11), (6265, 10), (1801282, 8), (11209026, 6), (1042522, 5), (2032582, 5), (2229616, 4), (696217, 4), (4880, 4)]
	uniqueRSIDs=385
	For 2 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: {154410, 17231380}
0 relations
	types=Counter()
```


### tmVarNorm
```Corpus short name: tmVarNorm 
Publication:tmVar 2.0: integrating genomic variant information from literature with dbSNP and ClinVar for precision medicine
Chih-Hsuan Wei, Lon Phan, Juliana Feltz, Rama Maiti, Tim Hefferon, and Zhiyong Lu
URL: https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/tmVar.html
Downloaded: 12.2.2019
Comments: 
```

Result of conversion:
```
#Offseterrors=0 in 0 docsset()
#docs=158
#entities=672
	types=Counter({'ProteinMutation': 434, 'DNAMutation': 190, 'SNP': 48})
	mostCommonTokens=[('R114H', 13), ('G-395A', 8), ('Met326Ile', 8), ('Cys 23 Ser', 8), ('Val175Met', 7), ('rs6232', 7), ('F826Y', 6), ('M404V', 6), ('Lys198Asn', 6), ('rs6235', 6)]
	Unique dbSNP Mentions:672
	mostCommonRSIDs=[(72556554, 15), (7946, 12), (1801133, 9), (6318, 9), (1207568, 8), (6232, 8), (3730089, 8), (121909210, 8), (28931614, 8), (1052133, 7)]
	For 3 dbSNP entries we could not find any information in dbSNP; potentially wrong IDs: {760040233, 11399890, 762198323}
#relations=0
	types=Counter()
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
Some corpora could not be correctly parsed are therefore not integrated into the repository.

### Nagel
Failed to correctly parse this corpus. The XML seems to be invalid and the standoff-file entities do (often) not match the string in the text.

```NagelCorpus.tar.gz
Corpus short name: Nagel
Publication: Nagel K (2009) Automatic functional annotation of predicted active sites: combining PDB and literature mining. Cambridge, UK: University of Cambridge.
Nagel K (2009) Automatic functional annotation of predicted active sites: combining PDB and literature mining. Cambridge, UK: University of Cambridge.
Nagel K, Jimeno-Yepes A, Rebholz-Schuhmann D (2009) Annotation of protein residues based on a literature analysis: cross-validation against UniProtKb. BMC Bioinformatics 10 (Suppl 8): S4.
URL: http://sourceforge.net/projects/bionlp-corpora/files/ProteinResidue/NagelCorpus.tar.gz
Downloaded: 12.2.2019
Comments: 
```

#### Nala
Interesting corpus. 
Parsed the JSON with named entities and relations, but the document format is unclear to me. 
Help highly appreciated.
```Corpus short name: Nala / tagtog_IDP4+
Publication:  Juan Miguel Cejuela, Aleksandar Bojchevski, Carsten Uhlig, Rustem Bekmukhametov, Sanjeev Kumar Karn, Shpend Mahmuti, Ashish Baghudana, Ankit Dubey, Venkata P Satagopam, Burkhard Rost; nala: text mining natural language mutation mentions, Bioinformatics, Volume 33, Issue 12, 15 June 2017, Pages 1852–1858
URL: https://www.tagtog.net/-corpora/IDP4+ and https://github.com/Rostlab/nala/tree/develop/resources/corpora
Downloaded: 12.2.2019
Comments: 
```

## Missing corpora
Some corpora we had problems to download.

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


## Visualize in BRAT
We also exported the !converted! JSON documents into BRAT. 
The BRAT exports can be found in folder BRAT. 
In order to visualize the brat-files you can  follow the docker recipe to set up a container.

### start brat docker-container:  
```shell script
docker run --name=brat -d -p 81:80 -v ~/.brat/data:/bratdata -v ~/.brat/config:/bratcfg -e BRAT_USERNAME=brat -e BRAT_PASSWORD=brat -e BRAT_EMAIL=brat@example.com cassj/brat
```
### update brat data with corpus:
```shell script
sudo rm -rf ~/.brat/data/corpus
sudo cp -r corpora/BRAT/ ~/.brat/data/corpus
sudo chmod -R 755 ~/.brat/data/corpus
sudo chown -R www-data:www-data ~/.brat/data/corpus
```

### Open browser
Visit [localhost:81](localhost:81) on your local machine to see BRAT.

## IOB export
In order to train custom NER-taggers we also export the !converted! JSON as IOB by using spacy as tokenizer.