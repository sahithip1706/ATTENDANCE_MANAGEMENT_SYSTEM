import java.awt.*;
class GridBagExample {
GridBagExample() {
Frame f = new Frame("GridBagLayout Example");
f.setSize(500, 500);
f.setLayout(new GridBagLayout());
GridBagConstraints gbc = new GridBagConstraints();
Button b1 = new Button("Button 1");
gbc.gridx = 0;
gbc.gridy = 0;
f.add(b1, gbc);
Button b2 = new Button("Button 2");
gbc.gridx = 1;
gbc.gridy = 0;
f.add(b2, gbc);
Button b3 = new Button("Button 3");
gbc.gridx = 0;
gbc.gridy = 1;
gbc.gridwidth = 2;
f.add(b3, gbc);
Button b4 = new Button("Button 4");
gbc.gridx = 1;
gbc.gridy = 2;
gbc.gridwidth = 1;
f.add(b4, gbc);
f.setVisible(true);
}
public static void main(String[] args) {new GridBagExample();
}
}