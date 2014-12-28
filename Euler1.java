//If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

//Find the sum of all the multiples of 3 or 5 below 1000.

//Congratulations, the answer you gave to problem 1 is correct.

//You are the 296926th person to have solved this problem.

public class Euler1 {

	public static void main(String[] args) {
   int sum = 0;
		for (int i=0;i<1000;i++) {
			if(i%3==0 || i%5==0){
				System.out.println(i);
				sum = sum + i;
			}//Enf of if
		} //End of for
	System.out.println(sum);
	} // End of Main
} // End of Class
