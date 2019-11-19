package lab7;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;


public class sessionTrack extends HttpServlet {
	private static final long serialVersionUID = 1L;

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		 try{  
			  
		        response.setContentType("text/html");  
		        PrintWriter out = response.getWriter();  
		          
		        HttpSession session=request.getSession(false);  
		        String n=(String)session.getAttribute("uname");  
		        String p=(String)session.getAttribute("password");
		        out.print("Hello "+n);  
		        out.print("ur password" +p);
		  
		        out.close();  
		  
		 }
		 catch(Exception e){
			 System.out.println(e);
		 }  
     }  
		
}

