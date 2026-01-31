using System;
using MySql.Data.MySqlClient;

class Program
{
    static void Main()
    {
        string connectionString = "Server=localhost;Database=test;User ID=root;Password=root;";
        
        using (MySqlConnection conn = new MySqlConnection(connectionString))
        {
            try
            {
                conn.Open();
                Console.WriteLine("Connected to MySQL!");
                string query = "SELECT * FROM users;";
                // MySqlCommand cmd = new MySqlCommand(query, conn);

                // using (MySqlDataReader reader = cmd.ExecuteReader())
                // {
                //     while (reader.Read())
                //     {
                //         Console.WriteLine($"ID: {reader["id"]}, Name: {reader["name"]}");
                //     }
                // }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }
}
