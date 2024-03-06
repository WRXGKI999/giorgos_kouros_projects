import java.net.*;
import java.util.*;
import java.io.*;
import java.lang.*;

public class Master {
    private boolean exitCode = false;
    ServerSocket clientServerSocket;
    Socket clientConnection;
    private static final int WORKER_PORT = 5000; //Set Manually
    private static final int CLIENT_PORT = 6000; //Set Manually
    private static final int CHUNK_SIZE = 4; //Set Manually
    private static int NUM_OF_WORKERS = 1; //Set Manually
    private ArrayList<Interval> IntervalsDatabase = new ArrayList<>();
    private ArrayList<Route> RoutesDatabase;
    private int currentRouteID = 1;
    private int usersCount = 0;

    public static void main(String[] args){
        new Master().openMasterServer();
    }

    void openMasterServer() {
        try {

            RoutesDatabase = new ArrayList<>();

            // ----- Workers -----

            // Wait for all the workers to connect
            ConnectionHandler connectionPool = new ConnectionHandler(WORKER_PORT);
            connectionPool.acceptConnections(NUM_OF_WORKERS);

            // Keep a list with each runnable class to help with the implementation of round-robin
            List<WorkerHandler> workerHandlerList = new ArrayList<>();

            // Class with an ArrayList that can be shared between individual threads
            SharedWaypointsArraylist SharedWaypoints = new SharedWaypointsArraylist(CHUNK_SIZE);

            // Creates and starts the threads for each worker handler
            for(int i = 0; i<NUM_OF_WORKERS ; i++){
                Socket workerSocket = connectionPool.getConnection();
                WorkerHandler workerHandler = new WorkerHandler(workerSocket, IntervalsDatabase, SharedWaypoints, this);
                Thread thread = new Thread(workerHandler);

                workerHandlerList.add(workerHandler);

                thread.start();
                // The thread goes to sleep inside the run, so it now waits for notify() to wake up
            }

            // ----- Clients -----

            // Wait for all clients to connect
            try {
                List<Socket> clientSockets = Collections.synchronizedList(new LinkedList<>());
                clientServerSocket = new ServerSocket(CLIENT_PORT, 10);
                List<ClientHandler> clientHandlerList = new ArrayList<>();

                System.out.println("----- Waiting for Clients to connect -----");
                try {
                    //For each new client connection we start a thread
                    //The thread ServerClient contains all the needed functions to calculate the recommendations
                    while(true) {
                        clientConnection = clientServerSocket.accept();
                        System.out.println("Client connected: " + clientConnection.getRemoteSocketAddress());
                        ClientHandler clientHandler = new ClientHandler(clientConnection, currentRouteID,CHUNK_SIZE, SharedWaypoints,workerHandlerList, NUM_OF_WORKERS, IntervalsDatabase, RoutesDatabase, this);

                        Thread clientthread = new Thread(clientHandler);

                        clientHandlerList.add(clientHandler);

                        clientthread.start();
                    }
                } catch(SocketTimeoutException Ex) {
                    System.err.println("No client connection received!");
                }
                    // The thread goes to sleep inside the run, so it now waits for notify() to wake up
            } catch (IOException ioException) {
                ioException.printStackTrace();
            } finally {
                clientServerSocket.close();
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public synchronized boolean getExitCode(){
        return exitCode;
    }
    synchronized void incrementCurrentRouteID() {
        currentRouteID++;
    }
    synchronized void addUser() {
        usersCount++;
    }
    public synchronized int getUserCount(){
        return usersCount;
    }
    synchronized int getCurrentRouteID() {
        return currentRouteID;
    }
}