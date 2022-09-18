#include <Arduino.h>

/*-----------------
  Oséias Farias 
-----------------*/

// Tarefas
TaskHandle_t Task1;
TaskHandle_t Task2;
TaskHandle_t Task3;

// LED pins
const int led1 = 2;
const int led2 = 4;

void Tarefa1( void * pvParameters );
void Tarefa2( void * pvParameters );
void ler_tensao( void * pvParameters );

void setup() {
    Serial.begin(115200); 
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);

    xTaskCreatePinnedToCore(
        Tarefa1,      /* Função para implementar a tarefa */
        "Tarefa1",
        10000,
        NULL,
        1,
        &Task1,
        0
  );
  delay(500);

  xTaskCreatePinnedToCore(
        ler_tensao,      /* Função para implementar a tarefa */
        "Tarefa3",
        10000,
        NULL,
        2,
        &Task1,
        0
  );
  delay(500);

  xTaskCreatePinnedToCore(
        Tarefa2,      /* Função para implementar a tarefa */
        "Tarefa2",
        10000,
        NULL,
        1,
        &Task2,
        1
  );
  delay(500);
}

//Tarefa1: Pisca o LED a cada 1000 ms
void Tarefa1( void * pvParameters ){
  Serial.print("Tarefa 1: rodando no núcleo 0");
  Serial.println(xPortGetCoreID());

  for(;;){
    Serial.print("Tarefa 1: rodando no núcleo 0");
    Serial.println(xPortGetCoreID());
    digitalWrite(led1, HIGH);
    delay(1000);
    digitalWrite(led1, LOW);
    delay(1000);
  } 
}

//Tarefa1: Pisca o LED a cada 700 ms
void Tarefa2( void * pvParameters ){
  Serial.print("Tarefa 1: rodando no núcleo 1");
  Serial.println(xPortGetCoreID());

  for(;;){
    digitalWrite(led2, HIGH);
    delay(100);
    digitalWrite(led2, LOW);
    delay(100);
  }
}

void ler_tensao( void * pvParameters ){
  // Lê a entrada no pino analógico ADC1_0:

  int potenciometro;
  for(;;){
        potenciometro = analogRead(A0);
        Serial.print("Tensão Quantizada: ");
        Serial.println(potenciometro);
        delay(500);
  }
}

void loop() {
}

