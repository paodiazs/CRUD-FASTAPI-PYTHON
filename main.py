from fastapi import FastAPI, Request, Form #
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database import get_connection

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#----------------------------------------------------------------------#
# MOSTRAR FORM
@app.get("/form", response_class=HTMLResponse)
def mostrar_formulario(request: Request):
    return templates.TemplateResponse(
        "form.html",
        {"request": request}
    )


#----------------------------------------------------------------------#
# ENDPOINT CREAR USUARIO
@app.post("/guardar")
def guardar_usuario(
    nombre: str = Form(...),
    edad: int = Form(...)
):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO usuarios (nombre, edad) VALUES (%s, %s)"
    valores = (nombre, edad)

    cursor.execute(sql, valores)
    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse(
            url="/usuarios",
            status_code = 303)


#----------------------------------------------------------------------#
# ENDPOINT OBTENER USUARIOS
@app.get("/usuarios")
def mostrar_usuarios(request : Request):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary = True)
        cursor.execute("SELECT id, nombre, edad FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return templates.TemplateResponse(
            "usuarios.html",{
                "request" : request,
                "usuarios" : usuarios
            }
        )
    except Exception as e:
        return {"error" : str(e)}


#----------------------------------------------------------------------#
# ENDPOINT EDITAR USUARIO       
@app.get("/usuarios/editar/{id}", response_class=HTMLResponse)
def editar_usuario_form(request: Request, id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT id, nombre, edad FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        return templates.TemplateResponse(
            "editar.html",
            {
                "request": request,
                "usuario": usuario
            }
        )

    except Exception as e:
        return {"error": str(e)}
@app.post("/usuarios/editar/{id}")
def editar_usuario(
    id: int,
    nombre: str = Form(...),
    edad: int = Form(...)
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE usuarios
            SET nombre = %s, edad = %s
            WHERE id = %s
        """
        cursor.execute(sql, (nombre, edad, id))
        conn.commit()

        cursor.close()
        conn.close()

        return RedirectResponse(
            url="/usuarios",
            status_code=303
        )

    except Exception as e:
        return {"error": str(e)}


#----------------------------------------------------------------------#
# ENDPOINT ELIMINAR USUARIO
@app.post("/eliminar/usuario/{id}")
def eliminar_usuario(id : int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        cursor.close()
        conn.close()
        return RedirectResponse(
            url="/usuarios",
            status_code = 303)
        
    except Exception as e:
        return {"error" : str(e)}
