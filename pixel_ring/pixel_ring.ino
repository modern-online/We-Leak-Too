#include <Adafruit_NeoPixel.h>

#define PIN 7 // On Trinket or Gemma, suggest changing this to 1
#define NUMPIXELS 24 // Popular NeoPixel ring size

int state = 1;
int data;
int prevState;

bool receive = 0;

long previousMillis = 0;
long previousMainMillis = 0;

//long intervalMain = 100; 
long intervalFade = 103;
long intervalThink = 205;

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void getState() {
  Serial.println(1);
  Serial.flush();
  delay(10); 
  
  if (Serial.available() > 0) {
      data = Serial.parseInt();
      delay(10);
    }

  if (data > 0 && data < 5)
    state = data; 
  
  //Serial.println(state);
  
  //state = random(1,2);
  //Serial.println(state);
  
}

void setup() {

  pixels.begin();
  delay(50); 
  
  Serial.begin(115200);
  delay(50);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

}

void loop() {
  
  //unsigned long mainMillis = millis();
  
  //if (mainMillis - previousMainMillis >= intervalMain) {
    //previousMainMillis = mainMillis;
      
    getState();

    //Serial.println(state);

    
  Serial.println(0);
  Serial.flush(); 
  delay(10);
  
  if (state == 1) { 
    think();
    //Serial.println("THINKING");
  }
    
  else if(state == 2) {
    confess();
    //Serial.println("CONFESSING");
  }
  
  else if(state == 3 && prevState!=3) {
    hear();
    //Serial.println("LISTENING");
  }
  
  else if(state == 4) {
    reply();
    //Serial.println("REPLYING");
  }
    
  prevState = state;  
}
