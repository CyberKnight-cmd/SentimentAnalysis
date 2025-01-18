import javax.bluetooth.*;
import javax.microedition.io.*;
import java.io.*;

public class BluetoothConnector {
    public static void main(String[] args) {
        String bluetoothAddress = "00:11:22:33:44:55"; // Replace with your device's address
        String serviceUUID = "1101"; // Standard UUID for Serial Port Profile (SPP)
        
        // Construct the connection URL
        String connectionURL = "btspp://" + bluetoothAddress + ":" + serviceUUID + ";authenticate=false;encrypt=false;master=false";

        try {
            System.out.println("Attempting to connect to device: " + bluetoothAddress);

            // Open a connection to the Bluetooth device
            StreamConnection connection = (StreamConnection) Connector.open(connectionURL);

            System.out.println("Connection established!");

            // Open input and output streams
            InputStream inputStream = connection.openInputStream();
            OutputStream outputStream = connection.openOutputStream();

            // Send data to the Bluetooth device
            String message = "Hello Bluetooth Device!";
            outputStream.write(message.getBytes());
            System.out.println("Message sent: " + message);

            // Read response from the Bluetooth device
            byte[] buffer = new byte[1024];
            int bytesRead = inputStream.read(buffer);
            String receivedMessage = new String(buffer, 0, bytesRead);
            System.out.println("Message received: " + receivedMessage);

            // Close streams and connection
            inputStream.close();
            outputStream.close();
            connection.close();
            System.out.println("Connection closed.");
        } catch (IOException e) {
            System.err.println("Failed to connect or communicate with the Bluetooth device.");
            e.printStackTrace();
        }
    }
}
