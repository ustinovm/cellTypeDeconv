import java.util.HashSet;

public class KMer {
    String kmerString;
    Long occurence;
    HashSet<String> foundInCells;

    public KMer(String kmerString, Long occurence){
        this.kmerString=kmerString;
        this.occurence=occurence;
        this.foundInCells = new HashSet<>();
    }

    public String getKmerString() {
        return kmerString;
    }

    public void setKmerString(String kmerString) {
        this.kmerString = kmerString;
    }

    public Long getOccurence() {
        return occurence;
    }

    public void setOccurence(Long occurence) {
        this.occurence = occurence;
    }

    public HashSet<String> getFoundInCells() {
        return foundInCells;
    }

    public void addFoundInCells(String cell) {
        this.foundInCells.add(cell);
    }
}
