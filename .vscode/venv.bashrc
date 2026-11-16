[ -f ~/.bashrc ] && . ~/.bashrc

if [ -f .venv/bin/activate ]; then
  . .venv/bin/activate
else
  echo "No .venv yet - run: uv sync"
fi
