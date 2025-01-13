import tkinter as tk
from tkinter import ttk
import pyautogui
import keyboard
import time
import json

# Configuração inicial do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.001  # Menor delay possível entre comandos

class BrawlhallaMacro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Brawlhalla Combo Macro")
        self.root.geometry("400x350")
        
        # Estado do macro
        self.active = False
        
        # Dicionário de combos com frames
        self.combos = {
            "Sword": {
                "DLight -> SAir": [
                    {"key": "s", "hold": True},  # down
                    {"key": "c", "frames": 2},   # light attack (dlight)
                    {"key": "s", "hold": False}, # soltar o down
                    {"key": "wait", "frames": 25},  # mesmo timing do dlight->recovery
                    {"key": "space", "frames": 2},  # jump
                    {"key": "d", "hold": True},  # right
                    {"key": "wait", "frames": 5},   # aumentado tempo de espera antes do sair
                    {"key": "c", "frames": 2}    # light attack (sair)
                ],
                "DLight -> Recovery": [
                    {"key": "s", "hold": True},  # down
                    {"key": "c", "frames": 2},   # light attack
                    {"key": "s", "hold": False}, # soltar o down
                    {"key": "wait", "frames": 25},  # aumentei o tempo de espera da animação do dlight
                    {"key": "space", "frames": 2},  # jump
                    {"key": "x", "frames": 2}    # heavy attack
                ]
            },
            "Axe": {
                "SLight -> SAir": [
                    {"key": "d", "hold": True},  # right
                    {"key": "c", "frames": 2},   # light attack (slight)
                    {"key": "d", "hold": False}, # soltar direita
                    {"key": "wait", "frames": 20},  # tempo de espera do slight
                    {"key": "space", "frames": 2},  # jump
                    {"key": "wait", "frames": 5},   # aumentado tempo de espera antes do sair
                    {"key": "w", "hold": True},   # pressiona cima
                    {"key": "d", "hold": True},   # pressiona direita
                    {"key": "c", "frames": 2},    # light attack (sair)
                    {"key": "w", "hold": False},  # solta cima
                    {"key": "d", "hold": False}   # solta direita
                ],
                "SLight -> NAir": [
                    {"key": "d", "hold": True},  # right
                    {"key": "c", "frames": 2},   # light attack (slight)
                    {"key": "d", "hold": False}, # soltar direita
                    {"key": "wait", "frames": 20},  # reduzido 2 frames do tempo de espera do slight
                    {"key": "space", "frames": 2},  # jump
                    {"key": "wait", "frames": 5},   # esperar subir no pulo
                    {"key": "w", "hold": True},   # pressiona cima
                    {"key": "c", "frames": 2},    # light attack (nair)
                    {"key": "w", "hold": False}   # solta cima
                ]
            }
        }
        
        self.setup_gui()
        self.setup_hotkeys()
        
    def setup_gui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Brawlhalla Combo Macro", font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Seleção de arma
        weapon_frame = ttk.LabelFrame(main_frame, text="Configuração", padding="5")
        weapon_frame.pack(fill=tk.X, pady=5)
        
        self.weapon_var = tk.StringVar()
        weapon_label = ttk.Label(weapon_frame, text="Arma:")
        weapon_label.pack(side=tk.LEFT, padx=5)
        weapon_combo = ttk.Combobox(weapon_frame, textvariable=self.weapon_var, width=15)
        weapon_combo['values'] = list(self.combos.keys())
        weapon_combo.pack(side=tk.LEFT, padx=5)
        weapon_combo.bind('<<ComboboxSelected>>', self.update_combos)
        
        # Lista de combos
        self.combo_var = tk.StringVar()
        combo_frame = ttk.LabelFrame(main_frame, text="Combo", padding="5")
        combo_frame.pack(fill=tk.X, pady=5)
        
        combo_label = ttk.Label(combo_frame, text="Selecione:")
        combo_label.pack(side=tk.LEFT, padx=5)
        self.combo_list = ttk.Combobox(combo_frame, textvariable=self.combo_var, width=25)
        self.combo_list.pack(side=tk.LEFT, padx=5)
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value="DESATIVADO")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                               font=('Helvetica', 12, 'bold'), foreground='red')
        self.status_label.pack(pady=5)
        
        # Instruções
        info_frame = ttk.LabelFrame(main_frame, text="Instruções", padding="5")
        info_frame.pack(fill=tk.X, pady=5)
        
        info_text = "1. Selecione a arma e o combo desejado\n" + \
                   "2. Pressione T para ativar/desativar o macro\n" + \
                   "3. Mova o mouse para o canto superior esquerdo para parar\n\n" + \
                   "Teclas:\n" + \
                   "- C: Ataque leve\n" + \
                   "- X: Ataque pesado\n" + \
                   "- SPACE: Pulo\n" + \
                   "- WASD: Movimento"
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(pady=5, padx=5)
        
    def setup_hotkeys(self):
        keyboard.on_press_key('t', self.toggle_macro)
        
    def update_combos(self, event=None):
        weapon = self.weapon_var.get()
        if weapon in self.combos:
            self.combo_list['values'] = list(self.combos[weapon].keys())
            
    def toggle_macro(self, e=None):
        self.active = not self.active
        status = "ATIVADO" if self.active else "DESATIVADO"
        color = 'green' if self.active else 'red'
        self.status_var.set(status)
        self.status_label.configure(foreground=color)
        
        if self.active:
            self.execute_combo()
            # Desativa automaticamente após executar o combo
            self.active = False
            self.status_var.set("DESATIVADO")
            self.status_label.configure(foreground='red')
            
    def execute_combo(self):
        if not self.active:
            return
            
        weapon = self.weapon_var.get()
        combo_name = self.combo_var.get()
        
        if not weapon or not combo_name:
            self.status_var.set("Selecione arma e combo!")
            self.status_label.configure(foreground='orange')
            self.active = False
            return
            
        if weapon in self.combos and combo_name in self.combos[weapon]:
            sequence = self.combos[weapon][combo_name]
            
            # Soltar todas as teclas antes de começar
            pyautogui.keyUp('all')
            
            try:
                for action in sequence:
                    if action.get("key") == "wait":
                        # Apenas espera os frames
                        if "frames" in action:
                            time.sleep(action["frames"] * (1/60))
                    else:
                        if action.get("hold", False):
                            pyautogui.keyDown(action["key"])
                        else:
                            if action.get("hold") == False:  # explicitamente False
                                pyautogui.keyUp(action["key"])
                            else:
                                pyautogui.press(action["key"])
                        
                        if "frames" in action:
                            time.sleep(action["frames"] * (1/60))
                    
                # Soltar todas as teclas no final
                pyautogui.keyUp('all')
                
            except Exception as e:
                self.status_var.set("Erro: " + str(e))
                self.status_label.configure(foreground='red')
                self.active = False
                
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BrawlhallaMacro()
    app.run()
