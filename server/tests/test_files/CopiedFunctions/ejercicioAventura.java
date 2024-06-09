import java.util.Scanner;

public class SimpleCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Welcome to the Simple Calculator!");

        double num1, num2;
        System.out.print("Enter the first number: ");
        num1 = scanner.nextDouble();
        System.out.print("Enter the second number: ");
        num2 = scanner.nextDouble();

        System.out.println("Select operation: ");
        System.out.println("1. Addition");
        System.out.println("2. Subtraction");
        System.out.println("3. Multiplication");
        System.out.println("4. Division");
        System.out.print("Enter choice (1-4): ");
        int choice = scanner.nextInt();

        double result;
        switch (choice) {
            case 1:
                result = num1 + num2;
                System.out.println("Result: " + result);
                break;
            case 2:
                result = num1 - num2;
                System.out.println("Result: " + result);
                break;
            case 3:
                result = num1 * num2;
                System.out.println("Result: " + result);
                break;
            case 4:
                if (num2 == 0) {
                    System.out.println("Error! Division by zero.");
                } else {
                    result = num1 / num2;
                    System.out.println("Result: " + result);
                }
                break;
            default:
                System.out.println("Invalid choice.");
        }
    }
	public static void encounterElf(String playerName, Scanner scanner) {
        System.out.println("You follow the path and encounter a friendly elf. He gives you a magic potion. Do you drink it? (yes/no)");
        String drinkPotion = scanner.nextLine();
        if (drinkPotion.equalsIgnoreCase("yes")) {
            System.out.println("You drink the potion and feel a surge of energy!");
        } else {
            System.out.println("You decide not to drink the potion and continue your journey.");
        }
    }
        public static void exploreCave(String playerName, Scanner scanner) {
        System.out.println("You enter the cave and find a treasure chest. Do you open it? (yes/no)");
        String openChest = scanner.nextLine();
        if (openChest.equalsIgnoreCase("yes")) {
            System.out.println("You open the chest and find a shiny sword!");
        } else {
            System.out.println("You leave the treasure chest untouched and explore further.");
        }
    }
}