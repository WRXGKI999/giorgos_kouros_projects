import java.io.Serializable;
public class Interval implements Serializable{
    private double distance;
    private double elevationGain;
    private double duration;
    private double averageSpeed;
    private int userID;
    private int routeID;
    public Interval(int routeID, int userID, double distance, double elevationGain, double duration, double averageSpeed) {
        this.routeID = routeID;
        this.userID = userID;
        this.distance = distance;
        this.elevationGain = elevationGain;
        this.duration = duration;
        this.averageSpeed = averageSpeed;
    }
    public int getRouteID() {
        return routeID;
    }
    public int getUserID() {
        return userID;
    }
    public double getDistance() {
        return distance;
    }
    public double getElevationGain() {
        return elevationGain;
    }
    public double getDuration() {
        return duration;
    }
    public double getAverageSpeed() {
        return averageSpeed;
    }
    public void setRouteID(int routeID) {
        this.routeID = routeID;
    }
    public void setUserID(int userID) {
        this.userID = userID;
    }
    public void setDistance(double distance) {
        this.distance = distance;
    }
    public void setElevationGain(double elevationGain) {
        this.elevationGain = elevationGain;
    }
    public void setDuration(double duration) {
        this.duration = duration;
    }
    public void setAverageSpeed(double averageSpeed) {
        this.averageSpeed = averageSpeed;
    }
}