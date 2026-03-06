# ==============================================================================
# PRODATA MOBILITY DASHBOARD - ARQUITETURA PYTHON (DASH + PANDAS)
# ==============================================================================
# Instalar dependências se necessário:
# pip install dash pandas plotly dash-bootstrap-components
# ==============================================================================

import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. MOTOR DE DADOS (Baseado no initialData do React)
# ==============================================================================
dados_iniciais = [
    { 'pedido': 218835, 'projeto': 'TAUBATE', 'filial': 'MTZ', 'gestor': 'TALYTA GODOY', 'jira': 'TAUBATE - REPUBLICAR APP', 'status': 'PARADO', 'capex': 0, 'opex': 0, 'total': 0, 'fat': 0, 'saldo': 0, 'data': '2026-02-10' },
    { 'pedido': 409607, 'projeto': 'RECIFE METROPOLITANA', 'filial': 'MTZ', 'gestor': 'TALYTA GODOY', 'jira': 'ATENDIDO POR ATSP', 'status': 'NAO INCIADO', 'capex': 101.91, 'opex': 0, 'total': 101.91, 'fat': 101.91, 'saldo': 0, 'data': '2026-05-15' },
    { 'pedido': 409621, 'projeto': 'BELO HORIZONTE METROPOLITANO', 'filial': 'BHO', 'gestor': 'MARIA CRISTINA DA SILVA', 'jira': 'BELO HORIZONTE', 'status': 'NAO INCIADO', 'capex': 1.99, 'opex': 0, 'total': 1.99, 'fat': 0, 'saldo': 1.99, 'data': '2026-08-20' },
    { 'pedido': 409725, 'projeto': 'ITATIBA', 'filial': 'MTZ', 'gestor': 'LEONARDO RAPOSO PIMENTEL', 'jira': 'ITATIBA - TCI - SOD800', 'status': 'EM ANDAMENTO', 'capex': 45000, 'opex': 5000, 'total': 50000, 'fat': 10000, 'saldo': 40000, 'data': '2026-01-05' },
    { 'pedido': 409726, 'projeto': 'ITATIBA', 'filial': 'MTZ', 'gestor': 'LEONARDO RAPOSO PIMENTEL', 'jira': 'ITATIBA - TCI - MANUTENCAO', 'status': 'EM ANDAMENTO', 'capex': 0, 'opex': 2000, 'total': 2000, 'fat': 1000, 'saldo': 1000, 'data': '2026-03-12' },
    { 'pedido': 409727, 'projeto': 'RIBEIRAO PRETO SUB URBANO', 'filial': 'MTZ', 'gestor': 'JOAO SILVA', 'jira': 'SP - IMPLANTACAO NOVO SISTEMA', 'status': 'PARADO', 'capex': 217800, 'opex': 73392, 'total': 291192, 'fat': 217799.99, 'saldo': 73392.01, 'data': '2026-11-25' },
    { 'pedido': 409728, 'projeto': 'SAO PAULO', 'filial': 'SPO', 'gestor': 'JOAO SILVA', 'jira': 'SP - SUPORTE CONTINUO', 'status': 'EM ANDAMENTO', 'capex': 0, 'opex': 8000, 'total': 8000, 'fat': 4000, 'saldo': 4000, 'data': '2026-07-30' },
    { 'pedido': 409729, 'projeto': 'SAO PAULO', 'filial': 'SPO', 'gestor': 'JOAO SILVA', 'jira': 'SP - HARDWARE', 'status': 'PARADO', 'capex': 12000, 'opex': 0, 'total': 12000, 'fat': 0, 'saldo': 12000, 'data': '2026-04-18' },
    { 'pedido': 999991, 'projeto': 'TESTE NANO 1', 'filial': 'NORTE', 'gestor': 'SISTEMA', 'jira': 'TESTE MÍNIMO 1', 'status': 'PARADO', 'capex': 0.50, 'opex': 0, 'total': 0.50, 'fat': 0, 'saldo': 0.50, 'data': '2026-01-01' },
    { 'pedido': 999992, 'projeto': 'TESTE NANO 2', 'filial': 'SUL', 'gestor': 'SISTEMA', 'jira': 'TESTE MÍNIMO 2', 'status': 'PARADO', 'capex': 0.10, 'opex': 0, 'total': 0.10, 'fat': 0, 'saldo': 0.10, 'data': '2026-01-01' },
]

