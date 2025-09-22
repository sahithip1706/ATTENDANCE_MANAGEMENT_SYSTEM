import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class OnlineBookStoreGUI {
    private Store store = new Store();
    private Cart cart = new Cart();
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new OnlineBookStoreGUI().showUserSelection());
    }
    public void showUserSelection() {
        String[] options = {"Admin", "Customer"};
        int choice = JOptionPane.showOptionDialog(null, "Select user type", "User Login",
                JOptionPane.DEFAULT_OPTION, JOptionPane.INFORMATION_MESSAGE, null, options, options[0]);
        if (choice == 0) {
            showAdminPanel();
        } else if (choice == 1) {
            showCustomerPanel();
        }
    }
    private void showAdminPanel() {
        JFrame frame = new JFrame("Admin Panel");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 400);
        frame.setLayout(new GridLayout(5, 1, 10, 10));
        JTextArea outputArea = new JTextArea();
        outputArea.setEditable(false);
        JButton btnAddBook = new JButton("Add Book");
        JButton btnRemoveBook = new JButton("Remove Book by Title");
        JButton btnViewBooks = new JButton("View All Books");
        JButton btnBack = new JButton("Back");
        frame.add(btnAddBook);
        frame.add(btnRemoveBook);
        frame.add(btnViewBooks);
        frame.add(btnBack);
        frame.add(new JScrollPane(outputArea));
        btnAddBook.addActionListener(e -> {
            String title = JOptionPane.showInputDialog("Enter Title:");
            String author = JOptionPane.showInputDialog("Enter Author:");
            String priceStr = JOptionPane.showInputDialog("Enter Price:");
            try {
                double price = Double.parseDouble(priceStr);
                store.addBook(new Book(title, author, price));
                outputArea.setText("Book added successfully.");
            } catch (NumberFormatException ex) {
                outputArea.setText("Invalid price.");
            }
        });
        btnRemoveBook.addActionListener(e -> {
            String title = JOptionPane.showInputDialog("Enter Title to remove:");
            boolean removed = store.removeBookByTitle(title);
            outputArea.setText(removed ? "Book removed." : "Book not found.");
        });
        btnViewBooks.addActionListener(e -> {
            StringBuilder sb = new StringBuilder("All Books:\n");
            for (Book book : store.getBooks()) {
                sb.append(book).append("\n");
            }
            outputArea.setText(sb.toString());
        });
        btnBack.addActionListener(e -> {
            frame.dispose();
            showUserSelection();
        });
        frame.setVisible(true);
    }
    private void showCustomerPanel() {
        JFrame frame = new JFrame("Customer Panel");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(450, 500);
        frame.setLayout(new GridLayout(9, 1, 10, 10));
        JTextArea outputArea = new JTextArea();
        outputArea.setEditable(false);
        JButton btnListBooks = new JButton("List all books");
        JButton btnSearchTitle = new JButton("Search books by title");
        JButton btnSearchAuthor = new JButton("Search books by author");
        JButton btnAddToCart = new JButton("Add book to cart by title");
        JButton btnRemoveFromCart = new JButton("Remove book from cart by title");
        JButton btnViewCart = new JButton("View cart");
        JButton btnCheckout = new JButton("Checkout");
        JButton btnBack = new JButton("Back");
        frame.add(btnListBooks);
        frame.add(btnSearchTitle);
        frame.add(btnSearchAuthor);
        frame.add(btnAddToCart);
        frame.add(btnRemoveFromCart);
        frame.add(btnViewCart);
        frame.add(btnCheckout);
        frame.add(btnBack);
        frame.add(new JScrollPane(outputArea));
        btnListBooks.addActionListener(e -> {
            StringBuilder sb = new StringBuilder("Available books:\n");
            for (Book book : store.getBooks()) {
                sb.append(book).append("\n");
            }
            outputArea.setText(sb.toString());
        });
        btnSearchTitle.addActionListener(e -> {
            String title = JOptionPane.showInputDialog("Enter title keyword:");
            java.util.List<Book> result = store.searchByTitle(title);
            outputArea.setText(result.isEmpty() ? "No books found." : result.toString());
        });
        btnSearchAuthor.addActionListener(e -> {
            String author = JOptionPane.showInputDialog("Enter author keyword:");
            java.util.List<Book> result = store.searchByAuthor(author);
            outputArea.setText(result.isEmpty() ? "No books found." : result.toString());
        });
        btnAddToCart.addActionListener(e -> {
            String title = JOptionPane.showInputDialog("Enter book title to add to cart:");
            Book book = store.getBookByTitle(title);
            if (book != null) {
                cart.addBook(book);
                outputArea.setText("Book added to cart.");
            } else {
                outputArea.setText("Book not found.");
            }
        });
        btnRemoveFromCart.addActionListener(e -> {
            String title = JOptionPane.showInputDialog("Enter book title to remove from cart:");
            cart.removeBookByTitle(title);
            outputArea.setText("Book removed from cart.");
        });
        btnViewCart.addActionListener(e -> {
            Map<Book, Integer> items = cart.getCartItems();
            if (items.isEmpty()) {
                outputArea.setText("Your cart is empty.");
            } else {
                StringBuilder sb = new StringBuilder("Your Cart:\n");
                for (Book book : items.keySet()) {
                    sb.append(book).append(" | Qty: ").append(items.get(book)).append("\n");
                }
                sb.append("Total: $").append(String.format("%.2f", cart.getTotalPrice()));
                outputArea.setText(sb.toString());
            }
        });
        btnCheckout.addActionListener(e -> {
            if (cart.getCartItems().isEmpty()) {
                outputArea.setText("Cart is empty.");
            } else {
                outputArea.setText("Thank you for your purchase!");
                cart.checkout();
            }
        });
        btnBack.addActionListener(e -> {
            frame.dispose();
            showUserSelection();
        });

        frame.setVisible(true);
    }
}
// ========== Supporting Classes ==========
class Book {
    private String title, author;
    private double price;
    public Book(String title, String author, double price) {
        this.title = title; this.author = author; this.price = price;
    }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public double getPrice() { return price; }
    @Override
    public String toString() {
        return String.format("%s by %s - $%.2f", title, author, price);
    }
    @Override
    public boolean equals(Object obj) {
        return (obj instanceof Book) && ((Book) obj).getTitle().equalsIgnoreCase(this.title);
    }
    @Override
    public int hashCode() {
        return title.toLowerCase().hashCode();
    }
}
class Store {
    private java.util.List<Book> books = new ArrayList<>();
    public Store() {
        books.add(new Book("The Alchemist", "Paulo Coelho", 10.99));
        books.add(new Book("Clean Code", "Robert C. Martin", 25.50));
        books.add(new Book("Effective Java", "Joshua Bloch", 30.75));
    }
    public void addBook(Book book) {
        books.add(book);
    }
    public boolean removeBookByTitle(String title) {
        return books.removeIf(book -> book.getTitle().equalsIgnoreCase(title));
    }
    public java.util.List<Book> getBooks() {
        return books;
    }
    public java.util.List<Book> searchByTitle(String keyword) {
        java.util.List<Book> result = new ArrayList<>();
        for (Book book : books) {
            if (book.getTitle().toLowerCase().contains(keyword.toLowerCase())) result.add(book);
        }
        return result;
    }
    public java.util.List<Book> searchByAuthor(String keyword) {
        java.util.List<Book> result = new ArrayList<>();
        for (Book book : books) {
            if (book.getAuthor().toLowerCase().contains(keyword.toLowerCase())) result.add(book);
        }
        return result;
    }
    public Book getBookByTitle(String title) {
        for (Book book : books) {
            if (book.getTitle().equalsIgnoreCase(title)) return book;
        }
        return null;
    }
}
class Cart {
    private Map<Book, Integer> cartItems = new HashMap<>();
    public void addBook(Book book) {
        cartItems.put(book, cartItems.getOrDefault(book, 0) + 1);
    }
    public void removeBookByTitle(String title) {
        cartItems.entrySet().removeIf(entry -> entry.getKey().getTitle().equalsIgnoreCase(title));
    }
    public double getTotalPrice() {
        double total = 0;
        for (Map.Entry<Book, Integer> entry : cartItems.entrySet()) {
            total += entry.getKey().getPrice() * entry.getValue();
        }
        return total;
    }
    public void checkout() {
        cartItems.clear();
    }
    public Map<Book, Integer> getCartItems() {
        return cartItems;
    }
}