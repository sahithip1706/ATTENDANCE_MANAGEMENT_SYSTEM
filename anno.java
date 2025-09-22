// 1. Create a custom annotation
@interface Info {
    String author();
    String date();
    String version() default "1.0";
}

// 2. Use the annotation and built-in annotations
public class anno {

    @Info(author = "Kavya", date = "2025-06-03")
    public void display() {
        System.out.println("Display method executed.");
    }

    @Deprecated  // Built-in annotation: marks the method as outdated
    public void oldMethod() {
        System.out.println("This method is deprecated.");
    }

    @Override
    public String toString() {
        return "AnnotationExample object";
    }

    public static void main(String[] args) {
        anno obj = new anno();
        obj.display();
        obj.oldMethod();
        System.out.println(obj.toString());
    }
}
