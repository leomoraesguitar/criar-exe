#!/usr/bin/env python3

import os
import sys

def create(base_path):
    folders = [
        # "src",
        # "src/controllers",
        # "src/models",
        # "src/views",
        "assets",
        "assets/uploads",
        "layout",
        "rotas",
        "classes",
        "componentes",
        '.github/workflows',  
    ]
    
    os.makedirs(base_path, exist_ok=True)
    if len(folders) > 0:
        for folder in folders:
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created: {folder_path}")

    # Cria o arquivo cf.py dentro da pasta base
    cf_file_path = os.path.join(base_path, "criar_exe.py")
    env_path = os.path.join(base_path, ".env")
    main_file_path = os.path.join(base_path, "main.py")
    requi_file_path = os.path.join(base_path, "requirements.txt")
    yml_file_path = os.path.join(base_path,'.github','workflows', "deploy-github-pages.yml")
    imports_path = os.path.join(base_path,"classes", "imports.py")
    componentes_path = os.path.join(base_path,"componentes", "componentes.py")
    tema_path = os.path.join(base_path,"classes", "temas.py")
    func_path = os.path.join(base_path,"rotas", "funcs.py")
    layout_principal_path  = os.path.join(base_path,"layout", "principal.py") 

    script_env = f"""
LOG = "True"
"""

    criar_exe = f"""
import PyInstaller.__main__
from os import path
from shutil  import rmtree


class Criar_exe:
    def __init__(self,
        programas = [
            'main.py',
            ] ,
            limpar_build = True,                
    ):
        if limpar_build:
            self.limpar_pasta('build')
        
        for i in programas:
            # if not i.endswith('.spec') and i.endswith('.py'):
            sp = i.split('.')[0]+'.spec'
            if  path.exists(sp):
                PyInstaller.__main__.run([
                    sp
                ])  
            elif i.endswith('.py'):
                assets_path = 'assets'
                add_data_option = f'{{assets_path}};{{assets_path}}'
                if path.exists('assets'):
                    PyInstaller.__main__.run([
                            i,
                            '--onefile',
                            '--windowed',
                            f'--add-data={{add_data_option}}'
                            '' 
                        ])
                else:
                    PyInstaller.__main__.run([
                            i,
                            '--onefile',
                            '--windowed',                       
                            ''
                        ])                    

        if limpar_build:
            self.limpar_pasta('build')

    def limpar_pasta(self, pasta):
        try:
            rmtree(pasta)
            print(f"A pasta {{pasta}} foi deletada com sucesso.")
        except OSError as e:
            print(f"Erro ao deletar a pasta: ")
            print(OSError)
            
programas = [
'main.py',
            ]  
if __name__ == "__main__":
    Criar_exe(programas, limpar_build=False)
"""

    principal = f"""


from rotas.funcs import Funcs
from classes.imports import ft, lg, load_dotenv, getenv, Saida, ConfirmarSaidaeResize, LimparMemoria


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Acessa a variável de ambiente
# connection_string = os.getenv("MYSQL_CONNECTION_STRING")





def main(page: ft.Page):
    page.data = ['', '', '']
    saida = Saida(page)
    pprint = saida.pprint
    funcs = Funcs(pprint)
    ConfirmarSaidaeResize(page = page, exibir = True)
    def GetRota(e):
        match e.route:
            case '/home':
                return 'home'  
            case '/principal':
                return funcs.AbrirPrincipal()  
            case '/temas':
                return funcs.AbrirTemas()                       
            # case '/salvar':
            #     funcs.Salvar(e)
            #     return None
            case _:
                pass

    def route_change(e):
        rota = GetRota(e)
        if rota is None:
            page.go('/home')
            lg('rota = None')
        elif rota == 'home':
            pass
            lg('rota = home')
        else:
            LimparMemoria()
            if len(page.views) > 0:
                recente = page.views[-1].route
            else:
                recente = '/principal'
            page.views.clear()


            page.views.append(rota)
            page.data[0] = recente
            page.update()

    page.on_route_change = route_change

    page.go('/principal')    




if __name__ == '__main__': 
    ft.app(target=main,upload_dir="assets/uploads")

"""

    script_components = f"""
import sys
from pathlib import Path

# Adicione o diretório raiz do projeto ao PATH do Python
CAMINHO_RAIZ = Path(__file__).parent.parent  # Volta duas pastas (layout -> projeto)
sys.path.append(str(CAMINHO_RAIZ))

from classes.imports import ft    
class Componentes:
    def __init__(self, layout):
        self.layout = layout
"""

    script_layout_principal = f"""
import sys
from pathlib import Path

# Adicione o diretório raiz do projeto ao PATH do Python
CAMINHO_RAIZ = Path(__file__).parent.parent  # Volta duas pastas (layout -> projeto)
sys.path.append(str(CAMINHO_RAIZ))

from classes.imports import ft,AppBar, IniciarTema,BarraLateral
from componentes.componentes import Componentes
class Principal(ft.View):
    def __init__(self,pprint,

                 *args, **kwargs
                 ):
        super().__init__(*args, **kwargs)
        self.appbar = AppBar('Principal', '/temas')
        self.pprint = pprint
        self.padding = ft.Padding(0,5,5,0)        
        self.controls = [
            ft.Row(
                [
                    ft.Column(
                        [
                            BarraLateral()
                        ],           
                    ),
                    ft.Column(
                        [
                            ft.Text('meu ovo', color=ft.Colors.PRIMARY),
                            ft.ElevatedButton('botão', on_click=lambda e: self.pprint('meu ovo'))
                        ],
                        expand=True
                    ),                    

                ],
                spacing = 0,
                expand=True
            )
        ]
    def did_mount(self):
        self.page = IniciarTema(self.page)
        self.page.update()

"""

    script_func = f"""

from layout.principal import Principal

class Funcs:
    def __init__(self,pprint):
        self.pprint = pprint

    def AbrirPrincipal(self):
        return Principal(self.pprint)

    def AbrirTemas(self):
        from classes.temas import TemaSelectSysten 
        return TemaSelectSysten()
       
"""

    script_imports = f"""from sys import modules,path as pthsys
from pathlib import Path

# Adicione o diretório raiz do projeto ao PATH do Python
CAMINHO_RAIZ = Path(__file__).parent.parent  # Volta duas pastas (layout -> projeto)
pthsys.append(str(CAMINHO_RAIZ))
import flet as ft
from dotenv import load_dotenv
from json import dump, load, JSONDecodeError
from os import environ, path, mkdir, getenv
from pickle import dump as dumpp, load as loadp
from gc import collect

import logging
logging.basicConfig(level=logging.WARNING)
try:
    log = getenv('LOG')
except:
    log = False

exibirlog = True if log == 'True' else False


def lg(texto):
    if exibirlog:
        logging.warning(texto)


def LimparMemoria():
    imported_modules = list(modules.keys())
    modflet = imported_modules.index('flet')
    for i in imported_modules[modflet:]:
        del i
    collect()
        


def Caminho(arquivo, PASTA_PADRAO = 'tabelamandadostjse'):
    from os import path, mkdir, environ
    base_path = path.join(environ.get('USERPROFILE'),PASTA_PADRAO)
    if not path.exists(base_path):
        mkdir(base_path)
    return path.join(base_path, arquivo)

def MatarProcesso(process_name = "main.exe"):
    from subprocess import run as sub_run    
    comando = f"taskkill /F /IM {{process_name}}"
    resultado = sub_run(comando, shell=True, capture_output=True, text=True)
    if resultado.returncode == 0:
        print(f"Processo {{process_name}} finalizado com sucesso.")
    else:
        print(f"Erro ao finalizar o processo {{process_name}}: {{resultado.stderr}}")

def Escrever_json(data, filename):
    # if not filename.endswith('.json'):
    #     filename += '.json'
    with open(filename, 'w') as f:
        dump(data, f, indent=4)

def Ler_json(filename, default=None):
    # if not filename.endswith('.json'):
    #     filename += '.json'
    try:
        with open(filename, 'r') as f:
            return load(f)
    except (FileNotFoundError, JSONDecodeError):
        try:
            Escrever_json(default, filename)
        except:
            pass
        return default or {{}}

def SalvarPickle(var, nome):
    # if not nome.endswith('.plk'):
    #     nome += '.plk'        
    with open(nome, 'wb') as arquivo:
        dumpp(var, arquivo)

def LerPickle(nome):
    # if not nome.endswith('.plk'):
    #     nome += '.plk'
    if path.isfile(nome):
        with open(nome, 'rb') as arquivo:
            return loadp(arquivo)
    else:
        return None 

class ConfirmarSaidaeResize:
    def __init__(self,page, funcao = None, exibir = True, width_min = None, height_min = None, onlyresize = False):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.width_min = width_min
        self.height_min = height_min
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.window.on_event = self.window_event
        self.onlyresize = onlyresize
        if not onlyresize:
            self.page.window.prevent_close = True 

        self.page.on_resized = self.page_resize
        # self.page.window.on_event = self.page_resize
        self.nome = f'{{self.page.title}}_tamanho'
        self.exibir = exibir
        if self.exibir:
            self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
            self.page.overlay.append(self.pw) 
        self.Ler_dados() 


    async def window_event(self, e):
        if e.data == 'resized' or e.data == 'moved':
            await self.page_resize(e)
        if e.data == "close" and not self.onlyresize:
            self.page.overlay.append(self.confirm_dialog)
            
            self.confirm_dialog.open = True
            self.page.update()

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window.destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()



    async def page_resize(self, e):
        if self.exibir:
            self.pw.value = f'{{self.page.window.width}}*{{self.page.window.height}} px'
            self.pw.update()
        valores = [self.page.window.width,self.page.window.height,self.page.window.top,self.page.window.left]
        if self.height_min:
            if valores[1]< self.height_min:
                valores[1] = self.height_min
        if self.width_min:
            if valores[0]< self.width_min:
                valores[0] = self.width_min      
        if valores[2] <0:
              valores[2] = 0   
        if valores[3] <0:
              valores[3] = 0                
        # with open('assets/tamanho.txt', 'w') as arq:
        #     arq.write(f'{{valores[0]}},{{valores[1]}},{{valores[2]}},{{valores[3]}}')
        await self.page.client_storage.set_async(self.nome, f'{{valores[0]}},{{valores[1]}},{{valores[2]}},{{valores[3]}}')
        
    def LerLocalStorage(self, page, key, tempo = 3):
        from time import sleep
        valor  = None
        valor = page.client_storage.get(key)
        for i in range(tempo*10):
            sleep(0.1)
            if valor:
                return valor
        return None
  

    def Ler_dados(self):
        try:
            # with open('assets/tamanho.txt', 'r') as arq:
            #     po = arq.readline()
            po = self.LerLocalStorage(self.page, key= self.nome, tempo = 3)
            # po = self.page.client_storage.get(self.nome)

            p1 = po.split(',')
            p = [int(float(i)) for i in p1]
            po = p[:4] 

            if self.width_min:
                if po[0]< self.width_min:
                    po[0] = self.width_min  
            if self.height_min:
                if po[1]< self.height_min:
                    po[1] = self.height_min 
            if po[2] <0:
                po[2] = 0   
            if po[3] <0:
                po[3] = 0                                   

            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = po
            # print('acerto')
        except:
            # print('erro!')
            # with open('assets/tamanho.txt', 'w') as arq:
            #     arq.write(f'{{self.page.window.width}},{{self.page.window.height}},{{self.page.window.top}},{{self.page.window.left}}')
            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = self.width_min,self.height_min,0,0


class Saida:
    def __init__(self,  page = None):
        self.page = page
        self.snac = ft.SnackBar(
            content = ft.Text('', selectable=True, color=ft.colors.WHITE),
            open=False,

            elevation=10,
            duration=6000,
            show_close_icon=True,  
            close_icon_color  = 'white',                 
            bgcolor=ft.colors.GREY_900,
            behavior=ft.SnackBarBehavior.FLOATING,
            dismiss_direction=ft.DismissDirection.END_TO_START,
            shape = ft.RoundedRectangleBorder(12)                    
        )
        self.page.overlay.append(self.snac)
 
    
    def pprint(self, *texto):
        self.snac.open = True
        for i in list(texto):
            self.snac.content.value = f'{{i}}'
            self.page.open(
                self.snac
            )            
        try:
            self.page.update()
        except:
            pass


def InserirCaixa(controls, page):
    return ft.Column(controls, expand=True, scroll=ft.ScrollMode.HIDDEN,height = page.height - 5 if page.web else page.window.height - 50)

def AppBar(titulo = None, rota = '/temas'):       
    return ft.AppBar(
        # actions=[ap.menubar],
        leading=ft.IconButton(
            icon=ft.Icons.PALETTE, 
            height=5,
            splash_radius=0,

            on_click=lambda e: e.page.go(rota)
        ),
        title=ft.Text(
            value=titulo,
            weight='BOLD',
            text_align='center',
            size=20,
            color=ft.Colors.PRIMARY,
            style=ft.TextStyle(
                shadow=ft.BoxShadow(
                    blur_radius=8,
                    color=ft.Colors.SHADOW,
                    offset = (-4,2),
                    blur_style = ft.ShadowBlurStyle.OUTER
                ),
                letter_spacing=5
            )
        ),

        # shadow_color=ft.Colors.with_opacity(1, ft.Colors.SHADOW),
        elevation=8,
        toolbar_height=30,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_SECONDARY),
        automatically_imply_leading=False,
    )







def IniciarTema(page):
    arquiv = Ler_json(
        Caminho('Tema.json', 'TEmas_flet'),
            default=  {{
                "black": {{
                    "background": None,
                    "error": None,
                    "error_container": None,
                    "inverse_primary": None,
                    "inverse_surface": None,
                    "on_background": None,
                    "on_error": None,
                    "on_error_container": None,
                    "on_inverse_surface": None,
                    "on_primary": "limeyellow",
                    "on_primary_container": None,
                    "on_secondary": None,
                    "on_secondary_container": "grey",
                    "on_surface": "cyan",
                    "on_surface_variant": "lightgreen",
                    "on_tertiary": None,
                    "on_tertiary_container": None,
                    "outline": "bluegrey",
                    "outline_variant": None,
                    "primary": "lightblue",
                    "primary_container": "grey",
                    "scrim": None,
                    "secondary": None,
                    "secondary_container": "white",
                    "shadow": "bluegrey",
                    "surface": "limeyellow",
                    "surface_tint": None,
                    "surfaceContainerHighest": "limeyellow",
                    "tertiary": None,
                    "tertiary_container": None
                }}
            }} 
        )

    temastxt= r'assets\mytheme.txt'
    if  path.exists(temastxt):
        with open(temastxt, 'r') as arq:
            tema = arq.read()
    else:
        with open(temastxt, 'w') as arq:
            arq.write('black')
        tema = 'black'
    
    if tema:
        page.bgcolor = 'surface'
        dic_atributos = arquiv[tema].copy()

        if dic_atributos.get("light", False):
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK

        page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                thickness=0
            ),
            color_scheme=ft.ColorScheme(
                primary = dic_atributos["primary"],
                on_primary = dic_atributos["on_primary"],
                on_secondary_container = dic_atributos["on_secondary_container"],
                outline = dic_atributos["outline"],
                shadow = dic_atributos["shadow"],
                on_surface_variant = dic_atributos["on_surface_variant"],
                surface_variant = dic_atributos["surfaceContainerHighest"],
                primary_container = dic_atributos["primary_container"],
                on_surface = dic_atributos["on_surface"],
                surface = dic_atributos["surface"],
            )
        )

    return page


def BarraLateral(width = 200):     
    content = ft.Column(
        controls = [
                ft.Text('meiuhkljlk aslkdjaslkj')                        
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll=ft.ScrollMode.ADAPTIVE
    ) 
    oculto = ft.Icon(ft.Icons.MENU, color='black,0.8')
    def Hover(e):
        if e.data == 'true':
            # e.control.gradient = ft.LinearGradient(
            #     colors= ['#0a0d40', ft.Colors.BLACK],
            #     stops=[0,0.5],
            # )
            e.control.bgcolor = 'white,0.05'
            e.control.width = width 
            e.control.alignment=ft.alignment.top_left
            e.control.content = content 
            
        else:
            e.control.bgcolor = 'white,0.02'
            e.control.width = 20 
            e.control.alignment=ft.alignment.center
            # e.control.gradient = None
            e.control.content = oculto                 
        e.control.update()

    return ft.Container( 
        content=oculto,                      
        width=20,
        bgcolor='white,0.02',
        alignment=ft.alignment.center,
        expand=True,
        on_hover=Hover
    )


"""
  

    script_temas  = f"""


from .imports import ft,dump, load, JSONDecodeError, environ, path, mkdir, Caminho, AppBar


class Componentes:
    def __init__(self, layout):
        self.layout = layout

        self.confirmar = ft.IconButton(icon = ft.Icons.SAVE, tooltip='Confirmar', on_click= self.layout.Salvar)
        self.cancelar = ft.IconButton(icon = ft.Icons.CANCEL, tooltip='Cancelar', on_click= self.layout.Cancelar)
        self.nome_tema = ft.TextField(
            hint_text='Digite o nome do tema', 
            label='Digite o nome do tema', 
            col = 96,
            filled=True,
            dense=True,
            border_width=0.5,
            content_padding = 5,
            border_radius=8,
            suffix=ft.Row([ self.confirmar, self.cancelar], tight=True, alignment=ft.MainAxisAlignment.END),
            visible=False,
        )


        self.conf = False
        self.linha_salve = ft.ResponsiveRow([self.nome_tema, self.confirmar, self.cancelar], columns=48,visible = False, col =96)
        self.btn_save = ft.FilledButton('Salvar Tema', on_click=self.layout.TornarVizivel, col = 24)

               
        self.select_dark_light = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value='DARK', label="DARK",label_style= ft.TextStyle(weight='BOLD')),
                    ft.Radio(value="LIGHT", label="LIGHT",label_style= ft.TextStyle(weight='BOLD')),
                
                ]
            ),
            on_change=self.layout.Change_dark_light,
        )

        self.tema_escolhido = ft.Dropdown(
            label='Selecione um tema',
            col = 3,
            options = [
                ft.dropdown.Option(i)
                for i in sorted(list(self.layout.arquiv.keys()))
            ],
            on_change=self.layout.EscolherTema
        )       


        self.ferramentas = ft.Container(
            bgcolor=ft.Colors.SURFACE,           
            expand=True,
            content = ft.ResponsiveRow(
                [
                    ft.ElevatedButton('ElevatedButton',),
                    ft.FilledButton(text = 'FilledButton'),                                                      
                    ft.FilledTonalButton(text = 'FilledTonalButton'),
                    ft.OutlinedButton(text = 'OutlinedButton'),
                    ft.TextField('ksajgh',label='texto', filled=True, dense = True,),
                    ft.Dropdown(
                        label='drop', 
                        options=[ft.dropdown.Option(i) for i in range(10)],
                        dense = True,
                        filled = True,
                    ),
                    ft.Slider(
                        min = 1,
                        max = 100,
                        divisions = 100,
                        label='casa',
                        value=50,
                    ),
                    ft.Switch(label = 'valor swith') ,
                    ft.Checkbox(label ='checkbox'),
                    ft.Icon(name = ft.Icons.BOOK),
                    ft.PopupMenuButton(
                        content=ft.Text('TEMA', weight=ft.FontWeight.W_900),
                        items = [
                            ft.PopupMenuItem('dark',checked=False),
                            ft.PopupMenuItem('light',checked=True ),
                        ],
                    ),   
                    ft.Text('título',color=ft.Colors.PRIMARY,),                              
                ],                
                columns={{'xs':48, 'sm':60 }},
                spacing = 0,
                run_spacing = 10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,            
            )
        )         
        self.sair = ft.FilledTonalButton('Sair', on_click=self.layout.RestaurarJanela)        

class TemaSelectSysten(ft.View):
    def __init__(self):
        super().__init__()    
        self.arquivo_temas = Caminho('Tema.json', 'TEmas_flet')
        self.appbar = AppBar('Temas', '/principal')
        self.appbar.leading.icon = ft.Icons.ARROW_BACK
        self.GetArquivo()
        self.componentes = Componentes(self)
        self.icon = ft.Icons.PALETTE
        self.scroll = ft.ScrollMode.HIDDEN

        self.icon = ft.Icons.PALETTE

        self.em_edicao = False
        self.GetTemastxt()




    def did_mount(self):
        # self.ct_old = self.page.controls.copy() 
        self.controls = [
            self.JanelaEditarTema()
        ]
        
        try:       
            with open(self.temastxt , 'r') as arq:
                tema = arq.read()
        except:
            tema = None
        if tema:
            self.page.bgcolor = 'surface'
            self.dic_atributos = self.arquiv.get(tema,self.arquiv.get('black')).copy()


            if self.dic_atributos.get("light", False):
                self.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                self.page.theme_mode = ft.ThemeMode.DARK


            self.page.theme = ft.Theme(
                color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
                color_scheme=ft.ColorScheme(
                    primary = self.dic_atributos["primary"],
                    on_primary = self.dic_atributos["on_primary"],
                    on_secondary_container = self.dic_atributos["on_secondary_container"],
                    outline = self.dic_atributos["outline"],
                    shadow = self.dic_atributos["shadow"],
                    on_surface_variant = self.dic_atributos["on_surface_variant"],
                    surface_variant = self.dic_atributos["surfaceContainerHighest"],
                    primary_container = self.dic_atributos["primary_container"],
                    on_surface = self.dic_atributos["on_surface"],
                    surface = self.dic_atributos["surface"],
                    # on_primary_container = self.dic_atributos["on_primary_container"],
                    # secondary = self.dic_atributos["secondary"],
                    # on_secondary = self.dic_atributos["on_secondary"],
                    # tertiary = self.dic_atributos["tertiary"],
                    # on_tertiary = self.dic_atributos["on_tertiary"],
                    # tertiary_container = self.dic_atributos["tertiary_container"],
                    # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
                    # error = self.dic_atributos["error"],
                    # on_error = self.dic_atributos["on_error"],
                    # error_container = self.dic_atributos["error_container"],
                    # on_error_container = self.dic_atributos["on_error_container"],
                    # background = self.dic_atributos["background"],
                    # on_background = self.dic_atributos["on_background"],
                    # outline_variant = self.dic_atributos["outline_variant"],
                    # scrim = self.dic_atributos["scrim"],
                    # inverse_surface = self.dic_atributos["inverse_surface"],
                    # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
                    # inverse_primary = self.dic_atributos["inverse_primary"],
                    # surface_tint = self.dic_atributos["surface_tint"],
                )
            )
                
            for i in list(self.dic_atributos.keys()):
            #     self.icones[i].color = self.dic_atributos[i]
                try:
                    self.menus[i].content.border = ft.border.all(5,self.dic_atributos[i])
                except:
                    pass
            self.menus.update()                  
        self.page.update()

    def GetArquivo(self):
        self.arquiv = self.ler_json(self.arquivo_temas, 
            default=  {{
                    "black": {{
                        "background": None,
                        "error": None,
                        "error_container": None,
                        "inverse_primary": None,
                        "inverse_surface": None,
                        "on_background": None,
                        "on_error": None,
                        "on_error_container": None,
                        "on_inverse_surface": None,
                        "on_primary": "limeyellow",
                        "on_primary_container": None,
                        "on_secondary": None,
                        "on_secondary_container": "grey",
                        "on_surface": "cyan",
                        "on_surface_variant": "lightgreen",
                        "on_tertiary": None,
                        "on_tertiary_container": None,
                        "outline": "bluegrey",
                        "outline_variant": None,
                        "primary": "lightblue",
                        "primary_container": "grey",
                        "scrim": None,
                        "secondary": None,
                        "secondary_container": "white",
                        "shadow": "bluegrey",
                        "surface": "limeyellow",
                        "surface_tint": None,
                        "surfaceContainerHighest": "limeyellow",
                        "tertiary": None,
                        "tertiary_container": None
                    }}
                }}                       
            )       

    def GetTemastxt(self):
        self.temastxt= r'assets\mytheme.txt'
        if not path.exists(self.temastxt):
            with open(self.temastxt, 'w') as arq:
                arq.write('black')


    def RestaurarJanela(self, e):
        e.page.controls = self.ct_old
        e.page.update()
        self.em_edicao = False

    def GerarMenus(self, i):
        return ft.PopupMenuButton(
            content = ft.Container(
                ft.Text(self.funcoes[i], no_wrap=False,), 
                border=ft.border.all(5,'blue'),
                padding = ft.Padding(5,0,5,0),
                margin=0,
                border_radius=12,
                

            ),                        
            splash_radius = 0,
            tooltip = '',
            items=[
                ft.PopupMenuItem(
                    content = self.paleta(i), 
                                            
                ),
                ft.PopupMenuItem(
                    content = self.GerarCores(i),                          
                ),                            
                
            ],
            col = 1 if len(self.funcoes[i]) <= len('labels, cor da caixa do checkbox e cor do check do popMenubutton') else 3
        
        
        ) 

    def Change_dark_light(self, e):
        match e.data:
            case "DARK":
                e.page.theme_mode = ft.ThemeMode.DARK
                self.dic_atributos["light"] = False
            case "LIGHT":
                e.page.theme_mode = ft.ThemeMode.LIGHT
                self.dic_atributos["light"] = True
        e.page.update()


    def GetAtributos(self):
        self.cores = [
            "white","black","red","pink","purple",
            "deeppurple","indigo", "blue","lightblue",
            "cyan","teal","green","lightgreen","lime"
        "yellow", "amber", "orange", "deeporange",
        "brown","bluegrey","grey"

        ]
        self.funcoes = {{
            'primary': 'primary: texto principal, fundo filledbutton, texto outlinedbutton, slider,  preenchimento do switch e checkbox, icone,  texto do elevatebuton',
            'on_primary': 'on_primary: texto filledbutton e bolinha do swicth com True',
            'on_secondary_container': 'on_secondary_container: texto filledtonalbutton',
            'outline': 'outline: borda do outliedbutton',
            'shadow': 'shadow: sombras',
            'on_surface_variant': 'on_surface_variant: labels, cor da caixa do checkbox e cor do check do popMenubutton',
            'surface_variant': 'surface_variant: slider e fundo do texfield e do dropbox',
            'primary_container': 'primary_container: HOVERED da bolinha do switch',
            'on_surface': 'on_surface: HOVERED do checkbox e cor dos items do popmenubuton',
            'surface': 'surface: cor de fundo',
            'color_scheme_seed':'color_scheme_seed',

        }}
        self.atributos_ColorScheme = list(self.funcoes.keys())
        
    def JanelaEditarTema(self):
        self.GetAtributos()
        self.dic_atributos = {{i:None for i in self.atributos_ColorScheme}}
        self.icones = {{i:ft.Icon(name = ft.Icons.SQUARE, data = [i, False], color = 'white') for i in self.atributos_ColorScheme}}
        
        self.menus = {{i:self.GerarMenus(i) for i in self.atributos_ColorScheme}}
        
        self.cts = [
            self.componentes.ferramentas, 
            self.componentes.tema_escolhido, 
            self.componentes.select_dark_light
        ]
        
        self.cts += [self.menus[i] for i in self.atributos_ColorScheme]
        
        self.cts += [
            ft.ResponsiveRow(
                [
                    self.componentes.btn_save, 
                    self.componentes.nome_tema
                ], 
                columns=96, 
                spacing=0, 
                run_spacing=0
            )
        ]
    
        return ft.ResponsiveRow(
            self.cts,
            columns={{'xs':2, 'sm':3 }},
            spacing=20,
            run_spacing = 10,                           
        )

    def GerarCores(self, data):
        return ft.GridView(
            [
                # ft.IconButton(icon = ft.Icons.SQUARE, icon_color = i, col = 0.2,splash_radius=0, padding = 0, on_focus=self.SelecColor) 
                ft.Container(
                    bgcolor = i, 
                    data = data,
                    col = 0.2, 
                    padding = 20, 
                    on_click=self.definirCor 
                ) 
                for i in list(ft.Colors)[list(ft.Colors).index('scrim')+1:]
            ],
            col = 2, 
            # columns=5,
            width=200,
            height=100,
            runs_count = 8,
            padding = 0,
            # aspect_ratio=1,
            run_spacing=0, 
            spacing=0
        )        



    def TornarVizivel(self, e):
        self.componentes.btn_save.visible = False
        # self.linha_salve.visible = True
        self.componentes.nome_tema.visible = True
        
        # self.linha_salve.update()
        self.componentes.nome_tema.update()
        self.componentes.btn_save.update()


    def Salvar(self, e):
        nome_tema = self.componentes.nome_tema.value
        if nome_tema not in ['', ' ', None]+list(self.arquiv.keys()):
            self.arquiv[nome_tema] = self.dic_atributos
            self.escrever_json(self.arquiv, self.arquivo_temas)
            self.componentes.nome_tema.visible = False
            self.componentes.btn_save.visible = True
        else:
            self.componentes.nome_tema.hint_text = 'Digite um nome de Tema válido ou clique em Cancelar'
            # self.nome_tema.hint_style = ft.TextStyle(size = 10)

        e.page.update()

    def EscolherTema(self, e):
        tema = self.componentes.tema_escolhido.value
        self.CarregarTema(tema, e.page)

    def CarregarTema(self, tema, page):
        if tema:
            page.bgcolor = 'surface'
            self.dic_atributos = self.arquiv[tema].copy()      

            if self.dic_atributos.get("light", False):
                self.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                self.page.theme_mode = ft.ThemeMode.DARK


            page.theme = ft.Theme(
                color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
                color_scheme=ft.ColorScheme(
                    primary = self.dic_atributos["primary"],
                    on_primary = self.dic_atributos["on_primary"],
                    on_secondary_container = self.dic_atributos["on_secondary_container"],
                    outline = self.dic_atributos["outline"],
                    shadow = self.dic_atributos["shadow"],
                    on_surface_variant = self.dic_atributos["on_surface_variant"],
                    surface_variant = self.dic_atributos["surfaceContainerHighest"],
                    primary_container = self.dic_atributos["primary_container"],
                    on_surface = self.dic_atributos["on_surface"],
                    surface = self.dic_atributos["surface"],
                )
            )
                
            for i in list(self.dic_atributos.keys()):
            #     self.icones[i].color = self.dic_atributos[i]
                try:
                    self.menus[i].content.border = ft.border.all(5,self.dic_atributos[i])
                except:
                    pass
            # self.menus[i].update()  

            with open(self.temastxt, 'w') as arq:
                arq.write(tema)

            # self.icones[i].update()                
            page.update()
            
    def Cancelar(self, e):
        self.componentes.nome_tema.value = ''
        self.componentes.nome_tema.visible = False
        self.componentes.btn_save.visible = True
        self.componentes.nome_tema.update()
        self.componentes.btn_save.update()        
        self.update()

    def escrever_json(self, data, filename):
        # if not filename.endswith('.json'):
        #     filename += '.json'
        with open(filename, 'w') as f:
            dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        # if not filename.endswith('.json'):
        #     filename += '.json'
        try:
            with open(filename, 'r') as f:
                return load(f)
        except (FileNotFoundError, JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {{}}


    def definirCor(self, e):
        self.menus[e.control.data].content.border = ft.border.all(5,e.control.bgcolor)
        self.menus[e.control.data].update()

        if e.control.data == 'surface':
            self.page.bgcolor = e.control.bgcolor

        self.dic_atributos[e.control.data] = e.control.bgcolor

        self.page.theme_mode = self.dic_atributos.get("theme_mode",None)

        self.page.theme = ft.Theme(
            color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
            color_scheme=ft.ColorScheme(
                primary = self.dic_atributos["primary"],
                on_primary = self.dic_atributos["on_primary"],
                on_secondary_container = self.dic_atributos["on_secondary_container"],
                outline = self.dic_atributos["outline"],
                shadow = self.dic_atributos["shadow"],
                on_surface_variant = self.dic_atributos["on_surface_variant"],
                surface_variant = self.dic_atributos["surfaceContainerHighest"],
                primary_container = self.dic_atributos["primary_container"],
                on_surface = self.dic_atributos["on_surface"],
                surface = self.dic_atributos["surface"],
  
            )
        )

        self.page.update()



    def paleta(self, data):
        return ft.GridView(
            [
                ft.Container(bgcolor = i, data = data,col = 0.2, padding = 20, on_click=self.definirCor) 
                for i in self.cores
            ],
            col = 2, 
            
            runs_count = 6,
            padding = 0,
            # aspect_ratio=16/9,
            run_spacing=0, 
            spacing=0
        )

    def Atributos(self, classe):
        return [attr for attr in dir(classe) if not attr.startswith('__')]


"""


    arq_yml = f"""
name: implantar pagina

on:
  # Runs on push to any of the below branches
#   push:
#     branches: 
#       - master
#       - main
#   # Runs on pull request events that target one of the below branches
#   pull_request:
#     branches: 
#       - master
#       - main

  # Allows you to run this workflow manually from the Actions tab of the repository
  workflow_dispatch:

# Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest queued.
# However, do NOT cancel in-progress runs as we want to allow these production deployments to complete.
concurrency:
  group: "pages"
  cancel-in-progress: false

env:
  # https://flet.dev/docs/publish#versioning
  BUILD_NUMBER: 1
  BUILD_VERSION: 1.0.0
  PYTHON_VERSION: 3.12.6
  FLUTTER_VERSION: 3.24
  
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Python ${{{{env.PYTHON_VERSION}}}}
      uses: actions/setup-python@v2
      with:
        python-version: ${{{{env.PYTHON_VERSION}}}}

    - name: Install Python Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -U -r requirements.txt
  
    - name: Setup Flutter ${{{{env.FLUTTER_VERSION}}}}
      uses: subosito/flutter-action@v2
      with:
        flutter-version: ${{{{env.FLUTTER_VERSION}}}}

    - name: Flet Build Web
      run: |
            echo "GITHUB_REPOSITORY: ${{GITHUB_REPOSITORY}}, USER: ${{GITHUB_REPOSITORY%/*}}, PROJECT_BASE_URL: ${{GITHUB_REPOSITORY#*/}}"
            flutter config --no-analytics
            flet build web --base-url ${{GITHUB_REPOSITORY#*/}} --route-url-strategy hash

    - name: Upload Artifact
      uses: actions/upload-pages-artifact@v3
      with:
        name: web-build-artifact  # the name of the artifact
        path: build/web

  deploy:
    needs: build  # wait for the "build" job to get done before executing this "deploy" job

    runs-on: ubuntu-latest

    # Grant GITHUB_TOKEN the permissions required to make a Pages deployment
    permissions:
      pages: write      # to deploy to Pages
      id-token: write   # to verify the deployment originates from an appropriate source

    # Deploy to the github-pages environment
    environment:
      name: github-pages
      url: ${{{{steps.deployment.outputs.page_url}}}}
      
    steps:
      - name: Setup Pages
        uses: actions/configure-pages@v5
        
      - name: Deploy to GitHub Pages 🚀
        if: ${{{{ github.event_name == 'push' || github.event_name == 'workflow_dispatch' }}}}  # Deploy em push ou execução manual
        id: deployment
        uses: actions/deploy-pages@v4.0.5
        with:
          artifact_name: web-build-artifact
        env:
          GITHUB_TOKEN: ${{{{ secrets.PERSONAL_ACCESS_TOKEN }}}}  # Adiciona o token aqui        
"""    


    requi = f"""flet
python-dotenv    

"""
   
    
    with open(cf_file_path, 'w', encoding="utf-8") as f:
        f.write(criar_exe)
    print(f"Created file: {cf_file_path}")
    with open(main_file_path, 'w', encoding = "utf-8") as f:
        f.write(principal)
    print(f"Created file: {cf_file_path}")
    with open(yml_file_path, 'w', encoding = "utf-8") as f:
        f.write(arq_yml)
    print(f"Created file: {yml_file_path}")    
    with open(requi_file_path, 'w', encoding = "utf-8") as f:
        f.write(requi)
    with open(imports_path, 'w', encoding = "utf-8") as f:
        f.write(script_imports)          
    with open(tema_path, 'w', encoding = "utf-8") as f:
        f.write(script_temas) 
    with open(componentes_path, 'w', encoding = "utf-8") as f:
        f.write(script_components)    
    with open(env_path, 'w', encoding = "utf-8") as f:
        f.write(script_env)    
    with open(func_path, 'w', encoding = "utf-8") as f:
        f.write(script_func)  
    with open(layout_principal_path, 'w', encoding = "utf-8") as f:
        f.write(script_layout_principal)          
                                                                           
    print(f"Created file: {requi_file_path}")     

    

if __name__ == "__main__":
    # Verifica se foi passado um nome
    if len(sys.argv) < 2:
        print("Por favor, forneça um nome para o projeto.")
        sys.exit(1)
    
    # Usa o nome passado como argumento
    project_name = sys.argv[1]
    base_path = f"./{project_name}"
    create(base_path)
