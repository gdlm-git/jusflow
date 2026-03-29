from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = "jusflow_secret"


def get_connection():
    return psycopg2.connect(
        "postgresql://postgres.uiyfmyhhuvdtiomnnhwt:Jusflow%402026@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
    )


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/entrar", methods=["POST"])
def entrar():
    email = request.form["email"]
    senha = request.form["senha"]
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    return redirect(url_for("login"))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/salvar-cliente", methods=["POST"])
def salvar_cliente():
    nome = request.form["nome"].strip()
    cpf = request.form["cpf"].strip()
    telefone = request.form["telefone"].strip()
    email = request.form["email"].strip()
    tipo_causa = request.form["tipo_causa"].strip()
    status = request.form["status"].strip()

    if not nome or not cpf or not telefone or not email or not tipo_causa or not status:
        flash("Preencha todos os campos antes de cadastrar.")
        return redirect(url_for("cadastro"))

    conn = get_connection()
    cursor = conn.cursor()

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
        INSERT INTO clientes (nome, cpf, telefone, email, tipo_causa, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (nome, cpf, telefone, email, tipo_causa, status)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Cliente cadastrado com sucesso!")
    return redirect(url_for("clientes"))


@app.route("/clientes")
def clientes():
    busca = request.args.get("busca", "").strip()

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if busca:
        cursor.execute(
            """
            SELECT id, nome, cpf, telefone, email, tipo_causa, status
            FROM clientes
            WHERE nome ILIKE %s OR cpf ILIKE %s
            ORDER BY id
            """,
            (f"%{busca}%", f"%{busca}%")
        )
    else:
        cursor.execute(
            """
            SELECT id, nome, cpf, telefone, email, tipo_causa, status
            FROM clientes
            ORDER BY id
            """
        )

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("clientes.html", clientes=clientes)


@app.route("/cliente/<int:id>")
def detalhe_cliente(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT id, nome, cpf, telefone, email, tipo_causa, status
        FROM clientes
        WHERE id = %s
        """,
        (id,)
    )
    cliente = cursor.fetchone()

    if not cliente:
        cursor.close()
        conn.close()
        return "Cliente não encontrado", 404

    cursor.execute(
        """
        SELECT id, numero_processo, descricao, data_abertura, status_processo
        FROM processos
        WHERE cliente_id = %s
        ORDER BY id DESC
        """,
        (id,)
    )
    processos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "detalhe_cliente.html",
        cliente=cliente,
        processos=processos
    )


@app.route("/cadastro-processo/<int:cliente_id>")
def cadastro_processo(cliente_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT id, nome, cpf, telefone, email, tipo_causa, status
        FROM clientes
        WHERE id = %s
        """,
        (cliente_id,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    if not cliente:
        return "Cliente não encontrado", 404

    return render_template("cadastro_processo.html", cliente=cliente)


@app.route("/salvar-processo/<int:cliente_id>", methods=["POST"])
def salvar_processo(cliente_id):
    numero_processo = request.form["numero_processo"].strip()
    descricao = request.form["descricao"].strip()
    data_abertura = request.form["data_abertura"].strip()
    status_processo = request.form["status_processo"].strip()

    if not numero_processo or not descricao or not data_abertura or not status_processo:
        flash("Preencha todos os campos do processo antes de salvar.")
        return redirect(url_for("cadastro_processo", cliente_id=cliente_id))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO processos (cliente_id, numero_processo, descricao, data_abertura, status_processo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (cliente_id, numero_processo, descricao, data_abertura, status_processo)
    )

    novo_processo_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    flash("Processo cadastrado com sucesso!")
    return redirect(url_for("detalhe_processo", id=novo_processo_id))


@app.route("/processo/<int:id>")
def detalhe_processo(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT
            p.id,
            p.cliente_id,
            p.numero_processo,
            p.descricao,
            p.data_abertura,
            p.status_processo,
            p.created_at,
            c.nome AS cliente_nome,
            c.cpf AS cliente_cpf,
            c.telefone AS cliente_telefone,
            c.email AS cliente_email
        FROM processos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.id = %s
        """,
        (id,)
    )

    processo = cursor.fetchone()

    cursor.close()
    conn.close()

    if not processo:
        return "Processo não encontrado", 404

    return render_template("detalhe_processo.html", processo=processo)


@app.route("/editar-cliente/<int:id>")
def editar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nome, cpf, telefone, email, tipo_causa, status
        FROM clientes
        WHERE id = %s
        """,
        (id,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/atualizar-cliente/<int:id>", methods=["POST"])
def atualizar_cliente(id):
    nome = request.form["nome"].strip()
    cpf = request.form["cpf"].strip()
    telefone = request.form["telefone"].strip()
    email = request.form["email"].strip()
    tipo_causa = request.form["tipo_causa"].strip()
    status = request.form["status"].strip()

    if not nome or not cpf or not telefone or not email or not tipo_causa or not status:
        flash("Preencha todos os campos antes de salvar.")
        return redirect(url_for("editar_cliente", id=id))

    conn = get_connection()
    cursor = conn.cursor()

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
        SET nome = %s,
            cpf = %s,
            telefone = %s,
            email = %s,
            tipo_causa = %s,
            status = %s
        WHERE id = %s
        """,
        (nome, cpf, telefone, email, tipo_causa, status, id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Cliente atualizado com sucesso!")
    return redirect(url_for("clientes"))


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