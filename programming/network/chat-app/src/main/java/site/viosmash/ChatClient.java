package site.viosmash;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

public class ChatClient {

    private Socket socket;
    private String name;
    private Scanner inputStream;
    private DataOutputStream outputStream;
    private Scanner userInput;

    public ChatClient(Socket socket, String name) throws IOException {
        this.socket = socket;
        this.name = name;
        this.inputStream = new Scanner(socket.getInputStream());
        this.outputStream = new DataOutputStream(socket.getOutputStream());
    }


    public Socket getSocket() {
        return socket;
    }

    public DataOutputStream getOutputStream() {
        return outputStream;
    }

    public Scanner getInputStream() {
        return inputStream;
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

    public void setUserInput(Scanner userInput) {
        this.userInput = userInput;
    }

    public void start() {
        new Thread(() -> {
            while(true) {
//                System.out.print("Enter your message: ");
                String yourMessage = userInput.nextLine();
                try {
                    outputStream.writeBytes(yourMessage + "\nEND\n");
                    outputStream.flush();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }).start();
    }

    public static void main(String[] args) throws IOException {
        System.out.print("Enter your name: ");
        Scanner input = new Scanner(System.in);
        String name = input.nextLine();



        ChatClient client = new ChatClient(
                new Socket("localhost", 8080),
                name
        );

        client.setUserInput(input);
        client.outputStream.writeBytes(client.getName() + "\nEND\n");
        client.outputStream.flush();

        //start chatting
        client.start();


        //receive message from other clients
        while(true) {
            String message = "";
            while(client.inputStream.hasNextLine()) {
                message = client.inputStream.nextLine();
                if(!message.equals("END")) break;
            }
            System.out.println(message);
        }

    }

}
