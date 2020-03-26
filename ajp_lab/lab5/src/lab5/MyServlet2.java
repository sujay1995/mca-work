package lab5;

import java.io.PrintWriter;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class MYServlet2
 */
//@WebServlet("/MYServlet2")
public class MyServlet2 extends HttpServlet {
	 /**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public void doGet(HttpServletRequest request, 
	    HttpServletResponse response){
	    try{
	       response.setContentType("text/html");
	       PrintWriter pwriter = response.getWriter();
	 
	       //Reading cookies
	       Cookie c[]=request.getCookies(); 
	       //Displaying User name value from cookie
	       pwriter.print("Name: "+c[1].getValue()); 
	       //Displaying user password value from cookie
	       pwriter.print("Password: "+c[2].getValue());
	 
	       pwriter.close();
	    }catch(Exception exp){
	       System.out.println(exp);
	     }
	  }
	}