## Find rare mutations in single cell bam file 


single-cell-bam-queries.py --help

usage: single-cell-bam-queries.py [-h] --input-file INPUT_FILE --output-file
                                  OUTPUT_FILE [--coordinates COORDINATES]
                                  [--filtered-cell-barcodes-file FILTERED_CELL_BARCODES_FILE]
                                  [--min-mapq MIN_MAPQ]
                                  [--max-gene-length MAX_GENE_LENGTH]
                                  [--threads THREADS] [--min-cells MIN_CELLS]
                                  [--max-cells MAX_CELLS]
                                  [--min-mutated-umis MIN_MUTATED_UMIS]
                                  [--max-mutated-umis MAX_MUTATED_UMIS]
                                  [--min-reads-per-non-mutated-umi MIN_READS_PER_NON_MUTATED_UMI]
                                  [--max-reads-per-non-mutated-umi MAX_READS_PER_NON_MUTATED_UMI]
                                  [--min-non-mutated-umis MIN_NON_MUTATED_UMIS]
                                  [--max-non-mutated-umis MAX_NON_MUTATED_UMIS]
                                  [--min-reads-per-mutated-umi MIN_READS_PER_MUTATED_UMI]
                                  [--max-reads-per-mutated-umi MAX_READS_PER_MUTATED_UMI]
                                  [--enable-cells-with-invalid-umis-num]
                                  [--enable-umis-with-invalid-reads-num]
                                  [--tag-of-umi TAG_OF_UMI]
                                  [--tag-of-cell-barcode TAG_OF_CELL_BARCODE]
                                  [--umi-start UMI_START]
                                  [--umi-length UMI_LENGTH]
                                  [--cell-barcode-start CELL_BARCODE_START]
                                  [--cell-barcode-length CELL_BARCODE_LENGTH]
                                  [--log-file LOG_FILE]

    Queries on bam file of single cell per genome position.

    The bam file must be sorted and indexed with the commands:

    samtools sort filename.bam > filename.sorted.bam
    samtools index filename.sorted.bam

    By default the umi and barcode cells are comptible to bam files from cellranger.
    For other formats you need to change the parameters of tags and cell barcodes.

optional arguments:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        Full path to input .bam or .sam file (default: None)
  --output-file OUTPUT_FILE
                        Full path to output file name (default: None)
  --coordinates COORDINATES
                        Coordinates of the genome. The default is all genome.
                        For example: chr1:1000000-2000000, or for all
                        chromosom: chr1 (default: all)
  --filtered-cell-barcodes-file FILTERED_CELL_BARCODES_FILE
                        Text file with list of cell barcodes. Counts only
                        these cells (optional) (default: None)
  --min-mapq MIN_MAPQ   Minimum quality of the read mapping (default: 10)
  --max-gene-length MAX_GENE_LENGTH
                        Maximum length of the gene. Reads that will be mapped
                        to longer bases will be discarded (default: 100000)
  --threads THREADS     number of threads. You can run the chromosome itself
                        in several threads. You can use this prameter only if
                        you specify the start and end coordinates explicitely
                        in the format: chr1:0-14000000 or if the bam file
                        contains header lines with the lengths of the
                        chromosomes, you can check it with the commands:
                        samtools view -h filename.bam (default: 1)
  --min-cells MIN_CELLS
                        mininum cells in genome position that contains the
                        number of umis and reads according to the other
                        parameters (default: 1)
  --max-cells MAX_CELLS
                        maximum cells in genome position that contains the
                        number of umis and reads according to the other
                        parameters (default: 1000000000)
  --min-mutated-umis MIN_MUTATED_UMIS
                        mininum umis per cell that all reads contain mutation
                        in the position (default: 1)
  --max-mutated-umis MAX_MUTATED_UMIS
                        maximum umis per cell that all reads contain mutation
                        in the position (default: 1000000000)
  --min-reads-per-non-mutated-umi MIN_READS_PER_NON_MUTATED_UMI
                        mininum reads in at least one of umis in the cell in
                        genome position (default: 1)
  --max-reads-per-non-mutated-umi MAX_READS_PER_NON_MUTATED_UMI
                        maximum reads in at least one of umis in the cell in
                        genome position (default: 1000000000)
  --min-non-mutated-umis MIN_NON_MUTATED_UMIS
                        mininum umis per cell that all reads not contain
                        mutation in the genome position (default: 1)
  --max-non-mutated-umis MAX_NON_MUTATED_UMIS
                        maximum umis per cell that all reads not contain
                        mutation in the genome position (default: 1000000000)
  --min-reads-per-mutated-umi MIN_READS_PER_MUTATED_UMI
                        mininum reads in at least one of umis in the cell in
                        genome position (default: 1)
  --max-reads-per-mutated-umi MAX_READS_PER_MUTATED_UMI
                        maximum reads in at least one of umis in the cell in
                        genome position (default: 1000000000)
  --enable-cells-with-invalid-umis-num
                        enable positions that contain cell/s with not valid
                        umis number (according to ther range in the other
                        parameters) (default: False)
  --enable-umis-with-invalid-reads-num
                        enable positions that contain umi/s with not valid
                        reads number (according to ther range in the other
                        parameters) (default: False)
  --tag-of-umi TAG_OF_UMI
                        the tag of umi in bam file (default: UR)
  --tag-of-cell-barcode TAG_OF_CELL_BARCODE
                        the tag of umi in bam file (default: CR)
  --umi-start UMI_START
                        location in tag where the umi start (0-based)
                        (default: 0)
  --umi-length UMI_LENGTH
                        length of umi (default: 10)
  --cell-barcode-start CELL_BARCODE_START
                        location in tag where the cell barcode start (0-based)
                        (default: 0)
  --cell-barcode-length CELL_BARCODE_LENGTH
                        length of cell barcode (default: 16)
  --log-file LOG_FILE   Log File (default: None)
