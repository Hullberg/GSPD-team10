package nxt;

import lejos.nxt.Button;
import lejos.nxt.LCD;
import lejos.nxt.SensorPort;
import lejos.nxt.UltrasonicSensor;

public class UltraSonicTest {
	
	public static void main(String[] args) throws Exception {
		UltrasonicSensor sonic = new UltrasonicSensor(SensorPort.S4);
		sonic.continuous();
		
		LCD.setAutoRefresh(false);
		LCD.clear();
		LCD.drawString(sonic.getVersion(), 0, 0);
		LCD.drawString(sonic.getVendorID(), 0, 1);
		LCD.drawString(sonic.getProductID(), 0, 2);
		
		while(!Button.ESCAPE.isDown()) {
			LCD.asyncRefreshWait();
			LCD.drawString("     ", 0, 3);
			LCD.drawInt(sonic.getDistance(), 0, 3);
			LCD.asyncRefresh();
			//Thread.sleep(500);
		}
		System.exit(0);
	}	
}
