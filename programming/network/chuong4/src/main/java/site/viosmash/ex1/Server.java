package site.viosmash.ex1;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;

public class Server {
    private ServerSocket serverSocket;
    private int port;
    private File[] files;
    private List<Socket> clients;
    public Server(int port) {
        try {
            this.port = port;
            serverSocket = new ServerSocket(port);
            Path path = Paths.get("./server");
            File file = new File(path.toUri());
            this.files = file.listFiles();
            this.clients = new ArrayList<>();
        } catch (Exception ex) {
            ex.printStackTrace();

        }
    }

    public void listenClient() throws IOException {
        System.out.println("Server listening at port: " + port);
        while(true) {
            Socket socket = serverSocket.accept();
            System.out.println("New socket coming: " + socket);
            clients.add(socket);

            DataInputStream dataInputStream = new DataInputStream(socket.getInputStream());
            DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());

            dataOutputStream.writeBytes(showScreen());
            dataOutputStream.writeBytes("END\n"); // Send a known marker
            dataOutputStream.flush();
            System.out.println("fuck");
            int choice = dataInputStream.readInt();
            System.out.println("fuck2");
            for(int i = 0; i < files.length; i++) {
                if(choice == i + 1) {
                    File file = files[i];
                    File copyFile = new File("./client/" + file.getName());
                    BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream(file));
                    BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(new FileOutputStream(copyFile));

                    byte[] buffer = new byte[1024];
                    int bytesRead;

                    while (true) {
                        try {
                            if (!((bytesRead = bufferedInputStream.read(buffer)) != -1)) break;
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                        try {
                            bufferedOutputStream.write(buffer, 0, bytesRead);
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    }
                    System.out.println(String.format("File '%s' copied successfully at: " + System.currentTimeMillis(), file.getName()));
                    dataOutputStream.writeBytes(String.format("File '%s' copied successfully at: " + System.currentTimeMillis(), file.getName()));
                    dataOutputStream.flush();
                    break;
                }
            }


        }
    }


    public String showScreen() {
        String vcl = "===========================Server message=======================\n" +
                "Copy file from server: \n";

        for(int i = 0; i < files.length; i++) {
            String f = String.format("%d. %s", i + 1, files[i].getName());
            vcl += f + "\n";
        }

        return vcl;
    }

    public ServerSocket getServerSocket() {
        return serverSocket;
    }

    public void setServerSocket(ServerSocket serverSocket) {
        this.serverSocket = serverSocket;
    }

    public File[] getFiles() {
        return files;
    }

    public void setFiles(File[] files) {
        this.files = files;
    }
}
