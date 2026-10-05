import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JSpinner;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.Timer;
import javax.swing.UIManager;
import javax.swing.border.EmptyBorder;
import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Polygon;
import java.awt.RenderingHints;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

/**
 * 純 JDK 的多執行緒賽馬程式。
 *
 * 編譯：javac -encoding UTF-8 HorseRace.java
 * 執行：java HorseRace
 */
public final class HorseRace {
    private static final int MIN_HORSES = 2;
    private static final int MAX_HORSES = 10;
    private static final double FINISH_DISTANCE = 1000.0;
    private static final long TICK_MILLIS = 25L;
    private static final long BOOST_MILLIS = 1000L;
    private static final double BOOST_MULTIPLIER = 1.20;
    private static final double SLOW_ANIMATION_SPEED = 118.0;
    private static final double FAST_ANIMATION_SPEED = 228.0;
    private static final long SLOW_FRAME_MILLIS = 200L;
    private static final long FAST_FRAME_MILLIS = 85L;
    private static final int RUNNING_FRAME_COUNT = 3;

    private HorseRace() { }

    static double currentSpeed(double baseSpeed, boolean boosting, boolean finished) {
        return finished ? 0.0 : baseSpeed * (boosting ? BOOST_MULTIPLIER : 1.0);
    }

    static long animationFrameDurationMillis(double speed) {
        double clamped = Math.max(SLOW_ANIMATION_SPEED,
                Math.min(FAST_ANIMATION_SPEED, speed));
        double ratio = (clamped - SLOW_ANIMATION_SPEED)
                / (FAST_ANIMATION_SPEED - SLOW_ANIMATION_SPEED);
        return Math.round(SLOW_FRAME_MILLIS
                - ratio * (SLOW_FRAME_MILLIS - FAST_FRAME_MILLIS));
    }