df_global = pd.DataFrame(dados_iniciais)

# Opções para os filtros (extraídas dinamicamente dos dados)
opcoes_filial = [{'label': 'Todas as Regionais', 'value': 'Todas'}] + [{'label': f, 'value': f} for f in sorted(df_global['filial'].unique())]
opcoes_gestor = [{'label': 'Todos os Gestores', 'value': 'Todos'}] + [{'label': g, 'value': g} for g in sorted(df_global['gestor'].unique())]
opcoes_projeto = [{'label': 'Todos os Projetos', 'value': 'Todos'}] + [{'label': p, 'value': p} for p in sorted(df_global['projeto'].unique())]

# ==============================================================================
# 2. CONFIGURAÇÃO E ESTILOS GLOBAIS
# ==============================================================================
# Utilizamos o tema FLATLY do Bootstrap para um aspeto corporativo moderno
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME])
app.title = "Prodata Mobility Dashboard"

# Paleta de Cores baseada na identidade fornecida
COLORS = {
    'primary': '#1e3a8a',    # Azul Navy (Sidebar)
    'secondary': '#3b82f6',  # Azul Claro
    'success': '#10b981',    # Verde (Faturado/Em Andamento)
    'warning': '#f59e0b',    # Laranja (Avisos)
    'danger': '#ef4444',     # Vermelho (Parado/Alerta)
    'dark': '#1e293b',       # Escuro
    'background': '#f8fafc', # Fundo da página
    'text': '#475569'        # Texto base
}

# Template padrão para os gráficos do Plotly
PLOTLY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Segoe UI, sans-serif", color=COLORS['text']),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=30, b=10),
        xaxis=dict(showgrid=True, gridcolor='#e2e8f0'),
        yaxis=dict(showgrid=False)
    )
)

# ==============================================================================
# 3. COMPONENTES DE UI REUTILIZÁVEIS
# ==============================================================================
def Criar_KPICard(titulo, id_valor, icone_class, cor_icone, subtexto=""):
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6(titulo, className="text-uppercase fw-bold mb-1", style={"fontSize": "0.75rem", "color": COLORS['text']}),
                    html.H4(id=id_valor, className="fw-bolder mb-0 text-dark"),
                    html.Small(subtexto, className="text-muted", style={"fontSize": "0.70rem"}) if subtexto else None
                ]),
                dbc.Col(
                    html.Div(
                        html.I(className=icone_class, style={"color": cor_icone, "fontSize": "1.3rem"}),
                        className="d-flex align-items-center justify-content-center rounded-circle shadow-sm",
                        style={"backgroundColor": f"{cor_icone}20", "width": "48px", "height": "48px"}
                    ), width="auto"
                )
            ], className="align-items-center")
        ]), className="shadow-sm border-0 mb-4 h-100 rounded-4 transition-transform hover-lift"
    )

def Criar_SecaoHeader(titulo, icone, cor, subtitulo):
    return html.Div([
        html.Div(
            html.I(className=icone, style={"fontSize": "1.2rem"}), 
            className="d-flex align-items-center justify-content-center rounded-3 me-3 text-white shadow-sm", 
            style={"backgroundColor": cor, "width": "40px", "height": "40px"}
        ),
        html.Div([
            html.H5(titulo, className="mb-0 fw-bolder text-dark tracking-tight"),
            html.Small(subtitulo, className="text-muted fw-semibold")
        ])
    ], className="d-flex align-items-center mb-4 mt-5")

