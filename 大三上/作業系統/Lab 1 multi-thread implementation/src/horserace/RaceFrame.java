package horserace;

import javax.imageio.ImageIO;
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
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.RenderingHints;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/** Main Swing window. All component mutations are marshalled onto the EDT. */
public final class RaceFrame extends JFrame implements RaceListener {
    private static final Color NAVY = new Color(32, 45, 70);
    private static final Color TEXT = new Color(38, 50, 75);
    private static final Color MUTED = new Color(94, 108, 132);
    private static final Color PALE_GREEN = new Color(232, 247, 239);
    private static final Color PALE_ORANGE = new Color(255, 247, 232);

    static {
        configureLookAndFeel();
    }

    private final RaceController controller;
    private final RacePanel racePanel = new RacePanel();
    private final JSpinner horseCountSpinner = new JSpinner(
            new SpinnerNumberModel(5, RaceController.MIN_HORSES, RaceController.MAX_HORSES, 1));
    private final JButton startButton = new JButton("開始比賽");
    private final JLabel raceNumberLabel = new JLabel("準備第 1 場");
    private final JPanel rankingItems = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 5));
    private final JLabel statusLabel = new JLabel("設定馬匹數量後，按下「開始比賽」。");
    private final Timer repaintTimer;
    private volatile int displayedRankingCount;
    private volatile boolean displayedBoosting;
    private volatile boolean displayedRaceComplete;
    private int raceNumber;

    public RaceFrame() {
        super("Java 多執行緒賽馬");
        controller = new RaceController(this);
        repaintTimer = new Timer(33, event -> {
            if (controller.isRunning()) {
                List<HorseSnapshot> latest = controller.getSnapshots();
                racePanel.setSnapshots(latest);
                displayedBoosting = containsBoostingHorse(latest);
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

    private static void configureLookAndFeel() {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignored) {
            // The cross-platform Swing look and feel remains a safe fallback.
        }
    }

    private void buildInterface() {
        JPanel root = new JPanel(new BorderLayout());
        root.setBackground(new Color(248, 250, 252));
        root.add(createHeader(), BorderLayout.NORTH);

        JPanel center = new JPanel(new BorderLayout(0, 10));
        center.setOpaque(false);
        center.setBorder(new EmptyBorder(12, 16, 12, 16));
        center.add(createControls(), BorderLayout.NORTH);
        racePanel.setBorder(BorderFactory.createLineBorder(new Color(218, 224, 232), 1, true));
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
        title.setFont(uiFont(Font.BOLD, 24));
        title.setAlignmentX(Component.LEFT_ALIGNMENT);
        JLabel subtitle = new JLabel("每匹馬由獨立 Thread 執行 · 首匹完賽後自動消耗體力加速 20%");
        subtitle.setForeground(new Color(205, 216, 235));
        subtitle.setFont(uiFont(Font.PLAIN, 13));
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

        GridBagConstraints constraints = new GridBagConstraints();
        constraints.gridy = 0;
        constraints.insets = new Insets(0, 0, 0, 8);
        constraints.anchor = GridBagConstraints.WEST;

        JLabel countLabel = new JLabel("馬匹數量");
        countLabel.setForeground(TEXT);
        countLabel.setFont(uiFont(Font.BOLD, 14));
        controls.add(countLabel, constraints);

        constraints.gridx = 1;
        horseCountSpinner.setFont(uiFont(Font.PLAIN, 14));
        horseCountSpinner.setPreferredSize(new Dimension(74, 31));
        controls.add(horseCountSpinner, constraints);

        constraints.gridx = 2;
        startButton.setFont(uiFont(Font.BOLD, 14));
        startButton.setFocusPainted(false);
        startButton.setPreferredSize(new Dimension(126, 33));
        controls.add(startButton, constraints);

        constraints.gridx = 3;
        constraints.weightx = 1.0;
        constraints.fill = GridBagConstraints.HORIZONTAL;
        controls.add(Box.createHorizontalGlue(), constraints);

        constraints.gridx = 4;
        constraints.weightx = 0.0;
        constraints.fill = GridBagConstraints.NONE;
        raceNumberLabel.setForeground(MUTED);
        raceNumberLabel.setFont(uiFont(Font.PLAIN, 13));
        controls.add(raceNumberLabel, constraints);
        return controls;
    }

    private JPanel createRankingArea() {
        JPanel ranking = new JPanel(new BorderLayout(10, 0));
        ranking.setBackground(Color.WHITE);
        ranking.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(218, 224, 232), 1, true),
                new EmptyBorder(8, 12, 8, 12)));
        JLabel title = new JLabel("完賽名次");
        title.setFont(uiFont(Font.BOLD, 14));
        title.setForeground(TEXT);
        ranking.add(title, BorderLayout.WEST);
        rankingItems.setOpaque(false);
        JLabel waiting = new JLabel("比賽開始後，名次會依序顯示在這裡");
        waiting.setFont(uiFont(Font.PLAIN, 13));
        waiting.setForeground(MUTED);
        rankingItems.add(waiting);
        ranking.add(rankingItems, BorderLayout.CENTER);
        return ranking;
    }

    private JPanel createStatusBar() {
        JPanel bar = new JPanel(new BorderLayout());
        bar.setBackground(PALE_GREEN);
        bar.setBorder(new EmptyBorder(10, 20, 10, 20));
        statusLabel.setForeground(new Color(27, 94, 63));
        statusLabel.setFont(uiFont(Font.BOLD, 13));
        bar.add(statusLabel, BorderLayout.WEST);

        JLabel hint = new JLabel("速度與體力每場重新隨機");
        hint.setHorizontalAlignment(SwingConstants.RIGHT);
        hint.setForeground(MUTED);
        hint.setFont(uiFont(Font.PLAIN, 12));
        bar.add(hint, BorderLayout.EAST);
        return bar;
    }

    private void bindActions() {
        horseCountSpinner.addChangeListener(event -> {
            if (!controller.isRunning()) {
                racePanel.showPreview(((Number) horseCountSpinner.getValue()).intValue());
            }
        });
        startButton.addActionListener(event -> startSelectedRace());
    }

    private void startSelectedRace() {
        if (controller.isRunning()) {
            return;
        }
        int horseCount = ((Number) horseCountSpinner.getValue()).intValue();
        raceNumber++;
        startButton.setText("比賽進行中");
        horseCountSpinner.setEnabled(false);
        startButton.setEnabled(false);
        rankingItems.removeAll();
        displayedRankingCount = 0;
        displayedBoosting = false;
        displayedRaceComplete = false;
        rankingItems.revalidate();
        rankingItems.repaint();
        raceNumberLabel.setText("第 " + raceNumber + " 場進行中");
        setStatus("比賽開始！" + horseCount + " 匹馬正在各自的執行緒中奔跑。", false);
        controller.startRace(horseCount);
        repaintTimer.start();
    }

    @Override
    public void onRaceStarted(final List<HorseSnapshot> horses) {
        dispatchOnEdt(new Runnable() {
            @Override public void run() {
                racePanel.setSnapshots(horses);
            }
        });
    }

    @Override
    public void onFirstHorseFinished(final int horseId) {
        dispatchOnEdt(new Runnable() {
            @Override public void run() {
                if (!displayedRaceComplete) {
                    setStatus(horseId + " 號馬率先抵達！其餘馬匹已自動進入有限次 20% 加速模式。", true);
                }
            }
        });
    }

    @Override
    public void onHorseFinished(int horseId, int place, final List<Integer> ranking) {
        dispatchOnEdt(new Runnable() {
            @Override public void run() {
                updateRanking(ranking);
            }
        });
    }

    @Override
    public void onRaceFinished(final List<Integer> ranking) {
        dispatchOnEdt(new Runnable() {
            @Override public void run() {
                repaintTimer.stop();
                displayedRaceComplete = true;
                racePanel.setSnapshots(controller.getSnapshots());
                updateRanking(ranking);
                horseCountSpinner.setEnabled(true);
                startButton.setEnabled(true);
                startButton.setText("再賽一場");
                raceNumberLabel.setText("第 " + raceNumber + " 場完成");
                setStatus("全部馬匹完賽！冠軍是 " + ranking.get(0) + " 號馬。", false);
            }
        });
    }

    @Override
    public void onRaceFailed(final String message) {
        dispatchOnEdt(new Runnable() {
            @Override public void run() {
                repaintTimer.stop();
                horseCountSpinner.setEnabled(true);
                startButton.setEnabled(true);
                setStatus("比賽已停止：" + message, true);
                JOptionPane.showMessageDialog(RaceFrame.this, message, "比賽錯誤", JOptionPane.ERROR_MESSAGE);
            }
        });
    }

    private void updateRanking(List<Integer> ranking) {
        if (ranking.size() < displayedRankingCount) {
            return;
        }
        rankingItems.removeAll();
        displayedRankingCount = ranking.size();
        for (int index = 0; index < ranking.size(); index++) {
            JLabel item = new JLabel((index + 1) + ".  " + ranking.get(index) + " 號馬");
            item.setOpaque(true);
            item.setFont(uiFont(index == 0 ? Font.BOLD : Font.PLAIN, 13));
            item.setForeground(index == 0 ? new Color(133, 77, 14) : TEXT);
            item.setBackground(index == 0 ? new Color(255, 244, 204) : new Color(238, 242, 247));
            item.setBorder(new EmptyBorder(5, 9, 5, 9));
            rankingItems.add(item);
        }
        rankingItems.revalidate();
        rankingItems.repaint();
    }

    private void setStatus(String text, boolean highlight) {
        statusLabel.setText(text);
        JPanel parent = (JPanel) statusLabel.getParent();
        parent.setBackground(highlight ? PALE_ORANGE : PALE_GREEN);
        statusLabel.setForeground(highlight ? new Color(154, 73, 7) : new Color(27, 94, 63));
    }

    static void dispatchOnEdt(Runnable action) {
        if (SwingUtilities.isEventDispatchThread()) {
            action.run();
        } else {
            SwingUtilities.invokeLater(action);
        }
    }

    void startRaceForCapture(int horseCount) {
        horseCountSpinner.setValue(horseCount);
        startSelectedRace();
    }

    void setHorseCountForCapture(int horseCount) {
        horseCountSpinner.setValue(horseCount);
    }

    boolean isRaceRunningForCapture() {
        return controller.isRunning();
    }

    boolean isRaceCompleteVisibleForCapture(int expectedHorseCount) {
        return displayedRaceComplete && displayedRankingCount == expectedHorseCount;
    }

    int getFinishedCountForCapture() {
        return controller.getFinishedCount();
    }

    boolean isBoostVisibleForCapture() {
        return displayedRankingCount > 0 && displayedBoosting;
    }

    private static boolean containsBoostingHorse(List<HorseSnapshot> snapshots) {
        for (HorseSnapshot snapshot : snapshots) {
            if (snapshot.isBoosting()) {
                return true;
            }
        }
        return false;
    }

    void captureContent(Path target) throws IOException {
        if (!SwingUtilities.isEventDispatchThread()) {
            throw new IllegalStateException("Screenshots must be captured on the EDT");
        }
        Dimension size = getContentPane().getSize();
        BufferedImage image = new BufferedImage(size.width, size.height, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics = image.createGraphics();
        try {
            graphics.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            getContentPane().printAll(graphics);
        } finally {
            graphics.dispose();
        }
        Files.createDirectories(target.getParent());
        ImageIO.write(image, "png", target.toFile());
    }

    void shutdownForCapture() {
        repaintTimer.stop();
        controller.stopRace();
        dispose();
    }

    private static Font uiFont(int style, int size) {
        return new Font("Microsoft JhengHei", style, size);
    }
}
