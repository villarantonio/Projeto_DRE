"""
Modulo de autenticacao do Dashboard.

Gerencia login, logout e validacao de credenciais.
"""

import hashlib
import streamlit as st


# =============================================================================
# Configuracoes de Autenticacao
# =============================================================================

# Credenciais (em producao, usar secrets management)
VALID_USERNAME = "mandapicanha"
VALID_PASSWORD_HASH = hashlib.sha256("MP@1234".encode()).hexdigest()


# =============================================================================
# Funcoes de Autenticacao
# =============================================================================

def hash_password(password: str) -> str:
    """
    Gera hash SHA-256 de uma senha.
    
    Args:
        password: Senha em texto plano.
        
    Returns:
        Hash da senha em hexadecimal.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_credentials(username: str, password: str) -> bool:
    """
    Verifica se as credenciais sao validas.
    
    Args:
        username: Nome de usuario.
        password: Senha em texto plano.
        
    Returns:
        True se credenciais validas, False caso contrario.
    """
    if not username or not password:
        return False
    
    password_hash = hash_password(password)
    return username == VALID_USERNAME and password_hash == VALID_PASSWORD_HASH


def init_session_state() -> None:
    """Inicializa variaveis de sessao para autenticacao."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0


def login(username: str, password: str) -> bool:
    """
    Realiza login do usuario.
    
    Args:
        username: Nome de usuario.
        password: Senha.
        
    Returns:
        True se login bem sucedido, False caso contrario.
    """
    if verify_credentials(username, password):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.login_attempts = 0
        return True
    else:
        st.session_state.login_attempts += 1
        return False


def logout() -> None:
    """Realiza logout do usuario."""
    st.session_state.authenticated = False
    st.session_state.username = None


def is_authenticated() -> bool:
    """
    Verifica se usuario esta autenticado.
    
    Returns:
        True se autenticado, False caso contrario.
    """
    return st.session_state.get("authenticated", False)


def render_login_page() -> None:
    """Renderiza pagina de login."""
    st.markdown("""
        <style>
            .login-container {
                max-width: 400px;
                margin: 0 auto;
                padding: 2rem;
            }
            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Container centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo e titulo
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <span style="font-size: 5rem;">🥩</span>
                <h1 style="color: #2C3E50; margin: 0.5rem 0;">Manda Picanha</h1>
                <p style="color: #6C757D; font-size: 1rem;">Dashboard Financeiro DRE</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Card de login
        st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h3 style="color: #2C3E50; text-align: center; margin-bottom: 1.5rem;">🔐 Acesso ao Sistema</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulario de login
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "Usuario",
                placeholder="Digite seu usuario",
                key="login_username",
            )
            
            password = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
                key="login_password",
            )
            
            submitted = st.form_submit_button(
                "🔓 Entrar",
                use_container_width=True,
                type="primary",
            )
            
            if submitted:
                if login(username, password):
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    attempts = st.session_state.login_attempts
                    if attempts >= 3:
                        st.error(f"⚠️ Muitas tentativas falhas ({attempts}). Verifique suas credenciais.")
                    else:
                        st.error("❌ Usuario ou senha incorretos.")
        
        # Rodape
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem; color: #ADB5BD; font-size: 0.8rem;">
                <p>v1.3.0 | Pipeline DRE</p>
                <p>© 2026 Manda Picanha</p>
            </div>
        """, unsafe_allow_html=True)


def render_logout_button() -> None:
    """Renderiza botao de logout na sidebar."""
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # Info do usuario logado
    username = st.session_state.get("username", "Usuario")
    st.markdown(f"""
        <div style="background: rgba(39, 174, 96, 0.2); border-left: 3px solid #27AE60; padding: 0.75rem; border-radius: 4px; margin-bottom: 0.75rem;">
            <p style="color: #27AE60; font-size: 0.7rem; margin: 0; text-transform: uppercase;">Logado como</p>
            <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 0;">👤 {username}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botao de logout
    if st.button("🚪 Sair", use_container_width=True, type="secondary"):
        logout()
        st.rerun()

