package Lab1;
import java.util.Scanner;

public class pro4 {

	private static Scanner sc;

	public static void main(String[] args) {
		int num1, num2;
        sc = new Scanner(System.in);
        System.out.print("Enter first number:");
        num1 = sc.nextInt();
        System.out.print("Enter second number:");
        num2 = sc.nextInt();
        num1 = num1 ^ num2;
        num2 = num1 ^ num2;
        num1 = num1 ^ num2;
        System.out.println("The First number after swapping:"+num1);
        System.out.println("The Second number after swapping:"+num2);

	}

}
