import re
import gzip
import sys
from collections import OrderedDict

class MissingColumns(LookupError):
    '''raise this when there's a missing column name'''

def read_gtf(gtf_file, selected_feature):
    # ['gene', 'transcript', 'exon']
    elements = list()

    fn_open = gzip.open if gtf_file.endswith('.gz') else open

    with fn_open(gtf_file, 'rt') as f:
        for line in f:
            fields = line.strip().split('\t')

            try:
                feature = fields[2]
            except IndexError:
                # Looks like we picked a comment line!
                continue

            if feature not in selected_feature:
                continue

            # We treat the first 8 rows, the 9th is the feature and will be parsed again
            names = ['seqname', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute']
            first_dict = OrderedDict(zip(names, fields[:7]))
            first_dict['start'], first_dict['end'] = int(first_dict['start']), int(first_dict['end'])

            info_field = fields[8].replace('"','').strip(';')
            info_fields = re.split('; | ', info_field)
            
            second_dict = OrderedDict(zip(*[iter(info_fields)]*2))

            element = OrderedDict()
            element.update(first_dict) or element.update(second_dict)

            elements.append(element)

    return elements

def get_common_cols(dicts_list):
    keys = []
    for dict_list in dicts_list:
        for key in dict_list.keys():
            keys.append(key)

    counted_keys = OrderedDict()
    for key in keys:
        try:
            counted_keys[key] += 1
        except KeyError:
            counted_keys[key] = 1

    common_cols = [key for key in counted_keys.keys() if counted_keys[key] == len(dicts_list)]

    return(common_cols)

def show_cols(dicts_list):
    print(','.join(get_common_cols(dicts_list)))

def print_table(dicts_list, selected_feature, output_cols = None, sep = '\t'):

    # Filter list by keeping only features matching the selected_feature
    dicts_list = [x for x in dicts_list if x['feature'] == selected_feature]

    # Those are the columns found for every line
    file_cols = get_common_cols(dicts_list)
    if output_cols is None:
        header = file_cols
    else:
        if set(output_cols).issubset(file_cols):
            header = output_cols
        else:
            raise MissingColumns('Some selected columns are absent from the GTF')

    print(sep.join(map(str, [ colname for colname in header ])))
    for line in dicts_list:
        print(sep.join(map(str, [ line[colname] for colname in header ])))

def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('action', choices = ['show_cols', 'print'], nargs = 1)
    parser.add_argument('-f', '--file', help='GTF path', type=str, required=True)
    parser.add_argument('-t', '--type', help='type of feature to extract (gene, transcript or exon)', type=str, required=True)
    parser.add_argument('-c', '--cols', help='list of columns to extract', type=str, default = None)
    parser.add_argument('-s', '--sep', help='separator to use when outputting the table', type=str, default = '\t')

    args = parser.parse_args()

    dicts_list = read_gtf(args.file, selected_feature = args.type)

    if args.action[0] == 'show_cols':
        show_cols(dicts_list)

    if args.action[0] == 'print':
        if args.cols is not None:
            output_cols = [str(item) for item in args.cols.split(',')]
        else:
            output_cols = None

        print_table(
            dicts_list,
            selected_feature = args.type,
            output_cols = output_cols,
            sep = args.sep
            )

if __name__ == '__main__':
    main()