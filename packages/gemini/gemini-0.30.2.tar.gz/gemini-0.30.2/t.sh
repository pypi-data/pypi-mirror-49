
gemini gene_wise \
 --columns "chrom,start,end,ref,alt,gene,impact,vep_feature_type,filter,gts,gt_quals,gt_depths" \
 --where "chrom='chrMT'" \
 --gt-filter-required "(gt_depths).(phenotype==2).(>=6).(count >= 1) and (gt_quals).(phenotype==2).(>=20).(count >= 1)" \
 --gt-filter-required "(gt_quals).(=HET).(>=20).(any) or (gt_quals).(=HOM_ALT).(>=20).(any)" \
 --gt-filter-required "(gt_depths).(=HET).(>=6).(any) or (gt_quals).(=HOM_ALT).(>=6).(any)" \
 --gt-filter "gt_types.151854 == HET" \
 --gt-filter "gt_types.171139 == HOM_ALT" \
 --min-filters 2 \
MT.VT.VEP.db

 jt.db
