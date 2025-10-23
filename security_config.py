"""
Configurações de Segurança para ComunaTec Landing Page
"""
import os
import secrets
from cryptography.fernet import Fernet

class SecurityConfig:
    """Configurações de segurança centralizadas"""
    
    # Headers de segurança
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        'Content-Security-Policy': (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self'"
        ),
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
    }
    
    # Configurações de rate limiting
    RATE_LIMITS = {
        'default': ["200 per day", "50 per hour"],
        'login': "10 per minute",
        'form_submit': "5 per minute"
    }
    
    # Configurações de upload
    UPLOAD_CONFIG = {
        'max_size': 16 * 1024 * 1024,  # 16MB
        'allowed_extensions': {'png', 'jpg', 'jpeg', 'gif'},
        'secure_filename': True
    }
    
    # Configurações de sessão
    SESSION_CONFIG = {
        'permanent': False,
        'use_signer': True,
        'key_prefix': 'comunatec:'
    }
    
    @staticmethod
    def get_secret_key():
        """Gera ou recupera SECRET_KEY segura"""
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            secret_key = secrets.token_urlsafe(32)
        return secret_key
    
    @staticmethod
    def get_admin_password():
        """Recupera senha do admin das variáveis de ambiente"""
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if not admin_password:
            raise ValueError("ADMIN_PASSWORD environment variable is required")
        return admin_password
    
    @staticmethod
    def get_redis_url():
        """Recupera URL do Redis"""
        return os.environ.get('REDIS_URL', 'memory://')
    
    @staticmethod
    def generate_encryption_key():
        """Gera chave de criptografia para dados sensíveis"""
        return Fernet.generate_key()
    
    @staticmethod
    def validate_environment():
        """Valida se todas as variáveis de ambiente necessárias estão definidas"""
        required_vars = ['ADMIN_PASSWORD']
        missing_vars = []
        
        for var in required_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
