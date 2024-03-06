import java.net.*;
import java.util.*;
import java.io.*;
import java.lang.*;
public class Worker extends Thread {
    private static final int PORT = 5000; // Set Manually
    private static final String IP = "localhost"; // Set Manually
    public static void main(String[] args) throws IOException {

        Socket requestSocket = new Socket(IP, PORT);
        System.out.println("Connected to the Master: " + requestSocket);
        System.out.println();

        ObjectInputStream in;

        while (true) {
            try {
                // Worker first opens a stream from the Master
                in = new ObjectInputStream(requestSocket.getInputStream());

                // Receive from Master ArrayList<Waypoint>
                ArrayList<Waypoint> currentChunkList = (ArrayList<Waypoint>) in.readObject();

                // Create a new thread to process the list of Waypoints
                new Thread(() -> processThread(currentChunkList, requestSocket)).start();

            } catch (UnknownHostException unknownHost) {
                System.err.println("You are trying to connect to an unknown host!");
            } catch (IOException ioException) {
                ioException.printStackTrace();
            } catch (ClassNotFoundException e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static void processThread(ArrayList<Waypoint> currentChunkList, Socket requestSocket) {
        System.out.println("New thread entry"); //debug tha to sbiso
        ObjectOutputStream out;
        ArrayList<Interval> IntervalsList = new ArrayList<>();
        int chunkRouteID;
        int chunkUserID;
        double chunkDistance = 0.0;
        double chunkElevationGain = 0.0;
        double chunkDuration = 0.0;
        double chunkAverageSpeed = 0.0;

        try {
            // Test Print
            System.out.println("----- Waypoints Received from Master -----");
            System.out.println();
            for(Waypoint wpt : currentChunkList){
                System.out.println("Waypoint's ID: " + wpt.getWaypointID());
                System.out.println("Waypoint's Route ID: " + wpt.getRouteID());
                System.out.println("Waypoint's User ID: " + wpt.getUserID());
                System.out.println("Waypoint's Latitude: " + wpt.getLatitude());
                System.out.println("Waypoint's Longitude: " + wpt.getLongitude());
                System.out.println("Waypoint's Elevation: " + wpt.getElevation());
                System.out.println();
            }

            chunkRouteID = currentChunkList.get(0).getRouteID();
            chunkUserID = currentChunkList.get(0).getUserID();

            // Calculate Chunk's data
            for (int i = 0; i < currentChunkList.size() - 1; i++) {
                IntervalsList.add(new Interval(chunkRouteID, chunkUserID, calculateDistance(currentChunkList.get(i), currentChunkList.get(i + 1)),
                        calculateElevationGain(currentChunkList.get(i), currentChunkList.get(i + 1)),
                        calculateDuration(currentChunkList.get(i), currentChunkList.get(i + 1)),
                        calculateAverageSpeed(currentChunkList.get(i), currentChunkList.get(i + 1))));

                chunkDistance += IntervalsList.get(i).getDistance();
                chunkElevationGain += IntervalsList.get(i).getElevationGain();
                chunkDuration += IntervalsList.get(i).getDuration();
                chunkAverageSpeed += IntervalsList.get(i).getAverageSpeed();
            }
            chunkAverageSpeed = chunkAverageSpeed / currentChunkList.size();

            Interval chunkInterval = new Interval(chunkRouteID, chunkUserID, chunkDistance, chunkElevationGain, chunkDuration, chunkAverageSpeed);

            // Worker then opens a stream to the Master
            out = new ObjectOutputStream(requestSocket.getOutputStream());

            // Send to Master Interval
            out.writeObject(chunkInterval);
            out.flush();

            // Test Print
            System.out.println("----- Interval Sent to Master -----");
            System.out.println();
            System.out.println("Interval's Route ID: " + chunkInterval.getRouteID());
            System.out.println("Interval's User ID: " + chunkInterval.getUserID());
            System.out.println("Interval's Distance: " + chunkInterval.getDistance());
            System.out.println("Interval's Elevation Gain: " + chunkInterval.getElevationGain());
            System.out.println("Interval's Duration: " + chunkInterval.getDuration());
            System.out.println("Interval's Average Speed: " + chunkInterval.getAverageSpeed());
            System.out.println();

        } catch (UnknownHostException unknownHost) {
            System.err.println("You are trying to connect to an unknown host!");
        } catch (IOException ioException) {
            ioException.printStackTrace();
        }
    }

    // Gets two WayPoint objects and return the distance between them in meters
    private synchronized static double calculateDistance(Waypoint wpt1, Waypoint wpt2){
        double latitude = Math.toRadians(wpt2.getLatitude() - wpt1.getLatitude());
        double longitude = Math.toRadians(wpt2.getLongitude() - wpt1.getLongitude());
        double aVariable = Math.sin(latitude / 2) * Math.sin(latitude / 2)
                + Math.cos(Math.toRadians(wpt2.getLatitude())) * Math.cos(Math.toRadians(wpt1.getLatitude()))
                * Math.sin(longitude / 2) * Math.sin(longitude / 2);
        double bVariable = 2 * Math.atan2(Math.sqrt(aVariable), Math.sqrt(1 - aVariable));
        return 6371.01 * bVariable * 1000;
    }

    // Gets two WayPoint objects and returns the elevation gain between them in meters. If there is elevation decline it returns 0
    private synchronized static double calculateElevationGain(Waypoint wpt1, Waypoint wpt2){
        double elevationGain;
        if(wpt2.getElevation() > wpt1.getElevation()){
            elevationGain = wpt2.getElevation() - wpt1.getElevation();
        }else{
            elevationGain = 0.0;
        }
        return elevationGain;
    }

    // Get two WayPoint objects and returns the duration between them in seconds
    private synchronized static double calculateDuration(Waypoint wpt1, Waypoint wpt2){
        Date time1 = wpt1.getTime();
        Date time2 = wpt2.getTime();
        long duration = (time2.getTime() - time1.getTime()) / 1000;
        return (double) duration;
    }

    // Gets two WayPoint objects and returns the average speed between them in meters/second
    private synchronized static double  calculateAverageSpeed(Waypoint wpt1, Waypoint wpt2){
        double distance = calculateDistance(wpt1, wpt2);
        double duration = calculateDuration(wpt1, wpt2);
        return distance / duration;
    }
}