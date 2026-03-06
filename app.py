# ==============================================================================
# SISTEMA DE DASHBOARD CORPORATIVO AVANÇADO (ARQUITETURA COMPONENTIZADA)
# ==============================================================================
# Este script foi desenhado para espelhar a estrutura de uma aplicação React moderna:
# - Componentização de UI
# - Roteamento do lado do cliente (Single Page Application)
# - Gestão de Estado Global (via dcc.Store)
# ==============================================================================

import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import date, timedelta
import random

# ==============================================================================
# 1. MOTOR DE DADOS (Simulação de Base de Dados / API)
# ==============================================================================
def gerar_dados_corporativos(num_linhas=5000):
    """Gera um dataset robusto simulando transações de um e-commerce corporativo."""
    np.random.seed(42)
    random.seed(42)
    
    datas = [date(2023, 1, 1) + timedelta(days=i) for i in range(365)]
    regioes = ['Norte', 'Sul', 'Centro', 'Lisboa e Vale do Tejo', 'Algarve', 'Madeira', 'Açores']
    categorias = {
        'Eletrónica': ['Portátil', 'Smartphone', 'Monitor', 'Teclado Mecânico', 'Rato Sem Fios'],
        'Mobiliário': ['Cadeira Ergonómica', 'Mesa de Escritório', 'Estante', 'Sofá de Receção'],
        'Software': ['Licença Antivírus', 'Subscrição Cloud', 'CRM Anual', 'Design Suite'],
        'Serviços': ['Consultoria TI', 'Instalação de Rede', 'Suporte Premium', 'Auditoria de Segurança']
    }
    
    dados = []
    for i in range(num_linhas):
        data_pedido = random.choice(datas)
        regiao = random.choice(regioes)
        categoria = random.choice(list(categorias.keys()))
        produto = random.choice(categorias[categoria])
        
        # Lógica para preços baseados na categoria
        if categoria == 'Eletrónica':
            preco = np.random.uniform(50, 2000)
            margem = np.random.uniform(0.1, 0.3)
        elif categoria == 'Mobiliário':
            preco = np.random.uniform(100, 800)
            margem = np.random.uniform(0.2, 0.4)
        elif categoria == 'Software':
            preco = np.random.uniform(10, 500)
            margem = np.random.uniform(0.6, 0.9) # Alta margem
        else:
            preco = np.random.uniform(200, 5000)
            margem = np.random.uniform(0.4, 0.7)
            
        quantidade = random.randint(1, 10)
        vendas = preco * quantidade
        custo = vendas * (1 - margem)
        lucro = vendas - custo
        
        dados.append({
            'ID_Pedido': f"ORD-{random.randint(10000, 99999)}-{i}",
            'Data': data_pedido,
            'Regiao': regiao,
            'Categoria': categoria,
            'Produto': produto,
            'Quantidade': quantidade,
            'Preco_Unitario': round(preco, 2),
            'Vendas': round(vendas, 2),
            'Custo': round(custo, 2),
            'Lucro': round(lucro, 2),
            'Avaliacao_Cliente': round(np.random.uniform(3.0, 5.0), 1)
        })
        
    df = pd.DataFrame(dados)
    df['Data'] = pd.to_datetime(df['Data'])
    df['Mes'] = df['Data'].dt.strftime('%Y-%m')
    df['DiaSemana'] = df['Data'].dt.day_name()
    return df

df_global = gerar_dados_corporativos(7500)

# ==============================================================================
# 2. CONFIGURAÇÃO DA APLICAÇÃO E ESTILOS GLOBAIS
# ==============================================================================
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.LUMEN, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = "Enterprise Analytics App"

# Paleta de Cores Corporativa
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#18bc9c',
    'accent': '#3498db',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'background': '#f4f6f9',
    'card_bg': '#ffffff',
    'text': '#333333',
    'text_muted': '#7f8c8d'
}

ESTILO_SIDEBAR = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0,
    "width": "16rem", "padding": "2rem 1rem",
    "backgroundColor": COLORS['primary'], "color": "white",
    "boxShadow": "4px 0 10px rgba(0,0,0,0.1)", "zIndex": 1000
}

ESTILO_CONTEUDO = {
    "marginLeft": "16rem",
    "backgroundColor": COLORS['background'],
    "minHeight": "100vh", "padding": "0"
}

