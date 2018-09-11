# VariantDatabase

An Django database for storing genetic variants found within a genetics laboratory.


## Features

VariantDatabase allows the following:


1) Basic sample tracking capabilities. Organise Projects, Runs and Samples.
1) Store variants that have been discovered.
2) Parse and store run QC data from Illumina InterOp files.
4) Parse and store sample QC data from SamStats. 
3) Allow searching for previously seen variants.
4) View variants that have been found within a specific sample.
5) Visualise variant annotation data.
6) Integrates IGV.js to allow VCF and BAM viewing.
6) Store the evidence and comments that Clinical Scientists make when analysing variants.


## Getting Started

### Requirements

The database has been tested on Centos7 using Python3. The best way to get all the requirements is to install the conda Python distribution and package manager from from: https://conda.io/docs/ 

You can then install all reqirements using a single command - see Install Requirements section for more detail. 

##### Other

To serve VCF and BAMs using IGV.js a webserver capable of HTTP range requests is required. Nginx is used in a typical deployment. Nginx is typically paired with Gunicorn which handles dynamic requests.

To annotate VCFs VEP is required (Tested on API and Cache Version 93). This is automatically installed if using the conda install method although the VEP cache will need to be installed separately. See https://bioconda.github.io/recipes/ensembl-vep/README.html for more information on how to do this.


### Installation

##### Step 1 - Install Requirements

`git clone https://github.com/WMRGL/VariantDatabase.git`

`cd VariantDatabase`

`conda env create -f envs/main.yaml`

`source activate variant_database`

`pip install -f https://github.com/Illumina/interop/releases/v1.0.25 interop`

##### Step 2 - Database Setup

`python manage.py migrate`

`python manage.py makemigrations VariantDatabase`

`python manage.py migrate`

`python manage.py createsuperuser` - follow instructions to create superuser.

##### Step 3 - Load initial data

`python manage.py loaddata db_setup.json`

##### Step 3 - Test


`python manage.py test`

##### Step 5 - Run

`python manage.py runserver`

Go to http://127.0.0.1:8000/ in your web browser to see welcome page.



## Uploading Data

### master_upload

The main utility for uploading data into the database is the master_upload management function.

For help using this program type:

`python manage.py master_upload -h`

For example to upload all data for a worksheet (SampleSheet, Variants, Run QC, Sample QC, Gene Coverage and Exon Coverage) enter the following:

`python manage.py master_upload --worksheet_dir /home/cuser/Documents/Project/DatabaseData/worksheet_dir/ --output_dir /home/cuser/Documents/Project/DatabaseData/MPN_213837/  --sample_sheet --run_qc --sample_qc --coverage --variants --subsection_name MPN_SureSeq_OGT`

It is important that the directories specified by the -w/ --worksheet_dir and output_dir/-o options are structured correctly.

###### --worksheet_dir

The path to the worksheet directory.

This is the Illumina directory containing the file SampleSheet.csv. It should be structured as shown below. Only the files needed for the VariantDatabase to function correctly are shown. Folder and file names are case sensitive.

```
worksheet_dir
│   SampleSheet.csv
│   RunParameters.xml  
│   RunInfo.xml  
│   RunCompletionStatus.xml  
│   RunParameters.xml  
│   CompletedJobInfo.xml
│   GenerateFASTQRunStatistics.xml
│
└───InterOp
│   │   ControlMetricsOut.bin
│   │   CorrectedIntMetricsOut.bin
│   │   ExtractionMetricsOut.bin
│   │   IndexMetricsOut.bin
│   │   QMetricsOut.bin
│   │   TileMetricsOut.bin

```
###### --output_dir

The path to the pipeline output directory.

The directory should be structured as shown below. Only the files needed for the VariantDatabase to function correctly are shown. Folder and file names are case sensitive.

\* = wildcard

sample_name = The unique sample name specified in the SampleSheet.csv file


```
output_dir
│
└───alignments*
│   │   sample_name.bwa.drm.realn.sorted.bam
│   │   sample_name.bwa.drm.realn.sorted.bam.bai
│   │   ...
│
└───archive*
│   │
│   └───*QC_stats.zip
│       │
│       └───*QC_stats
│           │   sample_name.bwa.drm.realn.sorted.bam.stats
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-acgt-cycles.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-coverage.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-gc-content.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-gc-depth.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-indel-cycles.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-indel-dist.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-insert-size.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-quals.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-quals2.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-quals3.png
│           │   sample_name.bwa.drm.realn.sorted.bam.stats-quals-hm.png
│           │   ...
│
└───reanalysis_data*
│   │   sample_name.exon-count-data.tsv.gz
│   │   sample_name.gene-count-data.tsv.gz
│   │   ...
│
└───vcfs*
│   │   sample_name*.vcf.gz
│   │   sample_name*.vcf.gz.tbi
│   │   ...

```
###### --sample_sheet

Add this option to import the information within the SampleSheet.csv file into the database. This will import a new worksheet and create sample objects as specified in the SampleSheet.

###### --run_qc

Add this option to import the run QC information into the database. This is the information contained within the InterOp files.

###### --sample_qc

Add this option to import the sample QC information into the database. This is the information created by the SamStats program.

###### --coverage

Add this option to import the Gene and Exon coverage information into the database.

###### --variants

Add this option to import the variant information contained within the VEP annotated vcf files.


###### --single_sample


Use this option to upload the data for a single sample. Example below:


`python manage.py master_upload --worksheet_dir /home/cuser/Documents/Project/DatabaseData/worksheet_dir/ --output_dir /home/cuser/Documents/Project/DatabaseData/MPN_213837/  --sample_qc --coverage --variants --single_sample 213837-2-D17-26177-HP_S2 --subsection_name MPN_SureSeq_OGT`

Note that the --sample_sheet and --run_qc options are not available when using the --single_sample option.

### master_upload

There is also a auto_uploader in development. This program monitors directories given in the auto_uploader/configs/auto_config.yaml configuration file. The program will check whether the specified directories contain runs which have not been uploaded to the database and then annotate them with vep before uploading them to the database if the match the rules specified in the config file.

To run this program:

`python auto_uploader/auto_uploader.py`




### VCF Format

For the vcf files to be correctly parsed by the VariantDatabase parser (parsers/vcf_parser.py) they must be annotated by VEP.

Once VEP is installed annotate your vcfs with the following command:

```
vep -i {input_vcf} -o {output_vcf} --cache --fork {n_forks} --vcf --flag_pick --format vcf --refseq 
		--exclude_predicted --everything --dont_skip --total_length  --offline --fasta {ref_genome} 
		--dir_cache {vep_cache_location} --compress_output bgzip
```
Other VCF annotations that are required include: INFO/Caller, FORMAT/AD, INFO/TCF, INFO/TCR and INFO/VAFS 

## User Guide

See the docs directory.


## Deployment

The database is designed to be deployed using gunicorn and Nginx.

To serve the BAMs and VCFs please configure the nginx config file to point at a storage location e.g. S drive. 

The settings.py file contains two variables FILE_STORAGE_ROOT and FILE_STORAGE_URL which should be entered using the named storage location in the Nginx file.

For example if in your Nginx config file says:

```
       location /files/ {
        autoindex on;
        alias   /home/joseph/Documents/variantdb_data/;
    }


```
Then within the settings.py file the two variables should be:


```
FILE_STORAGE_ROOT = '/home/joseph/Documents/variantdb_data/'
FILE_STORAGE_URL = '/files/'


```

## Authors

 * **Joseph Halstead**
