import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os

from database import iniciar_banco
from models import Carrinho


# ---------------- CONFIGURAÇÃO ----------------

ctk.set_appearance_mode("dark")

iniciar_banco()

app = ctk.CTk()
app.title("Hot Wheels Manager PRO Versão 1.0")
app.geometry("1000x550")

caminho_foto_temp = ""
carrinho_selecionado = None


# ---------------- FUNÇÕES ----------------

def selecionar_foto():
    global caminho_foto_temp

    arquivo = filedialog.askopenfilename(
        filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
    )

    if arquivo:
        caminho_foto_temp = arquivo
        btn_foto.configure(
            text="Foto Selecionada ✅",
            fg_color="green"
        )


def cadastrar():

    global caminho_foto_temp

    nome = entry_nome.get()
    modelo = entry_modelo.get()
    cor = entry_cor.get()
    ano = entry_ano.get()

    if not (nome and modelo and cor and ano and caminho_foto_temp):
        messagebox.showwarning(
            "Erro",
            "Preencha todos os campos!"
        )
        return

    carrinho = Carrinho(
        nome,
        modelo,
        cor,
        ano,
        caminho_foto_temp
    )

    carrinho.salvar()

    entry_nome.delete(0, "end")
    entry_modelo.delete(0, "end")
    entry_cor.delete(0, "end")
    entry_ano.delete(0, "end")

    btn_foto.configure(text="Upload Foto")
    caminho_foto_temp = ""

    atualizar_lista()


def atualizar_lista(event=None):

    for widget in frame_lista.winfo_children():
        widget.destroy()

    termo = entry_busca.get()

    carrinhos = Carrinho.listar(termo)

    for car in carrinhos:

        btn = ctk.CTkButton(
            frame_lista,
            text=f"🔥 {car.nome}\n{car.modelo} • {car.cor} • {car.ano}",
            fg_color="transparent",
            anchor="w",
            height=50,
            command=lambda c=car:
                exibir_detalhes(c)
        )

        btn.pack(fill="x", padx=5, pady=3)


def exibir_detalhes(carrinho):

    global carrinho_selecionado
    carrinho_selecionado = carrinho

    label_nome.configure(
        text=f"{carrinho.nome}\n"
             f"{carrinho.modelo}\n"
             f"Cor: {carrinho.cor} | Ano: {carrinho.ano}"
    )

    if os.path.exists(carrinho.foto_path):

        img = Image.open(carrinho.foto_path)

        img_ctk = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(280, 180)
        )

        label_imagem.configure(image=img_ctk, text="")
        label_imagem.image = img_ctk
    else:
        label_imagem.configure(
            image=None,
            text="Imagem não encontrada"
        )


def excluir():

    global carrinho_selecionado

    if carrinho_selecionado is None:
        return

    if messagebox.askyesno(
        "Confirmar",
        "Deseja excluir o carrinho?"
    ):
        carrinho_selecionado.excluir()

        label_nome.configure(text="Selecione um item")
        label_imagem.configure(
            image=None,
            text="Sem imagem"
        )

        atualizar_lista()


# ---------------- INTERFACE ----------------

# ===== COLUNA CADASTRO =====

frame_cadastro = ctk.CTkFrame(app, width=250)
frame_cadastro.pack(side="left", fill="y", padx=10, pady=10)

ctk.CTkLabel(
    frame_cadastro,
    text="CADASTRAR CARRINHO",
    font=("Arial", 16, "bold")
).pack(pady=15)

entry_nome = ctk.CTkEntry(
    frame_cadastro,
    placeholder_text="Nome do Carrinho"
)
entry_nome.pack(pady=5)

entry_modelo = ctk.CTkEntry(
    frame_cadastro,
    placeholder_text="Modelo do Veículo"
)
entry_modelo.pack(pady=5)

entry_cor = ctk.CTkEntry(
    frame_cadastro,
    placeholder_text="Cor"
)
entry_cor.pack(pady=5)

entry_ano = ctk.CTkEntry(
    frame_cadastro,
    placeholder_text="Ano"
)
entry_ano.pack(pady=5)

btn_foto = ctk.CTkButton(
    frame_cadastro,
    text="Upload Foto",
    command=selecionar_foto
)
btn_foto.pack(pady=10)

ctk.CTkButton(
    frame_cadastro,
    text="SALVAR",
    fg_color="red",
    command=cadastrar
).pack(pady=20)


# ===== COLUNA LISTA =====

frame_meio = ctk.CTkFrame(app)
frame_meio.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

entry_busca = ctk.CTkEntry(
    frame_meio,
    placeholder_text="🔍 Buscar carrinho..."
)
entry_busca.pack(fill="x", padx=10, pady=10)
entry_busca.bind("<KeyRelease>", atualizar_lista)

frame_lista = ctk.CTkScrollableFrame(
    frame_meio,
    label_text="MINHA COLEÇÃO"
)
frame_lista.pack(fill="both", expand=True)


# ===== COLUNA DETALHES =====

frame_detalhes = ctk.CTkFrame(app, width=320)
frame_detalhes.pack(
    side="right",
    fill="y",
    padx=10,
    pady=10
)

label_nome = ctk.CTkLabel(
    frame_detalhes,
    text="Selecione um item",
    font=("Arial", 16, "bold")
)
label_nome.pack(pady=20)

label_imagem = ctk.CTkLabel(
    frame_detalhes,
    text="Sem imagem",
    width=280,
    height=180
)
label_imagem.pack(pady=10)

ctk.CTkButton(
    frame_detalhes,
    text="EXCLUIR CARRINHO",
    fg_color="#7a0000",
    hover_color="red",
    command=excluir
).pack(side="bottom", pady=20)


# ---------------- START ----------------

atualizar_lista()
app.mainloop()