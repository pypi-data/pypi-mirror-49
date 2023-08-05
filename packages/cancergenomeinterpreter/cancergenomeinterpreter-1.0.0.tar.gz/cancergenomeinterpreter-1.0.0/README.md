# Cancer Genome Interpreter #

## What does Cancer Genome Interpreter do?

 * Flags validated oncogenic alterations, and predicts cancer drivers among mutations of unknown significance.
 * Flags genomic biomarkers of drug response with different levels of clinical relevance.


## How to build it

Build the Singularity image running:

``./build.sh``

or use the ``./build_develop.sh`` to run it in development mode.


## How to run it

Run a test like this:

``singularity run -B [CGI_DATASETS_BUILD_PATH]:/data cgi.simg -i ./tests/01_mut/input.tsv``