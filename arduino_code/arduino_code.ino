int val = -1;
int last_val = -1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    val = Serial.read() - '0';  // '0' to convert ASCII digit to integer
    
    if (val != last_val) {
      Serial.println(val);
    }

    if (val == 1) {
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (val == 2) {
      digitalWrite(LED_BUILTIN, LOW);
    }

    last_val = val;
  }
}

  