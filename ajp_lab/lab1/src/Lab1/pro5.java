package Lab1;

public class pro5 {

	public static void main(String[] args) {
		String str = "karthik";
		String str1 = "";
		for(int i = str.length() - 1;i>=0; i-- ) {
			str1 = str1 + str.charAt(i);
		}
		System.out.println("String before reversing: " + str);
		System.out.println("String after reversing: " + str1);
	}

}
