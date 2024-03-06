import java.util.Date;
import java.io.Serializable;
public class Waypoint implements Serializable{
    private int routeID;
    private int userID;
    private int waypointID;
    private double latitude;
    private double longitude;
    private double elevation;
    private Date time;
    public Waypoint(int waypointID, int routeID, int userID, double latitude, double longitude, double elevation, Date time) {
        this.waypointID = waypointID;
        this.routeID = routeID;
        this.userID = userID;
        this.latitude = latitude;
        this.longitude = longitude;
        this.elevation = elevation;
        this.time = time;
    }
    public int getWaypointID() {
        return waypointID;
    }
    public int getRouteID() {
        return routeID;
    }
    public int getUserID() {
        return userID;
    }
    public double getLatitude() {
        return latitude;
    }
    public double getLongitude() {
        return longitude;
    }
    public double getElevation() {
        return elevation;
    }
    public Date getTime() {
        return time;
    }
    public void setWaypointID(int waypointID) {
        this.waypointID = waypointID;
    }
    public void setRouteID(int routeID) {
        this.routeID = routeID;
    }
    public void setUserID(int userID) {
        this.userID = userID;
    }
    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }
    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }
    public void setElevation(double elevation) {
        this.elevation = elevation;
    }
    public void setTime(Date time) {
        this.time = time;
    }
}