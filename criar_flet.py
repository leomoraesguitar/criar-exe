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
        '.github/workflows'
    ]
    
    os.makedirs(base_path, exist_ok=True)
    if len(folders) > 0:
        for folder in folders:
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created: {folder_path}")

    # Cria o arquivo cf.py dentro da pasta base
    cf_file_path = os.path.join(base_path, "criar_exe.py")
    main_file_path = os.path.join(base_path, "main.py")
    requi_file_path = os.path.join(base_path, "requirements.txt")
    yml_file_path = os.path.join(base_path,'.github','workflows', "deploy-github-pages.yml")


    criar_exe = f"""
import PyInstaller.__main__
from os import path
from shutil  import rmtree


class Criar_exe:
    def __init__(self,
        programas = [
            'main.py',
            ]                 
    ):
        self.limpar_pasta('build')
        
        for i in programas:
            # if not i.endswith('.spec') and i.endswith('.py'):
            sp = i.split('.')[0]+'.spec'
            if  path.exists(sp):
                PyInstaller.__main__.run([
                    sp
                ])  
            elif i.endswith('.py'):
                PyInstaller.__main__.run([
                            i,
                            '--onefile',
                            '--windowed'
                        ])

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
    Criar_exe(programas)
"""


    principal = f"""

import flet as ft

class ConfirmarSaida:
    def __init__(self,page, funcao = None):
        super().__init__()
        self.page = page
        self.funcao = funcao
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
        self.page.window.prevent_close = True 
   


    def window_event(self, e):
            if e.data == "close":
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

class Resize:
    def __init__(self,page):
        self.page = page
        self.page.on_resized = self.page_resize
        self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
        self.page.overlay.append(self.pw)   

    def page_resize(self, e):
        self.pw.value = f'{{self.page.window.width}}*{{self.page.window.height}} px'
        self.pw.update()



class Saida:
    def __init__(self,  page = None):
        self.page = page
        self.snac = ft.SnackBar(
                    content = ft.Text('', selectable=True, color=ft.colors.BROWN_100),
                    open=True,
                    bgcolor=ft.colors.GREY_900,
                )
 
    
    def pprint(self, *texto):
        for i in list(texto):
            self.snac.content.value = f'{{i}}'
            self.page.open(
                self.snac
            )            
        try:
            self.page.update()
        except:
            pass



    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = height
        try:
            self.controls[0].content.height = self._height
            # print(self.controls[0])
            self.page.update()
        except:
            pass



class ClassName(ft.Column):
    def __init__(self,page, pprint):
        self.page = page
        self.pprint = pprint
        super().__init__()
        self.controls = [ft.Text('Meu ovo')]


def main(page: ft.Page):
    # Definindo o titulo da pagina
    page.title = 'Título'
    page.window.width = 500  # Define a largura da janela como 800 pixels
    page.window.height = 385  # 
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        scrollbar_theme = ft.ScrollbarTheme(
            thickness = {{
                ft.ControlState.HOVERED:20,
                ft.ControlState.DRAGGED:20, 
                ft.ControlState.SCROLLED_UNDER:20
                  }},
        ),
        use_material3 = True,
        color_scheme=ft.ColorScheme(
            primary = ft.colors.WHITE70, # cor fundo filledbutton e cor texto outlinedbutton
            on_primary = ft.colors.BLACK, #cor texto filledbutton e cor da bolinha do swicth com True
            secondary_container = ft.colors.GREY_700, # cor de fundo filledtonalbutton
            on_secondary_container = ft.colors.WHITE, # cor de tecto filledtonalbutton
            outline = ft.colors.GREY_600, #cor de borda do outliedbutton
            shadow = ft.colors.BLUE_300, # cor das sombras
            on_surface_variant = ft.colors.WHITE, #cor dos labela
            surface_variant = ft.colors.GREY_600, #cor do slider e cor de fundo do texfield
            primary_container = ft.colors.WHITE70, #cor da bolinha do switch
            on_surface = ft.colors.WHITE, #cor HOVERED do checkbox

        ),
        divider_theme=ft.DividerTheme(
            color=ft.colors.with_opacity(0.5, ft.colors.GREY_800),      # Cor do divisor
            thickness=1,               # Espessura da linha divisória
            leading_indent=1,                 # Recuo inicial
            trailing_indent=1              # Recuo final
        ),
        text_theme=ft .TextTheme(
            title_large=ft.TextStyle(
                size = 20,
                weight=ft.FontWeight.W_800,
            )
        ),
        slider_theme=ft.SliderTheme(
            thumb_color = ft.colors.GREY_700,
        ),
        switch_theme= ft.SwitchTheme(
            thumb_color = {{
                ft.ControlState.DEFAULT:ft.colors.GREY_400,
                ft.ControlState.HOVERED:None,
                ft.ControlState.SELECTED:ft.colors.GREY_300,

            }},
            track_color = {{
                ft.ControlState.DEFAULT:ft.colors.GREY_700,
                ft.ControlState.HOVERED:ft.colors.GREY_700,
            }},
            overlay_color = {{
                ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
            }},
            track_outline_color= {{
                ft.ControlState.DEFAULT:ft.colors.WHITE,
                ft.ControlState.HOVERED:ft.colors.WHITE,
            }},
            track_outline_width= {{
                ft.ControlState.DEFAULT:0,
                ft.ControlState.HOVERED:0
            }},
        ),
        checkbox_theme = ft.CheckboxTheme(
            overlay_color = {{
                ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
            }},                
        ),
    )    

    page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor= ft.colors.BLACK38,
            inactive_color=ft.colors.GREY,
            active_color=ft.colors.GREEN_800,
            on_change=lambda e: print("Selected tab:", e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.icons.BOOKMARK_BORDER,
                    selected_icon=ft.icons.BOOKMARK,
                    label="Explore",
                ),
            ]
        )
    
    page.appbar = ft.AppBar(
        actions = [ft.Container(ft.Text('meu pau')) for i in range(5)],
        title=ft.Text(
            value = 'Guerra de Clans', 
            weight='BOLD', 
            color=ft.colors.GREEN_600,
            style=ft.TextStyle(
                shadow = ft.BoxShadow(
                    blur_radius = 300,
                    # blur_style = ft.ShadowBlurStyle.OUTER,
                    color = ft.colors.WHITE
                ),                
            )
            ),
        shadow_color=ft.colors.BLUE,
        elevation=8,
        toolbar_height = 30,
        bgcolor=ft.colors.BLACK38,
        automatically_imply_leading=False,
    )     




    saida = Saida()
    print = saida.pprint 
    ConfirmarSaida()
    Resize(page)
    p = ClassName(page  = page, pprint = saida.pprint)
    page.add(p)

if __name__ == '__main__': 
    ft.app(target=main)

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
