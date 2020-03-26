package lab7;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Date;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

public class loginDetails extends HttpServlet {
	private static final long serialVersionUID = 1L;
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		try{  
			  
	        response.setContentType("text/html");  
	        PrintWriter out = response.getWriter();  
	          
	        String n=request.getParameter("uname");  
	        out.print("Welcome "+n);  
	        
	        String p=request.getParameter("psw");  
	        
	        HttpSession session=request.getSession(true);  
	        session.setAttribute("uname",n);
	        session.setAttribute("password",p);
	        Date createTime = new Date(session.getCreationTime());
	        Date lastAccessTime = new Date(session.getLastAccessedTime());
	        String title = "Welcome Back to my site";
	        Integer visitCount = new Integer(0);
	        String visitCountKey = new String("visitCount");
	        String userIDKey = new String("userID");
	        String userID = new String(n+1);
	        
	        

	  
	        out.print("<a href='/lab7/welcome'>visit</a>");  
	                  
	        out.close();  
	  
	    }
		catch(Exception e){
			System.out.println(e);
		}  
	}  
}
