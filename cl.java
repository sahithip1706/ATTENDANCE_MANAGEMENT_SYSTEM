import java.awt.*;
import java.awt.event.*;
class cl implements ActionListener
{
CardLayout l=new CardLayout();
Frame f=new Frame();
cl()
{
f.setSize(500,500);
f.setVisible(true);
f.setLayout(l);
f.setTitle("Card layout");
Button b1=new Button("B2");
Button b2=new Button("LAY");
Button b3=new Button("OUT");
Button b4=new Button("b4");
f.add(b1);
f.add(b2);
f.add(b3);
f.add(b4);
}
public void actionPerformed(ActionEvent e)
{
l.next(f);
}
public static void main(String args[])
{
cl m=new cl();
}
}