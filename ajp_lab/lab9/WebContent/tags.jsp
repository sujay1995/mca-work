    <%@ page language="java" contentType="text/html; charset=ISO-8859-1"
        pageEncoding="ISO-8859-1"%>
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
    <title>types of tags</title>
    </head>
    <body>
    <%-- this is comment tag --%>
    <%-- declaration tag --%>
    <%! int count =10; %>
    <% out.println("the count is = " +count); %></br>
    <%-- JSP Scriptlet tag --%>
    <% int num1=10;
       int num2=40;
       int num3 = num1+num2;
       out.println("Scriplet Number is " +num3);
    %><br/>
    <% out.println("The expression number is "); %>
    <%! int num1=10; int num2=10; int num3 = 20; %>
    <%-- expression tag  --%>
    <%= num1*num2+num3 %>
    </body>
    </html>