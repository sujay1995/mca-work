<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>session check</title>
</head>
<body>
<% if(request.getSession(false) == null){
    response.sendRedirect("login.jsp");
}
String a=session.getAttribute("username").toString();
if(a.equals("admin")){
	response.sendRedirect("admin.jsp");
}
else{
	response.sendRedirect("user.jsp");
}
%>


</body>
</html>