    static int animationFrame(double speed, long nowMillis, boolean moving) {
        if (!moving || speed <= 0.0) {
            return 0;
        }
        return (int) ((nowMillis / animationFrameDurationMillis(speed))
                % RUNNING_FRAME_COUNT);
    }

    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignored) {
            // 無法載入系統外觀時，Swing 會使用跨平台預設外觀。
        }
        SwingUtilities.invokeLater(new Runnable() {
            @Override public void run() {
                new RaceFrame().setVisible(true);
            }
        });
    }

    private interface RaceListener {
        void onRaceStarted(List<HorseSnapshot> horses);
        void onFirstHorseFinished(int horseId);
        void onHorseFinished(List<Integer> ranking);
        void onRaceFinished(List<Integer> ranking);
        void onRaceFailed(String message);
    }

    /** GUI 使用的不可變馬匹狀態，避免直接讀取背景執行緒中的物件。 */
    private static final class HorseSnapshot {
        final int id;
        final double progress;
        final int staminaRemaining;
        final int initialStamina;
        final double currentSpeed;
        final boolean boosting;
        final boolean finished;

        HorseSnapshot(int id, double progress, int staminaRemaining, int initialStamina,
                      double currentSpeed, boolean boosting, boolean finished) {
            this.id = id;
            this.progress = progress;
            this.staminaRemaining = staminaRemaining;
            this.initialStamina = initialStamina;
            this.currentSpeed = currentSpeed;
            this.boosting = boosting;
            this.finished = finished;
        }
    }

    /** 每匹馬都是一個獨立 Runnable。 */
    private static final class Horse implements Runnable {
        interface Events {
            void onHorseFinished(Horse horse);
            void onHorseFailed(Horse horse, Throwable failure);
        }

        private final int id;
        private final double baseSpeed;
        private final int initialStamina;
        private final Events events;

        private volatile double position;
        private volatile int staminaRemaining;
        private volatile boolean boosting;
        private volatile boolean finished;
        private volatile boolean stopRequested;
        private volatile boolean boostModeEnabled;
        private volatile long boostEndsAtNanos;

        Horse(int id, double baseSpeed, int stamina, Events events) {
            this.id = id;
            this.baseSpeed = baseSpeed;
            this.initialStamina = stamina;
            this.staminaRemaining = stamina;
            this.events = events;
        }

        @Override public void run() {
            long previousNanos = System.nanoTime();
            try {
                while (!stopRequested && !finished) {
                    Thread.sleep(TICK_MILLIS);
                    long nowNanos = System.nanoTime();
                    updateBoost(nowNanos);
                    double seconds = Math.min(0.25,
                            (nowNanos - previousNanos) / 1_000_000_000.0);
                    previousNanos = nowNanos;
                    double multiplier = boosting ? BOOST_MULTIPLIER : 1.0;
                    position = Math.min(FINISH_DISTANCE,
                            position + baseSpeed * multiplier * seconds);

                    if (position >= FINISH_DISTANCE) {
                        finished = true;
                        boosting = false;
                        events.onHorseFinished(this);
                    }
                }
            } catch (InterruptedException interrupted) {
                Thread.currentThread().interrupt();
            } catch (Throwable failure) {
                events.onHorseFailed(this, failure);
            }
        }

        synchronized void enableBoostMode() {
            if (boostModeEnabled || finished || stopRequested) {
                return;
            }
            boostModeEnabled = true;
            startNextBoost(System.nanoTime());
        }

        private synchronized void updateBoost(long nowNanos) {
            while (boosting && nowNanos >= boostEndsAtNanos) {
                boosting = false;
                if (staminaRemaining > 0 && !finished && !stopRequested) {
                    startNextBoost(boostEndsAtNanos);
                }
            }
        }

        private void startNextBoost(long startNanos) {
            if (staminaRemaining <= 0 || finished || stopRequested) {
                boosting = false;
                return;
            }
            staminaRemaining--;
            boosting = true;
            boostEndsAtNanos = startNanos + BOOST_MILLIS * 1_000_000L;
        }

        void stop() {
            stopRequested = true;
        }

        HorseSnapshot snapshot() {
            boolean isFinished = finished;
            boolean isBoosting = !isFinished && boosting;
            return new HorseSnapshot(
                    id,
                    Math.max(0.0, Math.min(1.0, position / FINISH_DISTANCE)),
                    staminaRemaining,
                    initialStamina,
                    currentSpeed(baseSpeed, isBoosting, isFinished),
                    isBoosting,
                    isFinished
            );
        }
    }

    /** 建立馬匹執行緒、記錄排名並保證首匹完賽事件只發生一次。 */
    private static final class RaceController implements Horse.Events {
        private final Object stateLock = new Object();
        private final Object eventLock = new Object();
        private final RaceListener listener;
        private final Random random = new Random();
        private final List<Integer> ranking = new ArrayList<Integer>();
        private final Set<Integer> finishedIds = new HashSet<Integer>();

        private List<Horse> horses = new ArrayList<Horse>();
        private List<Thread> threads = new ArrayList<Thread>();
        private volatile boolean running;
        private boolean boostTriggered;

        RaceController(RaceListener listener) {
            this.listener = listener;
        }

        void startRace(int horseCount) {
            if (horseCount < MIN_HORSES || horseCount > MAX_HORSES) {
                throw new IllegalArgumentException("馬匹數量必須介於 2 到 10");
            }

            List<Thread> threadsToStart;
            List<HorseSnapshot> initial;
            synchronized (stateLock) {
                if (running) {
                    return;
                }
                ranking.clear();
                finishedIds.clear();
                boostTriggered = false;
                horses = new ArrayList<Horse>(horseCount);
                threads = new ArrayList<Thread>(horseCount);

                Set<Integer> speeds = new HashSet<Integer>();
                for (int index = 0; index < horseCount; index++) {
                    int speed;
                    do {
                        speed = 118 + random.nextInt(73);
                    } while (!speeds.add(speed));
                    int stamina = 1 + random.nextInt(3);
                    Horse horse = new Horse(index + 1, speed, stamina, this);
                    horses.add(horse);
                    threads.add(new Thread(horse, "Horse-Thread-" + (index + 1)));
                }
                running = true;
                threadsToStart = new ArrayList<Thread>(threads);
                initial = snapshotsLocked();
            }

            listener.onRaceStarted(initial);
            for (Thread thread : threadsToStart) {
                thread.start();
            }
        }

        @Override public void onHorseFinished(Horse horse) {
            synchronized (eventLock) {
                publishFinish(horse);
            }
        }

        private void publishFinish(Horse horse) {
            List<Horse> horsesToBoost = Collections.emptyList();
            List<Integer> rankingCopy;
            boolean first = false;
            boolean complete;

            synchronized (stateLock) {
                if (!running || !horses.contains(horse) || !finishedIds.add(horse.id)) {
                    return;
                }
                ranking.add(horse.id);
                if (!boostTriggered) {
                    boostTriggered = true;
                    first = true;
                    horsesToBoost = new ArrayList<Horse>();
                    for (Horse candidate : horses) {
                        if (candidate != horse && !candidate.snapshot().finished) {
                            horsesToBoost.add(candidate);
                        }
                    }
                }
                complete = ranking.size() == horses.size();
                if (complete) {
                    running = false;
                }
                rankingCopy = immutableRanking();
            }

            for (Horse candidate : horsesToBoost) {
                candidate.enableBoostMode();
            }
            if (first) {
                listener.onFirstHorseFinished(horse.id);
            }
            listener.onHorseFinished(rankingCopy);
            if (complete) {
                listener.onRaceFinished(rankingCopy);
            }
        }

        @Override public void onHorseFailed(Horse horse, Throwable failure) {
            synchronized (eventLock) {
                List<Horse> horsesToStop;
                List<Thread> threadsToStop;
                synchronized (stateLock) {
                    if (!running || !horses.contains(horse)) {
                        return;
                    }
                    running = false;
                    horsesToStop = new ArrayList<Horse>(horses);
                    threadsToStop = new ArrayList<Thread>(threads);
                }
                stopWorkers(horsesToStop, threadsToStop);
                String detail = failure.getMessage() == null
                        ? failure.getClass().getSimpleName() : failure.getMessage();
                listener.onRaceFailed("馬匹 " + horse.id + " 執行失敗：" + detail);
            }
        }

        void stopRace() {
            List<Horse> horsesToStop;
            List<Thread> threadsToStop;
            synchronized (stateLock) {
                running = false;
                horsesToStop = new ArrayList<Horse>(horses);
                threadsToStop = new ArrayList<Thread>(threads);
            }
            stopWorkers(horsesToStop, threadsToStop);
        }

        private static void stopWorkers(List<Horse> horses, List<Thread> threads) {
            for (Horse horse : horses) {
                horse.stop();
            }
            for (Thread thread : threads) {
                if (thread.isAlive()) {
                    thread.interrupt();
                }
            }
        }

        List<HorseSnapshot> snapshots() {
            synchronized (stateLock) {
                return snapshotsLocked();
            }
        }

        private List<HorseSnapshot> snapshotsLocked() {
            List<HorseSnapshot> result = new ArrayList<HorseSnapshot>(horses.size());
            for (Horse horse : horses) {
                result.add(horse.snapshot());
            }
            return Collections.unmodifiableList(result);
        }

        private List<Integer> immutableRanking() {
            return Collections.unmodifiableList(new ArrayList<Integer>(ranking));
        }

        boolean isRunning() {
            return running;
        }
    }

    /** Java2D 跑道與馬匹畫面。 */
    private static final class RacePanel extends JPanel {
        private static final long serialVersionUID = 1L;
        private static final Color TRACK_LIGHT = new Color(232, 244, 233);
        private static final Color TRACK_DARK = new Color(220, 237, 222);
        private static final Color TRACK_LINE = new Color(188, 210, 190);
        private static final Color[] HORSE_COLORS = {
                new Color(43, 108, 176), new Color(197, 48, 48),
                new Color(47, 133, 90), new Color(128, 90, 213),
                new Color(221, 107, 32), new Color(49, 130, 206),
                new Color(183, 121, 31), new Color(56, 161, 105),
                new Color(184, 50, 128), new Color(74, 85, 104)
        };
        private static final int[] BODY_BOUNCE = {0, 1, -1};
        private static final int[] HEAD_BOB = {0, 1, -1};
        private static final int[] TAIL_LIFT = {-2, 2, -5};
        private static final int[][] HIND_LEGS = {{-3, -8}, {2, 0}, {4, 8}};
        private static final int[][] REAR_LEGS = {{3, 7}, {-2, -1}, {-4, -8}};
        private static final int[][] FORE_LEGS = {{4, 9}, {-2, 0}, {-4, -8}};
        private static final int[][] FRONT_LEGS = {{-3, -7}, {2, 1}, {4, 8}};

        private volatile List<HorseSnapshot> snapshots = Collections.emptyList();
        private volatile int previewCount = 5;

        RacePanel() {
            setBackground(new Color(248, 250, 252));
            setPreferredSize(new Dimension(1040, 520));
            setMinimumSize(new Dimension(720, 400));
        }

        void setSnapshots(List<HorseSnapshot> value) {
            snapshots = Collections.unmodifiableList(new ArrayList<HorseSnapshot>(value));
            repaint();
        }

        void showPreview(int count) {
            previewCount = count;
            snapshots = Collections.emptyList();
            repaint();
        }

        @Override protected void paintComponent(Graphics graphics) {
            super.paintComponent(graphics);
            Graphics2D g2 = (Graphics2D) graphics.create();
            try {
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                        RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
                        RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
                List<HorseSnapshot> current = snapshots;
                int count = current.isEmpty() ? previewCount : current.size();
                drawTrack(g2, current, count);
            } finally {
                g2.dispose();
            }
        }

        private void drawTrack(Graphics2D g2, List<HorseSnapshot> current, int count) {
            int width = getWidth();
            int height = getHeight();
            int startX = 105;
            int finishX = width - 66;
            int laneHeight = Math.max(38, (height - 36) / count);
            int trackHeight = laneHeight * count;
            int top = Math.max(18, (height - trackHeight) / 2);
            long animationTimeMillis = System.currentTimeMillis();

            for (int index = 0; index < count; index++) {
                int laneY = top + index * laneHeight;
                g2.setColor(index % 2 == 0 ? TRACK_LIGHT : TRACK_DARK);
                g2.fillRoundRect(10, laneY, width - 20, laneHeight - 3, 12, 12);
                g2.setColor(TRACK_LINE);
                g2.setStroke(new BasicStroke(1f, BasicStroke.CAP_BUTT,
                        BasicStroke.JOIN_BEVEL, 1f, new float[]{7f, 7f}, 0f));
                g2.drawLine(startX, laneY + laneHeight - 4,
                        finishX, laneY + laneHeight - 4);

                HorseSnapshot horse = current.isEmpty() ? null : current.get(index);
                drawLabel(g2, horse, index + 1, laneY, laneHeight);
                double progress = horse == null ? 0.0 : horse.progress;
                int horseWidth = Math.min(52, Math.max(40, laneHeight - 2));
                int x = startX + (int) Math.round(
                        (finishX - startX - horseWidth + 9) * progress);
                drawHorse(g2, x, laneY + (laneHeight - 3) / 2,
                        horseWidth, index, horse, animationTimeMillis);
            }
            drawFinishLine(g2, finishX, top, trackHeight - 3);
        }

        private void drawLabel(Graphics2D g2, HorseSnapshot horse, int id,
                               int laneY, int laneHeight) {
            boolean compact = laneHeight < 46;
            g2.setFont(font(Font.BOLD, compact ? 12 : 15));
            g2.setColor(new Color(39, 53, 76));
            g2.drawString(id + " 號馬", 20, laneY + (compact ? 15 : laneHeight / 2));

            String detail;
            if (horse == null) {
                detail = "等待起跑";
            } else if (horse.finished) {
                detail = "已完賽";
            } else {
                detail = "體力 " + horse.staminaRemaining + "/" + horse.initialStamina;
            }
            g2.setFont(font(Font.PLAIN, compact ? 10 : 11));
            g2.setColor(new Color(88, 102, 126));
            g2.drawString(detail, 20, laneY + laneHeight - (compact ? 6 : 9));
        }

        private void drawFinishLine(Graphics2D g2, int x, int y, int height) {
            int tile = 7;
            for (int row = 0; row < (height + tile - 1) / tile; row++) {
                for (int column = 0; column < 2; column++) {
                    g2.setColor((row + column) % 2 == 0
                            ? new Color(31, 41, 55) : Color.WHITE);
                    g2.fillRect(x + column * tile, y + row * tile, tile,
                            Math.min(tile, y + height - (y + row * tile)));
                }
            }
            g2.setColor(new Color(185, 28, 28));
            g2.setStroke(new BasicStroke(2f));
            g2.drawLine(x - 1, y, x - 1, y + height);
            g2.setFont(font(Font.BOLD, 11));
            g2.drawString("終點", x - 5, Math.max(12, y - 4));
        }

        private void drawHorse(Graphics2D g2, int x, int centerY, int width,
                                int colorIndex, HorseSnapshot horse,
                                long animationTimeMillis) {
            double scale = width / 52.0;
            int frame = horse == null ? 0 : animationFrame(
                    horse.currentSpeed, animationTimeMillis, !horse.finished);
            int poseCenterY = centerY
                    + (int) Math.round(BODY_BOUNCE[frame] * scale);
            int bodyW = (int) Math.round(29 * scale);
            int bodyH = (int) Math.round(15 * scale);
            int bodyX = x + (int) Math.round(7 * scale);
            int bodyY = poseCenterY - bodyH / 2;
            Color color = HORSE_COLORS[colorIndex % HORSE_COLORS.length];

            if (horse != null && horse.boosting) {
                g2.setColor(new Color(245, 158, 11, 80));
                g2.fillOval(x - 5, centerY - bodyH, width + 8, bodyH * 2);
                g2.setFont(font(Font.BOLD, 11));
                g2.setColor(new Color(180, 83, 9));
                g2.drawString("x1.2", x + width - 5, centerY - bodyH / 2 - 3);
                drawLightning(g2, x + 1, centerY - bodyH);
            }

            g2.setColor(color.darker());
            g2.setStroke(new BasicStroke(Math.max(1f, (float) scale * 1.6f),
                    BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
            int legTop = bodyY + bodyH - (int) Math.round(2 * scale);
            g2.setColor(color.darker().darker());
            drawLeg(g2, bodyX + (int) Math.round(9 * scale), legTop,
                    REAR_LEGS[frame][0], REAR_LEGS[frame][1], scale);
            drawLeg(g2, bodyX + bodyW - (int) Math.round(9 * scale), legTop,
                    FORE_LEGS[frame][0], FORE_LEGS[frame][1], scale);
            g2.setColor(color.darker());
            drawLeg(g2, bodyX + (int) Math.round(4 * scale), legTop,
                    HIND_LEGS[frame][0], HIND_LEGS[frame][1], scale);
            drawLeg(g2, bodyX + bodyW - (int) Math.round(4 * scale), legTop,
                    FRONT_LEGS[frame][0], FRONT_LEGS[frame][1], scale);

            int headOffsetY = (int) Math.round(HEAD_BOB[frame] * scale);
            g2.drawLine(bodyX + bodyW - 1, bodyY + 3,
                    bodyX + bodyW + (int) (8 * scale),
                    bodyY - (int) (6 * scale) + headOffsetY);
            g2.drawLine(bodyX + 2, bodyY + 4, x,
                    bodyY + (int) Math.round(TAIL_LIFT[frame] * scale));
            g2.setColor(color);
            g2.fillOval(bodyX, bodyY, bodyW, bodyH);
            int head = (int) Math.round(11 * scale);
            g2.fillOval(bodyX + bodyW + (int) (5 * scale),
                    bodyY - (int) (9 * scale) + headOffsetY, head, head);

            g2.setColor(new Color(255, 255, 255, 225));
            int badge = Math.max(12, (int) Math.round(14 * scale));
            int badgeX = bodyX + bodyW / 2 - badge / 2;
            int badgeY = poseCenterY - badge / 2;
            g2.fillOval(badgeX, badgeY, badge, badge);
            g2.setColor(new Color(31, 41, 55));
            g2.setFont(font(Font.BOLD, Math.max(9, (int) Math.round(10 * scale))));
            String number = Integer.toString(colorIndex + 1);
            g2.drawString(number,
                    badgeX + (badge - g2.getFontMetrics().stringWidth(number)) / 2,
                    badgeY + (badge + g2.getFontMetrics().getAscent()
                            - g2.getFontMetrics().getDescent()) / 2);
        }

        private void drawLeg(Graphics2D g2, int hipX, int hipY,
                             int kneeDx, int hoofDx, double scale) {
            int kneeX = hipX + (int) Math.round(kneeDx * scale);
            int kneeY = hipY + (int) Math.round(7 * scale);
            int hoofX = hipX + (int) Math.round(hoofDx * scale);
            int hoofY = hipY + (int) Math.round(14 * scale);
            g2.drawLine(hipX, hipY, kneeX, kneeY);
            g2.drawLine(kneeX, kneeY, hoofX, hoofY);
        }

        private void drawLightning(Graphics2D g2, int x, int y) {
            Polygon bolt = new Polygon();
            bolt.addPoint(x + 6, y);
            bolt.addPoint(x, y + 9);
            bolt.addPoint(x + 5, y + 9);
            bolt.addPoint(x + 2, y + 18);
            bolt.addPoint(x + 13, y + 6);
            bolt.addPoint(x + 8, y + 6);
            g2.setColor(new Color(245, 158, 11));
            g2.fillPolygon(bolt);
        }
    }

    /** Swing 主視窗；所有元件更新都回到 EDT 執行。 */
    private static final class RaceFrame extends JFrame implements RaceListener {
        private static final long serialVersionUID = 1L;
        private static final Color NAVY = new Color(32, 45, 70);
        private static final Color TEXT = new Color(38, 50, 75);
        private static final Color MUTED = new Color(94, 108, 132);
        private static final Color PALE_GREEN = new Color(232, 247, 239);
        private static final Color PALE_ORANGE = new Color(255, 247, 232);

        private final RaceController controller = new RaceController(this);
        private final RacePanel racePanel = new RacePanel();
        private final JSpinner countSpinner = new JSpinner(
                new SpinnerNumberModel(5, MIN_HORSES, MAX_HORSES, 1));
        private final JButton startButton = new JButton("開始比賽");
        private final JLabel raceLabel = new JLabel("準備第 1 場");
        private final JPanel rankingItems = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 5));
        private final JLabel statusLabel = new JLabel("設定馬匹數量後，按下「開始比賽」。");
        private final Timer repaintTimer;
        private int raceNumber;
        private int displayedRankingCount;
        private boolean raceComplete;

        RaceFrame() {
            super("Java 多執行緒賽馬");
            repaintTimer = new Timer(33, event -> {
                if (controller.isRunning()) {
                    racePanel.setSnapshots(controller.snapshots());
                }
            });
            buildInterface();
            bindActions();
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            setMinimumSize(new Dimension(860, 650));
            setSize(1120, 760);
            setLocationRelativeTo(null);
            addWindowListener(new WindowAdapter() {
                @Override public void windowClosing(WindowEvent event) {
                    repaintTimer.stop();
                    controller.stopRace();
                }
            });
        }

        private void buildInterface() {
            JPanel root = new JPanel(new BorderLayout());
            root.setBackground(new Color(248, 250, 252));
            root.add(createHeader(), BorderLayout.NORTH);

            JPanel center = new JPanel(new BorderLayout(0, 10));
            center.setOpaque(false);
            center.setBorder(new EmptyBorder(12, 16, 12, 16));
            center.add(createControls(), BorderLayout.NORTH);
            racePanel.setBorder(BorderFactory.createLineBorder(
                    new Color(218, 224, 232), 1, true));
            center.add(racePanel, BorderLayout.CENTER);
            center.add(createRankingArea(), BorderLayout.SOUTH);
            root.add(center, BorderLayout.CENTER);
            root.add(createStatusBar(), BorderLayout.SOUTH);
            setContentPane(root);
        }

        private JPanel createHeader() {
            JPanel header = new JPanel();
            header.setLayout(new BoxLayout(header, BoxLayout.Y_AXIS));
            header.setBackground(NAVY);
            header.setBorder(new EmptyBorder(16, 22, 14, 22));
            JLabel title = new JLabel("多執行緒賽馬場");
            title.setForeground(Color.WHITE);
            title.setFont(font(Font.BOLD, 24));
            title.setAlignmentX(Component.LEFT_ALIGNMENT);
            JLabel subtitle = new JLabel(
                    "每匹馬由獨立 Thread 執行 · 首匹完賽後自動消耗體力加速 20%");
            subtitle.setForeground(new Color(205, 216, 235));
            subtitle.setFont(font(Font.PLAIN, 13));
            subtitle.setAlignmentX(Component.LEFT_ALIGNMENT);
            header.add(title);
            header.add(Box.createVerticalStrut(4));
            header.add(subtitle);
            return header;
        }

        private JPanel createControls() {
            JPanel controls = new JPanel(new GridBagLayout());
            controls.setBackground(Color.WHITE);
            controls.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createLineBorder(new Color(218, 224, 232), 1, true),
                    new EmptyBorder(9, 12, 9, 12)));
            GridBagConstraints c = new GridBagConstraints();
            c.gridy = 0;
            c.insets = new Insets(0, 0, 0, 8);
            c.anchor = GridBagConstraints.WEST;

            JLabel countLabel = new JLabel("馬匹數量");
            countLabel.setForeground(TEXT);
            countLabel.setFont(font(Font.BOLD, 14));
            controls.add(countLabel, c);
            c.gridx = 1;
            countSpinner.setPreferredSize(new Dimension(74, 31));
            controls.add(countSpinner, c);
            c.gridx = 2;
            startButton.setFont(font(Font.BOLD, 14));
            startButton.setFocusPainted(false);
            startButton.setPreferredSize(new Dimension(126, 33));
            controls.add(startButton, c);
            c.gridx = 3;
            c.weightx = 1.0;
            c.fill = GridBagConstraints.HORIZONTAL;
            controls.add(Box.createHorizontalGlue(), c);
            c.gridx = 4;
            c.weightx = 0.0;
            c.fill = GridBagConstraints.NONE;
            raceLabel.setForeground(MUTED);
            raceLabel.setFont(font(Font.PLAIN, 13));
            controls.add(raceLabel, c);
            return controls;
        }

        private JPanel createRankingArea() {
            JPanel area = new JPanel(new BorderLayout(10, 0));
            area.setBackground(Color.WHITE);
            area.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createLineBorder(new Color(218, 224, 232), 1, true),
                    new EmptyBorder(8, 12, 8, 12)));
            JLabel title = new JLabel("完賽名次");
            title.setFont(font(Font.BOLD, 14));
            title.setForeground(TEXT);
            area.add(title, BorderLayout.WEST);
            rankingItems.setOpaque(false);
            JLabel waiting = new JLabel("比賽開始後，名次會依序顯示在這裡");
            waiting.setFont(font(Font.PLAIN, 13));
            waiting.setForeground(MUTED);
            rankingItems.add(waiting);
            area.add(rankingItems, BorderLayout.CENTER);
            return area;
        }

        private JPanel createStatusBar() {
            JPanel bar = new JPanel(new BorderLayout());
            bar.setBackground(PALE_GREEN);
            bar.setBorder(new EmptyBorder(10, 20, 10, 20));
            statusLabel.setForeground(new Color(27, 94, 63));
            statusLabel.setFont(font(Font.BOLD, 13));
            bar.add(statusLabel, BorderLayout.WEST);
            JLabel hint = new JLabel("速度與體力每場重新隨機");
            hint.setHorizontalAlignment(SwingConstants.RIGHT);
            hint.setForeground(MUTED);
            hint.setFont(font(Font.PLAIN, 12));
            bar.add(hint, BorderLayout.EAST);
            return bar;
        }

        private void bindActions() {
            countSpinner.addChangeListener(event -> {
                if (!controller.isRunning()) {
                    racePanel.showPreview(((Number) countSpinner.getValue()).intValue());
                }
            });
            startButton.addActionListener(event -> startRace());
        }

        private void startRace() {
            if (controller.isRunning()) {
                return;
            }
            int count = ((Number) countSpinner.getValue()).intValue();
            raceNumber++;
            raceComplete = false;
            displayedRankingCount = 0;
            startButton.setText("比賽進行中");
            startButton.setEnabled(false);
            countSpinner.setEnabled(false);
            rankingItems.removeAll();
            rankingItems.revalidate();
            rankingItems.repaint();
            raceLabel.setText("第 " + raceNumber + " 場進行中");
            setStatus("比賽開始！" + count + " 匹馬正在各自的執行緒中奔跑。", false);
            try {
                controller.startRace(count);
                repaintTimer.start();
            } catch (RuntimeException failure) {
                startButton.setEnabled(true);
                countSpinner.setEnabled(true);
                setStatus("無法開始比賽：" + failure.getMessage(), true);
            }
        }

        @Override public void onRaceStarted(final List<HorseSnapshot> horses) {
            onEdt(new Runnable() {
                @Override public void run() {
                    racePanel.setSnapshots(horses);
                }
            });
        }

        @Override public void onFirstHorseFinished(final int horseId) {
            onEdt(new Runnable() {
                @Override public void run() {
                    if (!raceComplete) {
                        setStatus(horseId + " 號馬率先抵達！其餘馬匹自動加速 20%。", true);
                    }
                }
            });
        }

        @Override public void onHorseFinished(final List<Integer> ranking) {
            onEdt(new Runnable() {
                @Override public void run() {
                    updateRanking(ranking);
                }
            });
        }

        @Override public void onRaceFinished(final List<Integer> ranking) {
            onEdt(new Runnable() {
                @Override public void run() {
                    raceComplete = true;
                    repaintTimer.stop();
                    racePanel.setSnapshots(controller.snapshots());
                    updateRanking(ranking);
                    countSpinner.setEnabled(true);
                    startButton.setEnabled(true);
                    startButton.setText("再賽一場");
                    raceLabel.setText("第 " + raceNumber + " 場完成");
                    setStatus("全部馬匹完賽！冠軍是 " + ranking.get(0) + " 號馬。", false);
                }
            });
        }

        @Override public void onRaceFailed(final String message) {
            onEdt(new Runnable() {
                @Override public void run() {
                    repaintTimer.stop();
                    countSpinner.setEnabled(true);
                    startButton.setEnabled(true);
                    startButton.setText("重新開始");
                    setStatus("比賽已停止：" + message, true);
                    JOptionPane.showMessageDialog(RaceFrame.this, message,
                            "比賽錯誤", JOptionPane.ERROR_MESSAGE);
                }
            });
        }

        private void updateRanking(List<Integer> ranking) {
            if (ranking.size() < displayedRankingCount) {
                return;
            }
            displayedRankingCount = ranking.size();
            rankingItems.removeAll();
            for (int index = 0; index < ranking.size(); index++) {
                JLabel item = new JLabel((index + 1) + ".  " + ranking.get(index) + " 號馬");
                item.setOpaque(true);
                item.setFont(font(index == 0 ? Font.BOLD : Font.PLAIN, 13));
                item.setForeground(index == 0 ? new Color(133, 77, 14) : TEXT);
                item.setBackground(index == 0
                        ? new Color(255, 244, 204) : new Color(238, 242, 247));
                item.setBorder(new EmptyBorder(5, 9, 5, 9));
                rankingItems.add(item);
            }
            rankingItems.revalidate();
            rankingItems.repaint();
        }

        private void setStatus(String text, boolean warning) {
            statusLabel.setText(text);
            JPanel bar = (JPanel) statusLabel.getParent();
            bar.setBackground(warning ? PALE_ORANGE : PALE_GREEN);
            statusLabel.setForeground(warning
                    ? new Color(154, 73, 7) : new Color(27, 94, 63));
        }

        private static void onEdt(Runnable action) {
            if (SwingUtilities.isEventDispatchThread()) {
                action.run();
            } else {
                SwingUtilities.invokeLater(action);
            }
        }
    }

    private static Font font(int style, int size) {
        return new Font("Microsoft JhengHei", style, size);
    }
}
