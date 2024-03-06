import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.*;
import java.net.Socket;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.HashSet;

public class ClientHandler implements Runnable{
    private Socket clientSocket;
    private boolean isAsleep = false;
    private boolean keepRunning = true;
    private int currentRouteID;
    private int chunkSize;
    private SharedWaypointsArraylist SharedWaypoints;
    private List<WorkerHandler> workerHandlerList;
    private ArrayList<Interval> IntervalsDatabase;
    private int numOfWorkers;
    private ArrayList<Route> RoutesDatabase;
    private Master master;

    public ClientHandler(Socket clientSocket, int currentRouteID, int chunkSize,
                         SharedWaypointsArraylist SharedWaypoints,  List<WorkerHandler> workerHandlerList, int numOfWorkers,
                         ArrayList<Interval> IntervalsDatabase, ArrayList<Route> RoutesDatabase,  Master master){
        this.clientSocket = clientSocket;
        this.currentRouteID = currentRouteID;
        this.chunkSize = chunkSize;
        this.SharedWaypoints = SharedWaypoints;
        this.workerHandlerList = workerHandlerList;
        this.numOfWorkers = numOfWorkers;
        this.IntervalsDatabase = IntervalsDatabase;
        this.RoutesDatabase = RoutesDatabase;
        this.master = master;
    }

