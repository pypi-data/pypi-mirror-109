import pandas as pd
import os
import csv
import sys

# sample_ID,CHROM,POS,REF,ALT,type,seq,chr,start,end,strand,predicted_efficiency
# FIG5G_HEK293T_HEK3_6XHIS_chr9_110184619_110184639_+_GGCCCAGACTGAGCACGTGA_candidate_1808,chr9,110184636,G,GCACCATCATCACCATCAT,ngRNA,GTCAACCAGTATCCCGGTGC,chr9,110184723,110184743,-,0.6275171041488647
npg_colors = ["#E64B35","#4DBBD5","#00A087","#3C5488","#F39B7F","#464d4f"]
my_colors = {}
my_colors['sgRNA'] = npg_colors[0]
my_colors['PBS'] = npg_colors[1]
my_colors['RTT'] = npg_colors[2]
my_colors['ngRNA'] = npg_colors[3]
my_colors['variant'] = "#e6fc3f"

def hex2rgba(h):
	h = h[1:]
	a="rgba%s"%(str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4))))
	a = a.replace(")","1)")
	return a

df = pd.read_csv(sys.argv[1])
label = "FIG5G_HEK293T_HEK3_6XHIS_chr9_110184619_110184639_+_GGCCCAGACTGAGCACGTGA_candidate_1808"
df = df[df.sample_ID==label]
df['name'] = df.apply(lambda r:"""{"strand":"%s","name":"%s","color":"%s"}"""%(r.strand,r['type'],my_colors[r['type']]),axis=1)
# df['name'] = df.apply(lambda r:"""{"strand":"%s","name":"%s","color":"%s"}"""%(r.strand,r['type'],hex2rgba(my_colors[r['type']])),axis=1)
df[['chr','start','end','name']].sort_values('start').to_csv("test.bed",sep="\t",header=False,index=False,quoting=csv.QUOTE_NONE)

os.system("bgzip {0}.bed;tabix -p bed {0}.bed.gz".format("test"))
