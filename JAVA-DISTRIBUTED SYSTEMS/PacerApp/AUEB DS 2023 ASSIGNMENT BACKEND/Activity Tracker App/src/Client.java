import java.net.*;
import java.util.*;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Client {
    private static final String MASTER_IP = "localhost"; //set manually
    private static final int MASTER_PORT = 6000; //set manually

    public static void main(String[] args) {
        new Client().startClient();
    }

    void startClient() {
        try {

            // Client initializes a socket and open the required streams
            Socket clientSocket = new Socket(MASTER_IP, MASTER_PORT);
            ObjectOutputStream out = new ObjectOutputStream(clientSocket.getOutputStream());
            ObjectInputStream in = new ObjectInputStream(clientSocket.getInputStream());
            OutputStream outputStream = clientSocket.getOutputStream();

            Scanner scanner = new Scanner(System.in);
            int userOption = -1;

            //Welcome Message
            String serverResponseWelcome = in.readUTF();
            System.out.println(serverResponseWelcome);

            while (userOption != 0) {

                //Menu Message
                String serverResponseMenu = in.readUTF();
                System.out.println(serverResponseMenu);

                userOption = scanner.nextInt();

                out.writeInt(userOption);
                out.flush();

                if (userOption == 1){ // Submit New Route

                    try {

                        //Enter ID Message
                        String serverResponseEnterID = in.readUTF();
                        System.out.println(serverResponseEnterID);

                        int currentRouteUserID = scanner.nextInt();

                        // Send User ID
                        out.writeInt(currentRouteUserID);
                        out.flush();

                        // Send .gpx file
                        String GPXFileName = null;
                        boolean gpxFileNameValid = false;
                        while (!gpxFileNameValid) {
                            //Enter GPX Message
                            String serverResponseEnterGPX = in.readUTF();
                            System.out.println(serverResponseEnterGPX);

                            GPXFileName = scanner.next();
                            Path gpxFilePath = Paths.get(GPXFileName);
                            if (Files.exists(gpxFilePath) && GPXFileName.toLowerCase().endsWith(".gpx")) {
                                gpxFileNameValid = true;
                                out.writeBoolean(gpxFileNameValid);
                                out.flush();

                                File gpxFile = new File(GPXFileName);
                                FileInputStream fileInputStream = new FileInputStream(gpxFile);

                                // Send the file size
                                long fileSize = gpxFile.length();
                                DataOutputStream dataOutputStream = new DataOutputStream(outputStream);
                                dataOutputStream.writeLong(fileSize);
                                dataOutputStream.flush();

                                byte[] buffer = new byte[1024];
                                int bytesRead;
                                while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                                    outputStream.write(buffer, 0, bytesRead);
                                }
                                fileInputStream.close();
                                outputStream.flush();

                            } else {
                                System.err.println(GPXFileName + " file could not be found...");
                                gpxFileNameValid = false;
                                out.writeBoolean(gpxFileNameValid);
                                out.flush();
                            }
                        }
                        System.out.println();

                        // Receive Data
                        String serverResponse = in.readUTF();
                        System.out.println(serverResponse);

                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                } else if (userOption == 2){ // Calculate Specific User Data

                    // Send User ID
                    String serverResponseEnterPrintID = in.readUTF();
                    System.out.println(serverResponseEnterPrintID);

                    int printUserID = scanner.nextInt();
                    out.writeInt(printUserID);
                    out.flush();

                    //Receive Data or Error Message
                    String userData = in.readUTF();
                    String PercentageData = in.readUTF();
                    System.out.println(userData);
                    System.out.println(PercentageData);

                } else if (userOption == 3) { // Calculate Total Users Data

                    //Receive Data or Error Message
                    String totalData = in.readUTF();
                    System.out.println(totalData);

                } else if (userOption == 0){ // Exit App

                    //Send Exit Message
                    String serverResponseExit = in.readUTF();
                    System.out.println(serverResponseExit);

                } else { // Invalid Menu Option

                    String serverResponseInvalidOption = in.readUTF();
                    System.out.println(serverResponseInvalidOption);
                    System.out.println();

                }
            }

            in.close();
            out.close();
            clientSocket.close();
            scanner.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}