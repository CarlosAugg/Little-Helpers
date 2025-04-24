import threading
import pyperclip
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import ttkbootstrap as tb
from ttkbootstrap.constants import PRIMARY, INFO, SUCCESS, WARNING, DANGER, SECONDARY
from tkinter import filedialog, messagebox

# --- Funções de lógica ---

def obter_video_id(url):
    try:
        parsed = urlparse(url)
        if parsed.netloc in ('www.youtube.com', 'youtube.com'):
            return parse_qs(parsed.query).get('v', [None])[0]
        if parsed.netloc == 'youtu.be':
            return parsed.path.lstrip('/')
    except Exception:
        return None
    return None


def obter_transcricao(video_id):
    try:
        lista = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            trans = lista.find_transcript(['pt'])
        except NoTranscriptFound:
            trans = next(iter(lista))
        texto = ' '.join(item['text'] for item in trans.fetch())
        return texto, trans.language_code
    except TranscriptsDisabled:
        return None, 'Transcrições desabilitadas.'
    except NoTranscriptFound:
        return None, 'Nenhuma transcrição disponível.'
    except Exception as e:
        return None, str(e)


def set_status(msg, color=SECONDARY):
    status_label.config(text=msg, bootstyle=color)

# --- Callbacks ---

def processar_transcricao():
    video_id = obter_video_id(entry_url.get())
    if not video_id:
        set_status('URL inválida ou ID não encontrado.', DANGER)
        bot_buscar.state(['!disabled'])
        return

    set_status('Obtendo transcrição...', INFO)
    texto, idioma = obter_transcricao(video_id)
    text_box.delete('1.0', 'end')

    if texto:
        text_box.insert('1.0', texto)
        set_status(f'Transcrição completa (idioma: {idioma}).', SUCCESS)
    else:
        set_status(f'Erro: {idioma}', WARNING)

    bot_buscar.state(['!disabled'])


def buscar():
    bot_buscar.state(['disabled'])
    threading.Thread(target=processar_transcricao, daemon=True).start()


def copiar():
    texto = text_box.get('1.0', 'end').strip()
    if texto:
        pyperclip.copy(texto)
        set_status('Transcrição copiada!', INFO)
    else:
        set_status('Nada para copiar.', WARNING)


def salvar():
    texto = text_box.get('1.0', 'end').strip()
    if not texto:
        messagebox.showwarning('Aviso', 'Nada para salvar.')
        return
    caminho = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Texto', '*.txt')])
    if caminho:
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(texto)
        set_status('Arquivo salvo com sucesso.', SUCCESS)


def limpar():
    text_box.delete('1.0', 'end')
    set_status('', SECONDARY)


def toggle_theme():
    tema = 'litera' if theme_var.get() else 'darkly'
    app.style.theme_use(tema)

# --- Configuração da GUI ---
app = tb.Window(themename='darkly')  # inicia em modo noturno
app.title('YouTube Transcriber')
app.geometry('800x600')

# Header com título e switch de tema
header = tb.Frame(app, padding=10)
header.pack(fill=tb.X)
tb.Label(header, text='📜 YouTube Transcriber', font=('Segoe UI', 18, 'bold')).pack(side=tb.LEFT)

theme_var = tb.BooleanVar(value=False)
switch = tb.Checkbutton(header, text='Modo Claro', variable=theme_var,
                        bootstyle='switch', command=toggle_theme)
switch.pack(side=tb.RIGHT)

# Frame principal
main = tb.Frame(app, padding=15)
main.pack(fill=tb.BOTH, expand=True)

# Entrada de URL
tb.Label(main, text='🔗 URL do vídeo:', font=('Segoe UI', 12)).grid(row=0, column=0, sticky='w')
entry_url = tb.Entry(main, width=60, font=('Segoe UI', 11))
entry_url.grid(row=0, column=1, pady=5, sticky='we')
bot_buscar = tb.Button(main, text='Buscar', bootstyle=PRIMARY, width=12, command=buscar)
bot_buscar.grid(row=0, column=2, padx=5)

# Área de transcrição
text_box = tb.Text(main, wrap=tb.WORD, font=('Consolas', 11), height=20)
text_box.grid(row=1, column=0, columnspan=3, pady=10, sticky='nsew')
scroll = tb.Scrollbar(main, command=text_box.yview)
scroll.grid(row=1, column=3, sticky='ns')
text_box['yscrollcommand'] = scroll.set

main.rowconfigure(1, weight=1)
main.columnconfigure(1, weight=1)

# Botões com ações rápidas
actions = tb.Frame(main)
actions.grid(row=2, column=0, columnspan=3, pady=10)
btns = [
    ('📋 Copiar', copiar, INFO),
    ('💾 Salvar', salvar, SUCCESS),
    ('🧹 Limpar', limpar, WARNING)
]
for txt, cmd, style in btns:
    tb.Button(actions, text=txt, bootstyle=style, command=cmd).pack(side=tb.LEFT, padx=5)

# Status bar
status_label = tb.Label(app, text='', bootstyle=SECONDARY, anchor='w')
status_label.pack(fill=tb.X, side=tb.BOTTOM)

app.mainloop()