# Estilos em linha CSS customizados
ESTILO_SIDEBAR = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "18rem", 
    "padding": "2rem 1.5rem", "backgroundColor": COLORS['primary'], "color": "white", 
    "zIndex": 1000, "boxShadow": "4px 0 15px rgba(0,0,0,0.1)"
}
ESTILO_CONTEUDO = {
    "marginLeft": "18rem", "padding": "2rem", "backgroundColor": COLORS['background'], 
    "minHeight": "100vh"
}

# ==============================================================================
# 4. ESTRUTURA DO LAYOUT PRINCIPAL
# ==============================================================================
Sidebar = html.Div([
    # Logo / Header da Sidebar
    html.Div([
        html.I(className="fas fa-bus-alt fs-2 me-3 text-info"),
        html.Span("PRODATA", className="fs-3 fw-bolder tracking-wide")
    ], className="mb-5 d-flex align-items-center justify-content-start border-bottom border-secondary pb-3"),
    
    html.P("FILTROS GLOBAIS", className="text-info text-uppercase fw-bold mb-3", style={"fontSize": "0.75rem", "letterSpacing": "1px"}),
    
    # Filtros
    html.Div([
        html.Label([html.I(className="fas fa-map-marker-alt me-2"), "Regional"], className="text-light small mb-1 fw-semibold"),
        dcc.Dropdown(id='filtro-filial', options=opcoes_filial, value='Todas', clearable=False, className="mb-4 text-dark shadow-sm")
    ]),
    html.Div([
        html.Label([html.I(className="fas fa-user-tie me-2"), "Gestor"], className="text-light small mb-1 fw-semibold"),
        dcc.Dropdown(id='filtro-gestor', options=opcoes_gestor, value='Todos', clearable=False, className="mb-4 text-dark shadow-sm")
    ]),
    html.Div([
        html.Label([html.I(className="fas fa-project-diagram me-2"), "Projeto"], className="text-light small mb-1 fw-semibold"),
        dcc.Dropdown(id='filtro-projeto', options=opcoes_projeto, value='Todos', clearable=False, className="mb-4 text-dark shadow-sm")
    ]),
    
    # Rodapé da Sidebar
    html.Div([
        html.Small("Prodata Mobility v2.90.0", className="text-muted"),
        html.Br(),
        html.Small("Arquitetura Python/Dash", className="text-muted")
    ], style={"position": "absolute", "bottom": "2rem"})
    
], style=ESTILO_SIDEBAR)

Topbar = html.Div([
    dbc.Row([
        dbc.Col(html.H4("Visão Geral do Portfólio", className="fw-bolder mb-0 text-dark"), width=4),
        dbc.Col(
            dbc.Row([
                dbc.Col([html.Small("Total Contratado", className="text-muted text-uppercase fw-bold d-block text-end", style={"fontSize": "0.7rem"}), html.Strong(id='global-total', className="text-primary fs-4 d-block text-end")]),
                dbc.Col([html.Small("Faturado", className="text-muted text-uppercase fw-bold d-block text-end", style={"fontSize": "0.7rem"}), html.Strong(id='global-fat', className="text-success fs-4 d-block text-end")]),
                dbc.Col([html.Small("Saldo Restante", className="text-muted text-uppercase fw-bold d-block text-end", style={"fontSize": "0.7rem"}), html.Strong(id='global-saldo', className="text-danger fs-4 d-block text-end")]),
            ], className="g-3"), width=8
        )
    ], className="align-items-center")
], className="bg-white px-4 py-3 shadow-sm mb-4 rounded-4 border")

