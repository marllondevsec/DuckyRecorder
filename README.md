# 🦆 DuckyRecorder

DuckyRecorder é uma ferramenta CLI avançada para gravação de eventos HID (teclado e mouse) e exportação desses eventos em formatos compatíveis com Rubber Ducky e Arduino Leonardo/ATmega32u4. Permite automação e reprodução de interações humanas com precisão temporal.

---

## ✨ Funcionalidades

* 🎙️ **Gravação em tempo real** – Captura eventos de teclado e mouse com timestamps precisos
* ⏯️ **Controle inteligente** – Pausa/continuação com teclas configuráveis (F9/F10 padrão)
* 👁️ **Visualização ao vivo** – Exibe eventos capturados em tempo real durante a gravação
* 💾 **Armazenamento estruturado** – Salva gravações em formato JSON com metadados
* 📤 **Exportação multiplataforma** – Converte para:

  * Rubber Ducky (`.ducky.txt`)
  * Arduino HID (`.ino`) com suporte a `Keyboard.h` e `Mouse.h`
* 🌍 **Internacionalização** – Suporte a múltiplos idiomas (Português e Inglês)
* 🎨 **Interface CLI rica** – Cores, banners adaptativos e menus interativos
* ⚙️ **Configuração persistente** – Configurações salvas automaticamente em JSON
* 🔧 **Sistema de logs** – Logs detalhados para debugging e monitoramento
* 🖱️ **Controle de mouse preciso** – Movimento relativo, cliques e zeramento inicial

---

## 📁 Estrutura do Projeto

```text
DuckyRecorder/
├── DuckyRecorder/
│   ├── cli/               # Interface CLI e menus interativos
│   ├── core/              # Lógica principal (gravação, eventos, timeline)
│   │   ├── colors.py      # Cores ANSI para terminal
│   │   ├── events.py      # Classes de eventos (dataclasses)
│   │   ├── hotkeys.py     # Mapeamento de teclas de atalho
│   │   ├── language.py    # Gerenciador de idiomas
│   │   ├── recorder.py    # Gravação de eventos HID
│   │   └── timeline.py    # Linha do tempo de eventos
│   ├── exporters/         # Exportadores para diferentes formatos
│   │   ├── ducky.py       # Exportação para Rubber Ducky
│   │   └── arduino.py     # Exportação para Arduino HID
│   ├── utils/             # Utilitários
│   │   ├── console.py     # Limpeza de console
│   │   └── logger.py      # Sistema de logs centralizado
│   ├── config/            # Configuração persistente
│   ├── lang/              # Arquivos de idioma (JSON)
│   ├── __init__.py        # Banner e funções principais
│   ├── main.py            # Ponto de entrada
│   └── __main__.py        # Execução via python -m
├── config/                # Configurações do usuário
│   └── config.json
├── recordings/            # Gravações salvas (JSON)
├── exports/               # Arquivos exportados
├── logs/                  # Logs de debug (gerado automaticamente)
├── requirements.txt       # Dependências Python
├── LICENSE                # Licença MIT
└── README.md              # Este arquivo
```

---

## 🛠️ Instalação

### Pré-requisitos

* Python 3.8 ou superior
* `pip` (gerenciador de pacotes Python)

### Instalação passo a passo

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/DuckyRecorder.git
cd DuckyRecorder

# Instale as dependências
pip install -r requirements.txt
```

### Dependências

* `pynput>=1.7.6` – Captura de eventos de teclado e mouse
* `colorama>=0.4.6` – Cores no terminal (cross-platform)

---

## ▶️ Como Usar

### Execução básica

```bash
# Método 1: Executar como módulo
python -m DuckyRecorder

# Método 2: Executar o script principal
python DuckyRecorder/main.py

# Método 3: Se estiver no diretório do projeto
python DuckyRecorder/DuckyRecorder/main.py
```

### Fluxo de trabalho típico

1. **Iniciar gravação** – Começa a capturar eventos
2. **Executar ações** – Digitar texto, clicar mouse, etc.
3. **Parar gravação** – Pressionar F10 (configurável)
4. **Exportar** – Converter para Ducky ou Arduino
5. **Executar no dispositivo** – Carregar no dispositivo alvo

---

## 📋 Menu Principal

| Opção | Descrição         | Atalho |
| ----- | ----------------- | ------ |
| 1)    | Iniciar gravação  | -      |
| 2)    | Listar gravações  | -      |
| 3)    | Exportar gravação | -      |
| 4)    | Configurações     | -      |
| 5)    | Logs de debug     | -      |
| 0)    | Sair              | -      |

### Durante a gravação

* **F9** – Pausar/Continuar gravação
* **F10** – Parar e salvar gravação
* **Visualização ao vivo** – Mostra últimos eventos em tempo real

---

## 📦 Formatos de Exportação

### 1. Rubber Ducky (`.ducky.txt`)

* Converte digitação em comandos `STRING`, `ENTER`, `DELAY`, etc.
* Agrupa caracteres digitados para maior eficiência
* Preserva delays entre eventos
* Comentários para eventos não suportados (mouse)

```ducky
REM Rubber Ducky Script
DELAY 1000
STRING Hello World
ENTER
DELAY 500
STRING Next Command
```

---

### 2. Arduino HID (`.ino`)

Gera código compatível com placas USB HID:

* Arduino Leonardo
* Arduino Micro
* Pro Micro
* ATmega32u4

Usa bibliotecas nativas `Keyboard.h` e `Mouse.h`.

Suporte completo a:

* Movimento relativo do mouse (com passos para grandes distâncias)
* Cliques (esquerdo, direito, meio)
* Texto e caracteres especiais
* Teclas de controle (Ctrl, Alt, Shift, etc.)
* Zeramento inicial do cursor

```cpp
#include <Keyboard.h>
#include <Mouse.h>

