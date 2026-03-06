#!/bin/bash

# ==============================================================================
# SCRIPT DE SETUP: NEXUS ANALYTICS DASHBOARD
# ==============================================================================
# Este script prepara a infraestrutura do projeto.
# Coloque este ficheiro e o ficheiro 'app.py' na mesma pasta e execute:
# bash setup.sh
# ==============================================================================

echo "=================================================="
echo "🚀 A iniciar a configuração do projeto..."
echo "=================================================="

# 1. Inicializar o repositório Git
echo "📦 A inicializar o repositório Git..."
git init

# 2. Criar .gitignore
echo "📄 A criar .gitignore..."
cat << 'EOF' > .gitignore
# Ambientes Virtuais
venv/
env/
.env/

# Ficheiros Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Jupyter Notebooks
.ipynb_checkpoints

# OS
.DS_Store
Thumbs.db
EOF

# 3. Criar requirements.txt
echo "📄 A criar requirements.txt..."
cat << 'EOF' > requirements.txt
dash>=2.14.0
pandas>=2.1.0
plotly>=5.18.0
dash-bootstrap-components>=1.5.0
numpy>=1.26.0
EOF

# 4. Criar README.md
echo "📄 A criar README.md..."
cat << 'EOF' > README.md
# Nexus Analytics Dashboard 📊

Painel corporativo avançado construído em Python, utilizando **Dash**, **Pandas** e **Plotly**.

## 🚀 Como Executar Localmente

1. **Criar e ativar o ambiente virtual** (Recomendado):
   - Windows: `python -m venv venv` e depois `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` e depois `source venv/bin/activate`

2. **Instalar as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar o servidor**:
   ```bash
   python app.py
   ```

4. **Aceder à aplicação**:
   Abra o browser em [http://127.0.0.1:8050/](http://127.0.0.1:8050/)
EOF

# 5. Realizar o primeiro commit no Git (se o app.py já estiver na pasta)
echo "💾 A gravar o commit inicial..."
git add .
git commit -m "feat: setup inicial do projeto com dashboard base, gitignore e dependências"

echo "=================================================="
echo "✅ SETUP CONCLUÍDO COM SUCESSO!"
echo "=================================================="
echo "Para arrancar com o seu projeto siga estes passos:"
echo "  1. python -m venv venv"
echo "  2. Ative o ambiente virtual (ex: source venv/bin/activate ou venv\Scripts\activate no Windows)"
echo "  3. pip install -r requirements.txt"
echo "  4. python app.py"
echo "=================================================="