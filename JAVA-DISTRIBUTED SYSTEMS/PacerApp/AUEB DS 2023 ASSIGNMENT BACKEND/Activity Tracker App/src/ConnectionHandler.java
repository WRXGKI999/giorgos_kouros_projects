import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
public class ConnectionHandler {
    private List<Socket> workersSockets;
    private ServerSocket serverSocket;

    public ConnectionHandler(int PORT) throws IOException{
        workersSockets = Collections.synchronizedList(new LinkedList<>());
        serverSocket = new ServerSocket(PORT, 10);
    }

    public void acceptConnections(int NUM_OF_WORKERS) throws IOException {
        System.out.println("----- Waiting for " + NUM_OF_WORKERS + " Worker/Workers to connect -----");
        Socket workerSocket;
        while(workersSockets.size() < NUM_OF_WORKERS) {
            workerSocket = serverSocket.accept();
            workersSockets.add(workerSocket);
            System.out.println("Worker connected: " + workerSocket.getRemoteSocketAddress());
        }
        System.out.println();
    }

    public synchronized Socket getConnection() {
        while (workersSockets.isEmpty()) {
            try {
                wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        return workersSockets.remove(0);
    }
}