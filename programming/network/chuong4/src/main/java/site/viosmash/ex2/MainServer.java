package site.viosmash.ex2;

import java.io.IOException;

public class MainServer {
    public static void main(String[] args) throws IOException {
        new CalculationServer(8787).serverListening();
    }
}