ESTILO_CARD = {
    "backgroundColor": COLORS['card_bg'],
    "borderRadius": "12px", "border": "none",
    "boxShadow": "0 4px 6px rgba(0,0,0,0.05)", "marginBottom": "1.5rem"
}

# ==============================================================================
# 3. COMPONENTES REUTILIZÁVEIS
# ==============================================================================
def KPICard(titulo, id_valor, icone_class, id_subtexto=None, cor_icone=COLORS['accent']):
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6(titulo, className="text-uppercase text-muted fw-bold mb-1", style={"fontSize": "0.75rem"}),
                    html.H3(id=id_valor, className="fw-bold mb-0", style={"color": COLORS['text']}),
                    html.Small(id=id_subtexto, className="text-success fw-bold") if id_subtexto else None
                ]),
                dbc.Col(
                    html.Div(
                        html.I(className=icone_class, style={"fontSize": "1.5rem", "color": cor_icone}),
                        style={
                            "backgroundColor": f"{cor_icone}20",
                            "borderRadius": "50%", "width": "48px", "height": "48px",
                            "display": "flex", "alignItems": "center", "justifyContent": "center"
                        }
                    ),
                    width="auto"
                )
            ], className="align-items-center")
        ]),
        style=ESTILO_CARD
    )

def NavLinkCustom(texto, href, icone_class):
    return dbc.NavLink(
        [html.I(className=f"{icone_class} me-3"), texto],
        href=href, active="exact",
        className="text-white py-3 rounded-3 mb-1",
        style={"transition": "all 0.3s ease"}
    )

def GraficoWrapper(id_grafico, titulo, altura=350):
    return dbc.Card(
        dbc.CardBody([
            html.H5(titulo, className="fw-bold mb-3 text-muted", style={"fontSize": "1rem"}),
            dcc.Loading(
                type="dot", color=COLORS['secondary'],
                children=dcc.Graph(id=id_grafico, style={"height": f"{altura}px"})
            )
        ]),
        style=ESTILO_CARD
    )

# ==============================================================================
# 4. ESTRUTURA PRINCIPAL: SIDEBAR E TOPBAR
# ==============================================================================
Sidebar = html.Div([
    html.Div([
        html.I(className="fas fa-cube me-2 fs-3 text-info"),
        html.Span("Nexus", className="fs-3 fw-bold tracking-wide"),
        html.Span("Analytics", className="fs-3 fw-light")
    ], className="mb-5 text-center mt-2 d-flex align-items-center justify-content-center"),
    
    html.P("MENU PRINCIPAL", className="text-uppercase text-muted fw-bold mb-3 ms-2", style={"fontSize": "0.7rem", "letterSpacing": "1px"}),
    
    dbc.Nav([
        NavLinkCustom("Visão Geral", "/", "fas fa-home"),
        NavLinkCustom("Análise de Vendas", "/vendas", "fas fa-chart-line"),
        NavLinkCustom("Produtos & Inventário", "/produtos", "fas fa-box-open"),
        NavLinkCustom("Demografia & Clientes", "/clientes", "fas fa-users"),
    ], vertical=True, pills=True),
    
    html.Div([
        html.Hr(style={"borderColor": "rgba(255,255,255,0.1)"}),
        html.Div([
            html.Img(src="https://ui-avatars.com/api/?name=Admin+User&background=18bc9c&color=fff", className="rounded-circle me-3", style={"width": "40px"}),
            html.Div([
                html.P("Admin User", className="mb-0 fw-bold", style={"fontSize": "0.9rem"}),
                html.P("admin@nexus.com", className="mb-0 text-muted", style={"fontSize": "0.75rem"})
            ])
        ], className="d-flex align-items-center mt-4")
    ], style={"position": "absolute", "bottom": "2rem", "left": "1rem", "right": "1rem"})
], style=ESTILO_SIDEBAR)

