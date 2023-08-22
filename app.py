import requests
from tkinter import *
from tkinter import ttk
from datetime import datetime, date
from PIL import Image, ImageTk  # Importa o módulo PIL para trabalhar com imagens
from tkinter import messagebox

# Nome do usuário logado (será definido após o login bem-sucedido)
usuario_logado = None


# Dicionário de usuários e senhas
usuarios_senhas = {
    'claudio x': 'x',
    'daniele x': 'x',
    'gustavo x': 'x',
    'simone x': 'x',
    'bertiani x': 'x',
    'thatiana x': 'x'
}

# Dicionário de tokens associados aos usuários
usuarios_tokens = {
    'claudio': 'x',
    'daniele': 'x',
    'gustavo': 'x',
    'simone': 'x',
    'bertiani': 'x',
    'thatiana': 'x'

}




def reiniciar_tela_principal(janela):
    janela.destroy()  # Fecha a janela atual
    iniciar_tela_principal(usuario_logado)  # Chama a função para recriar a tela principal




# Função para verificar o login
def verificar_login():
    global usuario_logado
    username = username_entry.get().lower()  # Transforma em minúsculas
    password = password_entry.get()

    # Verificar as credenciais
    if username in usuarios_senhas and usuarios_senhas[username] == password:
        primeiro_nome = username.split()[0]  # Pega o primeiro nome
        usuario_logado = primeiro_nome
        login_window.destroy()
        iniciar_tela_principal(primeiro_nome)
    else:
        messagebox.showerror("Erro de Login", "Credenciais inválidas")


# Função para iniciar a tela principal após o login bem-sucedido
def iniciar_tela_principal(usuario):
    token_RD = usuarios_tokens[usuario]

    # Variável global para armazenar os orçamentos
    orcamentos = []

    # Variável global para armazenar as variáveis das caixas de seleção
    checkboxes = []

    # Função para buscar e imprimir os orçamentos