Conteudo_Principal = html.Div([
    Topbar,
    
    # --- SECÇÃO 1: BACKLOG (EM ESPERA) ---
    Criar_SecaoHeader("Carteira em Espera", "fas fa-pause-circle", COLORS['warning'], "Pedidos classificados como Parados ou Não Iniciados"),
    dbc.Row([
        dbc.Col(Criar_KPICard("Saldo Parado", "bg-saldo", "fas fa-briefcase", COLORS['danger'], "Volume financeiro travado"), md=3),
        dbc.Col(Criar_KPICard("Faturado (Retido)", "bg-fat", "fas fa-file-invoice-dollar", COLORS['success'], "Faturado antes da pausa"), md=3),
        dbc.Col(Criar_KPICard("Contratos Pendentes", "bg-total", "fas fa-layer-group", COLORS['warning'], "Valor total pendente"), md=3),
        dbc.Col(Criar_KPICard("Pedidos Travados", "bg-qtd", "fas fa-hand-paper", COLORS['dark'], "Quantidade de OS na fila"), md=3),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardHeader("Saldo Pendente por Regional", className="bg-transparent fw-bolder border-0 pt-3 pb-0"), dbc.CardBody(dcc.Graph(id='chart-bg-regional', style={"height": "280px"}))]), className="shadow-sm border-0 rounded-4", md=4),
        dbc.Col(dbc.Card([dbc.CardHeader("Top 10 Gestores (Maior Saldo Parado)", className="bg-transparent fw-bolder border-0 pt-3 pb-0"), dbc.CardBody(dcc.Graph(id='chart-bg-gestor', style={"height": "280px"}))]), className="shadow-sm border-0 rounded-4", md=4),
        dbc.Col(dbc.Card([dbc.CardHeader("Top 10 Projetos (Maior Saldo Parado)", className="bg-transparent fw-bolder border-0 pt-3 pb-0"), dbc.CardBody(dcc.Graph(id='chart-bg-projeto', style={"height": "280px"}))]), className="shadow-sm border-0 rounded-4", md=4),
    ], className="mb-5 g-3"),

    # --- SECÇÃO 2: CARTEIRA (EM EXECUÇÃO) ---
    Criar_SecaoHeader("Carteira em Execução", "fas fa-play-circle", COLORS['success'], "Pedidos classificados como Em Andamento"),
    dbc.Row([
        dbc.Col(Criar_KPICard("Saldo Ativo", "cx-saldo", "fas fa-briefcase", COLORS['secondary'], "Saldo a faturar ativo"), md=3),
        dbc.Col(Criar_KPICard("Receita Realizada", "cx-fat", "fas fa-chart-line", COLORS['success'], "Caixa já capturado"), md=3),
        dbc.Col(Criar_KPICard("Contratos Ativos", "cx-total", "fas fa-check-circle", COLORS['success'], "Volume de contratos vivos"), md=3),
        dbc.Col(Criar_KPICard("Pedidos em Execução", "cx-qtd", "fas fa-cogs", COLORS['secondary'], "Total de OS em andamento"), md=3),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardHeader("Faturamento por Regional", className="bg-transparent fw-bolder border-0 pt-3 pb-0"), dbc.CardBody(dcc.Graph(id='chart-cx-regional', style={"height": "280px"}))]), className="shadow-sm border-0 rounded-4", md=4),
        dbc.Col(dbc.Card([dbc.CardHeader("Top 10 Gestores (Mais Faturam)", className="bg-transparent fw-bolder border-0 pt-3 pb-0"), dbc.CardBody(dcc.Graph(id='chart-cx-gestor', style={"height": "280px"}))]), className="shadow-sm border-0 rounded-4", md=4),
        dbc.Col(dbc.Card([dbc.CardHeader("Top 10 Projetos (Mais Faturam)", className="bg-transparent fw-bolder border-0 pt-3 pb-0"), dbc.CardBody(dcc.Graph(id='chart-cx-projeto', style={"height": "280px"}))]), className="shadow-sm border-0 rounded-4", md=4),
    ], className="mb-5 g-3"),

    # --- SECÇÃO 3: TABELA DETALHADA ---
    Criar_SecaoHeader("Detalhamento Financeiro", "fas fa-table", COLORS['dark'], "Visão tabular e pesquisável de todos os pedidos"),
    dbc.Card(
        dbc.CardBody(
            dash_table.DataTable(
                id='tabela-pedidos',
                columns=[
                    {"name": "Pedido", "id": "pedido"},
                    {"name": "Status", "id": "status"},
                    {"name": "Regional", "id": "filial"},
                    {"name": "Projeto", "id": "projeto"},
                    {"name": "Gestor", "id": "gestor"},
                    {"name": "Total Contratado", "id": "total", "type": "numeric", "format": dash_table.FormatTemplate.money(2)},
                    {"name": "Já Faturado", "id": "fat", "type": "numeric", "format": dash_table.FormatTemplate.money(2)},
                    {"name": "Saldo Pendente", "id": "saldo", "type": "numeric", "format": dash_table.FormatTemplate.money(2)},
                ],
                style_table={'overflowX': 'auto', 'minWidth': '100%'},
                style_header={
                    'backgroundColor': '#f1f5f9', 'fontWeight': 'bold', 'color': COLORS['dark'],
                    'borderBottom': '2px solid #cbd5e1', 'padding': '12px'
                },
                style_cell={
                    'padding': '12px', 'textAlign': 'left', 'fontFamily': 'Segoe UI, sans-serif', 
                    'fontSize': '13px', 'borderBottom': '1px solid #f1f5f9'
                },
                style_data_conditional=[
                    # Colorir linhas com base no status (Semelhante ao React)
                    {'if': {'filter_query': '{status} = "EM ANDAMENTO"'}, 'backgroundColor': '#ecfdf5', 'color': '#065f46'},
                    {'if': {'filter_query': '{status} = "PARADO"'}, 'backgroundColor': '#fff7ed', 'color': '#9a3412'},
                    {'if': {'filter_query': '{status} contains "NAO INC"'}, 'backgroundColor': '#f8fafc', 'color': '#475569'},
                    # Destacar a coluna de Saldo
                    {'if': {'column_id': 'saldo'}, 'fontWeight': 'bold', 'color': COLORS['secondary']}
                ],
                page_size=15,
                sort_action="native",
                filter_action="native"
            )
        ), className="shadow-sm border-0 mb-5 rounded-4 p-2"
    )

], style=ESTILO_CONTEUDO)