Topbar = html.Div([
    dbc.Row([
        dbc.Col(html.H4(id="titulo-pagina", className="fw-bold mb-0 text-dark pt-2"), width=4),
        dbc.Col([
            html.Div([
                html.I(className="far fa-calendar-alt me-2 text-muted"),
                dcc.DatePickerRange(
                    id='filtro-data-global',
                    min_date_allowed=df_global['Data'].min().date(),
                    max_date_allowed=df_global['Data'].max().date(),
                    start_date=df_global['Data'].min().date(),
                    end_date=df_global['Data'].max().date(),
                    display_format='DD/MM/YYYY',
                    className="shadow-sm",
                    style={"border": "none", "borderRadius": "8px"}
                )
            ], className="d-flex align-items-center justify-content-end")
        ], width=8)
    ], className="g-0 align-items-center")
], style={"backgroundColor": "#ffffff", "padding": "1.5rem 2rem", "boxShadow": "0 2px 10px rgba(0,0,0,0.05)", "marginBottom": "2rem"})

# ==============================================================================
# 5. PÁGINAS (Layouts)
# ==============================================================================
layout_visao_geral = html.Div([
    dbc.Row([
        dbc.Col(KPICard("Receita Total", "kpi-receita", "fas fa-euro-sign", cor_icone=COLORS['secondary']), width=12, md=6, lg=3),
        dbc.Col(KPICard("Lucro Líquido", "kpi-lucro", "fas fa-wallet", cor_icone=COLORS['accent']), width=12, md=6, lg=3),
        dbc.Col(KPICard("Pedidos Concluídos", "kpi-pedidos", "fas fa-shopping-cart", cor_icone=COLORS['warning']), width=12, md=6, lg=3),
        dbc.Col(KPICard("Ticket Médio", "kpi-ticket", "fas fa-receipt", cor_icone=COLORS['danger']), width=12, md=6, lg=3),
    ]),
    dbc.Row([
        dbc.Col(GraficoWrapper('chart-receita-tempo', 'Evolução de Receita e Lucro', altura=400), width=12, lg=8),
        dbc.Col(GraficoWrapper('chart-vendas-categoria', 'Distribuição por Categoria', altura=400), width=12, lg=4),
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Transações Recentes", className="fw-bold mb-3 text-muted"),
                    html.Div(id="tabela-transacoes-recentes")
                ])
            ], style=ESTILO_CARD), width=12
        )
    ])
], className="px-4 pb-4")

layout_vendas = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filtros Específicos", className="mb-3 text-muted"),
                    html.Label("Selecione as Regiões:", className="fw-bold mb-1", style={"fontSize": "0.8rem"}),
                    dcc.Dropdown(
                        id='filtro-regiao',
                        options=[{'label': r, 'value': r} for r in df_global['Regiao'].unique()],
                        value=df_global['Regiao'].unique()[:3].tolist(),
                        multi=True,
                        className="mb-4"
                    ),
                ])
            ], style=ESTILO_CARD)
        ], width=12, lg=3),
        dbc.Col([
            dbc.Row([
                dbc.Col(GraficoWrapper('chart-vendas-regiao', 'Performance por Região', altura=300), width=12, md=6),
                dbc.Col(GraficoWrapper('chart-dispersao-vendas', 'Relação: Preço vs Quantidade', altura=300), width=12, md=6),
            ]),
            dbc.Row([
                dbc.Col(GraficoWrapper('chart-heatmap-dias', 'Vendas por Dia da Semana', altura=350), width=12)
            ])
        ], width=12, lg=9)
    ])
], className="px-4 pb-4")

layout_produtos = html.Div([
    dbc.Row([
        dbc.Col(GraficoWrapper('chart-top-produtos', 'Top 10 Produtos (Receita)', altura=450), width=12, lg=6),
        dbc.Col(GraficoWrapper('chart-treemap-produtos', 'Hierarquia: Categoria > Produto', altura=450), width=12, lg=6),
    ])
], className="px-4 pb-4")

layout_clientes = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-star text-warning fs-1 mb-3"),
                        html.H2(id="kpi-avaliacao", className="display-4 fw-bold"),
                        html.P("Avaliação Média Global (CSAT)", className="text-muted text-uppercase fw-bold")
                    ], className="text-center py-5")
                ])
            ], style=ESTILO_CARD), width=12, md=4
        ),
        dbc.Col(GraficoWrapper('chart-distribuicao-avaliacao', 'Distribuição das Avaliações', altura=350), width=12, md=8)
    ])
], className="px-4 pb-4")

