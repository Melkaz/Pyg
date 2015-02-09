import re
import gzip


def read_gtf(gtf_file, interesting_features = ['gene', 'transcript', 'exon']):
    elements = list()

    if gtf_file.lower().endswith('.gz'):
        opener = gzip.open
    else:
        opener = open

    with opener(gtf_file, 'rt') as f:
        for line in f:
            fields = line.strip().split('\t')

            try:
                feature = fields[2]
            except IndexError:
                # Looks like we picked a comment line!
                continue

            if feature not in interesting_features:
                continue

            # We treat the first 8 rows, the 9th is the feature and will be parsed again
            names = ['seqname', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute']
            first_dict = dict(zip(names, fields[:7]))

            info_field = fields[8].replace('"','').strip(';')
            info_fields = re.split('; | ', info_field)
            second_dict = dict(zip(*[iter(info_fields)]*2))

            element = {}
            element.update(first_dict) or element.update(second_dict)

            elements.append(element)

    return elements

if __name__ == '__main__':
    gtf_file = "Data/Homo_sapiens.GRCh37.75.SAMPLE.gtf.gz"
    # gtf_file = "Data/Homo_sapiens.GRCh37.75.SAMPLE.gtf"
    features = read_gtf(gtf_file)
    print(features[1:10])
