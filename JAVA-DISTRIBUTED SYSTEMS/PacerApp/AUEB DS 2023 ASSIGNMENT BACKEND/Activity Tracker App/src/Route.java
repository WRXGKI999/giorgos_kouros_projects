public class Route{
    private double distance;
    private double elevationGain;
    private double duration;
    private double averageSpeed;
    private int userID;
    public Route(int userID, double distance, double elevationGain, double duration, double averageSpeed) {
        this.userID = userID;
        this.distance = distance;
        this.elevationGain = elevationGain;
        this.duration = duration;
        this.averageSpeed = averageSpeed;
    }
    public int getUserID() {
        return userID;
    }
    public double getAverageSpeed() {
        return averageSpeed;
    }
    public double getDistance() {
        return distance;
    }
    public double getDuration() {
        return duration;
    }
    public double getElevationGain() {
        return elevationGain;
    }
    public void setAverageSpeed(double averageSpeed) {
        this.averageSpeed = averageSpeed;
    }
    public void setDuration(double duration) {
        this.duration = duration;
    }
    public void setElevationGain(double elevationGain) {
        this.elevationGain = elevationGain;
    }
    public void setDistance(double distance) {
        this.distance = distance;
    }
    public void setUserID(int userID) {
        this.userID = userID;
    }
    @Override
    public String toString() {
        return "User ID → " + userID + "-----" + "-----" +
                String.format("%.2f",distance / 1000) + "-----" + "Distance(km)" + "-----" +
                String.format("%.2f",elevationGain) + "-----" + "Elevation Gain(m)" + "-----" +
                String.format("%.2f",duration / 60) + "-----" + "Duration(min)" + "-----" +
                String.format("%.2f",(duration / 60) / (distance / 1000)) + "-----" + "Pace(min/km)";
    }
}