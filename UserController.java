import java.sql.*;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class UserController extends HttpServlet {
    
    private static final String DB_URL = "jdbc:mysql://localhost:3306/testdb";
    private static final String DB_USER = "root";
    private static final String DB_PASS = "root123"; // Hardkodovana lozinka u kodu
    
    // SQL Injection - direktna konkatenacija korisničkog inputa
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String userId = request.getParameter("id");
        String query = "SELECT * FROM users WHERE id = " + userId;
        
        try {
            Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(query); // SQL injection!
            
            while (rs.next()) {
                response.getWriter().println("User: " + rs.getString("username"));
                response.getWriter().println("Password: " + rs.getString("password")); // Loša praksa
            }
        } catch (SQLException e) {
            e.printStackTrace(); // Loša praksa - stack trace može otkriti informacije
        }
    }
    
    // Još jedna SQL injection greška
    public void updateUserEmail(String username, String email) {
        String sql = "UPDATE users SET email = '" + email + "' WHERE username = '" + username + "'";
        
        try {
            Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
            Statement stmt = conn.createStatement();
            stmt.executeUpdate(sql); // SQL injection!
        } catch (SQLException e) {
            // Ignoriše grešku - loša praksa
        }
    }
    
    // XSS vulnerability - direktan output korisničkog inputa
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String comment = request.getParameter("comment");
        response.getWriter().println("<div>" + comment + "</div>"); // XSS!
    }
    
    // Command injection
    public void executeCommand(String userInput) throws IOException {
        Runtime.getRuntime().exec("ping " + userInput); // Command injection!
    }
    
    // Hardkodovani secret key
    private static final String SECRET_KEY = "mySecretKey123"; // Hardkodovani secret
}
