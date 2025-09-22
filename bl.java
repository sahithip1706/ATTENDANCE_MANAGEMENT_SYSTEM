import java.awt.*;
class bl
{
bl()
{
Frame f=new Frame();
BorderLayout l = new BorderLayout();
f.setSize(500,500);
f.setVisible(true);
f.setLayout(l);
f.setTitle("Border layout");
Button b1=new Button("Bl");
Button b2=new Button("B2");
Button b3=new Button("B3");
Button b4=new Button("B4");
Button b5=new Button("B5");
f.add(b1,l.NORTH);
f.add(b2,l.SOUTH);
f.add(b3,l.WEST);
f.add(b4,l.EAST);
f.add(b5,l.CENTER);
}
public static void main(String args[])
{
bl m=new bl();
}}