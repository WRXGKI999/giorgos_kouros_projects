import java.util.ArrayList;
public class SharedWaypointsArraylist {
    private ArrayList<Waypoint> waypointsArrayList;
    private int chunkSize;
    private boolean isEmpty = true;
    SharedWaypointsArraylist(int chunkSize){
        this.chunkSize = chunkSize;
    }

    public synchronized ArrayList<Waypoint> getWaypoints() throws InterruptedException {
        while (waypointsArrayList.size() == 0) {
            wait();
        }
        ArrayList<Waypoint> chunkList;
        if(waypointsArrayList.size() == chunkSize){
            chunkList = new ArrayList<>(waypointsArrayList.subList(0, chunkSize));
            waypointsArrayList.subList(0, chunkSize).clear();
            isEmpty = true;
        }else if(waypointsArrayList.size() > chunkSize){
            chunkList = new ArrayList<>(waypointsArrayList.subList(0, chunkSize));
            waypointsArrayList.subList(0, chunkSize-1).clear();
            isEmpty = false;
        } else {
            chunkList = new ArrayList<>(waypointsArrayList.subList(0, waypointsArrayList.size()));
            waypointsArrayList.subList(0, waypointsArrayList.size()).clear();
            isEmpty = true;
        }
        return chunkList;
    }

    public synchronized void setList(ArrayList<Waypoint> waypointsArrayList) {
        this.waypointsArrayList = waypointsArrayList;
        isEmpty = false;
        notify();
    }

    public synchronized boolean isEmpty(){
        if(isEmpty){
            return true;
        } else {
            return false;
        }
    }
}