# Servidor de letras de Wu en Render (plan gratis)

1. Sube la carpeta `servidor/` a un repositorio de GitHub (tu cuenta).
2. En Render: New + → Blueprint → elige el repositorio. Render lee `render.yaml`.
3. Cuando te pida `ANTHROPIC_API_KEY`, pega tu llave de Anthropic. La llave solo vive en Render.
4. Al terminar, Render te da una URL tipo https://wuwi-letras.onrender.com.
5. Pruébalo: curl -X POST https://TU-URL/letra -H 'content-type: application/json' -d '{"tema":"lluvia","genero":"balada"}'

Nota del plan gratis: el servicio se duerme tras 15 minutos sin uso; la primera petición tarda unos 30 segundos.