    @Override
    public void run(){

        boolean exitCode = false;
        ObjectInputStream clientIn = null;
        ObjectOutputStream clientOut = null;
        try {
            clientIn = new ObjectInputStream(clientSocket.getInputStream());
            clientOut = new ObjectOutputStream(clientSocket.getOutputStream());
            InputStream gpxInputStream = clientSocket.getInputStream();

            while (!exitCode) {

                // Reads User Option
                String userOption = clientIn.readUTF();

                if (userOption.equals("submit")) { // Submit New Route Button
                    try {

                        // Read User ID
                        int currentRouteUserID = clientIn.readInt();

                        // Total Users Count
                        boolean userExists = false;
                        synchronized (RoutesDatabase) {
                            for(Route route : RoutesDatabase){
                            if(currentRouteUserID == route.getUserID()){
                                userExists = true;
                                break;
                            }
                        }}
                        if(!userExists){
                            master.addUser();
                        }

                        // Preparations to read .gpx file
                        File gpxFile = new File("newRoute.gpx");
                        FileOutputStream fileOutputStream = new FileOutputStream(gpxFile);
                        byte[] buffer = new byte[1024];
                        DataInputStream dataInputStream = new DataInputStream(gpxInputStream);
                        long fileSize = dataInputStream.readLong();
                        long totalBytesRead = 0;
                        int bytesRead;

                        // Reads .gpx file
                        while (totalBytesRead < fileSize) {
                            bytesRead = gpxInputStream.read(buffer);
                            if (bytesRead == -1) {
                                break;
                            }
                            fileOutputStream.write(buffer, 0, bytesRead);
                            totalBytesRead += bytesRead;
                        }
                        /*while ((bytesRead = gpxInputStream.read(buffer)) != -1) {
                            fileOutputStream.write(buffer, 0, bytesRead);
                        }*/
                        fileOutputStream.flush();
                        fileOutputStream.close();

                        // Preparations to decode .gpx file
                        ArrayList<Waypoint> WaypointsList = new ArrayList<>();
                        Document GPXDocument = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(gpxFile);
                        GPXDocument.getDocumentElement().normalize();
                        NodeList wptList = GPXDocument.getElementsByTagName("wpt");
                        SimpleDateFormat timeFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");

                        // Decodes .gpx file
                        for (int i = 0; i < wptList.getLength(); i++) {
                            Element wpt = (Element) wptList.item(i);
                            double lat = Double.parseDouble(wpt.getAttribute("lat"));
                            double lon = Double.parseDouble(wpt.getAttribute("lon"));
                            double ele = Double.parseDouble(wpt.getElementsByTagName("ele").item(0).getTextContent());
                            String timeStr = wpt.getElementsByTagName("time").item(0).getTextContent();
                            Date time = timeFormat.parse(timeStr);
                            WaypointsList.add(new Waypoint(i, master.getCurrentRouteID(), currentRouteUserID, lat, lon, ele, time));
                        }

                        SharedWaypoints.setList(WaypointsList);
                        int index = 0;
                        while (!SharedWaypoints.isEmpty()) {
                            // Wait for thread to sleep before waking it up
                            while (!workerHandlerList.get(index).isAsleep()) {
                                try {
                                    Thread.sleep(100);
                                } catch (InterruptedException e) {
                                    e.printStackTrace();
                                }
                            }
                            workerHandlerList.get(index).wakeUp();
                            // Thread will go on with its processes and then again go to sleep inside its run

                            // We wait for thread to finish processing
                            while (!workerHandlerList.get(index).isAsleep()) {
                                try {
                                    Thread.sleep(100);
                                } catch (InterruptedException e) {
                                    e.printStackTrace();
                                }
                            }
                            index++;
                            if (index == numOfWorkers) {
                                index = 0;
                            }
                        }

                        // Test Print - Intervals Received From Each Worker
                        synchronized (IntervalsDatabase) {System.out.println("----- Intervals Received from Workers -----");
                        for (Interval interval : IntervalsDatabase) {
                            System.out.println("Interval's Route ID: " + interval.getRouteID());
                            System.out.println("Interval's User ID: " + interval.getUserID());
                            System.out.println("Interval's Distance: " + interval.getDistance());
                            System.out.println("Interval's Elevation Gain: " + interval.getElevationGain());
                            System.out.println("Interval's Duration: " + interval.getDuration());
                            System.out.println("Interval's Average Speed: " + interval.getAverageSpeed());
                            System.out.println();
                        }}

                        // Adds the current route data into the database
                        synchronized (RoutesDatabase){RoutesDatabase.add(CalculateRouteData(IntervalsDatabase, master.getCurrentRouteID(), currentRouteUserID));}

                        // Send Data
                        clientOut.writeUTF(CalculateRouteData(IntervalsDatabase, master.getCurrentRouteID(), currentRouteUserID).toString());
                        clientOut.flush();

                        // Increment the currentRouteID for the next route submission
                        master.incrementCurrentRouteID();

                    } catch (IOException e) {
                        e.printStackTrace();
                        try {
                            clientOut.writeUTF("Error Processing Route...");
                            clientOut.flush();
                        } catch (IOException ioException) {
                            ioException.printStackTrace();
                        }
                    } catch (ParserConfigurationException e) {
                        throw new RuntimeException(e);
                    } catch (ParseException e) {
                        throw new RuntimeException(e);
                    } catch (SAXException e) {
                        throw new RuntimeException(e);
                    }

                } else if (userOption.equals("stats")) { // Statistics Button

                    // Reads and Checks for user ID
                    int printUserID = clientIn.readInt();
                    boolean flag = false;
                    synchronized (RoutesDatabase){
                        for (Route route : RoutesDatabase) {
                            if (printUserID == route.getUserID()) {
                                if (!flag) {
                                    flag = true;
                                    break;
                                }
                            }
                        }
                    }
                    clientOut.writeBoolean(flag);
                    clientOut.flush();

                    // Sends Statistical Data to client
                    if (flag){
                        String userData = CalculateUserData(printUserID, RoutesDatabase);
                        String percentageData = CalculatePercentageData(printUserID, RoutesDatabase);
                        clientOut.writeUTF(userData);
                        clientOut.flush();
                        clientOut.writeUTF(percentageData);
                        clientOut.flush();
                        String totalData = CalculateTotalData(RoutesDatabase);
                        clientOut.writeUTF(totalData);
                        clientOut.flush();;
                    }

                } else if (userOption.equals("exit")) { // Exit Button

                    exitCode = true;
                    clientIn.close();
                    clientOut.close();
                    clientSocket.close();
                } else {

                    //Send Invalid Input Message
                    clientOut.writeUTF("Invalid option...");
                    clientOut.flush();
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    // Calculate, print and return route's data
    synchronized Route CalculateRouteData(ArrayList<Interval> IntervalsDatabase, int currentRouteID, int currentRouteUserID){

        double currentRouteDistance = 0;
        double currentRouteElevationGain = 0;
        double currentRouteDuration = 0;

        for (Interval interval : IntervalsDatabase) {
            if (interval.getRouteID() == currentRouteID) {
                currentRouteDistance = currentRouteDistance + interval.getDistance();
                currentRouteElevationGain = currentRouteElevationGain + interval.getElevationGain();
                currentRouteDuration = currentRouteDuration + interval.getDuration();
            }
        }

        // Test Print - Route data calculated from intervals
        System.out.println("----- Current Route's Data -----");
        System.out.println("User ID: " + currentRouteUserID);
        System.out.println("Route ID: " + currentRouteID);
        System.out.println("Distance: " + currentRouteDistance + " meters");
        System.out.println("Elevation Gain: " + currentRouteElevationGain + " meters");
        System.out.println("Duration: " + currentRouteDuration + " seconds");
        System.out.println("Average Speed: " + (currentRouteDistance/currentRouteDuration) + " meters/second");
        System.out.println();

        return new Route(currentRouteUserID, currentRouteDistance, currentRouteElevationGain, currentRouteDuration, currentRouteDistance/currentRouteDuration);
    }

    // Statistics -> User Data Box
     synchronized String CalculateTotalData(ArrayList<Route> RoutesDatabase) {
        double totalRouteDistance = 0;
        double totalRouteElevationGain = 0;
        double totalRouteDuration = 0;
        StringBuilder returnString = new StringBuilder();

        for (Route route : RoutesDatabase) {
            totalRouteDistance += route.getDistance();
            totalRouteElevationGain += route.getElevationGain();
            totalRouteDuration += route.getDuration();
        }

        //Correct Format For Android
        returnString.append(master.getUserCount()).append(" Users").append("-----").append("-----");
        returnString.append(String.format("%.2f",totalRouteDistance / 1000)).append("-----").append("Distance(km)").append("-----");
        returnString.append(String.format("%.2f",totalRouteElevationGain)).append("-----").append("Elevation Gain(m)").append("-----");
        returnString.append(String.format("%.2f",totalRouteDuration / 60)).append("-----").append("Duration(min)").append("-----");
        returnString.append(String.format("%.2f",(totalRouteDuration / 60) / (totalRouteDistance / 1000))).append("-----").append("Pace(min/km)").append("-----");

        return returnString.toString();
    }

    // Statistics -> Global Data Box
     synchronized String CalculateUserData(int printUserID, ArrayList<Route> RoutesDatabase) {
        double userDistance = 0;
        double userDuration = 0;
        double userElevationGain = 0;
        StringBuilder returnString = new StringBuilder();

        for (Route route : RoutesDatabase) {
            if (printUserID == route.getUserID()) {
                userDistance += route.getDistance();
                userElevationGain += route.getElevationGain();
                userDuration += route.getDuration();
            }
        }

        //Correct Format For Android
        returnString.append("User ID → ").append(printUserID).append("-----").append("-----");
        returnString.append(String.format("%.2f",userDistance / 1000)).append("-----").append("Distance(km)").append("-----");
        returnString.append(String.format("%.2f",userElevationGain)).append("-----").append("Elevation Gain(m)").append("-----");
        returnString.append(String.format("%.2f",userDuration / 60)).append("-----").append("Duration(min)").append("-----");
        returnString.append(String.format("%.2f",(userDuration / 60) / (userDistance / 1000))).append("-----").append("Pace(min/km)").append("-----");

        return returnString.toString();
    }

    // Statistics -> Statistics Percentages Box (This implementation shows the percentages of the selected user's total data to al the other user's total data in average)
     synchronized String CalculatePercentageData (int selectedUserID, ArrayList<Route> RoutesDatabase) {

        double selectedUser_avgRouteDistance = 0;
        double selectedUser_avgElevationGain = 0;
        double selectedUser_avgDuration = 0;

        double otherUser_totalRouteDistance = 0;
        double otherUser_totalElevationGain = 0;
        double otherUser_totalDuration = 0;

        double usersAverage_totalRouteDistance = 0;
        double usersAverage_totalElevationGain = 0;
        double usersAverage_totalDuration = 0;

        StringBuilder returnString = new StringBuilder();

        ArrayList<Integer> uniqueIDs = new ArrayList<>();
        HashSet<Integer> addedIDs = new HashSet<>();

        for (Route route : RoutesDatabase) {
            int userID = route.getUserID();

            if (!addedIDs.contains(userID)) {
                uniqueIDs.add(userID);
                addedIDs.add(userID);
            }
        }
        int userRouteCounter = 0;

        //uniqueIDs has all the users IDs
        for(int currentID : uniqueIDs){
            for (Route route : RoutesDatabase) {
                if (currentID == route.getUserID()) {

                    if(currentID == selectedUserID){ // Total Data of the Selected User
                        selectedUser_avgRouteDistance += route.getDistance();
                        selectedUser_avgElevationGain += route.getElevationGain();
                        selectedUser_avgDuration += route.getDuration();

                        userRouteCounter++;

                    } else { // Total Data of Other User
                        otherUser_totalRouteDistance += route.getDistance();
                        otherUser_totalElevationGain += route.getElevationGain();
                        otherUser_totalDuration += route.getDuration();
                    }
                }
            }
            usersAverage_totalRouteDistance += otherUser_totalRouteDistance;
            usersAverage_totalElevationGain += otherUser_totalElevationGain;
            usersAverage_totalDuration += otherUser_totalDuration;

            otherUser_totalRouteDistance = 0;
            otherUser_totalElevationGain = 0;
            otherUser_totalDuration = 0;
        }

        selectedUser_avgRouteDistance = selectedUser_avgRouteDistance / userRouteCounter;
        selectedUser_avgElevationGain = selectedUser_avgElevationGain / userRouteCounter;
        selectedUser_avgDuration = selectedUser_avgDuration / userRouteCounter;

        if(master.getUserCount() > 1){ //if we have more than 1 user calculate global average data
            usersAverage_totalRouteDistance = usersAverage_totalRouteDistance / (master.getCurrentRouteID() - 1 - userRouteCounter);
            usersAverage_totalElevationGain = usersAverage_totalElevationGain / (master.getCurrentRouteID() - 1 - userRouteCounter);
            usersAverage_totalDuration = usersAverage_totalDuration / (master.getCurrentRouteID() -1 - userRouteCounter);
        } else {
            usersAverage_totalRouteDistance = selectedUser_avgRouteDistance;
            usersAverage_totalElevationGain = selectedUser_avgElevationGain;
            usersAverage_totalDuration = selectedUser_avgDuration;
        }

        returnString.append(String.format("%.2f",selectedUser_avgRouteDistance/1000)).append(String.format("%.2f",selectedUser_avgElevationGain)).append(String.format("%.2f",selectedUser_avgDuration/60)).append(String.format("%.2f",usersAverage_totalRouteDistance/1000)).append(String.format("%.2f",usersAverage_totalElevationGain)).append(String.format("%.2f",usersAverage_totalDuration/60));

        double DistancePercentage = 100 - (selectedUser_avgRouteDistance * 100) / usersAverage_totalRouteDistance;
        double DurationPercentage = 100 - (selectedUser_avgDuration * 100) / usersAverage_totalDuration;
        double ElevationPercentage = 100 - (selectedUser_avgElevationGain * 100) / usersAverage_totalElevationGain;

        //Correct Format For Android
        if (DistancePercentage > 0) {
            returnString.append("• Distance ").append(String.format("%.1f",DistancePercentage)).append("% less than global average").append("\n");
        } else if (DistancePercentage < 0) {
            DistancePercentage *= -1;
            returnString.append("• Distance ").append(String.format("%.1f",DistancePercentage)).append("% more than global average").append("\n");
        } else {
            returnString.append("• Distance same as the global").append("\n");
        }
        if (DurationPercentage > 0) {
            returnString.append("• Duration ").append(String.format("%.1f",DurationPercentage)).append("% less than global average").append("\n");
        } else if (DurationPercentage < 0) {
            DurationPercentage *= -1;
            returnString.append("• Duration ").append(String.format("%.1f",DurationPercentage)).append("% more than global average").append("\n");
        } else {
            returnString.append("• Duration same as global").append("\n");
        }
        if (ElevationPercentage > 0) {
            returnString.append("• Elevation Gain ").append(String.format("%.1f",ElevationPercentage)).append("% less than global average");
        } else if (ElevationPercentage < 0) {
            ElevationPercentage *= -1;
            returnString.append("• Elevation Gain ").append(String.format("%.1f",ElevationPercentage)).append("% more than global average");
        } else {
            returnString.append("• Elevation Gain same as global");
        }
        return returnString.toString();
    }
}
