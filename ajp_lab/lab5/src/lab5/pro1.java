package lab5;

import java.io.IOException;

import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class pro1
 */
//@WebServlet("/pro1")
public class pro1 extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public pro1() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
	      response.setContentType("text/html; charset=UTF-8");
	      PrintWriter out = response.getWriter();
	      out.println("<!DOCTYPE html>");
	      out.println("<html><head>");
	      out.println("<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>");
	      out.println("<title>login details</title></head>");
	      out.println("<body><h1>login details</h1>");
	      String usrname =  request.getParameter("uname");
	      String password = request.getParameter("psw");
	      out.println("<h2>your username = "+ usrname +"</h2>");
	      out.println("<h2>your password = "+ password +"</h2></body></html>");

	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
