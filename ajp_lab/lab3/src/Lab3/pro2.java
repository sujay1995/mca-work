package Lab3;
import java.sql.*;
public class pro2 {
	static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
	static final String DB_URL = "jdbc:mysql://localhost:3306/student";
	static final String USER = "root";
	static final String PASS = "student";
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try{
		      Class.forName(JDBC_DRIVER);
		      System.out.println("Connecting to database...");
		      Connection con = DriverManager.getConnection(DB_URL,USER,PASS);
		      CallableStatement sts = con.prepareCall("{call getEmpInfo()}");
		      ResultSet rs = sts.executeQuery();
		      while (rs.next()) {
	                 System.out.println(String.format(rs.getInt("EMPLOYEEID") +
	" " + rs.getString("EMPFNAME") + " " + rs.getString("EMPLNAME")));
	             }

		}
		catch(Exception e) {
			System.out.println(e);
		}
		

	}

}

