# 🦆 DuckyRecorder

DuckyRecorder é uma ferramenta CLI para gravação de eventos HID (teclado e mouse) e exportação desses eventos em formatos compatíveis com **Rubber Ducky** e **Arduino Leonardo/ATmega32u4**, permitindo automação e reprodução de interações humanas.

---

## ✨ Funcionalidades

* 🎙️ Grava eventos de teclado e mouse em tempo real.
* 💾 Salva gravações em formato JSON.
* 📤 Exporta para:

  * Rubber Ducky (`.ducky.txt`)
  * Arduino HID (`.ino`)
* 🌍 Suporte a múltiplos idiomas (Português e Inglês).
* 🎨 Interface CLI com cores e menus interativos.
* ⚙️ Sistema de configuração persistente.

---

## 📁 Estrutura do Projeto

```text
DuckyRecorder/
├── DuckyRecorder/
│   ├── cli/            # Interface CLI e menus
│   ├── core/           # Lógica principal (gravação, eventos, idiomas)
│   ├── exporters/      # Exportadores (Ducky, Arduino)
│   ├── utils/          # Utilitários (console, etc.)
│   ├── config/         # Configuração persistente
│   ├── lang/           # Arquivos de idioma (JSON)
│   ├── main.py         # Ponto de entrada
│   └── __main__.py     # Execução via python -m
├── recordings/         # Gravações salvas
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🛠️ Instalação

```bash
git clone https://github.com/seu-usuario/DuckyRecorder.git
cd DuckyRecorder
pip install -r requirements.txt
```

> Requer Python 3.8+

---

## ▶️ Como Usar

### Executar o programa:

```bash
python -m DuckyRecorder
```

ou

```bash
python DuckyRecorder/main.py
```

---

## 📋 Menu Principal

* **1) Iniciar gravação** — Começa a capturar eventos HID.
* **2) Listar gravações** — Mostra gravações salvas.
* **3) Exportar gravação** — Converte para Ducky ou Arduino.
* **4) Alterar idioma** — Alterna entre PT/EN.
* **0) Sair** — Encerra o programa.

---

## 📦 Formatos de Exportação

### Rubber Ducky (`.ducky.txt`)

* Converte digitação em comandos `STRING`, `ENTER`, `DELAY`, etc.
* Agrupa caracteres digitados para maior eficiência.

### Arduino HID (`.ino`)

* Gera código compatível com placas como:

  * Arduino Leonardo
  * Arduino Micro
  * ATmega32u4
* Usa `Keyboard.h` e `Mouse.h`.
* Suporta:

  * Movimento do mouse
  * Cliques
  * Texto
  * Teclas especiais

---

## ⚙️ Configuração

Um arquivo `config.json` é criado automaticamente no diretório raiz com opções como:

```json
{
  "language": "pt",
  "mouse_speed": "FAST",
  "zero_mouse_on_start": true,
  "auto_save": true
}
```

---

## 🔐 Aviso de Uso Ético

Esta ferramenta deve ser utilizada **apenas em ambientes autorizados**, para fins educacionais, automação legítima, testes de segurança ou acessibilidade. O uso indevido pode violar leis e políticas locais.

---

## 🧠 Ideias Futuras

* Exportação para PowerShell/Bash.
* Replay automático local.
* Filtros avançados (ex: ignorar mouse move).
* Editor visual de timelines.

---

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

Se quiser, posso também gerar:

* Documentação técnica
* README em inglês
* Manual de uso avançado
* Exemplos práticos
