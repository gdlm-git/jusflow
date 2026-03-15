from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "jusflow_secret"

# Função que cria uma nova conexão com o banco sempre que precisar
def get_connection():
    return psycopg2.connect(
        "postgresql://postgres.uiyfmyhhuvdtiomnnhwt:Jusflow%402026@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
    )

# Tela de login fake
@app.route("/")
def login():
    return render_template("login.html")

# Processa o login fake
@app.route("/entrar", methods=["POST"])
def entrar():
    email = request.form["email"]
    senha = request.form["senha"]

    return redirect(url_for("home"))

# Logout fake
@app.route("/logout")
def logout():
    return redirect(url_for("login"))

# Página inicial do sistema
@app.route("/home")
def home():
    return render_template("home.html")

# Página de cadastro
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

# Salvar cliente no banco
@app.route("/salvar-cliente", methods=["POST"])
def salvar_cliente():

    nome = request.form["nome"].strip()
    cpf = request.form["cpf"].strip()
    telefone = request.form["telefone"].strip()
    email = request.form["email"].strip()
    tipo_causa = request.form["tipo_causa"].strip()

    # Validação para não salvar vazio
    if not nome or not cpf or not telefone or not email or not tipo_causa:
        flash("Preencha todos os campos antes de cadastrar.")
        return redirect(url_for("cadastro"))

    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se já existe cliente com o mesmo CPF
    cursor.execute(
        "SELECT id FROM clientes WHERE cpf = %s",
        (cpf,)
    )

    cliente_existente = cursor.fetchone()

    if cliente_existente:
        cursor.close()
        conn.close()

        flash("CPF já cadastrado no sistema!")
        return redirect(url_for("cadastro"))

    cursor.execute(
        """
        INSERT INTO clientes (nome, cpf, telefone, email, tipo_causa)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nome, cpf, telefone, email, tipo_causa)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Cliente cadastrado com sucesso!")

    return redirect(url_for("clientes"))

# Lista de clientes com busca
@app.route("/clientes")
def clientes():

    busca = request.args.get("busca", "").strip()

    conn = get_connection()
    cursor = conn.cursor()

    if busca:
        cursor.execute(
            """
            SELECT id, nome, cpf, telefone, email, tipo_causa
            FROM clientes
            WHERE nome ILIKE %s OR cpf ILIKE %s
            """,
            (f"%{busca}%", f"%{busca}%")
        )
    else:
        cursor.execute("SELECT id, nome, cpf, telefone, email, tipo_causa FROM clientes")

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("clientes.html", clientes=clientes)

# Abrir tela de edição
@app.route("/editar-cliente/<int:id>")
def editar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nome, cpf, telefone, email, tipo_causa FROM clientes WHERE id = %s",
        (id,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("editar_cliente.html", cliente=cliente)

# Atualizar cliente
@app.route("/atualizar-cliente/<int:id>", methods=["POST"])
def atualizar_cliente(id):

    nome = request.form["nome"].strip()
    cpf = request.form["cpf"].strip()
    telefone = request.form["telefone"].strip()
    email = request.form["email"].strip()
    tipo_causa = request.form["tipo_causa"].strip()

    if not nome or not cpf or not telefone or not email or not tipo_causa:
        flash("Preencha todos os campos antes de salvar.")
        return redirect(url_for("editar_cliente", id=id))

    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se já existe outro cliente com o mesmo CPF
    cursor.execute(
        "SELECT id FROM clientes WHERE cpf = %s AND id <> %s",
        (cpf, id)
    )

    cliente_existente = cursor.fetchone()

    if cliente_existente:
        cursor.close()
        conn.close()

        flash("Já existe outro cliente com este CPF!")
        return redirect(url_for("editar_cliente", id=id))

    cursor.execute(
        """
        UPDATE clientes
        SET nome = %s, cpf = %s, telefone = %s, email = %s, tipo_causa = %s
        WHERE id = %s
        """,
        (nome, cpf, telefone, email, tipo_causa, id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Cliente atualizado com sucesso!")

    return redirect(url_for("clientes"))

# Excluir cliente
@app.route("/excluir-cliente/<int:id>")
def excluir_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Cliente excluído com sucesso!")

    return redirect(url_for("clientes"))

if __name__ == "__main__":
    app.run(debug=True)