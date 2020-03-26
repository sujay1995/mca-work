package Lab3;

import java.sql.*;

public class pro1 {
	static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
	static final String DB_URL = "jdbc:mysql://localhost:3306/student";
	static final String USER = "root";
	static final String PASS = "student";
	public static void main(String args[]) {
		Connection conn = null;
		Statement stmt = null;
		try {
		      Class.forName(JDBC_DRIVER);
		      System.out.println("Connecting to database...");
		      conn = DriverManager.getConnection(DB_URL,USER,PASS);
		      stmt = conn.createStatement();
		      String sql = "create table department " +
	                   "(depId varchar(20) not NULL, " +
	                   " depName varchar(50),depStrength integer ," + 
	                   " primary key (depId))";
		      stmt.executeUpdate(sql);
		      String sql1 = "insert into department values('D001','accounts',20)";
		      stmt.executeUpdate(sql1);      
		      String sql2 = "insert into department values('D002','hr',45)";
              stmt.executeUpdate(sql2);
              stmt.close();
		      conn.close();
		}
		catch(Exception e){ 
			System.out.println(e);
		}  
		
	}
}
