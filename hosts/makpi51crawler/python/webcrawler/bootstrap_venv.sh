#!/usr/bin/env bash
set -Eeuo pipefail

# English:
# This script creates or reuses a local Python virtual environment for the
# webcrawler surface and installs the tracked repository dependencies from
# requirements.txt. It does not introduce a second dependency truth.
#
# Türkçe:
# Bu betik, webcrawler yüzeyi için yerel bir Python sanal ortamı oluşturur
# veya varsa yeniden kullanır ve izlenen repository bağımlılıklarını
# requirements.txt dosyasından kurar. İkinci bir bağımlılık doğrusu üretmez.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
REQ_FILE="${SCRIPT_DIR}/requirements.txt"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "== WEBCRAWLER BOOTSTRAP VENV =="
date -Is
echo "SCRIPT_DIR=${SCRIPT_DIR}"
echo "VENV_DIR=${VENV_DIR}"
echo "REQ_FILE=${REQ_FILE}"
echo "PYTHON_BIN=${PYTHON_BIN}"
echo

# English:
# The tracked dependency surface must exist before bootstrap can proceed.
#
# Türkçe:
# Bootstrap işlemi ilerlemeden önce izlenen bağımlılık yüzeyi mevcut olmalıdır.
[ -f "${REQ_FILE}" ] || {
  echo "FAIL requirements.txt not found: ${REQ_FILE}" >&2
  exit 1
}

# English:
# The selected Python interpreter must be available on the machine.
#
# Türkçe:
# Seçilen Python yorumlayıcısı makinede mevcut olmalıdır.
command -v "${PYTHON_BIN}" >/dev/null 2>&1 || {
  echo "FAIL python interpreter not found: ${PYTHON_BIN}" >&2
  exit 1
}

# English:
# Create the local virtual environment only when it does not exist yet.
#
# Türkçe:
# Yerel sanal ortam yalnızca henüz yoksa oluşturulur.
if [ ! -d "${VENV_DIR}" ]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# English:
# Activate the local virtual environment inside this script so subsequent
# python and pip commands target the controlled local environment.
#
# Türkçe:
# Sonraki python ve pip komutlarının kontrollü yerel ortama yönlenmesi için
# bu betiğin içinde yerel sanal ortamı aktif et.
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

# English:
# Upgrade local packaging tools for reliable installation behavior without
# changing the tracked dependency truth of the repository.
#
# Türkçe:
# Repository'nin izlenen bağımlılık doğrusunu değiştirmeden daha güvenilir
# kurulum davranışı için yerel paketleme araçlarını yükselt.
python -m pip install --upgrade pip setuptools wheel

# English:
# Install the tracked dependency set from requirements.txt.
#
# Türkçe:
# İzlenen bağımlılık kümesini requirements.txt dosyasından kur.
python -m pip install -r "${REQ_FILE}"

# English:
# Print a small proof block so the operator can verify the bound interpreter
# and pip inside the local environment.
#
# Türkçe:
# Operatörün yerel ortama bağlı yorumlayıcıyı ve pip'i doğrulayabilmesi için
# küçük bir kanıt bloğu yazdır.
echo
echo "== VENV PROOF =="
echo "python=$(command -v python)"
python --version
echo "pip=$(command -v pip)"
pip --version
echo
echo "OK webcrawler local venv bootstrap completed"
echo "NEXT source \"${VENV_DIR}/bin/activate\""
