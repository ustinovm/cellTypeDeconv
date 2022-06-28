#options(datatable.fread.datatable=FALSE)

genesunnor <- data.table::fread("Marrow-countsrenamed.tsv")
genesmat <- data.table::fread("Marrow-countsrenamed_normalized_filteredNames.tsv")
genesindex <- data.table::fread("Marrow-countsrenamed_normalized_indexed.tsv")

kmerunnor <- data.table::fread("marrow15.tsv")
kmermat <- data.table::fread("marrow15_reallynormalized_norm_importantFeatdiv200.tsv")
kmerindex <- data.table::fread("marrow15_normalized_indexed.tsv")


##GENE
genes <- colnames(genesmat)[-1]   # speicher gene als liste, alle spaltennamen ausser 1
genesmat <- t(genesmat)   # matrix transponiert
colnames(genesmat) <- unlist(genesmat[1,])   # spaltennamen standen in zeile 1, sind jetzt spaltennamen
genesmat <- genesmat[-1,]   # zeile 1 entfernt
genesmat <- data.frame(genesmat, check.names = F)   # data frame erstellt 
rownames(genesmat) <- genes           # gene list aus zeile 12 als zeilennamen


##KMER
kmers <- colnames(kmermat)[-1]
kmermat <- t(kmermat)
colnames(kmermat)<-unlist(kmermat[1,])
kmermat <- kmermat[-1,]
kmermat <- data.frame(kmermat, check.names=F)
rownames(kmermat) <- kmers


##GENE
genesunnor <- data.frame(genesunnor, check.names = F)     # data frame erstellt 
rownames(genesunnor) <- genesunnor$V1    # gene namen standen in erster spalte (V1), jetzt als zeilennamen
genesunnor$V1 <- NULL                    # spalte 1 entfernen
tmp <- lapply(colnames(genesunnor), function(x){strsplit(x, '_')[[1]][-1]})   # jeden spaltennamen gesplittet nach _, dann ersten index in gesplitteter liste entfernt
cell_ids <- lapply(tmp, function(x){x[-length(x)]})                          # von result oben entferne letztes element in jeder liste
cell_ids <- unlist(sapply(cell_ids, paste, collapse = " "))                  # alle restlichen elemente in liste zusammenklatschen
colnames(genesunnor) <- cell_ids         # spaltennamen mit neuen cell ids ersetzen


##KMER
kmerunnor <- data.frame(kmerunnor, check.names = F)     # data frame erstellt 
rownames(kmerunnor) <- kmerunnor$V1    # gene namen standen in erster spalte (V1), jetzt als zeilennamen
kmerunnor$V1 <- NULL                    # spalte 1 entfernen
temp <- lapply(colnames(kmerunnor), function(x){strsplit(x, '_')[[1]][-1]})   # jeden spaltennamen gesplittet nach _, dann ersten index in gesplitteter liste entfernt
kmer_ids <- lapply(temp, function(x){x[-length(x)]})                          # von result oben entferne letztes element in jeder liste
kmer_ids <- unlist(sapply(kmer_ids, paste, collapse = " "))                  # alle restlichen elemente in liste zusammenklatschen
colnames(kmerunnor) <- kmer_ids         # spaltennamen mit neuen cell ids ersetzen


# keep only cells and genes that are in both GENE
cell_intersection <- Reduce(intersect, list(colnames(genesmat), colnames(genesunnor)))   # intersection aus cell ids in normalized und raw matrix
genes_intersection <- Reduce(intersect, list(rownames(genesmat), rownames(genesunnor)))  # gleiche aber auf gene ids
genesunnor <- genesunnor[genes_intersection,cell_intersection]      # nehmen diese intersection sets aus unnormalized matrix

# keep only cells and genes that are in both KMER
kmer_cell_intersection <- Reduce(intersect,list(colnames(kmermat), colnames(kmerunnor)))
kmer_intersection <- Reduce(intersect, list(rownames(kmermat),rownames(kmerunnor)))
kmerunnor <- kmerunnor[kmer_intersection, kmer_cell_intersection]

# handle index GENE
genesindex <- t(genesindex)  
genesindex <- genesindex[-1,]     # leere zeile weg
genesindex <- data.frame(genesindex)
colnames(genesindex) <- c('ID','cell_type')   # spaltennamen setzen -> so brauchts SimBu
genesindex <- genesindex[genesindex[["ID"]] %in% cell_intersection, ]  # intersection von cells auch im index nehmen

# handle index KMER
kmerindex <- t(kmerindex)
kmerindex <- kmerindex[-1,]
kmerindex <- data.frame(kmerindex)
colnames(kmerindex) <- c('ID','cell_type')
kmerindex <- kmerindex[kmerindex[["ID"]] %in% kmer_cell_intersection, ]

#cell_intersection <- as.list(cell_intersection)


# convert data frame to sparse matrix
genesunnor <- as(as.matrix(genesunnor), 'dgCMatrix')         # dataframe als sparse matrix
genesmat <- as(as.matrix(genesmat), 'dgCMatrix')

kmerunnor <- as(as.matrix(kmerunnor),'dgCMatrix')
kmermat <- as(as.matrix(kmermat), 'dgCMatrix')

