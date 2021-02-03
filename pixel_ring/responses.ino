// THINKING STATE
void think() {

  pixels.clear();

  int i = 0;
  while (i < NUMPIXELS) {
    unsigned long currentMillis = millis(); 
    if (currentMillis - previousMillis >= intervalThink) {
      previousMillis = currentMillis;
      pixels.setPixelColor(i, pixels.Color(255, 0, 0));
      pixels.setPixelColor((i-1), pixels.Color(0, 0, 0));
      pixels.show();   // Send the updated pixel colors to the hardware.
      i++;
      getState();
      if(state != 1){
          state = 0; 
          break;
      }
    }
  } 
}

// CONFESSION STATE
void confess() {

  pixels.clear();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= intervalFade) {
    previousMillis = currentMillis;
    for (int j = 0; j <= 200; j = j + 4) {
      for (int i = 0; i < NUMPIXELS; i++) {
        pixels.setPixelColor(i, j, 0, 0);
        pixels.show();
      }
    }

    for (int j = 200; j >= 0; j = j - 4) {
      for (int i = 25; i >= 0; i--) {
        pixels.setPixelColor(i, j, 0, 0);
        pixels.show();
      }
    }
  }
}

// LISTENING STATE
void hear() {
  
  pixels.clear();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= intervalFade) {
    previousMillis = currentMillis;
    for (int j = 0; j <= 255; j = j + 8) {
      for (int i = 0; i < NUMPIXELS; i++) {
        pixels.setPixelColor(i, j, j, j);
        pixels.show();
      }
    }
  }
}

// NORMAL RESPONSE STATE
void reply() {
  
  pixels.clear();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= intervalFade) {
    previousMillis = currentMillis;
    for (int j = 0; j <= 200; j = j + 4) {
      for (int i = 0; i < NUMPIXELS; i++) {
        pixels.setPixelColor(i, 0, j, j);
        pixels.show();
      }
    }

    for (int j = 200; j >= 0; j = j - 4) {
      for (int i = 25; i >= 0; i--) {
        pixels.setPixelColor(i, 0, j, j);
        pixels.show();
      }
    }
  }
}
