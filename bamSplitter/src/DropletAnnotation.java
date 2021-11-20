public class DropletAnnotation {
    String barcode;
    String originalCellname;
    String cell_ontology_class;
    String cell_ontology_ID;
    String channel;
    String cluster_ids;
    String free_annotation;
    String mouse_id;
    String mouse_sex;
    String tissue;

    public DropletAnnotation(String barcode, String originalCellname, String cell_ontology_class, String cell_ontology_ID, String channel, String cluster_ids, String free_annotation, String mouse_id, String mouse_sex, String tissue) {
        this.barcode = barcode;
        this.originalCellname = originalCellname;
        this.cell_ontology_class = originalCellname;
        this.cell_ontology_class = cell_ontology_class;
        this.cell_ontology_ID = cell_ontology_ID;
        this.channel = channel;
        this.cluster_ids = cluster_ids;
        this.free_annotation = free_annotation;
        this.mouse_id = mouse_id;
        this.mouse_sex = mouse_sex;
        this.tissue = tissue;
    }

    public String getBarcode() {
        return barcode;
    }

    public void setBarcode(String barcode) {
        this.barcode = barcode;
    }

    public String getOriginalCellname() {
        return originalCellname;
    }

    public void setOriginalCellname(String originalCellname) {
        this.originalCellname = originalCellname;
    }

    public String getCell_ontology_class() {
        return cell_ontology_class;
    }

    public void setCell_ontology_class(String cell_ontology_class) {
        this.cell_ontology_class = cell_ontology_class;
    }

    public String getCell_ontology_ID() {
        return cell_ontology_ID;
    }

    public void setCell_ontology_ID(String cell_ontology_ID) {
        this.cell_ontology_ID = cell_ontology_ID;
    }

    public String getChannel() {
        return channel;
    }

    public void setChannel(String channel) {
        this.channel = channel;
    }

    public String getCluster_ids() {
        return cluster_ids;
    }

    public void setCluster_ids(String cluster_ids) {
        this.cluster_ids = cluster_ids;
    }

    public String getFree_annotation() {
        return free_annotation;
    }

    public void setFree_annotation(String free_annotation) {
        this.free_annotation = free_annotation;
    }

    public String getMouse_id() {
        return mouse_id;
    }

    public void setMouse_id(String mouse_id) {
        this.mouse_id = mouse_id;
    }

    public String getMouse_sex() {
        return mouse_sex;
    }

    public void setMouse_sex(String mouse_sex) {
        this.mouse_sex = mouse_sex;
    }

    public String getTissue() {
        return tissue;
    }

    public void setTissue(String tissue) {
        this.tissue = tissue;
    }
}
