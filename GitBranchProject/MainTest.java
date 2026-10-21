public class MainTest {
    public static void main(String[] args) {
        if (Main.add(2, 3) != 5) {
            throw new RuntimeException("Test failed");
        }

        System.out.println("All tests passed");
    }
}