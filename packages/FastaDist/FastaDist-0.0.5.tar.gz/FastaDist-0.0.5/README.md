## FastaDist
![build](https://gitlab.com/antunderwood/fastadist/badges/master/pipeline.svg)
![coverage](https://gitlab.com/antunderwood/fastadist/badges/master/coverage.svg?job=coverage)

This small utility package will calculate number of differences between all samples in a fasta alignment file.
It will count any position where there is a G,A,T or C (case insensitive) in both sequences that differ as 1 SNV.

Output formats are a square distance matrix in tsv, csv or phylip formats
It is fast since it first converts sequences to bit arrays and then uses fast bit operations to calculate the differences.

On a mid-range laptop a distance matrix was produced in 11 minutes from a 764 sequence alignment of length 1,082,859 using -p 1 and 4.5 minutes with -p 4

#### Installation
FastaDist is available as [PyPi](https://pypi.org/project/FastaDist/) package for Python3

```
pip3 install fastadist
```

#### Usage
```
usage: fastadist [-h] -i ALIGNMENT_FILEPATH -o OUTPUT_FILEPATH [-f FORMAT]
                 [-p PARALLEL_PROCESSES] [-v]

    A script to calculate distances by converting sequences to bit arrays.
    Specify number of processes as -p N to speed up the calculation


optional arguments:
  -h, --help            show this help message and exit
  -i ALIGNMENT_FILEPATH, --alignment_filepath ALIGNMENT_FILEPATH
                        path to multiple sequence alignment input file
  -o OUTPUT_FILEPATH, --output_filepath OUTPUT_FILEPATH
                        path to distance matrix output file
  -f FORMAT, --format FORMAT
                        output format for distance matrix (one of tsv
                        [default], csv and phylip
  -p PARALLEL_PROCESSES, --parallel_processes PARALLEL_PROCESSES
                        number of parallel processes to run (default 1)
  -v, --version         print out software version
```