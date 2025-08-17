package site.viosmash;

import java.io.*;
import java.util.Arrays;
import java.util.List;

public class E1 {
    static class Pair {
        String file;
        long timeMiniSecond;

        public Pair(String file, long timeMiniSecond) {
            this.file = file;
            this.timeMiniSecond = timeMiniSecond;
        }
    }
    public static void main(String[] args) throws IOException, InterruptedException {
        String small =  "C:\\Users\\FPT\\Downloads\\[Vietsub] TURNS - LIONZED (Bây Giờ Mình Gặp Nhau Đi Ost -Let's Meet Now Ost).mp3";
        String medium = "C:\\Users\\FPT\\Downloads\\Homenaje a Tim Bergling  Tributo a Avicii (1989 - 2018)  Mix Mejores Canciones  Q.D.E.P.mp3";
        String large = "D:\\WorkSpaceD\\Music\\Nhạc Nhật Bản Không Lời Hay Nhất - Nhạc Anime Không Lời Nhẹ Nhàng Thư Giãn Cafe Piano Sâu Lắng.mp4";
        List<Pair> paths = Arrays.asList(
                new Pair(small, 2000),
                new Pair(medium, 4000),
                new Pair(large, 7000));

        long start = System.currentTimeMillis();

        for(int i = 0; i < paths.size(); i++) {
            File file = new File(paths.get(i).file);
            File newFile = new File(file.getName());

            if(!newFile.exists()) {
                newFile.createNewFile();
            }
            FileOutputStream fos = new FileOutputStream(newFile);
            FileInputStream fis = new FileInputStream(file);



            BufferedInputStream bufferedInputStream = new BufferedInputStream(fis);
            BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(fos);

            byte[] buffer = new byte[1024];
            int bytesRead;

            while ((bytesRead = bufferedInputStream.read(buffer)) != -1) {
                bufferedOutputStream.write(buffer, 0, bytesRead);
            }

            Thread.sleep(paths.get(i).timeMiniSecond);
            System.out.println(String.format("File '%s' copied successfully at: " + System.currentTimeMillis(), file.getName()));
        }

        long end = System.currentTimeMillis();

        double seconds = (end - start)/1000;
        System.out.println("Completed seconds: " + seconds);
    }
}
