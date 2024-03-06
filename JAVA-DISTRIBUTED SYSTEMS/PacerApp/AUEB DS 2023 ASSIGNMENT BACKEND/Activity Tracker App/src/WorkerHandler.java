import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.StreamCorruptedException;
import java.net.Socket;
import java.net.SocketException;
import java.util.ArrayList;

class WorkerHandler implements Runnable{
    private Socket openSocket;
    private ArrayList<Interval> IntervalsDatabase;
    private SharedWaypointsArraylist SharedWaypoints;
    private Master master;
    private boolean isAsleep = false;
    private boolean keepRunning = true;

    public WorkerHandler(Socket openSocket, ArrayList<Interval> IntervalsDatabase, SharedWaypointsArraylist SharedWaypoints, Master master){
        this.openSocket = openSocket;
        this.IntervalsDatabase = IntervalsDatabase;
        this.SharedWaypoints = SharedWaypoints;
        this.master = master;
    }

    @Override
    public void run(){

        while(keepRunning) {
            synchronized (this) {
                goToSleep();
                // When we call wakeUp() from Master the thread goes on the next block of code
            }

            try {

                ObjectInputStream in = null;
                ObjectOutputStream out = null;

                while (!SharedWaypoints.isEmpty()) {

                    ArrayList<Waypoint> currentChunkList = SharedWaypoints.getWaypoints();

                    // Test Print
                    System.out.println("----- Waypoints Sent to Workers -----");
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

                    out = new ObjectOutputStream(openSocket.getOutputStream());
                    // Send to Worker ArrayList<Waypoint>
                    out.writeObject(currentChunkList);
                    out.flush();

                    in = new ObjectInputStream(openSocket.getInputStream());
                    // Receive from Worker
                    Interval chunkInterval = (Interval) in.readObject();

                    //Adds Interval to Database
                    addToIntervalsDatabase(IntervalsDatabase, chunkInterval);

                }

                // This if loop will be true when the exit code of the Master class is true
                if(master.getExitCode()){
                    stopRunning();
                    if (in != null) {
                        in.close();
                    }
                    if (out != null) {
                        out.close();
                    }
                    if (openSocket != null) {
                        openSocket.close();
                    }
                }

            } catch (SocketException se) {
                System.err.println("Connection was forcibly closed by the remote host: " + se.getMessage());
            } catch (StreamCorruptedException sce) {
                System.err.println("Error in object stream: " + sce.getMessage());
            } catch (IOException | ClassNotFoundException e) {
                System.err.println("Error handling object streams: " + e.getMessage());
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public void addToIntervalsDatabase(ArrayList<Interval> IntervalsDatabase, Interval chunkInterval) {
        synchronized(IntervalsDatabase){
            IntervalsDatabase.add(chunkInterval);
        }
    }

    public synchronized void goToSleep(){
        try{
            isAsleep = true;
            wait();
            isAsleep = false;
        }catch(InterruptedException ie){
            ie.printStackTrace();
        }
    }

    public synchronized void wakeUp(){
        notify();
    }

    public boolean isAsleep(){
        return isAsleep;
    }

    public void stopRunning(){keepRunning = false;}
}