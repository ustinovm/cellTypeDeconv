import org.apache.commons.cli.*;

import java.io.*;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.text.DecimalFormat;
import java.time.Duration;
import java.util.zip.GZIPInputStream;
import java.util.*;
import java.time.LocalDateTime;

public class Main {

    public static void main(String[] args) {
        Options options = new Options();

        Option fasta = new Option("f", "fasta", true, "filepath to fasta file. required ending: .bam.1");
        fasta.setRequired(true);
        options.addOption(fasta);

        Option kmers = new Option("k", "kmer", true, "filepath to kmer count file.tsv");
        kmers.setRequired(true);
        options.addOption(kmers);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;


        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("utility-name", options);
            System.exit(1);
        }

        String fastastr = cmd.getOptionValue("f");
        String kmerstr = cmd.getOptionValue("k");

        LocalDateTime startTime = LocalDateTime.now();

        ArrayList<KMer> kmerList = new ArrayList<>();
        try (BufferedReader TSVReader = new BufferedReader(new FileReader(kmerstr))) {
            String line;
            while ((line = TSVReader.readLine()) != null) {
                String kmerstring = line.split("\t")[0];
                long occ = Long.parseLong(line.split("\t")[1]);
                KMer k = new KMer(kmerstring, occ);
                kmerList.add(k);
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(-1);
        }

        System.out.println("K-Mer List has been read");

        HashSet<String> cellList = new HashSet<>();
        try {
            FileInputStream fin = new FileInputStream(fastastr);
            GZIPInputStream gzis = new GZIPInputStream(fin);
            InputStreamReader xover = new InputStreamReader(gzis);
            BufferedReader is = new BufferedReader(xover);
            String line;
            String barcode = null;
            while ((line = is.readLine()) != null) {
                if (line.startsWith(">")) {
                    barcode = line.substring(line.indexOf("|") - 16, line.indexOf("|"));
                    cellList.add(barcode);
                } else {
                    for (KMer kmer : kmerList) {
                        if (line.contains(kmer.kmerString)) {
                            kmer.addFoundInCells(barcode);
                            System.out.println("cell: " + barcode + " \t k-mer: " + kmer.kmerString);
                        }
                    }
                }
            }
            System.out.println("Number of total Cells: " + cellList.size() + "\nThis took: " + Duration.between(startTime, LocalDateTime.now()));

            FileWriter fw = new FileWriter(kmerstr.substring(0, kmerstr.length() - 3) + "_kmerpercentage.tsv");
            DecimalFormat df = new DecimalFormat("#.##");
            BufferedWriter bw = new BufferedWriter(fw);
            bw.write("#total number of cells:\t" + cellList.size() + "\n");
            for (KMer kmer : kmerList) {
                double d = (double) kmer.foundInCells.size() / cellList.size();
                bw.write(kmer.kmerString + "\t" + kmer.occurence + "\t" + df.format(d) + "\n");
            }

        } catch (IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }

    }
}
