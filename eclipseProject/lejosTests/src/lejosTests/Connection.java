package lejosTests;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.IntBuffer;

import lejos.hardware.lcd.LCD;
import lejos.remote.nxt.BTConnection;
import lejos.remote.nxt.BTConnector;

/**
*Connection to the server.
*/

public class Connection {
	
	private DataInputStream dis;	
	private DataOutputStream dos;
	
	private byte[] buf = new byte[64];

	/**
	 *
	 *Creates a connection to the server
	 * 
	 */
	public Connection(){
		
	    LCD.drawString("Connecting", 1,1 );
	    BTConnector bt = new BTConnector();
		BTConnection conn = bt.waitForConnection(10000, 2);
		LCD.clear();
		LCD.drawString("Connected", 1, 1);
		
	    this.dis = conn.openDataInputStream();
	    this.dos = conn.openDataOutputStream();
		
	}
	
	/**
	 *
	 * @return      An int array containing 6 integers. The first three are the x,y, and z coordinates of the from location. 
	 * 				The last three are the x,y, and z coordinates	 of the to location
	 */
	
	
	public int[] readCoordinates(){
		int[] coords = new int[6];
		
		try {
			dis.read(buf, 0, 64);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		for(int i = 0; i < 6; i++ ){
	    	coords[i] = ByteBuffer.wrap(buf).getInt((4*i)); //read one int at a time from the bytebuffer   	
	    	LCD.drawInt(coords[i], 4, i+2); //print them (debug)
		}
		return coords;
	}

	public int readInt(){
		int i;
		try {
			dis.read(buf, 0, 64);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		i = ByteBuffer.wrap(buf).getInt();
		return i;
	}
	
	
	/**
	 * @param coords  an int array containing x,y, and z coordinates of the robots current position.
	 *       
	 *       
	 */
	
	public void sendCoordinates(int[] coords){
		assert coords.length == 3;
		
		ByteBuffer b = ByteBuffer.allocate(4*coords.length);
		IntBuffer c = b.asIntBuffer();
		c.put(coords);
		buf = b.array();
		
		try {
			dos.write(buf, 0, 12);
			dos.flush();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	} 
	/**
	 *
	 * @param i 	an int to tell whether the task was a success or not. 0 is failure. 1 is success.
	 */
	
   public void sendInt(int i){
	   try {
		 dos.writeInt(i);
		 dos.flush();
	} catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	  
	   
   }
   
   
   /**
     * 	
	 * Closes a connection. 
	 * 
	 */
   
   public void closeConnection(){
	   try {
		dis.close();
		dos.close();
	} catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	   
	   
	   
   }
	
}
