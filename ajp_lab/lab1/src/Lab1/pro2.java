package Lab1; 

public class pro2 {
	
	public static void main(String[] args) {
		double principle = 10000, rate = 10.25, time = 5; 
        double CI = principle * (Math.pow((1 + rate / 100), time)); 
        System.out.println("Compound Interest is "+ CI); 
	}
}
