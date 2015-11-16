/* Código-base do curso de robótica da Novatec modificado pelos estudantes Felipe Martins e Eduardo Ribeiro. */
/* Inclusão da biblioteca DualMotor que permite controlar a caixa de engrenagem com os dois motores. */
#include <DualMotor.h>

DualMotor dualmotor;
int pinSensor1 = A0;
int pinSensor2 = A1;
int pinSensor3 = A2;
int preto = 800;
int velocidadeReta = 255; 
int velocidadeCruzamento = 160;
int velocidadeCurva = 140;
int velocidadeAcelCurva = 45;
int tempoEspera = 1;

/*
 Inicialização do programa.
 */
void setup() {
  Serial.begin(9600);
}  

/*
 Loop principal. Enquanto o robô estiver ativo, essa função é chamada pelo Arduino.
 */
void loop() {
  /* Definição de quais são cada um dos sensores de refletância. */
  int s1 = analogRead(pinSensor1);
  int s2 = analogRead(pinSensor2);
  int s3 = analogRead(pinSensor3);
  
  /* Leitura e impressão dos valores lidos por cada um dos sensores de refletância a cada execução da função loop. */
  Serial.print(analogRead(A0));
  Serial.print(" : ");
  Serial.print(analogRead(A1));
  Serial.print(" : ");
  Serial.println(analogRead(A2));

  /* Verifica se o valor do sensor 1 corresponde ao preto e se o valor do sensor 3 corresponde ao branco. */
  if (s1 >= preto && s3 < preto) {
      // Serial.print("Virarei para a esquerda.");
      esquerda (velocidadeCurva);
      delay (tempoEspera);
  /* Verifica se o valor do sensor 1 corresponde ao branco e se o valor do sensor 3 corresponde ao preto. */
  } else if (s1 < preto && s3 >= preto) {
      // Serial.print("Virarei para a direita.");
      direita (velocidadeCurva);
      delay (tempoEspera);
  /* Verifica se o valor dos 3 sensores corresponde ao preto. */
  } else if (s1 >= preto && s2 >= preto && s3 >= preto) {
      frente (velocidadeCruzamento);
      delay (tempoEspera);
  /* Outras situações. */
  } else {
      // Serial.print("Seguirei em frente.");    
      frente (velocidadeReta);
      delay (tempoEspera);
  }
    

}

void frente(int velocidade) {
  dualmotor.M1move(velocidade,0);
  dualmotor.M2move(velocidade,0);
}
void esquerda(int velocidade) {
  dualmotor.M1move(velocidade,1);
  dualmotor.M2move(velocidade,0);
}
void direita(int velocidade) {
  dualmotor.M1move(velocidade,0);
  dualmotor.M2move(velocidade,1);
}
void tras(int velocidade) {
  dualmotor.M1move(velocidade,1);
  dualmotor.M2move(velocidade,1);
}
void para() {
  dualmotor.M1parar();
  dualmotor.M2parar();
}

