import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;

public final class HorseRaceAnimationTest {
    private HorseRaceAnimationTest() { }

    public static void main(String[] args) throws Exception {
        assertEquals(200L, HorseRace.animationFrameDurationMillis(118.0),
                "slow horse frame duration");
        assertEquals(85L, HorseRace.animationFrameDurationMillis(228.0),
                "fast horse frame duration");
        assertTrue(HorseRace.animationFrameDurationMillis(180.0)
                        < HorseRace.animationFrameDurationMillis(150.0),
                "higher speed must shorten frame duration");
        assertEquals(0, HorseRace.animationFrame(150.0, 400L, false),
                "stationary horse uses neutral frame");
        assertTrue(HorseRace.animationFrame(118.0, 200L, true)
                        != HorseRace.animationFrame(228.0, 200L, true),
                "slow and fast horses can show different poses");
        assertDoubleEquals(150.0, HorseRace.currentSpeed(150.0, false, false),
                "normal speed");
        assertDoubleEquals(180.0, HorseRace.currentSpeed(150.0, true, false),
                "boosted speed");
        assertDoubleEquals(0.0, HorseRace.currentSpeed(150.0, true, true),
                "finished speed");

        BufferedImage slowHorse = renderHorse(118.0, false, 200L);
        BufferedImage fastHorse = renderHorse(228.0, false, 200L);
        assertTrue(pixelDifference(slowHorse, fastHorse) > 20,
                "slow and fast speeds must render different horse poses");

        BufferedImage stoppedAtStart = renderHorse(0.0, true, 0L);
        BufferedImage stoppedLater = renderHorse(0.0, true, 500L);
        assertEquals(0, pixelDifference(stoppedAtStart, stoppedLater),
                "finished horse image must remain still");
        System.out.println("HorseRaceAnimationTest: PASS");
    }

    private static BufferedImage renderHorse(double speed, boolean finished,
                                             long animationTimeMillis)
            throws Exception {
        Class<?> snapshotClass = Class.forName("HorseRace$HorseSnapshot");
        Constructor<?> snapshotConstructor = snapshotClass.getDeclaredConstructor(
                int.class, double.class, int.class, int.class,
                double.class, boolean.class, boolean.class);
        snapshotConstructor.setAccessible(true);
        Object snapshot = snapshotConstructor.newInstance(
                1, 0.5, 2, 2, speed, false, finished);

        Class<?> panelClass = Class.forName("HorseRace$RacePanel");
        Constructor<?> panelConstructor = panelClass.getDeclaredConstructor();
        panelConstructor.setAccessible(true);
        Object panel = panelConstructor.newInstance();
        Method drawHorse = panelClass.getDeclaredMethod(
                "drawHorse", Graphics2D.class, int.class, int.class,
                int.class, int.class, snapshotClass, long.class);
        drawHorse.setAccessible(true);

        BufferedImage image = new BufferedImage(
                80, 60, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics = image.createGraphics();
        try {
            drawHorse.invoke(panel, graphics, 5, 28, 52, 0,
                    snapshot, animationTimeMillis);
        } finally {
            graphics.dispose();
        }
        return image;
    }

    private static int pixelDifference(BufferedImage first,
                                       BufferedImage second) {
        int difference = 0;
        for (int y = 0; y < first.getHeight(); y++) {
            for (int x = 0; x < first.getWidth(); x++) {
                if (first.getRGB(x, y) != second.getRGB(x, y)) {
                    difference++;
                }
            }
        }
        return difference;
    }

    private static void assertEquals(long expected, long actual, String message) {
        if (expected != actual) {
            throw new AssertionError(message + ": expected "
                    + expected + ", got " + actual);
        }
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static void assertDoubleEquals(double expected, double actual,
                                           String message) {
        if (Math.abs(expected - actual) > 0.000001) {
            throw new AssertionError(message + ": expected "
                    + expected + ", got " + actual);
        }
    }
}
