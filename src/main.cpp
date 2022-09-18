#include <Arduino.h>
#define LED 2

//variaveis que indicam o núcleo
static uint8_t taskCoreZero = 0;
static uint8_t taskCoreOne  = 1;

void ler_tensao();

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);

  //cria uma tarefa que será executada na função coreTaskZero, com prioridade 1 e execução no núcleo 0
  //coreTaskZero: piscar LED e contar quantas vezes
//  xTaskCreatePinnedToCore(
//                    ler_tensao,       /* função que implementa a tarefa */
//                    "coreTaskZero",   /* nome da tarefa */
//                    10000,            /* número de palavras a serem alocadas para uso com a pilha da tarefa */
//                    NULL,             /* parâmetro de entrada para a tarefa (pode ser NULL) */
//                    1,                /* prioridade da tarefa (0 a N) */
//                    NULL,             /* referência para a tarefa (pode ser NULL) */
//                    taskCoreZero);    /* Núcleo que executará a tarefa */
//                    
//  delay(500); //tempo para a tarefa iniciar

}

void loop() {
  ler_tensao();
}

void ler_tensao(){
  // Lê a entrada no analógico ADC1_0:
  int potenciometro = analogRead(A0);
  Serial.println(potenciometro);

  digitalWrite(LED, HIGH);
  delay(50);
  digitalWrite(LED, LOW);
  delay(50);

}
