#include <Keyboard.h>
#include <Mouse.h>

void setup() {
  // Delay de segurança para evitar execução acidental
  delay(3000);
  
  Keyboard.begin();
  Mouse.begin();
  delay(1000);  // Aguarda inicialização

  // Zera posição do mouse (move para canto superior esquerdo)
  for(int i=0; i<40; i++) {
    Mouse.move(-127, -127);
    delay(10); // Pequeno delay entre movimentos
  }
  delay(100);
  delay(1000);
  Keyboard.press(KEY_LEFT_GUI);
  delay(100);
  Keyboard.release(KEY_LEFT_GUI);
  delay(500);
  Keyboard.print("c");
  delay(10);
  delay(100);
  Keyboard.print("m");
  delay(10);
  delay(99);
  Keyboard.print("d");
  delay(10);
  delay(300);
  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.release(KEY_RETURN);

  Keyboard.end();
  Mouse.end();
}

void loop() {}