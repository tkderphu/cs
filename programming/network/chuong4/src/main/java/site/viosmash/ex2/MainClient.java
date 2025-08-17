package site.viosmash.ex2;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

public class MainClient {
    public static void main(String[] args) throws IOException {
        Socket socket = new Socket("localhost", 8787);

        Scanner scanner = new Scanner(socket.getInputStream());
        DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());

        while(scanner.hasNextLine()) {
            String line = scanner.nextLine();
            if(line.equals("END")) break;
            System.out.println(line);
        }

        Scanner input = new Scanner(System.in);
        System.out.println("A = ");
        int a = input.nextInt();
        System.out.println("B = ");
        int b = input.nextInt();
        System.out.println("C = ");
        int c = input.nextInt();


        dataOutputStream.writeInt(a);
        dataOutputStream.writeInt(b);
        dataOutputStream.writeInt(c);

        dataOutputStream.flush();


        while(scanner.hasNextLine()) {
            String line = scanner.nextLine();
            if(line.equals("END")) break;
            System.out.println(line);
        }

    }
}
