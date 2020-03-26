package Lab1;

import java.util.Scanner;

public class pro6 {

	private static Scanner input;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int a, b, result;
		 
		  input = new Scanner(System.in);
		  System.out.println("Input two integers");
		 
		  a = input.nextInt();
		  b = input.nextInt();
		 
		  try {
		    result  = a / b;
		    System.out.println("Result = " + result);
		  }
		 
		  catch (ArithmeticException e) {
		    System.out.println("Exception caught: Division by zero.");
		  }

	}

}
