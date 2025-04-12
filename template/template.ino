uint8_t cube[8][8];


void setup() {

  for(uint8_t i = 0; i < 8; i++){
    for(uint8_t j = 0; j < 8; j++){
      for(uint8_t k = 0; k < 8; k++){
        if(voxelPositions[i][j][k] == 1){
          setVoxel(k, i, j);
        }
      }
    }
  }

  pinMode(SS, OUTPUT);    //these two lines might be unnecessary idk
  digitalWrite(SS, HIGH); //delete these first if it doesnt work
  
  SPI.begin();
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));

}

void loop() {

  renderCube();
  delay(1); //adding a delay might help with some of the visual gliches we've been getting idk how long it should be though.

}

void renderCube() {
  for (uint8_t i = 0; i < 8; i++) {
    digitalWrite(SS, LOW);
    SPI.transfer(0x01 << i);
    for (uint8_t j = 0; j < 8; j++) {
      SPI.transfer(cube[i][j]);
    }
    digitalWrite(SS, HIGH);
  }
}

void setVoxel(uint8_t x, uint8_t y, uint8_t z) {
  cube[7 - y][7 - z] |= (0x01 << x);
}

void clearCube() {
  for (uint8_t i = 0; i < 8; i++) {
    for (uint8_t j = 0; j < 8; j++) {
      cube[i][j] = 0;
    }
  }
}
