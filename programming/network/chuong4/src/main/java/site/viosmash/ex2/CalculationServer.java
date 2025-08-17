package site.viosmash.ex2;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class CalculationServer {
    private ServerSocket serverSocket;
    public CalculationServer(int port) throws IOException {
        serverSocket = new ServerSocket(port);
    }


    void serverListening() throws IOException {
        while(true) {
            Socket socket = serverSocket.accept();
            System.out.println(socket);
            new Thread(() -> {
                try {
                    String message = "Solve quadratic equaltion: a.x^2 + b.x + c.\n" +
                            "Please enter a, b, c.\n" +
                            "END\n";
                    DataInputStream dataInputStream = new DataInputStream(socket.getInputStream());
                    DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());

                    dataOutputStream.writeBytes(message);
                    dataOutputStream.flush();

                    int a = dataInputStream.readInt();
                    int b = dataInputStream.readInt();
                    int c = dataInputStream.readInt();

                    Pair pair = calculate(a, b, c);

                    dataOutputStream.writeBytes("result: " + pair + "\nEND\n");
                    dataOutputStream.flush();
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }).start();
        }
    }

    /**
     * quadratic equation: a.x^2 + bx + c
     * delta = b^2 - 4ac
     *
     * x = (-b +[-] (sqrt(delta))/2a
     * @param a
     * @param b
     * @param c
     * @return
     */
    public Pair calculate(int a, int b, int c) {
        float delta = b * b - 4 * a* c;
        if(delta == 0) {
            Pair pair = new Pair(-b*1.0/(2*a), -b*1.0/(2*a));
            return pair;
        } else if(delta < 0) {
    return null;
        } else {
            Pair pair = new Pair(
                    (-b + Math.sqrt(delta))/(2 * a),
                    (-b - Math.sqrt(delta))/(2 * a)
            );

            return pair;
        }

    }

}
