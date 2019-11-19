package Lab2;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class por3 {
	static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";  
	static final String DB_URL = "jdbc:mysql://localhost:3306/student";
	static final String USER = "root";
	static final String PASS = "student";
	   

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Connection conn = null;
		   Statement stmt = null;
		   try{
		      Class.forName(JDBC_DRIVER);
		      System.out.println("Connecting to database...");
		      conn = DriverManager.getConnection(DB_URL,USER,PASS);
		      stmt = conn.createStatement();
		      String sql = "create table stu " +
	                   "(id integer not NULL, " +
	                   " firstName varchar(50), " + 
	                   " primary key ( id ))";
		      stmt.executeUpdate(sql);
    		   System.out.println("created table");
			    
			  String sql1 = "insert into stu " + 
			    		" values (001, 'harsha')";
			  stmt.executeUpdate(sql1);
   		   System.out.println("inserted into table");

		      stmt.close();
		      conn.close();
			}
			catch(Exception e){ 
				System.out.println(e);
			}  
	}

}
