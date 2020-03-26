package Lab2;
import java.sql.*;  
public class pro1 {
		// TODO Auto-generated method stub
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
		      sql = "select * from EMPLOYEE";
		      ResultSet rs = stmt.executeQuery(sql);
		      
		      while(rs.next()){
		         
		         int id  = rs.getInt("EMPLOYEEID");
		         String first = rs.getString("EMPFNAME");
		         String last = rs.getString("EMPLNAME");
		         String dept = rs.getString("DEPT");
		         int salary = rs.getInt("SALARY");

		         
		         System.out.print("ID: " + id);
		         System.out.print(", First Name: " + first);
		         System.out.print(", Last Name: " + last);
		         System.out.print(", Department Name: " + dept);
		         System.out.print(", Salary: " + salary);
		         System.out.println("");
		      }
		      rs.close();
		      conn.close();
		    }
		    catch(Exception e){ 
				System.out.println(e);
			}  

	}

}
