package site.viosmash.ex1;

import java.io.IOException;
import java.net.Socket;
import java.util.UUID;

public class Client {
    private String id;
    private Socket socket;
    private String name;

    public Client(String name, String serverHost, int serverPort) throws IOException {
        this.id = UUID.randomUUID().toString();
        this.name = name;
        this.socket = new Socket(serverHost, serverPort);
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Socket getSocket() {
        return socket;
    }

    public void setSocket(Socket socket) {
        this.socket = socket;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

}