# Função para buscar e imprimir os orçamentos
    def buscar_orcamentos():
        # Limpa o texto na saída
        output_text.delete(1.0, END)

        # Data informada pelo usuário
        data_informada = date_entry.get()

        # URL da primeira API para obter o token de acesso
        token_url = "https://api-erp.metroex.com.br/api/v1/auth/token"

        # Parâmetros para autenticação no corpo da solicitação
        body = {
            "login": "claudio.moraes@lempe",
            "password": "8574"
        }

        try:
            # Faz a solicitação POST para obter o token
            response = requests.post(token_url, json=body)

            # Verifica se a solicitação foi bem-sucedida (código de status 200)
            if response.status_code == 200:
                # Obtém o token de acesso a partir da resposta
                token = response.json().get("access_token")

                # URL da segunda API para obter todos os orçamentos com a data informada
                second_api_url = f'https://api-erp.metroex.com.br/api/v1/budgets/?fields=["identifier","Code","SendDate","Customer.Name","CustomerContact.Name","Responsible.Name","Status","FinalValue"]&orderBy=["SendDate DESC"]'

                # Define o cabeçalho de autorização
                headers = {
                    "Authorization": f"Bearer {token}"
                }

                # Faz a solicitação GET com o cabeçalho de autorização
                response2 = requests.get(second_api_url, headers=headers)

                # Verifica se a solicitação foi bem-sucedida (código de status 200)
                if response2.status_code == 200:
                    # Processa a resposta da segunda solicitação
                    data = response2.json()

                    # Converta a data informada pelo usuário para o formato correto
                    data_informada = datetime.strptime(data_informada, "%Y-%m-%d").date()

                    # Limpa a lista de orçamentos
                    orcamentos.clear()

                    # Loop para cada item no resultado
                    for item in data:
                        SendDate = item.get('SendDate', '')
                        if SendDate:
                            send_date = datetime.strptime(SendDate.split('T')[0], "%Y-%m-%d").date()
                        else:
                            send_date = None

                        if send_date and send_date == data_informada:
                            code = item['Code']
                            customer_name = item['Customer']['Name']
                            responsible_name = item['Responsible']['Name']
                            status = item['Status']
                            final_value = item['FinalValue']
                            customer_contact = item['CustomerContact']['Name'] or 'N/A'

                            # Adiciona o orçamento à lista
                            orcamentos.append({
                                "identifier": code,
                                "customer_name": customer_name,
                                "responsible_name": responsible_name,
                                "status": status,
                                "final_value": final_value,
                                "customer_contact": customer_contact
                            })

                    # Exibe os orçamentos na interface
                    exibir_orcamentos(orcamentos)
                else:
                    output_text.insert(END, f"Falha na segunda solicitação. Código de status: {response2.status_code}\n")
                    output_text.insert(END, "Resposta:\n")
                    output_text.insert(END, response2.text + "\n")
            else:
                output_text.insert(END, f"Falha na primeira solicitação. Código de status: {response.status_code}\n")
                output_text.insert(END, "Resposta:\n")
                output_text.insert(END, response.text + "\n")
        except Exception as e:
            output_text.insert(END, f"Ocorreu um erro: {e}\n")

        # Função para exibir os orçamentos na interface
    def exibir_orcamentos(orcamentos):
        # Limpa a lista de checkboxes anteriores
        checkboxes.clear()

        # Cria um novo frame para os checkboxes
        checkbox_frame = Frame(root)

        # Adiciona o frame ao Canvas para permitir rolagem
        canvas = Canvas(checkbox_frame)
        scrollbar = Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Adiciona o Canvas e a barra de rolagem ao frame principal
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Cria um frame para os checkboxes dentro do Canvas
        inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Exibe a lista de orçamentos na interface
        for count, orcamento in enumerate(orcamentos, start=1):
            responsible_name = orcamento['responsible_name']
            responsible_name = responsible_name.split()[0].lower()

            if usuario_logado == 'claudio':
                
                identifier = orcamento['identifier']
                customer_name = orcamento['customer_name']
                customer_contact = orcamento['customer_contact'] or 'N/A'
                status = orcamento['status']
                final_value = orcamento['final_value']

                                # Cria uma variável para a caixa de seleção
                var = IntVar()
                checkboxes.append(var)

                # Exibe a caixa de seleção
                checkbox = Checkbutton(inner_frame, variable=var, text=f"Orçamento {count}")
                checkbox.grid(row=count-1, column=0, sticky="w", padx=5, pady=5)

                # Formatação para exibição
                output = f"Orçamento {count}\n"
                output += f"Identificador: {identifier}\n"
                output += f"Nome do Cliente: {customer_name}\n"
                output += f"Contato do Cliente: {customer_contact}\n"
                output += f"Nome do Responsável: {responsible_name}\n"
                output += f"Status: {status}\n"
                output += f"Valor Final: {final_value}\n"
                output += "--------------------------\n"

                # Insere o texto formatado na saída
                output_text.insert(END, output)
            
            elif responsible_name == usuario_logado:
                identifier = orcamento['identifier']
                customer_name = orcamento['customer_name']
                customer_contact = orcamento['customer_contact'] or 'N/A'
                status = orcamento['status']
                final_value = orcamento['final_value']

                # Cria uma variável para a caixa de seleção
                var = IntVar()
                checkboxes.append(var)

                # Exibe a caixa de seleção
                checkbox = Checkbutton(inner_frame, variable=var, text=f"Orçamento {count}")
                checkbox.grid(row=count-1, column=0, sticky="w", padx=5, pady=5)

                # Formatação para exibição
                output = f"Orçamento {count}\n"
                output += f"Identificador: {identifier}\n"
                output += f"Nome do Cliente: {customer_name}\n"
                output += f"Contato do Cliente: {customer_contact}\n"
                output += f"Nome do Responsável: {responsible_name}\n"
                output += f"Status: {status}\n"
                output += f"Valor Final: {final_value}\n"
                output += "--------------------------\n"

                # Insere o texto formatado na saída
                output_text.insert(END, output)

            # Configura o Canvas para rolagem
            inner_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        # Empacota o frame do Canvas
        checkbox_frame.pack(pady=10)

    # Função para processar a seleção dos orçamentos
    def processar_selecao():
        # Limpa o texto na saída
        output_text.delete(1.0, END)

        # Itera sobre os orçamentos e executa a ação para os selecionados
        for i, (orcamento, var) in enumerate(zip(orcamentos, checkboxes), start=1):
            if var.get():
                customer_name = orcamento['customer_name']
                final_value = orcamento['final_value']
                customer_contact = orcamento['customer_contact']
                # Insira aqui o código para cada orçamento selecionado
                url = f'https://crm.rdstation.com/api/v1/deals?token={token_RD}'
                headers = {
                    'accept': 'application/json',
                    'content-type': 'application/json'
                }
                data = {
                    "deal": {
                        "deal_stage_id": "648b61d549c590002446195e",
                        "name": customer_name
                    },

                    "deal_products": [
                        {
                            "description": "Descrição detalhada",
                            "name": "Orçamento",
                            "price": final_value
                        }
                    ],
                    "contacts": [
                        {
                        "name": customer_contact
                        }
                    ]
                        
                }

                response = requests.post(url, json=data, headers=headers)

                if response.status_code == 200:
                    output_text.insert(END, f"Orçamento {i} processado com sucesso!\n")
                    output_text.insert(END, "Resposta:\n")
                    output_text.insert(END, str(response.json()) + "\n")
                else:
                    output_text.insert(END, f"Falha ao processar o orçamento {i}. Código de status: {response.status_code}\n")
                    output_text.insert(END, "Resposta:\n")
                    output_text.insert(END, response.text + "\n")



    # Cria a janela principal
    root = Tk()
    root.title("Buscar Orçamentos")
    root.geometry("800x600")

    # Carrega a imagem da logo (substitua pelo caminho para sua própria imagem)
    logo_path = "images.png"
    logo_image = Image.open(logo_path)
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Mostra a logo na interface
    logo_label = Label(root, image=logo_photo)
    logo_label.pack(pady=10)

