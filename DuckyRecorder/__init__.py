"""
DuckyRecorder - Ferramenta para gravação de eventos HID
"""

__version__ = "1.0.0"
__author__ = "MarllonDevSec"

# ANSI colors
DARK_BLUE = '\033[1;34m'
BLUE = '\033[0;34m'
CYAN = '\033[1;36m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
RESET = '\033[0m'


def _make_box(plain_lines, inner_width):
    """
    Recebe uma lista de linhas em texto "plano" (sem cores).
    Retorna a caixa pronta onde cada linha é preenchida até inner_width,
    e depois aplicamos coloração de forma que não altere o alinhamento.
    """
    top = "╔" + "═" * inner_width + "╗"
    bottom = "╚" + "═" * inner_width + "╝"
    boxed = [top]
    # cada linha deve caber na largura interna
    for line in plain_lines:
        # corta se for maior que inner_width
        visible = line[:inner_width].ljust(inner_width)
        boxed.append("║" + visible + "║")
    boxed.append(bottom)
    return "\n".join(boxed)


def _apply_highlights(box_text, highlights):
    """
    Recebe o texto da caixa (com paddings já calculados)
    e aplica códigos ANSI sobrescrevendo ocorrências dos substrings indicados em `highlights`.
    highlights: lista de tuplas (substring_plain, color_code, mode)
      mode = "first" (default)  -> substitui apenas a primeira ocorrência
      mode = "all"              -> substitui todas as ocorrências
    Observação: as substituições ocorrem sobre o texto já padronizado,
    então a largura visível não muda.
    """
    result = box_text
    for item in highlights:
        if len(item) == 2:
            substr, color = item
            mode = "first"
        else:
            substr, color, mode = item

        colored = f"{color}{substr}{RESET}"
        if mode == "all":
            result = result.replace(substr, colored)
        else:
            result = result.replace(substr, colored, 1)
    return result


def get_ducky_banner():
    """Banner com o pato em azul escuro e caixa de informações alinhada corretamente"""
    duck_art = f'''
{DARK_BLUE}
                                            ██████████                                  
                                      ░░  ██░░░░░░░░░░██                                
                                        ██░░░░░░░░░░░░░░██                              
                                        ██░░░░░░░░████░░██████████                      
                            ██          ██░░░░░░░░████░░██▒▒▒▒▒▒██                      
                          ██░░██        ██░░░░░░░░░░░░░░██▒▒▒▒▒▒██                      
                          ██░░░░██      ██░░░░░░░░░░░░░░████████                        
                        ██░░░░░░░░██      ██░░░░░░░░░░░░██                              
                        ██░░░░░░░░████████████░░░░░░░░██                                
                        ██░░░░░░░░██░░░░░░░░░░░░░░░░░░░░██                              
                        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            
                        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            
                        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            
                        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            
                        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            
                        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            
                        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                            
                        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██                              
                          ██░░░░░░░░░░░░░░░░░░░░░░░░░░██                                
                            ██████░░░░░░░░░░░░░░░░████                                  
                                  ████████████████                                      
{RESET}
'''

    # Montamos linhas "plain" (sem cor) e só depois aplicamos cor
    inner_width = 58  # largura interna da caixa, ajustar se quiser mais largo

    # Criar as linhas com largura consistente
    # bloco verde (linha inteira de blocos)
    block_line = "▓" * inner_width

    # Linha de título: colocamos '▓▓' nas laterais e centralizamos o texto
    title_text = "D U C K Y   R E C O R D E R"
    # Reservamos 4 colunas para os dois pares de '▓' (2 no início + 2 no final),
    # então o espaço disponível para o título é inner_width - 4
    padded_title = title_text.center(inner_width - 4)
    title_line = f"▓▓{padded_title}▓▓"

    plain_lines = [
        " " * inner_width,  # linha vazia dentro da caixa
        " " * inner_width,
        block_line,
        title_line,
        block_line,
        " " * inner_width,
        f"Version: {__version__}",
        f"Author:  {__author__}",
        " " * inner_width,
    ]

    # Gera caixa com padding baseado nas linhas "plain"
    box_plain = _make_box(plain_lines, inner_width)

    # Define destaques e cores
    highlights = [
        # colorir todas as linhas de blocos
        (block_line, GREEN, "all"),
        # colorir o título apenas na primeira ocorrência (apenas uma existência esperada)
        (title_line, GREEN, "first"),
        ("Version:", YELLOW, "first"),
        (__version__, YELLOW, "first"),
        ("Author:", YELLOW, "first"),
        (__author__, YELLOW, "first"),
    ]

    # Aplica a coloração sem alterar o alinhamento
    colored_box = _apply_highlights(box_plain, highlights)

    # Moldura externa em ciano (bordas) - aplicamos por último
    # substituímos os caracteres de borda pela versão ciano apenas visualmente
    # usamos replace em todas as ocorrências (bordas múltiplas)
    colored_box = colored_box.replace("╔", f"{CYAN}╔{RESET}")
    colored_box = colored_box.replace("╚", f"{CYAN}╚{RESET}")
    colored_box = colored_box.replace("╗", f"{CYAN}╗{RESET}")
    colored_box = colored_box.replace("╝", f"{CYAN}╝{RESET}")
    colored_box = colored_box.replace("║", f"{CYAN}║{RESET}")

    return duck_art + colored_box