library(SimBu)
# simbu datatset
# http://omnideconv.org/SimBu/articles/simulator_documentation.html#simulate-pseudo-bulk-datasets
dataset_genes <- dataset(annotation = genesindex, 
                         count_matrix = genesunnor, 
                         tpm_matrix = genesmat, 
                         name = 'test', 
                         filter_genes = T, variance_cutoff = .1)

dataset_kmers <- dataset(annotation = kmerindex,
                         count_matrix = kmerunnor,
                         tpm_matrix = kmermat,
                         name = "kmersmatrix",
                         variance_cutoff = .1
                         )

# outputs: http://omnideconv.org/SimBu/articles/simulator_input_output.html#output
simulation <- SimBu::simulate_bulk(data = dataset_genes, 
                                   scenario = "random", 
                                   scaling_factor = "NONE", 
                                   ncells=100,
                                   nsamples = 20, 
                                   BPPARAM = BiocParallel::MulticoreParam(workers = 4), 
                                   run_parallel = TRUE)

simulation_kmer <- SimBu::simulate_bulk(data=dataset_kmers,
                                        scenario ="random",
                                        scaling_factor = "NONE",
                                        ncells=100,
                                        nsamples=20,
                                        BPPARAM =BiocParallel::MulticoreParam(workers=4),
                                        run_parallel = TRUE)



simulated_count_matrix <- as.matrix(SummarizedExperiment::assays(simulation$bulk)[["bulk_tpm"]]) # das hier ist dann die simulierte matrix, die du in ein deconvolution tool rein steckst)
simulated_kmer_matrix <- as.matrix(SummarizedExperiment::assays(simulation_kmer$bulk)[["bulk_tpm"]])

# run deconvolution (quantiseq method)
signature_matrix <- omnideconv::build_model(as.matrix(genesmat), genesindex$cell_type,
                        method = "dwls")
result <- omnideconv::deconvolute_dwls(bulk_gene_expression = simulated_count_matrix, 
                                       signature = signature_matrix)



sigmat_gene_momf <- omnideconv::build_model(bulk_gene_expression=simulated_count_matrix, 
                                              as.matrix(genesmat), genesindex$cell_type,
                                              method="momf")
res_gene_momf <- omnideconv::deconvolute(bulk_gene_expression=simulated_count_matrix,
                                         genesmat, 
                                         signature=sigmat_gene_momf, 
                                         method="momf")



sig_kmer_matrix <-omnideconv::build_model(bulk_gene_expression=simulated_kmer_matrix, 
                                          as.matrix(kmermat), kmerindex$cell_type,
                                          method="momf")
result_kmer <- omnideconv::deconvolute(bulk_gene_expression=simulated_kmer_matrix,
                                       kmermat, 
                                       signature=sig_kmer_matrix, 
                                       method="momf")




a <- melt(simulation$cell_fractions,variable.name = "cell_type", value.name = "simulated_fraction")
b <- melt(as.data.frame(result), variable.name="cell_type",value.name="deconv_fraction")
b <- b["deconv_fraction"]
combined_frac <- cbind(a,b)
ggplot(combined_frac,aes(x=simulated_fraction, y=deconv_fraction)) + 
  geom_point(aes(color=cell_type))+ coord_fixed(ratio=1)+ geom_abline() #+ facet_wrap(~cell_type)

kmertru <-melt(simulation_kmer$cell_fractions,variable.name = "cell_type", value.name = "simulated_fraction")
kmerpred <- melt(as.data.frame(result_kmer), variable.name="cell_type",value.name="deconv_fraction")
kmerpred <- kmerpred["deconv_fraction"]
kmer_combined_Frac <- cbind(kmertru,kmerpred)
ggplot(kmer_combined_Frac, aes(x=simulated_fraction, y=deconv_fraction,color=cell_type))+
  geom_point() + coord_fixed(ratio=1) + geom_abline()+ geom_smooth(method="lm",se = FALSE) +ggtitle("k-mer Deconvolution - MOMF")

ggscatter(kmer_combined_Frac, x = "simulated_fraction", y = "deconv_fraction", 
          add = "reg.line", conf.int = TRUE, 
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "Simulated Fraction", ylab = "Deconvolution Fraction") + facet_wrap(~cell_type)

gmomftru <- melt(simulation$cell_fractions,variable.name = "cell_type", value.name = "simulated_fraction")
gmomfpred <- melt(as.data.frame(res_gene_momf), variable.name="cell_type", value.name="deconv_fraction")
gmomfpred <- gmomfpred["deconv_fraction"]
gmomf_combined_frac <- cbind(gmomftru,gmomfpred)
ggplot(gmomf_combined_frac, aes(x=simulated_fraction, y=deconv_fraction,color=cell_type))+
  geom_point() + coord_fixed(ratio=1) + geom_abline() + geom_smooth(method="lm",se = FALSE) +ggtitle("Gene Expression Deconvolution - MOMF")


library("ggpubr")
ggscatter(gmomf_combined_frac, x = "simulated_fraction", y = "deconv_fraction", 
          add = "reg.line", conf.int = TRUE, 
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "Simulated Fraction", ylab = "Deconvolution Fraction") + facet_wrap(~cell_type)

#facet_wrap(cell_type~method, scales="free_y", ncol = 2) + 

