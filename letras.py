# Servidor de letras de Wu. La llave vive aquí, nunca en la app.
# Uso: ANTHROPIC_API_KEY=... python3 letras.py   (puerto 8800)
import json, os, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

MODELO = "claude-haiku-5-5"
PUERTO = int(os.environ.get("PORT", "8800"))

def pedir_letra(tema, genero):
    llave = os.environ.get("ANTHROPIC_API_KEY", "")
    if not llave:
        raise RuntimeError("Falta ANTHROPIC_API_KEY en el servidor")
    cuerpo = {
        "model": MODELO,
        "max_tokens": 400,
        "messages": [{"role": "user", "content":
            f"Escribe una letra corta en español de México para una canción de {genero}, "
            f"sobre: {tema}. Exactamente 3 versos de una línea cada uno, sin título, sin explicación."}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(cuerpo).encode(),
        headers={"x-api-key": llave, "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        datos = json.loads(r.read())
    texto = "".join(b.get("text", "") for b in datos.get("content", []) if b.get("type") == "text")
    versos = [v.strip() for v in texto.split("\n") if v.strip()][:3]
    if len(versos) < 3:
        raise RuntimeError("La respuesta no trae 3 versos")
    return versos

class Handler(BaseHTTPRequestHandler):
    def _json(self, codigo, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def do_OPTIONS(self):
        self._json(204, {})
    def do_POST(self):
        if self.path != "/letra":
            return self._json(404, {"error": "no existe"})
        try:
            n = int(self.headers.get("content-length", "0"))
            datos = json.loads(self.rfile.read(n) or b"{}")
            tema = str(datos.get("tema", "amor"))[:120]
            genero = str(datos.get("genero", "pop"))[:40]
            self._json(200, {"versos": pedir_letra(tema, genero)})
        except Exception as e:
            self._json(503, {"error": str(e)})

if __name__ == "__main__":
    print("Servidor de letras en puerto", PUERTO)
    HTTPServer(("0.0.0.0", PUERTO), Handler).serve_forever()
