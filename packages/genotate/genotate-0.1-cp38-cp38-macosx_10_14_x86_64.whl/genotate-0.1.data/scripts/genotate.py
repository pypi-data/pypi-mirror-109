import sys
sys.path.pop(0)
import genotate.windows as gw

dna = 'atggtgatcgtactgactgatcgtagctagctgactg' * 10
for row in gw.get_windows(dna):
	print("\t".join([str(round(item, 3)) for item in row]))
