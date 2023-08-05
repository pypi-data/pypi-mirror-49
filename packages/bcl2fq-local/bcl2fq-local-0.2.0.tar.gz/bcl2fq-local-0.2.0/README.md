# bcl2fq-local

A bcl2fastq and qc wrapper

# Install
```bash
pip install bcl2fq-local
```
or 

```bash
git clone URL
cd bcl2fq-local
python setup.py install

```

# Usage
For Bcl2fastq
```text
usage: bcl2fq-local [-h] [-i DirPath] [-o DirPath] [--sample-sheet File]
                    [--mismatch N] [--process N] [--io-process Num]
                    [--binpath File] [--dry-run] [--mask MASK]
                    [--mask-reads N] [--mask-index N] [-v]

A bcl2fastq wrapper

optional arguments:
  -h, --help           show this help message and exit
  -i DirPath           Sequence run dir
  -o DirPath           Output dir for fastq files
  --sample-sheet File  Using custom sample sheet file
  --mismatch N         Mismatch for barcode, default: 1
  --process N          Process number for demultiplexing and processing
  --io-process Num     Process number for reading and writing
  --binpath File       bcl2fastq binary file path
  --dry-run            Only print the cmd without running it
  --mask MASK          using self defined mask
  --mask-reads N       set reads mask base count, default is: 0,0
  --mask-index N       set index mask base count, default is: 0,0
  -v, --version        show version info
```

For QC
```text
usage: qc-local [-h] [-r RAW_DIR] [-c CLEAN_DIR] [-q QC_DIR] [-2 ADAPTER_DIR]
                [-t THREADS] [--paired-end] [-v]

A qc wrapper

optional arguments:
  -h, --help      show this help message and exit
  -r RAW_DIR      Raw reads dir input
  -c CLEAN_DIR    Dir to write output clean reads
  -q QC_DIR       Dir to write qc info file, default: <clean_dir>/QC
  -2 ADAPTER_DIR  Dir to write removed reads, default: <clean_dir>/002
  -t THREADS      Threads number for parallel, default:8
  --paired-end    Use qc for paired end reads
  -v, --version   Show version info
```