# ==============================================================================
# 6. LAYOUT MESTRE (Router)
# ==============================================================================
app.layout = html.Div([
    dcc.Store(id='store-dados-filtrados'),
    dcc.Location(id='url', refresh=False),
    Sidebar,
    html.Div([
        Topbar,
        html.Div(id='page-content')
    ], style=ESTILO_CONTEUDO)
])

# ==============================================================================
# 7. CALLBACKS (Lógica de Negócio)
# ==============================================================================
PLOTLY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif", color=COLORS['text']),
        plot_bgcolor="white", paper_bgcolor="white",
        colorway=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning'], COLORS['danger']],
        margin=dict(l=20, r=20, t=30, b=20)
    )
)

@app.callback(
    [Output('page-content', 'children'), Output('titulo-pagina', 'children')],
    [Input('url', 'pathname')]
)
def renderizar_pagina(pathname):
    if pathname == '/': return layout_visao_geral, "Visão Geral do Negócio"
    elif pathname == '/vendas': return layout_vendas, "Análise Detalhada de Vendas"
    elif pathname == '/produtos': return layout_produtos, "Performance de Produtos"
    elif pathname == '/clientes': return layout_clientes, "Satisfação e Demografia"
    else: return html.Div([html.H1("404: Página não encontrada")]), "Erro 404"

@app.callback(
    Output('store-dados-filtrados', 'data'),
    [Input('filtro-data-global', 'start_date'), Input('filtro-data-global', 'end_date')]
)
def atualizar_estado_global(start_date, end_date):
    mask = (df_global['Data'] >= start_date) & (df_global['Data'] <= end_date)
    return df_global.loc[mask].to_dict('records')