def get_compact_banner():
    """Banner compacto para telas menores com caixa alinhada"""
    compact_duck = f'''
{DARK_BLUE}
        ████████
      ██░░░░░░░░██
    ██░░░░░░░░░░░░██
    ██░░░░░░████░░████
    ██░░░░░░████░░██▒▒██
    ██░░░░░░░░░░░░██▒▒██
    ██░░░░░░░░░░░░████
      ██░░░░░░░░██
        ████████
{RESET}
'''
    inner_width = 38

    block_line = "▓" * inner_width
    title_text = f"DUCKY RECORDER v{__version__}"
    # Reservamos 4 colunas para os '▓▓' laterais
    padded_title = title_text.center(inner_width - 4)
    title_line = f"▓▓{padded_title}▓▓"

    plain_lines = [
        " " * inner_width,
        block_line,
        title_line,
        block_line,
        f"by {__author__}",
        " " * inner_width,
    ]

    box_plain = _make_box(plain_lines, inner_width)

    highlights = [
        (block_line, GREEN, "all"),
        (title_line, GREEN, "first"),
        (f"by {__author__}", YELLOW, "first"),
    ]

    colored_box = _apply_highlights(box_plain, highlights)

    colored_box = colored_box.replace("╔", f"{CYAN}╔{RESET}")
    colored_box = colored_box.replace("╚", f"{CYAN}╚{RESET}")
    colored_box = colored_box.replace("╗", f"{CYAN}╗{RESET}")
    colored_box = colored_box.replace("╝", f"{CYAN}╝{RESET}")
    colored_box = colored_box.replace("║", f"{CYAN}║{RESET}")

    return compact_duck + colored_box


def get_minimal_banner():
    """Banner minimalista para linha de comando"""
    return f'''
{DARK_BLUE}
        🦆 DUCKY RECORDER {GREEN}v{__version__}{RESET}
        {YELLOW}by {__author__}{RESET}
        
        Hid Event Recorder & Exporter
{RESET}
'''


# Função principal que escolhe o banner automaticamente
def get_banner(screen_width=80):
    """Retorna o banner apropriado baseado na largura da tela"""
    import os

    try:
        # Tenta obter o tamanho do terminal
        terminal_size = os.get_terminal_size()
        width = terminal_size.columns
    except:
        width = screen_width  # Valor padrão

    if width >= 100:
        return get_ducky_banner()
    elif width >= 60:
        return get_compact_banner()
    else:
        return get_minimal_banner()


def show_banner():
    """Exibe o banner do DuckyRecorder"""
    print(get_banner())

# Exportar funções importantes
__all__ = ['show_banner', 'get_banner', 'get_ducky_banner', 
           'get_compact_banner', 'get_minimal_banner', 
           '__version__', '__author__']
