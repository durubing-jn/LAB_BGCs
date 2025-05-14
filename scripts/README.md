# Biosynthetic gene clusters (BGCs) in Lactobacillaceae

## 1.BGC prediction

```sh
#GENOME.FA epresents input in fasta format
antismash GENOME.FA --taxon bacteria --output-dir PATH OF OUTPUT --genefinding-tool prodigal --cb-knownclusters -c 20 --cc-mibig --fullhmmer
```

## 2.BiG-SCAPE

```sh
#GCF analysis on a default score cutoff (c=0.3)
python bigscape.py -i gbk.files -o CGF.out --pfam_dir PFAM.db –cutoffs 0.3 -c 60 --include_singletons --mode auto
#GCF analysis on different cutoffs (c=0.5 and c=0.7)
python bigscape.py -i gbk.files -o CGF.out --pfam_dir PFAM.db –cutoffs 0.5 0.7 -c 60 --include_singletons --mode auto --mix --no_classify

```

## 3.Extraction of precursor peptide

```sh
#The precursor peptide, including leader and core peptide regions, are obtained from gbk files using a Python script
#extract_peptides.py utilized in this study is saved in the directory named scripts/
extract_peptides.py
```



## 3.BiG-SLiCE

```sh
#The BGC files in gbk format are organized into the input folder according to the developer's requirements (https://github.com/medema-group/bigslice), "bigslice_2.0.0_T0.4_16April" is downloaded from BGC Atlas database.

bigslice --query BGC/ --n_ranks 1 bigslice_2.0.0_T0.4_16April -t 60

```

## 4.BGC_function_prediction

```sh
#run with Resistance Gene Identifier (RGI)
rgi main --input_sequence bgc_fasta.file --output_file bgc.rgi --input_type contig --local --clean -n 1
#
./cluster_function_prediction.py ./gbk.files ./bgc.rgi --output ./BGC_function_prediction --antismash_version 5 --rgi_version 5
```

