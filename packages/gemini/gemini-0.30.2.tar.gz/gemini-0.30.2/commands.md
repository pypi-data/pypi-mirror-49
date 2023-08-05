```
bgzip -c MT.VT.VEPv89.vcf > MT.VT.VEPv89.vcf.gz
gemini load -v MT.VT.VEPv89.vcf.gz -t VEP --skip-cadd --skip-gerp-bp --skip-pls --cores 1 MT.VT.VEP.db
gemini amend --sample MT.ped MT.VT.VEP.db

gemini query -q "select * from samples" MT.VT.VEP.db
```

```
#family_id	name	paternal_id	maternal_id	sex	phenotype	investigator_relationship
10733	151852	0	0	1	0	Father
10733	151853	0	0	2	1	Mother
10733	151854	151852	151853	1	2	Proband
11086	171139	171141	171140	2	2	Proband
11086	171140	0	0	2	1	Mother
11086	171141	0	0	1	0	Father
```

> 9545
> father              mother              proband
> 0/0:0,2:2:6:90,6,0	0/1:0,8:8:6:0,6,90	1/1:0,11:11:99:0,6,90
>
> 14318
> proband                 mother                  father
> 0/1:8,5:13:24:0,24,267	0/0:7,0:7:21:0,21,241	0/0:2,0:2:6:0,6,74



```
gemini query --header --show-samples -q "select chrom,start,end,ref,alt,filter,gts.151852,gts.151853,gts.151854,gts.171139,gts.171140,gts.171141,gt_quals.151852,gt_quals.151853,gt_quals.151854,gt_quals.171139,gt_quals.171140,gt_quals.171141,gt_depths.151852,gt_depths.151853,gt_depths.151854,gt_depths.171139,gt_depths.171140,gt_depths.171141 from variants" --gt-filter "gt_quals.151854 >= 20 and gt_depths.151854 >= 6" MT.VT.VEP.db





# NOTE!  You can't directly access gts, gt_depths, or gt_quals in the gene_wise columns, i.e. gts.151854,gts.171139

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


gemini query --header -q "select chrom,start,end,ref,alt,filter,gts.151854,gts.171139,gt_quals.151854,gt_quals.171139,gt_depths.151854,gt_depths.171139 from variants" --gt-filter "gt_quals.151854 >= 20 and gt_depths.151854 >= 6" MT.VT.VEP.db | column -t

```