app.layout = html.Div([Sidebar, Conteudo_Principal])

# ==============================================================================
# 5. CALLBACKS (Motor de Lógica e Filtragem Interativa)
# ==============================================================================
@app.callback(
    [
        # Topbar
        Output('global-total', 'children'), Output('global-fat', 'children'), Output('global-saldo', 'children'),
        # Backlog (Em Espera)
        Output('bg-saldo', 'children'), Output('bg-fat', 'children'), Output('bg-total', 'children'), Output('bg-qtd', 'children'),
        Output('chart-bg-regional', 'figure'), Output('chart-bg-gestor', 'figure'), Output('chart-bg-projeto', 'figure'),
        # Carteira (Em Execução)
        Output('cx-saldo', 'children'), Output('cx-fat', 'children'), Output('cx-total', 'children'), Output('cx-qtd', 'children'),
        Output('chart-cx-regional', 'figure'), Output('chart-cx-gestor', 'figure'), Output('chart-cx-projeto', 'figure'),
        # Tabela
        Output('tabela-pedidos', 'data')
    ],
    [Input('filtro-filial', 'value'), Input('filtro-gestor', 'value'), Input('filtro-projeto', 'value')]
)
def atualizar_dashboard(filial, gestor, projeto):
    # 1. Aplicar Filtros Globais selecionados na Sidebar
    df = df_global.copy()
    if filial != 'Todas': df = df[df['filial'] == filial]
    if gestor != 'Todos': df = df[df['gestor'] == gestor]
    if projeto != 'Todos': df = df[df['projeto'] == projeto]

    # Função interna para formatar moeda no padrão BRL
    def fmt_moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # 2. Atualizar Topbar Global
    g_tot, g_fat, g_sal = fmt_moeda(df['total'].sum()), fmt_moeda(df['fat'].sum()), fmt_moeda(df['saldo'].sum())

    # 3. Separar as duas visões (Backlog vs Execução)
    df_bg = df[df['status'].isin(['PARADO', 'NAO INCIADO', 'NÃO INICIADO'])]
    df_cx = df[df['status'] == 'EM ANDAMENTO']

    # 4. Calcular KPIs - Backlog
    bg_sal, bg_fat, bg_tot, bg_qtd = fmt_moeda(df_bg['saldo'].sum()), fmt_moeda(df_bg['fat'].sum()), fmt_moeda(df_bg['total'].sum()), str(len(df_bg))
    
    # 5. Calcular KPIs - Carteira
    cx_sal, cx_fat, cx_tot, cx_qtd = fmt_moeda(df_cx['saldo'].sum()), fmt_moeda(df_cx['fat'].sum()), fmt_moeda(df_cx['total'].sum()), str(len(df_cx))

    # Função Auxiliar: Criador de Gráficos de Barras Horizontais Customizados
    def criar_grafico_barras(dff, coluna_y, coluna_x, titulo_ausente, cor_barra, limite_top_n=None):
        if dff.empty: 
            return go.Figure().update_layout(title="Sem dados para este filtro", template=PLOTLY_TEMPLATE)
        
        # Agrupar, somar e ordenar do menor para o maior (para barra horizontal ficar com o maior no topo)
        df_grp = dff.groupby(coluna_y)[coluna_x].sum().reset_index().sort_values(by=coluna_x, ascending=True)
        if limite_top_n: 
            df_grp = df_grp.tail(limite_top_n)
            
        # Encurtar nomes de projetos/gestores muito longos para não estragar o eixo Y
        df_grp[coluna_y] = df_grp[coluna_y].apply(lambda x: str(x)[:20] + '...' if len(str(x)) > 20 else str(x))
        
        fig = px.bar(df_grp, x=coluna_x, y=coluna_y, orientation='h', text_auto='.2s', color_discrete_sequence=[cor_barra])
        fig.update_layout(template=PLOTLY_TEMPLATE, xaxis_title=None, yaxis_title=None, showlegend=False)
        fig.update_traces(textposition="outside", textfont_size=11, textfont_color=COLORS['text'], cliponaxis=False)
        fig.update_xaxes(showticklabels=False) # Esconder eixo X para ficar mais limpo (os valores já estão nas barras)
        return fig

    # 6. Gerar Gráficos do Backlog (O foco do Backlog é o SALDO pendente)
    fig_bg_reg = criar_grafico_barras(df_bg, 'filial', 'saldo', 'Regional', COLORS['warning'])
    fig_bg_ges = criar_grafico_barras(df_bg, 'gestor', 'saldo', 'Gestor', COLORS['danger'], limite_top_n=10)
    fig_bg_prj = criar_grafico_barras(df_bg, 'projeto', 'saldo', 'Projeto', COLORS['dark'], limite_top_n=10)

    # 7. Gerar Gráficos da Carteira (O foco da Execução é o FATURAMENTO alcançado)
    fig_cx_reg = criar_grafico_barras(df_cx, 'filial', 'fat', 'Regional', COLORS['secondary'])
    fig_cx_ges = criar_grafico_barras(df_cx, 'gestor', 'fat', 'Gestor', COLORS['success'], limite_top_n=10)
    fig_cx_prj = criar_grafico_barras(df_cx, 'projeto', 'fat', 'Projeto', COLORS['primary'], limite_top_n=10)

    # 8. Atualizar Tabela (enviar dados filtrados como dicionário)
    dados_tabela = df.to_dict('records')

    # Devolver todas as 16 saídas na ordem exata solicitada no decorador @app.callback
    return (
        g_tot, g_fat, g_sal,
        bg_sal, bg_fat, bg_tot, bg_qtd, fig_bg_reg, fig_bg_ges, fig_bg_prj,
        cx_sal, cx_fat, cx_tot, cx_qtd, fig_cx_reg, fig_cx_ges, fig_cx_prj,
        dados_tabela
    )

# ==============================================================================
# 6. ARRANQUE DO SERVIDOR
# ==============================================================================
if __name__ == '__main__':
    # Instrução de rede recomendada para Windows Corporativo (host='0.0.0.0', porta alternativa 8080)
    app.run(debug=True, host='0.0.0.0', port=8080)