#########
    # Carrega a imagem da empresa e redimensiona
    empresa_image_path = "prog.png"
    empresa_image = Image.open(empresa_image_path)
    width, height = empresa_image.size
    new_width = 20  # Novo valor de largura desejado
    new_height = int((new_width / width) * height)
    empresa_image = empresa_image.resize((new_width, new_height), Image.ANTIALIAS)
    empresa_photo = ImageTk.PhotoImage(empresa_image)

    # Cria um Frame para o rodapé
    rodape_frame = Frame(root)
    rodape_frame.pack(side="bottom", fill="both", padx=10, pady=10)

    # Exibe o texto no rodapé
    texto_label = Label(rodape_frame, text="© - Todos os direitos reservados", font=("Helvetica", 8))
    texto_label.pack(side="right")

    # Exibe a imagem da empresa no rodapé
    empresa_label = Label(rodape_frame, image=empresa_photo)
    empresa_label.pack(side="right")



#############



    # Etiqueta e campo de entrada para a data
    Label(root, text="Informe a data (AAAA-MM-DD):").pack(pady=10)
    today = date.today().strftime("%Y-%m-%d")
    date_entry = Entry(root, width=20)
    date_entry.insert(0, today)  # Define a data de hoje como padrão
    date_entry.pack()


    # Botão para buscar os orçamentos
    buscar_button = Button(root, text="Buscar Orçamentos", command=buscar_orcamentos, width=30)
    buscar_button.pack(pady=10)

    # Botão para reiniciar tela

    reiniciar_button = Button(root, text="Reiniciar Tela", command=lambda: reiniciar_tela_principal(root), width=30)
    reiniciar_button.pack(pady=5)

    

    # Frame para os checkboxes
    checkbox_frame = Frame(root)
    checkbox_frame.pack(pady=10)

    # Lista para armazenar as variáveis das checkboxes
    checkboxes = []

    # Cria e organiza os checkboxes em sequência horizontal
    for i in range(len(orcamentos)):
        var = IntVar()
        checkboxes.append(var)  # Adicione a variável à lista
        checkbox = ttk.Checkbutton(checkbox_frame, text=f"Orçamento {i+1}", variable=var)
        checkbox.grid(row=0, column=i, padx=10, sticky="w")

    # Área de saída (scrollbar para permitir rolagem)
    output_text = Text(root, height=10, width=80)
    scrollbar = Scrollbar(root, command=output_text.yview)
    output_text.config(yscrollcommand=scrollbar.set)
    output_text.pack(pady=10, padx=10, fill="both", expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Botão para processar a seleção dos orçamentos
    processar_button = Button(root, text="Processar Seleção", command=processar_selecao, width=30)
    processar_button.pack(pady=10)

    # Estilo para os botões (usando ttk)
    style = ttk.Style()
    style.configure("TButton", padding=5, relief="flat", background="#007acc", foreground="white")
    style.map("TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[("pressed", "!focus", "#005082"), ("active", "#005082")])

    # Inicia a interface gráfica
    root.mainloop()

# Cria a janela de login
login_window = Tk()
login_window.title("Login")

# Ajuste da geometria da janela
largura = 400
altura = 300
x_pos = (login_window.winfo_screenwidth() - largura) // 2
y_pos = (login_window.winfo_screenheight() - altura) // 2
login_window.geometry(f"{largura}x{altura}+{x_pos}+{y_pos}")

# Campos de entrada para usuário e senha
ttk.Label(login_window, text="Usuário:").place(x=50, y=50)
username_entry = ttk.Entry(login_window)
username_entry.place(x=150, y=50)

ttk.Label(login_window, text="Senha:").place(x=50, y=100)
password_entry = ttk.Entry(login_window, show="*")
password_entry.place(x=150, y=100)

# Botão de login
login_button = ttk.Button(login_window, text="Login", command=verificar_login)
login_button.place(x=150, y=150)

# Inicia a janela de login
login_window.mainloop()