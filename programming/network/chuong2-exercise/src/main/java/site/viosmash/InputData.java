package site.viosmash;

import java.io.*;
import java.net.URI;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Scanner;

public class InputData {
    public static void main(String[] args) throws IOException {
        //read
//        Scanner scanner = new Scanner(System.in);
//        Scanner scanner = new Scanner(new File("text.txt"));
//        Scanner scanner = new Scanner(Paths.get("chuong2-exercise/vc"));

//
//        BufferedInputStream bufferedInputStream = new BufferedInputStream(System.in);
//        byte[] xl = new byte[3];
//        bufferedInputStream.read(xl);
//        String vc = new String(xl);
//        System.out.println("vc: " + vc);

//        Reader reader = new InputStreamReader(System.in);
//        char[] tmp = new char[10];
//        reader.read(tmp);
//
//        System.out.println(String.valueOf(tmp));


        OutputStream fos = new FileOutputStream("text.txt");

        //write
        DataOutputStream outputStream = new DataOutputStream(fos);

        outputStream.writeBytes("hello guys");
        outputStream.flush();
    }
}
