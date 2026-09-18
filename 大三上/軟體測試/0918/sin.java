public class Sin {

    public static void main(String[] args) {
        Sin s = new Sin();

        System.out.println("The value of sin(30')");
        System.out.println(s.sin(Math.PI / 6.0));
    }

    public double sin(double x) {
        int n = 2;
        int inc = 3;
        double stop = 0.0000001;

        double s1 = sin(x, n);

        n = n + inc;
        double s2 = sin(x, n);

        while (Math.abs(s2 - s1) >= stop) {
            s1 = s2;
            n = n + inc;
            s2 = sin(x, n);
        }

        return s2;
    }

    double sin(double x, int n) {
        double v = x;
        int positive = -1;

        for (int i = 1; i < n; i++) {
            v = v + positive * (Math.pow(x, 2 * i + 1) / factorial(2 * i + 1));

            positive = positive * -1;
        }

        return v;
    }

    double factorial(double s) {
        double r = 1;

        for (int i = 1; i <= s; i++) {
            r = r * i;
        }

        return r;
    }
}
