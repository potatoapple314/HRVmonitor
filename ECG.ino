const int heartPin = 34;
void setup() {
  Serial.begin(115200);
//  SerialBT.begin("ESP32test");
}
void loop() {
  int heartValue = analogRead(heartPin);
  Serial.println(heartValue);
//  SerialBT.println(heartValue);
  delay(5);
}
