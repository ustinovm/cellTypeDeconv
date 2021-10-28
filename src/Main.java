
import htsjdk.samtools.*;
import org.apache.commons.cli.*;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.*;


public class Main {

    public static void main(String[] args) throws IOException {
        Options options = new Options();

        Option bam = new Option("bam", "bam", true, "filepath to bam file. required ending: .bam.1");
        bam.setRequired(true);
        options.addOption(bam);

        Option barcodes = new Option("b", "barcodes", true, "filepath to barcodes");
        barcodes.setRequired(true);
        options.addOption(barcodes);

        Option annotations = new Option("a", "annotations", true, "path to annotations csv");
        annotations.setRequired(true);
        options.addOption(annotations);

        Option out = new Option("o", "out", true, "output directory");
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

        int lastSlashIndex = bamstr.lastIndexOf(File.separator);

        String experimentID = bamstr.substring(lastSlashIndex + 1, bamstr.length() - 6);

        LocalDateTime startTime = LocalDateTime.now();


        ArrayList<String> barcodeList = barcodeRead(barcodefilepath);
        HashMap<String, Integer> discardedBarcodes = new HashMap<>();

        Set<String> filenames = new HashSet<>();

        HashMap<String, DropletAnnotation> annotation = annotationRead(annotationfilepath, experimentID, barcodeList);


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
            String read = sr.getReadString();
            //String SAMString = sr.getSAMString();
            String barcodeCB = attributes.get(0).value.toString();
            String barcode = barcodeCB.substring(0, barcodeCB.length() - 2);
            if (attributes.size() == 14) {
                String other = attributes.get(8).value.toString();
                if (!barcode.equals(other)) {
                    barcodeMismatch++;
                    if (other.length() != 16) {
                        //System.out.println("validatedBC: " + barcode + " | researcherBC: " + other);
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
                if (annotation.get(barcode) != null) {
                    //DropletAnnotation disone = annotation.get(barcode); //debugging
                    String name = annotation.get(barcode).cell_ontology_class;
                    if (name.equals("")) {
                        name = "unknown";
                    }
                    /*if(attributes.get(4).value.toString().contains("Missing")){ //seems like this is ok?
                        continue;
                    }*/
                    numOfSupposedCorrect++;
                    if(numOfSupposedCorrect%1000000 ==0){
                        System.out.println("the " + numOfSupposedCorrect +" th read will be written to a fasta now.");
                        System.out.println(Duration.between(startTime,LocalDateTime.now()));
                    }
                    name = name.replace(" ", "_");
                    name = experimentID + "_" + name;
                    name = name + "_" + annotation.get(barcode).cell_ontology_ID.replace(":", "_") + ".fasta";
                    writeFile(outfilepath, name, read, annotation.get(barcode));
                    filenames.add(name);
                }

            }

        }
        LocalDateTime endtime = LocalDateTime.now();
        Duration duration = Duration.between(startTime, endtime);

        File report = new File(outfilepath + File.separator + "report.txt");
        try {
            FileWriter fw = new FileWriter(report);
            BufferedWriter bw = new BufferedWriter(fw);
            bw.write("the run took " + duration.toMinutes() + " \n");
            bw.write("total number of reads: " + numOfReads + "\n");
            bw.write("number of supposedly correctly identifiable reads: " + numOfSupposedCorrect + "\n");
            bw.write("number of discarded barcodes: " + numOfDiscardedBarcodes + "\n");
            bw.write("barcode mismatches: " + barcodeMismatch);
            bw.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }

        System.out.println("the run took " + duration.toMinutes() + " \n");
        System.out.println("total number of reads: " + numOfReads + "\n");
        System.out.println("number of supposedly correctly identifiable reads: " + numOfSupposedCorrect + "\n");
        System.out.println("number of discarded barcodes: " + numOfDiscardedBarcodes + "\n");
        System.out.println("barcode mismatches: " + barcodeMismatch);

    }

    public static ArrayList<String> barcodeRead(String barcodefilepath) throws IOException {
        ArrayList<String> barcodeList = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(barcodefilepath))) {
            String line;
            while ((line = br.readLine()) != null) {
                barcodeList.add(line);
            }
        }
        return barcodeList;
    }

    public static HashMap<String, DropletAnnotation> annotationRead(String annotationfilepath, String experimentID, ArrayList<String> barcodeList) throws IOException {
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
        return annotation;
    }

    public static void writeFile(String outpath, String fileName, String read, DropletAnnotation annot) throws IOException {
        File directory = new File(outpath);
        if (!directory.exists()) {
            Files.createDirectory(Paths.get(outpath));
            // If you require it to make the entire directory path including parents,
            // use directory.mkdirs(); here instead.
        }
        File file = new File(outpath + File.separator + fileName);
        try {
            FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
            BufferedWriter bw = new BufferedWriter(fw);
            String header = ">" + annot.channel + "_" + annot.barcode + "|" + annot.cell_ontology_class + "|" + annot.cell_ontology_ID;
            bw.write(header + "\n");
            bw.write(read + "\n");
            bw.close();
            fw.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }
    }

}
