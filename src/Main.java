
import htsjdk.samtools.*;
import org.apache.commons.cli.*;

import java.io.*;
import java.util.*;


public class Main {

    public static void main(String[] args) throws IOException {
        Options options = new Options();

        Option bam = new Option("bam", "bam", true, "filepath to bam file");
        bam.setRequired(true);
        options.addOption(bam);

        Option barcodes = new Option("b", "barcodes", true, "filepath to barcodes");
        barcodes.setRequired(true);
        options.addOption(barcodes);

        Option annotations = new Option("a", "annotations", true, "path to annotations csv");
        annotations.setRequired(true);
        options.addOption(annotations);

        Option out = new Option("out", "out", true, "output directory");
        out.setRequired(true);
        options.addOption(out);

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

        String bamstr = cmd.getOptionValue("bam");
        String outfilepath = cmd.getOptionValue("o");
        String barcodefilepath = cmd.getOptionValue("b");
        String annotationfilepath = cmd.getOptionValue("a");

        int lastSlashIndex = bamstr.lastIndexOf('/');
        if (lastSlashIndex == -1) {
            lastSlashIndex = bamstr.lastIndexOf('\\');
        }
        String experimentID = bamstr.substring(lastSlashIndex + 1, bamstr.length() - 6);


        ArrayList<String> barcodeList = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(barcodefilepath))) {
            String line;
            while ((line = br.readLine()) != null) {
                barcodeList.add(line);
            }
        }
        HashMap<String, Integer> discardedBarcodes = new HashMap<>();

        HashMap<String, DropletAnnotation> annotation = new HashMap<>();
        try (BufferedReader br = new BufferedReader(new FileReader(annotationfilepath))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.startsWith("cell") || !line.startsWith(experimentID)) {
                    continue;
                }
                String[] con = line.split(",");
                String annotBarcode = con[0].substring(con[0].length() - 16);
                String testBarcode = annotBarcode + "-1";
                if (barcodeList.contains(testBarcode)) {
                    DropletAnnotation current = new DropletAnnotation(annotBarcode, con[0], con[1], con[2], con[3], con[4], con[5], con[6], con[7], con[17]);
                    annotation.put(annotBarcode, current);
                } else {
                    System.out.println(annotBarcode);
                }
            }
        }

        long barcodeMismatch = 0;
        long numOfReads = 0;
        long numOfSupposedCorrect = 0;
        long numOfDiscardedBarcodes = 0;
        SamReader samReader = SamReaderFactory.makeDefault().validationStringency(ValidationStringency.SILENT).open(new File(bamstr));
        Iterator<SAMRecord> it = samReader.iterator();
        while (it.hasNext()) {
            SAMRecord sr = it.next();
            numOfReads++;
            List<SAMRecord.SAMTagAndValue> attributes = sr.getAttributes();
            if (attributes.size() == 13) {
                continue;
            }
            //String read = sr.getReadString();
            //String SAMString = sr.getSAMString();
            String barcodeCB = attributes.get(0).value.toString();
            String barcode = barcodeCB.substring(0, barcodeCB.length() - 2);
            if (attributes.size() == 14) {
                String other = attributes.get(8).value.toString();
                if (!barcode.equals(other)) {
                    barcodeMismatch++;
                    if (other.length() != 16) {
                        System.out.println("validatedBC: "+barcode + " | researcherBC: " + other);
                        continue;
                    }
                }
            }
            if (!barcodeList.contains(barcodeCB)) {
                if (discardedBarcodes.containsKey(barcodeCB)) {
                    discardedBarcodes.put(barcodeCB, discardedBarcodes.get(barcodeCB) + 1);
                    numOfDiscardedBarcodes++;
                } else {
                    discardedBarcodes.put(barcodeCB, 0);
                }
            } else {
                numOfSupposedCorrect++;
                //TODO: create a FASTA for each cell type
            }

        }
        System.out.println("total number of reads: " + numOfReads);
        System.out.println("number of supposedly correctly identifiable reads: " + numOfSupposedCorrect);
        System.out.println("number of discarded barcodes: " + numOfDiscardedBarcodes);
        System.out.println("barcode mismatches: " + barcodeMismatch);

    }
}
