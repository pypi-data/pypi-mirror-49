# Cancer Genome Interpreter #

## What does Cancer Genome Interpreter do?

 * Flags validated oncogenic alterations, and predicts cancer drivers among mutations of unknown significance.
 * Flags genomic biomarkers of drug response with different levels of clinical relevance.


## How to install

Cancer Genome Interpreter requires Python 3.5 and 
can be installed with ``pip``:

``pip install cancergenomeinterpreter``


## How to use

CGI provides one high level command ``cgi`` and
four low level commands (``cgi-cna``, ``cgi-mut``, ``cgi-fus`` and ``cgi-prescription``)
that perform part of the tasks
done by the high level one.

E.g.:

```bash
$ cgi -i muts.tsv -t BLCA
```

The ``-i`` flag indicates the input file (see the next section for more details).

The ``-t`` option can be used to indicate the cancer type.
By default (if not provided or set to CANCER) refers to any cancer type.
Available cancer types are the same that can be found in the website
(https://www.cancergenomeinterpreter.org/analysis) or in the
``ctypes.tsv`` file in this repository.


## Accepted inputs

When using the ``cgi`` command different files for mutations, CNA and
translocations can be provided by using ``-i`` multiple times; e.g.: 

```bash
$ cgi -i muts.tsv -i cnas.tsv
```

Input files need to be tab separated files where the first line
will be treated as header. Columns not mentioned below
will be ignored but included in the output.
An optional ``sample`` column can be included with the sample identifier
in all files.

**Mutations** can be stated as:
 
- *protein changes* following
  [HGVS format](http://www.hgvs.org/mutnomen/examplesAA.html)
  on the ``protein`` column
  
- *chromosomal changes* following
  [HGVS format](http://www.hgvs.org/mutnomen/recs-DNA.html)
  on the ``gdna`` column
  
- *chromosomal changes* following
  genomic tabular format with
  ``chr``, ``pos``, ``ref`` and ``alt`` columns
  
- *chromosomal changes* following
  [VCF format](http://www.1000genomes.org/wiki/Analysis/vcf4.0)
  
**Copy Number Alterations** require two columns:
``gene`` and ``cna``. Possible values in the later are ``amp`` and ``del``.
  
**Translocations** require a ``fus`` column
in which both partners are separated by two underscores ("__").

See https://www.cancergenomeinterpreter.org/formats for further details.


## Data needed

Before executing, it requires certain datasets to be accessible,
and they are read from the following environment variables:

```bash
export CGI_DATA=/path/to/datasets
export TRANSVAR_CFG=${CGI_DATA}/transvar.cfg
export TRANSVAR_DOWNLOAD_DIR=${CGI_DATA}/transvar
```

