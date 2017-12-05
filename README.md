# Pyg - Python GTF parser

Pyg is designed to read GTF files and return dictionary in Python.
It can also be used to directly output a table.

## Getting Started

### Prerequisites

You will need Python 2.7 or 3 in order to run the module.

### Installing

Clone the repository

```
git clone https://github.com/Melkaz/Pyg.git
```

### Usage

Download an example GTF (here, it's a human definition from Ensembl):

```
wget ftp://ftp.ensembl.org/pub/release-90/gtf/homo_sapiens/Homo_sapiens.GRCh38.90.gtf.gz
```

#### Through python

Run your Python

```
python3
```

Load the Pyg module and parse the downloaded GTF file

```
import pyg

# GTF file path
GTF = 'Homo_sapiens.GRCh38.90.gtf.gz'

# Feature to extract. Due to memory, you have to select a feature to extract (gene, transcript or exon)
feature = 'gene'

# Read the GTF file and get a list of dictionnaries. Each line ends up being a dictionary.
dicts_list = pyg.read_gtf(GTF, selected_feature = feature)
```

From here, you can do some stuff.

"On which chromosome is TLR4 ?"

```
for gene in dicts_list:
    if gene['gene_name'] == 'TLR4':
        print(gene['seqname'])
        break
```

What is the mean length of genes ?

```
genes_lengths = []
for gene in dicts_list:
    genes_lengths.append(gene['end'] - gene['start'])

sum(genes_lengths) / len(genes_lengths)
```

Show the list of available columns (those that can be used when outputting a table)

```
pyg.show_cols(dicts_list)
```

And print the table

```
pyg.print_table(
        dicts_list,
        selected_feature = 'gene',
        output_cols = ['seqname', 'gene_id', 'start', 'end'],
        sep = '\t'
        )
# Note that both output_cols and sep are optional.

```

```
seqname gene_id start   end
1       ENSG00000227232 14404   29570
1       ENSG00000278267 17369   17436
1       ENSG00000243485 29554   31109
1       ENSG00000284332 30366   30503
1       ENSG00000237613 34554   36081
1       ENSG00000268020 52473   53312
1       ENSG00000240361 57598   64116
1       ENSG00000186092 65419   71585
1       ENSG00000238009 89295   133723
...
```
#### From the command line

You may want to simply use Pyg to only keep a feature and output a table

To output all genes:
```
python3 pyg.py print -f Homo_sapiens.GRCh38.90.gtf.gz -t gene
```

To see what columns are available for selection:
```
python3 pyg.py show_cols -f Homo_sapiens.GRCh38.90.gtf.gz -t gene
```

To only output columns you select:
```
python3 pyg.py print -f Homo_sapiens.GRCh38.90.gtf.gz -t gene -c seqname,gene_id,start,end
```

## Authors

* **Yohann Nédélec**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

