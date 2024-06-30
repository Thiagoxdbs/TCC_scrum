import customtkinter as ctk
from app import AplicativoScrum

if __name__ == "__main__":
    # Cria a raiz da aplicação e inicializa o aplicativo Scrum
    raiz = ctk.CTk()
    app = AplicativoScrum(raiz)
    raiz.mainloop()
