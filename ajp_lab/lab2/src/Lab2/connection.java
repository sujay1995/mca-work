package Lab2;
import java.sql.*; 
public class connection {

	   static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";  
	   static final String DB_URL = "jdbc:mysql://localhost:3306/student";
	   static final String USER = "root";
	   static final String PASS = "student";
	   
	   public static void main(String[] args) {
	   Connection conn = null;
	   Statement stmt = null;
	   try{
	      Class.forName(JDBC_DRIVER);
	      System.out.println("Connecting to database...");
	      conn = DriverManager.getConnection(DB_URL,USER,PASS);
	      stmt = conn.createStatement();
	      String sql;
	      sql = " DELETE FROM EMPLOYEE WHERE EMPLOYEEID=002 ";
	      stmt.executeUpdate(sql);
		  System.out.println("the employee id 002 as been sucessfully deleted");
	      stmt.close();
	      conn.close();
		}
		catch(Exception e){ 
			System.out.println(e);
		}  
	}
  
}
