package horserace;

import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicBoolean;
import javax.swing.SwingUtilities;

/** Pure-JDK tests. Run with: java -ea -cp out horserace.HorseRaceTest */
public final class HorseRaceTest {
    public static void main(String[] args) throws Exception {
        ensureAssertionsEnabled();
        testHorseCountValidation();
        testBoostConsumesStaminaAndAddsTwentyPercent();
        testConcurrentFinishCreatesOneCompleteRanking();
        testEveryHorseUsesADistinctThreadAndSpeed();
        testStopTerminatesWorkers();
        testUiDispatchRunsOnEventDispatchThread();
        System.out.println("PASS: 6 horse-race tests");
    }

    private static void ensureAssertionsEnabled() {
        boolean enabled = false;
        assert enabled = true;
        if (!enabled) {
            throw new IllegalStateException("Run tests with -ea");
        }
    }

    private static void testHorseCountValidation() {
        RaceController controller = new RaceController(new RecordingListener());
        expectIllegalArgument(new Runnable() {
            @Override public void run() { controller.startRace(1); }
        });
        expectIllegalArgument(new Runnable() {
            @Override public void run() { controller.startRace(11); }
        });
    }

    private static void testBoostConsumesStaminaAndAddsTwentyPercent() {
        RaceParameters parameters = new RaceParameters(1000.0, 10L, 1000L, 100, 200);
        Horse horse = new Horse(1, 100.0, 2, parameters, new NoOpHorseEvents());

        horse.enableBoostAt(0L);
        assert horse.snapshot().isBoosting();
        assert horse.snapshot().getStaminaRemaining() == 1;
        assert Math.abs(horse.currentSpeedMultiplier() - 1.20) < 0.0001;

        horse.updateBoostAt(1_000_000_000L);
        assert horse.snapshot().isBoosting();
        assert horse.snapshot().getStaminaRemaining() == 0;
        assert Math.abs(horse.currentSpeedMultiplier() - 1.20) < 0.0001;

        horse.updateBoostAt(2_000_000_000L);
        assert !horse.snapshot().isBoosting();
        assert Math.abs(horse.currentSpeedMultiplier() - 1.0) < 0.0001;
    }

    private static void testConcurrentFinishCreatesOneCompleteRanking() throws Exception {
        RecordingListener listener = new RecordingListener();
        RaceParameters fast = new RaceParameters(12.0, 1L, 5L, 200, 260);
        RaceController controller = new RaceController(listener, new Random(7L), fast);

        controller.startRace(10);
        assert listener.finishedLatch.await(3L, TimeUnit.SECONDS) : "Race did not finish";
        assert controller.awaitTermination(1000L) : "Workers did not terminate";

        List<Integer> ranking = controller.getRanking();
        assert ranking.size() == 10 : ranking;
        assert new HashSet<Integer>(ranking).size() == 10 : ranking;
        assert listener.firstFinisherEvents.get() == 1;
        assert listener.horseFinishedEvents.get() == 10;
        assert listener.finalRanking.size() == 10;
    }

    private static void testEveryHorseUsesADistinctThreadAndSpeed() throws Exception {
        RecordingListener listener = new RecordingListener();
        RaceParameters slow = new RaceParameters(100000.0, 2L, 10L, 100, 200);
        RaceController controller = new RaceController(listener, new Random(19L), slow);
        controller.startRace(5);

        long deadline = System.currentTimeMillis() + 1000L;
        List<HorseSnapshot> snapshots = controller.getSnapshots();
        while (!allThreadsStarted(snapshots) && System.currentTimeMillis() < deadline) {
            Thread.sleep(5L);
            snapshots = controller.getSnapshots();
        }

        Set<String> threadNames = new HashSet<String>();
        Set<Double> speeds = new HashSet<Double>();
        for (HorseSnapshot snapshot : snapshots) {
            threadNames.add(snapshot.getThreadName());
            speeds.add(snapshot.getBaseSpeed());
        }
        assert threadNames.size() == 5 : threadNames;
        assert speeds.size() == 5 : speeds;

        controller.stopRace();
        assert controller.awaitTermination(1000L) : "Workers did not stop";
    }

    private static void testStopTerminatesWorkers() throws Exception {
        RecordingListener listener = new RecordingListener();
        RaceParameters slow = new RaceParameters(100000.0, 10L, 10L, 100, 200);
        RaceController controller = new RaceController(listener, new Random(3L), slow);
        controller.startRace(3);
        Thread.sleep(30L);
        controller.stopRace();
        assert !controller.isRunning();
        assert controller.awaitTermination(1000L);
    }

    private static void testUiDispatchRunsOnEventDispatchThread() throws Exception {
        final CountDownLatch callback = new CountDownLatch(1);
        final AtomicBoolean ranOnEdt = new AtomicBoolean(false);
        Thread background = new Thread(new Runnable() {
            @Override public void run() {
                RaceFrame.dispatchOnEdt(new Runnable() {
                    @Override public void run() {
                        ranOnEdt.set(SwingUtilities.isEventDispatchThread());
                        callback.countDown();
                    }
                });
            }
        }, "UI-dispatch-test");
        background.start();
        background.join(1000L);
        assert callback.await(1L, TimeUnit.SECONDS);
        assert ranOnEdt.get();
    }

    private static boolean allThreadsStarted(List<HorseSnapshot> snapshots) {
        for (HorseSnapshot snapshot : snapshots) {
            if ("尚未啟動".equals(snapshot.getThreadName())) {
                return false;
            }
        }
        return true;
    }

    private static void expectIllegalArgument(Runnable action) {
        boolean thrown = false;
        try {
            action.run();
        } catch (IllegalArgumentException expected) {
            thrown = true;
        }
        assert thrown;
    }

    private static final class NoOpHorseEvents implements Horse.Events {
        @Override public void onHorseFinished(Horse horse) { }
        @Override public void onHorseFailed(Horse horse, Throwable failure) { }
    }

    private static final class RecordingListener implements RaceListener {
        private final AtomicInteger firstFinisherEvents = new AtomicInteger();
        private final AtomicInteger horseFinishedEvents = new AtomicInteger();
        private final CountDownLatch finishedLatch = new CountDownLatch(1);
        private volatile List<Integer> finalRanking;

        @Override public void onRaceStarted(List<HorseSnapshot> horses) { }
        @Override public void onFirstHorseFinished(int horseId) {
            firstFinisherEvents.incrementAndGet();
        }
        @Override public void onHorseFinished(int horseId, int place, List<Integer> ranking) {
            horseFinishedEvents.incrementAndGet();
        }
        @Override public void onRaceFinished(List<Integer> ranking) {
            finalRanking = ranking;
            finishedLatch.countDown();
        }
        @Override public void onRaceFailed(String message) {
            throw new AssertionError(message);
        }
    }
}
