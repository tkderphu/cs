package site.viosmash;

import java.io.*;
import java.util.Arrays;
import java.util.List;

public class E2 {
    static class FileCopy implements Runnable{
        private E1.Pair pair;

        public FileCopy(E1.Pair pair) {
            this.pair = pair;
        }

        @Override
        public void run() {
            File file = new File(pair.file);
            File newFile = new File(file.getName());

            if(!newFile.exists()) {
                try {
                    newFile.createNewFile();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            FileOutputStream fos = null;
            try {
                fos = new FileOutputStream(newFile);
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }
            FileInputStream fis = null;
            try {
                fis = new FileInputStream(file);
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }


            BufferedInputStream bufferedInputStream = new BufferedInputStream(fis);
            BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(fos);

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

            try {
                Thread.sleep(pair.timeMiniSecond);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            System.out.println(String.format("File '%s' copied successfully at: " + System.currentTimeMillis(), file.getName()));
        }
    }

    public static void main(String[] args) {
        String small =  "C:\\Users\\FPT\\Downloads\\[Vietsub] TURNS - LIONZED (Bây Giờ Mình Gặp Nhau Đi Ost -Let's Meet Now Ost).mp3";
        String medium = "C:\\Users\\FPT\\Downloads\\Homenaje a Tim Bergling  Tributo a Avicii (1989 - 2018)  Mix Mejores Canciones  Q.D.E.P.mp3";
        String large = "D:\\WorkSpaceD\\Music\\Nhạc Nhật Bản Không Lời Hay Nhất - Nhạc Anime Không Lời Nhẹ Nhàng Thư Giãn Cafe Piano Sâu Lắng.mp4";
        List<E1.Pair> paths = Arrays.asList(
                new E1.Pair(small, 2000),
                new E1.Pair(medium, 4000),
                new E1.Pair(large, 7000));


        for(int i = 0; i < paths.size(); i++) {
            Thread thread = new Thread(new FileCopy(paths.get(i)));
            thread.start();
        }
    }
}
