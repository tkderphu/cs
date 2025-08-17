package site.viosmash.ex1;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class ClientMain {
    public static void main(String[] args) throws IOException {
        Client client = new Client("phu", "localhost", 8787);
        BufferedReader reader = new BufferedReader(
                new InputStreamReader(client.getSocket().getInputStream(), StandardCharsets.UTF_8)
        );

        StringBuilder fullMessage = new StringBuilder();
        String line;

        while ((line = reader.readLine()) != null) {
            if (line.equals("END")) break; // Stop when end marker received
            fullMessage.append(line).append("\n");
        }

        System.out.println("Received:\n" + fullMessage.toString());

        System.out.println("Choose options: ");

        DataOutputStream dataOutputStream = new DataOutputStream(client.getSocket().getOutputStream());
        Scanner sx = new Scanner(System.in);

        int choice = sx.nextInt();

        System.out.println("You have chosen options: " + choice);

        dataOutputStream.writeInt(choice);
        dataOutputStream.flush();


//        System.out.println(new String(dataInputStream.readAllBytes()));
    }
}
