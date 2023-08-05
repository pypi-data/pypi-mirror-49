set -euo pipefail
zcat /data/gemini_install/data/gemini_data/clinvar_20170130.tidy.vcf.gz \
    | awk 'BEGIN{FS=OFS="\t"}($1 == "#CHROM"){ print "##FORMAT=<ID=GQ,Number=1,Type=Float,Description=\"Genotype Quality\">"; print "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">"; print "##FORMAT=<ID=AD,Number=R,Type=Integer,Description=\"Allelic depths for the ref and alt alleles in the order listed\">"; print $0,"FORMAT","sample";next}($0 ~ /^#/){ print;next } { print $0, "GT:AD:GQ", "0/1:20,20:30" }' \
    | bcftools view  -O z -o cv.test.vcf.gz /dev/stdin

echo $'fam1\tsample\t-9\t-9\t1\t1' > cv.test.ped

#wget ftp://ftp.ensembl.org/pub/grch37/release-84/gff3/homo_sapiens/Homo_sapiens.GRCh37.82.gff3.gz

gff=Homo_sapiens.GRCh37.82.gff3.gz
fasta=/data/human/g1k_v37_decoy.fa


bcftools csq -g $gff -f $fasta -l  --samples - cv.test.vcf.gz -O z -o cv.anno.vcf.gz


gemini load -t BCFT -v cv.anno.vcf.gz -p cv.test.ped cv.test.db