void setup() {
  delay(3000);
  Keyboard.begin();
  Mouse.begin();
  delay(1000);
  
  // Zera posição do mouse
  for(int i=0; i<40; i++) {
    Mouse.move(-127, -127);
    delay(10);
  }
  
  // Sequência gravada
  Keyboard.print("Hello");
  delay(100);
  Keyboard.press(KEY_RETURN);
  // ... mais comandos
}
```

---

## ⚙️ Configuração

O arquivo `config/config.json` é criado automaticamente e pode ser editado manualmente ou pelo menu de configurações:

```json
{
  "language": "pt",
  "mouse_speed": "FAST",
  "zero_mouse_on_start": true,
  "auto_save": true,
  "pause_key": "F9",
  "stop_key": "F10",
  "default_recording_name": "",
  "show_live_preview": true,
  "max_events_display": 10
}
```

### Opções configuráveis

| Configuração        | Valores                  | Descrição                           |
| ------------------- | ------------------------ | ----------------------------------- |
| language            | pt, en                   | Idioma da interface                 |
| mouse_speed         | FAST, MEDIUM, SLOW       | Velocidade do movimento do mouse    |
| zero_mouse_on_start | true, false              | Zera cursor no início da reprodução |
| pause_key           | F1–F12, teclas especiais | Tecla para pausar gravação          |
| stop_key            | F1–F12, teclas especiais | Tecla para parar gravação           |
| show_live_preview   | true, false              | Mostra eventos em tempo real        |

---

## 🔐 Aviso de Uso Ético

⚠️ **AVISO IMPORTANTE**

Esta ferramenta deve ser utilizada **APENAS** em:

* Ambientes autorizados e de sua propriedade
* Testes de segurança com permissão explícita
* Automação de tarefas legítimas
* Projetos educacionais e de pesquisa
* Acessibilidade e automação assistiva

O uso indevido pode violar:

* Leis de privacidade
* Políticas de uso aceitável
* Termos de serviço de sistemas

O desenvolvedor não se responsabiliza pelo uso indevido desta ferramenta.

---

## 🐛 Sistema de Logs

O DuckyRecorder inclui um sistema de logs completo para debugging:

* **Logs em tempo real** – Últimas 20 mensagens visíveis no menu
* **Arquivo persistente** – Logs salvos em `logs/debug_YYYYMMDD_HHMMSS.log`
* **Níveis de log** – DEBUG, INFO, WARNING, ERROR
* **Rotação automática** – Mantém apenas 1000 mensagens em memória

### Acesso aos logs

Menu principal → Opção 5 **"Logs de debug"**

Permite:

* Visualizar
* Limpar
* Exportar logs

Úteis para troubleshooting e desenvolvimento.

---

## 🧠 Ideias Futuras

* Exportação para PowerShell/Bash – Scripts para automação em sistemas operacionais
* Replay automático local – Reproduzir gravações diretamente no computador
* Filtros avançados – Ignorar eventos específicos (ex: movimento excessivo do mouse)
* Editor visual de timeline – Ajustar timestamps e remover eventos
* Suporte a mais idiomas – Espanhol, Francês, Alemão, etc.
* Plugins de exportação – Sistema modular para novos formatos
* Gravação de tela integrada – Capturar screenshots durante a gravação
* Cloud sync – Sincronizar gravações entre dispositivos
* API REST – Controle remoto via HTTP

---

## 🛠️ Desenvolvimento

Para contribuir:

```bash
# 1. Faça um fork do repositório
# 2. Clone seu fork
git clone https://github.com/seu-usuario/DuckyRecorder.git

# 3. Crie um ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 4. Instale dependências
pip install -r requirements.txt

# 5. Execute em modo desenvolvimento
python -m DuckyRecorder
```

### Estrutura de código

* **Modular** – Cada funcionalidade em seu próprio módulo
* **Tipagem** – Type hints para melhor manutenção
* **Documentação** – Docstrings e comentários explicativos
* **Logging** – Sistema centralizado para debugging

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT – veja o arquivo LICENSE para detalhes.

```text
MIT License

Copyright (c) 2026 MarllonDevSec

Permissão é concedida, gratuitamente, a qualquer pessoa que obtenha uma cópia
deste software e arquivos de documentação associados...
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

* **Issues** – Reporte bugs ou sugira features no GitHub Issues
* **Documentação** – Consulte os comentários no código e este README
* **Comunidade** – Participe das discussões no repositório

---

## 🏗️ Arquitetura Técnica

### Componentes principais

#### Recorder (`core/recorder.py`)

* Gerencia listeners de teclado/mouse
* Processa eventos em tempo real
* Controla pausa e parada

#### Timeline (`core/timeline.py`)

* Sequência temporal de eventos
* Conversão de eventos brutos para ações

#### Exporters (`exporters/`)

* Transformam timeline em formatos específicos
* Preservam timing e ordem dos eventos

#### Language Manager (`core/language.py`)

* Carregamento dinâmico de idiomas
* Fallback automático para inglês

#### Config Manager (`config/__init__.py`)

* Persistência de configurações
* Valores padrão e merge automático

---

**DuckyRecorder – Automatize com precisão, desenvolva com responsabilidade. 🦆**
