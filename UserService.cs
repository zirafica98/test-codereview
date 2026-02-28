using System;
using System.Data.SqlClient;

public class UserService
{
    private string connectionString = "Server=localhost;Database=TestDB;User Id=sa;Password=password123;";

    // SQL Injection vulnerability - direktno spajanje korisničkog inputa u SQL upit
    public User GetUserByUsername(string username)
    {
        string query = "SELECT * FROM Users WHERE Username = '" + username + "'";
        
        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            connection.Open();
            SqlCommand command = new SqlCommand(query, connection);
            SqlDataReader reader = command.ExecuteReader();
            
            if (reader.Read())
            {
                return new User
                {
                    Id = (int)reader["Id"],
                    Username = reader["Username"].ToString(),
                    Password = reader["Password"].ToString() // Loša praksa - vraćanje lozinke
                };
            }
        }
        return null;
    }

    // Još jedna SQL injection greška
    public void DeleteUser(string userId)
    {
        string sql = "DELETE FROM Users WHERE Id = " + userId;
        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            conn.Open();
            SqlCommand cmd = new SqlCommand(sql, conn);
            cmd.ExecuteNonQuery(); // Nema provere da li je korisnik autorizovan
        }
    }

    // Hardkodovani credentials
    public bool Authenticate(string username, string password)
    {
        if (username == "admin" && password == "admin1234")
        {
            return true; // Hardkodovani admin credentials
        }
        return false;
    }

    // Command injection mogućnost
    public void ExecuteSystemCommand(string command)
    {
        System.Diagnostics.Process.Start("cmd.exe", "/c " + command); // Command injection
    }
}

public class User
{
    public int Id { get; set; }
    public string Username { get; set; }
    public string Password { get; set; }
}
