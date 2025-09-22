import java.awt.*;
class gl
{
gl()
{
Frame f=new Frame();
GridLayout l =new GridLayout(3,3);
f.setSize(500,500);
f.setVisible(true);
f.setLayout(l);
f.setTitle("Grid layout");
Button bl=new Button("bl");
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
gl m=new gl();
}
}