package site.viosmash.ex1;

import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        Server server = new Server(8787);
        server.listenClient();
    }
}
