package Lab1;
import java.util.Scanner;
public class pro3 {

	private static Scanner sc;

	public static void main(String[] args) {
        sc = new Scanner(System.in); 
        double[] mylist =  new double[10];
        double avg = 0.0,sum = 0.0;
        int num;
        System.out.println("how many numbers:");
        num = sc.nextInt();
        System.out.printf("enter %d numbers",num);
        for(int i = 0; i < num; i++) {
        	mylist[i] = sc.nextDouble();
        	sum += mylist[i];
        }
        avg = sum/num;
        System.out.printf("the average value is =  %.3f ", avg);
  
	}

}
