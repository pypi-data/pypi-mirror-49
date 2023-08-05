import sys
import click

from . import _fileio, _pairsam_format, cli, _headerops, common_io_options

UTIL_NAME = 'pairtools_flip'

@cli.command()

@click.argument(
    'pairs_path', 
    type=str,
    required=False)

@click.option(
    "-c", "--chroms-path",
    type=str,
    required=True,
    help='Chromosome order used to flip interchromosomal mates: '
         'path to a chromosomes file (e.g. UCSC chrom.sizes or similar) whose '
         'first column lists scaffold names. Any scaffolds not listed will be '
         'ordered lexicographically following the names provided.')

@click.option(
    '-o', "--output", 
    type=str, 
    default="", 
    help='output file.'
        ' If the path ends with .gz or .lz4, the output is pbgzip-/lz4c-compressed.'
        ' By default, the output is printed into stdout.')

@common_io_options

def flip(
    pairs_path, chroms_path, output,
    **kwargs
    ):
    '''Flip pairs to get an upper-triangular matrix.

    Change the order of side1 and side2 in pairs, such that 
    (order(chrom1) < order(chrom2)
     or (order(chrom1) == order(chrom2)) and (pos1 <=pos2))
    Equivalent to reflecting the lower triangle of a Hi-C matrix onto
    its upper triangle, resulting in an upper triangular matrix.
    The order of chromosomes must be provided via a .chromsizes file.

    PAIRS_PATH : input .pairs/.pairsam file. If the path ends with .gz or .lz4, the
    input is decompressed by pbgzip/lz4c. By default, the input is read from stdin.

    '''
    flip_py(
        pairs_path, chroms_path, output,
        **kwargs
    )
    
def flip_py(
    pairs_path, chroms_path, output,
    **kwargs
    ):

    instream = (_fileio.auto_open(pairs_path, mode='r', 
                                  nproc=kwargs.get('nproc_in'),
                                  command=kwargs.get('cmd_in', None)) 
                if pairs_path else sys.stdin)
    outstream = (_fileio.auto_open(output, mode='w', 
                                   nproc=kwargs.get('nproc_out'),
                                   command=kwargs.get('cmd_out', None)) 
                 if output else sys.stdout)

    chromosomes = _headerops.get_chrom_order(chroms_path)
    chrom_enum = dict(zip([_pairsam_format.UNMAPPED_CHROM] + list(chromosomes), 
                          range(len(chromosomes)+1)))

    header, body_stream = _headerops.get_header(instream)
    header = _headerops.append_new_pg(header, ID=UTIL_NAME, PN=UTIL_NAME)
    outstream.writelines((l+'\n' for l in header))

    column_names = _headerops.extract_column_names(header)
    if len(column_names) == 0:
        column_names = _pairsam_format.COLUMNS

    chrom1_col = column_names.index('chrom1')
    chrom2_col = column_names.index('chrom2')
    pos1_col = column_names.index('pos1')
    pos2_col = column_names.index('pos2')
    pair_type_col = (column_names.index('pair_type') 
                     if 'pair_type' in column_names
                     else -1)

    col_pairs_to_flip = [
        (column_names.index(col), column_names.index(col[:-1]+'2')) 
        for col in column_names
        if col.endswith('1') and (col[:-1]+'2') in column_names]

    for line in body_stream:
        cols = line.rstrip().split(_pairsam_format.PAIRSAM_SEP)

        has_correct_order = (
                (chrom_enum[cols[chrom1_col]], int(cols[pos1_col]))
             <= (chrom_enum[cols[chrom2_col]], int(cols[pos2_col]))
             )

        if not has_correct_order:
            for col1, col2 in col_pairs_to_flip:
                if (col1 < len(cols)) and (col2 < len(cols)):
                    cols[col1], cols[col2] = cols[col2], cols[col1]
            if pair_type_col != -1 and pair_type_col < len(cols):
                cols[pair_type_col] = (
                    cols[pair_type_col][1] + cols[pair_type_col][0])

        outstream.write(_pairsam_format.PAIRSAM_SEP.join(cols))
        outstream.write('\n')

    if instream != sys.stdin:
        instream.close()

    if outstream != sys.stdout:
        outstream.close()


if __name__ == '__main__':
    pair()
