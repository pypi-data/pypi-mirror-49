# bcl2fq-local

A bcl2fastq wrapper

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
```text
usage:  bcl2fq-local -i <seq_dir> -o <ou_dir>
    
optional arguments:
    --sample-sheet Path  Using custom sample sheet file
    --mismatch N         Mismatch for barcode, default: 1
    --process N          Process number for demultiplexing and processing
    --io-process N       Process number for reading and writing
    --binpath   Path     Bcl2fastq binary file path
    --dry-run            Only print the cmd without running it
    --mask String        Use self defined mask, instead of 
    --mask-reads         Mask last few base of reads, default is: 0,0
    --mask-index         Mask last few base of index, default is: 0,0
    --version            Show  version info
```

