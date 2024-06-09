import java.util.Scanner;

public class TextAdventureGame {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Welcome to the Text Adventure Game!");

        System.out.println("What's your name?");
        String playerName = scanner.nextLine();
        System.out.println("Hello, " + playerName + "! Let's begin.");

        exploreForest(playerName, scanner);

        System.out.println("Congratulations, " + playerName + "! You've completed the Text Adventure Game!");
    }

    public static void exploreForest(String playerName, Scanner scanner) {
        System.out.println("You wake up in a mysterious forest. You see a path to the left and a cave to the right. Which way do you go? (left/right)");
        String direction = scanner.nextLine();

        if (direction.equalsIgnoreCase("left")) {
            encounterElf(playerName, scanner);
        } else if (direction.equalsIgnoreCase("right")) {
            exploreCave(playerName, scanner);
        } else {
            System.out.println("Invalid choice. Please choose 'left' or 'right'.");
            exploreForest(playerName, scanner);
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