@app.callback(
    [Output('kpi-receita', 'children'), Output('kpi-lucro', 'children'),
     Output('kpi-pedidos', 'children'), Output('kpi-ticket', 'children'),
     Output('chart-receita-tempo', 'figure'), Output('chart-vendas-categoria', 'figure'),
     Output('tabela-transacoes-recentes', 'children')],
    [Input('store-dados-filtrados', 'data'), Input('url', 'pathname')]
)
def atualizar_visao_geral(dados_json, pathname):
    if pathname != '/': raise dash.exceptions.PreventUpdate
    df = pd.DataFrame(dados_json)
    if df.empty: return ["€ 0"] * 4 + [go.Figure()] * 2 + [html.P("Sem dados")]
    
    rt = df['Vendas'].sum()
    kpi1 = f"€ {rt:,.0f}".replace(',', '.')
    kpi2 = f"€ {df['Lucro'].sum():,.0f}".replace(',', '.')
    kpi3 = f"{len(df):,}".replace(',', '.')
    kpi4 = f"€ {(rt / len(df) if len(df) > 0 else 0):,.2f}".replace(',', '.')
    
    df['Data'] = pd.to_datetime(df['Data'])
    df_tempo = df.groupby(df['Data'].dt.to_period('M')).agg({'Vendas': 'sum', 'Lucro': 'sum'}).reset_index()
    df_tempo['Data'] = df_tempo['Data'].astype(str)
    
    fig_tempo = px.area(df_tempo, x='Data', y='Vendas')
    fig_tempo.add_trace(go.Scatter(x=df_tempo['Data'], y=df_tempo['Lucro'], mode='lines', name='Lucro', line=dict(color=COLORS['secondary'], width=3)))
    fig_tempo.update_layout(template=PLOTLY_TEMPLATE)

    df_cat = df.groupby('Categoria')['Vendas'].sum().reset_index()
    fig_cat = px.pie(df_cat, values='Vendas', names='Categoria', hole=0.6, color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning']])
    fig_cat.update_layout(template=PLOTLY_TEMPLATE, showlegend=True, legend=dict(orientation="h", y=-0.2))

    df_recentes = df.sort_values('Data', ascending=False).head(5)
    df_recentes['Data'] = df_recentes['Data'].dt.strftime('%d/%m/%Y')
    df_recentes['Vendas'] = df_recentes['Vendas'].apply(lambda x: f"€ {x:,.2f}")
    df_recentes['Cliente'] = [f"Cliente {random.randint(100,999)}" for _ in range(5)]
    
    tabela = dash_table.DataTable(
        data=df_recentes.to_dict('records'),
        columns=[{"name": i.replace("_", " "), "id": i} for i in ['ID_Pedido', 'Data', 'Cliente', 'Categoria', 'Produto', 'Vendas']],
        style_table={'overflowX': 'auto'}, style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
        style_cell={'padding': '12px', 'textAlign': 'left', 'borderBottom': '1px solid #f0f0f0'}, style_as_list_view=True
    )
    return kpi1, kpi2, kpi3, kpi4, fig_tempo, fig_cat, tabela

@app.callback(
    [Output('chart-vendas-regiao', 'figure'), Output('chart-dispersao-vendas', 'figure'), Output('chart-heatmap-dias', 'figure')],
    [Input('store-dados-filtrados', 'data'), Input('filtro-regiao', 'value'), Input('url', 'pathname')]
)
def atualizar_vendas(dados_json, regioes, pathname):
    if pathname != '/vendas': raise dash.exceptions.PreventUpdate
    df = pd.DataFrame(dados_json)
    if df.empty or not regioes: return [go.Figure()] * 3
    df = df[df['Regiao'].isin(regioes)]
    
    df_reg = df.groupby('Regiao')['Vendas'].sum().sort_values().reset_index()
    fig_reg = px.bar(df_reg, x='Vendas', y='Regiao', orientation='h', color='Vendas', color_continuous_scale='Blues')
    fig_reg.update_layout(template=PLOTLY_TEMPLATE, coloraxis_showscale=False)
    
    fig_disp = px.scatter(df, x='Preco_Unitario', y='Quantidade', color='Categoria', size='Lucro')
    fig_disp.update_layout(template=PLOTLY_TEMPLATE)
    
    df['Data'] = pd.to_datetime(df['Data'])
    df['Mes_Nome'] = df['Data'].dt.strftime('%b')
    pivot = df.pivot_table(values='Vendas', index='DiaSemana', columns='Mes_Nome', aggfunc='sum', observed=False).fillna(0)
    fig_heat = px.imshow(pivot, labels=dict(x="Mês", y="Dia", color="Vendas"), aspect="auto", color_continuous_scale="Teal")
    fig_heat.update_layout(template=PLOTLY_TEMPLATE)
    return fig_reg, fig_disp, fig_heat

@app.callback(
    [Output('chart-top-produtos', 'figure'), Output('chart-treemap-produtos', 'figure')],
    [Input('store-dados-filtrados', 'data'), Input('url', 'pathname')]
)
def atualizar_produtos(dados_json, pathname):
    if pathname != '/produtos': raise dash.exceptions.PreventUpdate
    df = pd.DataFrame(dados_json)
    if df.empty: return [go.Figure()] * 2
    
    df_prod = df.groupby('Produto')['Vendas'].sum().sort_values(ascending=True).tail(10).reset_index()
    fig_top = px.bar(df_prod, x='Vendas', y='Produto', orientation='h', text_auto='.2s', color='Vendas', color_continuous_scale='Mint')
    fig_top.update_layout(template=PLOTLY_TEMPLATE, coloraxis_showscale=False)
    
    df_tree = df.groupby(['Categoria', 'Produto']).agg({'Vendas': 'sum', 'Lucro': 'sum'}).reset_index()
    fig_tree = px.treemap(df_tree, path=[px.Constant("Portfólio"), 'Categoria', 'Produto'], values='Vendas', color='Lucro', color_continuous_scale='RdBu')
    fig_tree.update_layout(template=PLOTLY_TEMPLATE, margin=dict(t=10, l=10, r=10, b=10))
    return fig_top, fig_tree

@app.callback(
    [Output('kpi-avaliacao', 'children'), Output('chart-distribuicao-avaliacao', 'figure')],
    [Input('store-dados-filtrados', 'data'), Input('url', 'pathname')]
)
def atualizar_clientes(dados_json, pathname):
    if pathname != '/clientes': raise dash.exceptions.PreventUpdate
    df = pd.DataFrame(dados_json)
    if df.empty: return "0.0", go.Figure()
    
    kpi_csat = f"{df['Avaliacao_Cliente'].mean():.1f} / 5.0"
    fig_hist = px.histogram(df, x='Avaliacao_Cliente', nbins=10, color='Categoria')
    fig_hist.update_layout(template=PLOTLY_TEMPLATE, barmode='overlay')
    return kpi_csat, fig_hist

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)