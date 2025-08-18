package site.viosmash;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ChatServer {
    private int port;
    private ServerSocket serverSocket;
    private List<ChatClient> clients;


    public ChatServer(int port) throws IOException {
        this.serverSocket = new ServerSocket(port);
        this.clients = new ArrayList<>();
        this.port = port;
    }


    public void listening() throws IOException {
        System.out.println("===============Server listening at port: " + port + "==================");
        while(true) {
            Socket socket = serverSocket.accept();
            new Thread(() -> {
                try {
                    System.out.println("socket: " + socket);
                    Scanner inputStream = new Scanner(socket.getInputStream());
                    DataOutputStream outputStream = new DataOutputStream(socket.getOutputStream());
                    String clientName = "";
                    while(inputStream.hasNextLine()) {
                        clientName = inputStream.nextLine();
                        if(!clientName.equals("END")) break;
                    }
                    ChatClient client = new ChatClient(socket, clientName);
                    System.out.println("[+]New member join: " + clientName + " [+]");
                    String message = "You have joined group\nEND\n";
                    outputStream.writeBytes(message);
                    outputStream.flush();
                    clients.add(client);

                    //notify to all other client except current user, new user join
                    notifyAllUser(
                            clients,
                            String.format("[+]New member join: %s [+]\nEND\n", clientName),
                            clientName);

                    //read chat message from current socket
                    while (true) {
                        String chatMessage = "";
                        while(inputStream.hasNextLine()) {
                            chatMessage = inputStream.nextLine();
                            if(!chatMessage.equals("END")) break;
                        }

                        notifyAllUser(
                                clients,
                                String.format("%s: %s\nEND\n", clientName, chatMessage),
                                clientName);
                    }

                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }).start();
        }
    }

    private void notifyAllUser(List<ChatClient> clients, String message, String exclusiveClientName) {
        clients.forEach(client -> {
            if(!client.getName().equals(exclusiveClientName)) {
                try {
                    client.getOutputStream().writeBytes(message);
                    client.getOutputStream().flush();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        });

    }

    public int getPort() {
        return port;
    }

    public ServerSocket getServerSocket() {
        return serverSocket;
    }

    public List<ChatClient> getClients() {
        return clients;
    }


    public static void main(String[] args) throws IOException {
        new ChatServer(8080).listening();
    }
}
