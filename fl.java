import java.awt.*; 
class fl
{
fl()
{
Frame f=new Frame();
FlowLayout l = new FlowLayout();
f.setSize(500,500);
f.setVisible(true);
f.setLayout(l);
f.setTitle("flow layout");
Button bl=new Button("b1");
Button b2=new Button("b2");
Button b3=new Button("b3");
Button b4=new Button("b4");
f.add(bl);
f.add(b2);
f.add(b3);
f.add(b4);
}
public static void main(String args[])
{
fl m = new fl();
}
}