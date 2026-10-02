package horserace;

import javax.swing.SwingUtilities;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.BooleanSupplier;

/** Generates the three assignment screenshots from the real Swing window. */
public final class ScreenshotGenerator {
    private ScreenshotGenerator() { }

    public static void main(String[] args) throws Exception {
        final Path outputDirectory = args.length == 0
                ? Paths.get("screenshots").toAbsolutePath()
                : Paths.get(args[0]).toAbsolutePath();
        final int horseCount = args.length < 2 ? 5 : Integer.parseInt(args[1]);
        final AtomicReference<RaceFrame> frameReference = new AtomicReference<RaceFrame>();

        SwingUtilities.invokeAndWait(new Runnable() {
            @Override public void run() {
                RaceFrame frame = new RaceFrame();
                frame.setVisible(true);
                frameReference.set(frame);
            }
        });

        final RaceFrame frame = frameReference.get();
        try {
            SwingUtilities.invokeAndWait(new Runnable() {
                @Override public void run() {
                    frame.setHorseCountForCapture(horseCount);
                }
            });
            capture(frame, outputDirectory.resolve("01-ready.png"));
            SwingUtilities.invokeAndWait(new Runnable() {
                @Override public void run() {
                    frame.startRaceForCapture(horseCount);
                }
            });

            waitUntil(new BooleanSupplier() {
                @Override public boolean getAsBoolean() {
                    return frame.getFinishedCountForCapture() > 0
                            && frame.isRaceRunningForCapture()
                            && frame.isBoostVisibleForCapture();
                }
            }, 15000L, "Timed out waiting for an in-progress race");
            flushEdt();
            capture(frame, outputDirectory.resolve("02-racing-and-boosting.png"));

            waitUntil(new BooleanSupplier() {
                @Override public boolean getAsBoolean() {
                    return frame.isRaceCompleteVisibleForCapture(horseCount);
                }
            }, 15000L, "Timed out waiting for the completed race");
            flushEdt();
            capture(frame, outputDirectory.resolve("03-complete-ranking.png"));
            System.out.println("Created screenshots in " + outputDirectory);
        } finally {
            SwingUtilities.invokeAndWait(new Runnable() {
                @Override public void run() {
                    frame.shutdownForCapture();
                }
            });
        }
    }

    private static void capture(final RaceFrame frame, final Path target) throws Exception {
        SwingUtilities.invokeAndWait(new Runnable() {
            @Override public void run() {
                try {
                    frame.captureContent(target);
                } catch (Exception failure) {
                    throw new RuntimeException(failure);
                }
            }
        });
    }

    private static void flushEdt() throws Exception {
        SwingUtilities.invokeAndWait(new Runnable() {
            @Override public void run() { }
        });
    }

    private static void waitUntil(BooleanSupplier condition, long timeoutMillis, String message)
            throws InterruptedException {
        long deadline = System.currentTimeMillis() + timeoutMillis;
        while (!condition.getAsBoolean() && System.currentTimeMillis() < deadline) {
            Thread.sleep(20L);
        }
        if (!condition.getAsBoolean()) {
            throw new IllegalStateException(message);
        }
    }
}
