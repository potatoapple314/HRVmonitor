const int heartPin = 34;
const int threshold_v = 2400;
const int threshold_t = 350;
int p = 0;
int snap_time = 0;

void setup() {
  //シリアル通信の初期化しシリアルモニタへ文字列を出力できるようにする
  Serial.begin(115200);
//  SerialBT.begin("ESP32test");
}
void loop() {
  int heartValue = analogRead(heartPin);
  if (heartValue > threshold_v && p == 0){
    p = p + 1;
    snap_time = millis();
    }
  int present_time = millis();
  int RRI = present_time - snap_time;
  if(heartValue > threshold_v && RRI > threshold_t){
    Serial.println(RRI);
    snap_time = 0;
    snap_time = millis();
    }
}
