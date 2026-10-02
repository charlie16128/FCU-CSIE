package horserace;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

/** Owns race lifecycle, one thread per horse, ranking, and the one-time boost event. */
public final class RaceController implements Horse.Events {
    public static final int MIN_HORSES = 2;
    public static final int MAX_HORSES = 10;

    private final Object lock = new Object();
    private final RaceListener listener;
    private final Random random;
    private final RaceParameters parameters;

    private List<Horse> horses = new ArrayList<Horse>();
    private List<Thread> horseThreads = new ArrayList<Thread>();
    private final List<Integer> ranking = new ArrayList<Integer>();
    private final Set<Integer> finishedIds = new HashSet<Integer>();
    private volatile boolean running;
    private boolean boostTriggered;

    public RaceController(RaceListener listener) {
        this(listener, new Random(), RaceParameters.defaults());
    }

    RaceController(RaceListener listener, Random random, RaceParameters parameters) {
        if (listener == null || random == null || parameters == null) {
            throw new IllegalArgumentException("Race dependencies cannot be null");
        }
        this.listener = listener;
        this.random = random;
        this.parameters = parameters;
    }

    public void startRace(int horseCount) {
        validateHorseCount(horseCount);

        List<Thread> threadsToStart;
        List<HorseSnapshot> initialSnapshots;
        synchronized (lock) {
            if (running) {
                throw new IllegalStateException("A race is already running");
            }

            ranking.clear();
            finishedIds.clear();
            boostTriggered = false;
            horses = new ArrayList<Horse>(horseCount);
            horseThreads = new ArrayList<Thread>(horseCount);

            Set<Integer> usedSpeeds = new HashSet<Integer>();
            for (int index = 0; index < horseCount; index++) {
                int speed = nextUniqueSpeed(usedSpeeds);
                int stamina = 1 + random.nextInt(3);
                Horse horse = new Horse(index + 1, speed, stamina, parameters, this);
                horses.add(horse);
                horseThreads.add(new Thread(horse, "Horse-Thread-" + (index + 1)));
            }
            running = true;
            threadsToStart = new ArrayList<Thread>(horseThreads);
            initialSnapshots = snapshotsLocked();
        }

        listener.onRaceStarted(initialSnapshots);
        for (Thread thread : threadsToStart) {
            thread.start();
        }
    }

    private int nextUniqueSpeed(Set<Integer> usedSpeeds) {
        int range = parameters.maximumSpeed - parameters.minimumSpeed + 1;
        if (range < MAX_HORSES) {
            throw new IllegalStateException("Speed range cannot provide unique horse speeds");
        }
        int speed;
        do {
            speed = parameters.minimumSpeed + random.nextInt(range);
        } while (!usedSpeeds.add(speed));
        return speed;
    }

    private static void validateHorseCount(int horseCount) {
        if (horseCount < MIN_HORSES || horseCount > MAX_HORSES) {
            throw new IllegalArgumentException("Horse count must be between 2 and 10");
        }
    }

    @Override
    public void onHorseFinished(Horse horse) {
        List<Horse> horsesToBoost = Collections.emptyList();
        List<Integer> rankingCopy;
        int place;
        boolean firstFinisher = false;
        boolean raceComplete;

        synchronized (lock) {
            if (!finishedIds.add(horse.getId())) {
                return;
            }
            ranking.add(horse.getId());
            place = ranking.size();

            if (!boostTriggered) {
                boostTriggered = true;
                firstFinisher = true;
                horsesToBoost = new ArrayList<Horse>();
                for (Horse candidate : horses) {
                    if (candidate.getId() != horse.getId() && !candidate.snapshot().isFinished()) {
                        horsesToBoost.add(candidate);
                    }
                }
            }

            raceComplete = ranking.size() == horses.size();
            if (raceComplete) {
                running = false;
            }
            rankingCopy = immutableCopy(ranking);
        }

        for (Horse candidate : horsesToBoost) {
            candidate.enableBoostMode();
        }
        if (firstFinisher) {
            listener.onFirstHorseFinished(horse.getId());
        }
        listener.onHorseFinished(horse.getId(), place, rankingCopy);
        if (raceComplete) {
            listener.onRaceFinished(rankingCopy);
        }
    }

    @Override
    public void onHorseFailed(Horse horse, Throwable failure) {
        List<Horse> horsesToStop;
        synchronized (lock) {
            if (!running) {
                return;
            }
            running = false;
            horsesToStop = new ArrayList<Horse>(horses);
        }
        for (Horse candidate : horsesToStop) {
            candidate.requestStop();
        }
        interruptWorkerThreads();
        String detail = failure.getMessage() == null ? failure.getClass().getSimpleName() : failure.getMessage();
        listener.onRaceFailed("馬匹 " + horse.getId() + " 執行失敗：" + detail);
    }

    public void stopRace() {
        List<Horse> horsesToStop;
        synchronized (lock) {
            running = false;
            horsesToStop = new ArrayList<Horse>(horses);
        }
        for (Horse horse : horsesToStop) {
            horse.requestStop();
        }
        interruptWorkerThreads();
    }

    private void interruptWorkerThreads() {
        List<Thread> threads;
        synchronized (lock) {
            threads = new ArrayList<Thread>(horseThreads);
        }
        for (Thread thread : threads) {
            if (thread.isAlive()) {
                thread.interrupt();
            }
        }
    }

    public boolean awaitTermination(long timeoutMillis) throws InterruptedException {
        long deadline = System.currentTimeMillis() + timeoutMillis;
        List<Thread> threads;
        synchronized (lock) {
            threads = new ArrayList<Thread>(horseThreads);
        }
        for (Thread thread : threads) {
            long remaining = deadline - System.currentTimeMillis();
            if (remaining <= 0L) {
                return false;
            }
            thread.join(remaining);
        }
        for (Thread thread : threads) {
            if (thread.isAlive()) {
                return false;
            }
        }
        return true;
    }

    public List<HorseSnapshot> getSnapshots() {
        synchronized (lock) {
            return snapshotsLocked();
        }
    }

    private List<HorseSnapshot> snapshotsLocked() {
        List<HorseSnapshot> snapshots = new ArrayList<HorseSnapshot>(horses.size());
        for (Horse horse : horses) {
            snapshots.add(horse.snapshot());
        }
        return Collections.unmodifiableList(snapshots);
    }

    public List<Integer> getRanking() {
        synchronized (lock) {
            return immutableCopy(ranking);
        }
    }

    public int getFinishedCount() {
        synchronized (lock) {
            return ranking.size();
        }
    }

    public boolean isRunning() {
        return running;
    }

    private static List<Integer> immutableCopy(List<Integer> source) {
        return Collections.unmodifiableList(new ArrayList<Integer>(source));
    }
}
