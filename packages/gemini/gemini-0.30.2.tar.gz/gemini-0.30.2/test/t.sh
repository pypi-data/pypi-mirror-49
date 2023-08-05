<<DONE
gemini query --header -q "select v.variant_id, v.chrom, v.gene, \
               g.transcript_status, g.transcript, g.transcript_start, \
                g.transcript_end, g.synonym, g.rvis_pct, g.protein_length, \
                v.impact from variants v, gene_detailed g \
                    WHERE v.chrom = g.chrom AND \
                          v.gene = g.gene AND v.impact_severity='HIGH' AND \
                          v.biotype='protein_coding' AND \
                          v.transcript = g.transcript" test.query.db

DONE
gemini query --header -q "select v.transcript, v.chrom, v.gene, \
                v.impact from variants v WHERE v.impact_severity='HIGH' AND \
                          v.biotype='protein_coding'" test.query.db
