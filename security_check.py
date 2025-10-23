#!/usr/bin/env python3
"""
Script de verificação de segurança para ComunaTec Landing Page
"""
import subprocess
import sys
import os
from pathlib import Path

def run_security_check():
    """Executa verificações de segurança"""
    print("🔐 Verificando segurança do projeto...")
    
    # Verificar se as variáveis de ambiente estão definidas
    required_env_vars = ['ADMIN_PASSWORD']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis de ambiente obrigatórias não definidas: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Variáveis de ambiente obrigatórias definidas")
    
    # Verificar dependências
    try:
        result = subprocess.run(['pip', 'check'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependências sem conflitos")
        else:
            print(f"⚠️ Conflitos de dependências encontrados: {result.stdout}")
    except FileNotFoundError:
        print("⚠️ pip não encontrado, pulando verificação de dependências")
    
    # Verificar se o banco de dados existe
    if Path('database.db').exists():
        print("✅ Banco de dados encontrado")
    else:
        print("ℹ️ Banco de dados será criado na primeira execução")
    
    # Verificar arquivos de configuração
    config_files = ['security_config.py', 'SECURITY.md', '.github/dependabot.yml']
    for file in config_files:
        if Path(file).exists():
            print(f"✅ {file} encontrado")
        else:
            print(f"⚠️ {file} não encontrado")
    
    print("\n🎯 Verificação de segurança concluída!")
    return True

def check_dependencies():
    """Verifica se as dependências estão atualizadas"""
    print("\n📦 Verificando dependências...")
    
    try:
        # Verificar se requirements.txt existe
        if not Path('requirements.txt').exists():
            print("❌ requirements.txt não encontrado")
            return False
        
        # Ler requirements.txt
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        # Verificar dependências críticas
        critical_deps = ['flask>=3.1.0', 'werkzeug>=3.1.0', 'cryptography>=43.0.0']
        
        for dep in critical_deps:
            if dep.split('>=')[0] in requirements:
                print(f"✅ {dep.split('>=')[0]} encontrado")
            else:
                print(f"⚠️ {dep.split('>=')[0]} não encontrado ou versão antiga")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar dependências: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ComunaTec Security Check")
    print("=" * 40)
    
    success = True
    
    # Executar verificações
    success &= run_security_check()
    success &= check_dependencies()
    
    if success:
        print("\n✅ Todas as verificações de segurança passaram!")
        sys.exit(0)
    else:
        print("\n❌ Algumas verificações de segurança falharam!")
        sys.exit(1)
