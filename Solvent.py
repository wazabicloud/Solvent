import tkinter as tk
from tkinter import StringVar, ttk, messagebox
import re
import math

ELEMENT_LIST = {"H": float(1.0079),
"He": float(4.0026),
"Li": float(6.941),
"Be": float(9.0122),
"B": float(10.811),
"C": float(12.0107),
"N": float(14.0067),
"O": float(15.9994),
"F": float(18.9984),
"Ne": float(20.1797),
"Na": float(22.9897),
"Mg": float(24.305),
"Al": float(26.9815),
"Si": float(28.0855),
"P": float(30.9738),
"S": float(32.065),
"Cl": float(35.453),
"K": float(39.0983),
"Ar": float(39.948),
"Ca": float(40.078),
"Sc": float(44.9559),
"Ti": float(47.867),
"V": float(50.9415),
"Cr": float(51.9961),
"Mn": float(54.938),
"Fe": float(55.845),
"Ni": float(58.6934),
"Co": float(58.9332),
"Cu": float(63.546),
"Zn": float(65.39),
"Ga": float(69.723),
"Ge": float(72.64),
"As": float(74.9216),
"Se": float(78.96),
"Br": float(79.904),
"Kr": float(83.8),
"Rb": float(85.4678),
"Sr": float(87.62),
"Y": float(88.9059),
"Zr": float(91.224),
"Nb": float(92.9064),
"Mo": float(95.94),
"Tc": float(98),
"Ru": float(101.07),
"Rh": float(102.9055),
"Pd": float(106.42),
"Ag": float(107.8682),
"Cd": float(112.411),
"In": float(114.818),
"Sn": float(118.71),
"Sb": float(121.76),
"I": float(126.9045),
"Te": float(127.6),
"Xe": float(131.293),
"Cs": float(132.9055),
"Ba": float(137.327),
"La": float(138.9055),
"Ce": float(140.116),
"Pr": float(140.9077),
"Nd": float(144.24),
"Pm": float(145),
"Sm": float(150.36),
"Eu": float(151.964),
"Gd": float(157.25),
"Tb": float(158.9253),
"Dy": float(162.5),
"Ho": float(164.9303),
"Er": float(167.259),
"Tm": float(168.9342),
"Yb": float(173.04),
"Lu": float(174.967),
"Hf": float(178.49),
"Ta": float(180.9479),
"W": float(183.84),
"Re": float(186.207),
"Os": float(190.23),
"Ir": float(192.217),
"Pt": float(195.078),
"Au": float(196.9665),
"Hg": float(200.59),
"Tl": float(204.3833),
"Pb": float(207.2),
"Bi": float(208.9804),
"Po": float(209),
"At": float(210),
"Rn": float(222),
"Fr": float(223),
"Ra": float(226),
"Ac": float(227),
"Pa": float(231.0359),
"Th": float(232.0381),
"Np": float(237),
"U": float(238.0289),
"Am": float(243),
"Pu": float(244),
"Cm": float(247),
"Bk": float(247),
"Cf": float(251),
"Es": float(252),
"Fm": float(257),
"Md": float(258),
"No": float(259),
"Rf": float(261),
"Lr": float(262),
"Db": float(262),
"Bh": float(264),
"Sg": float(266),
"Mt": float(268),
"Rg": float(272),
"Hs": float(277)}


def extract_mm(entry):
	"""
	extract_mm prende una stringa e cerca di calcolare la massa molare del composto
	"""

	sum = float()

	# Prima cosa da fare è collassare le parentesi
	# Per esempio (NO3)2 viene trasformato in N2O6
	while True:
		
		# Vengono trovare tutte le parentesi più interne
		in_par = re.compile("\([A-Za-z0-9]+\)[0-9]*")
		par_found = in_par.findall(entry)

		# Se non ci sono parentesi il ciclo si chiude
		if not par_found:
			break

		for item in par_found:
			new_string = str()

			# Dalle parentesi vengono presi i contenuti e i coefficienti
			# Se non ci sono coefficienti viene assegnato 1 in automatico
			par_content = re.findall("\((.+)\)", item)
			par_coeff = re.findall("\)([0-9]+)", item)

			if not par_coeff:
				par_coeff = ["1"]

			# Vengono trovati i diversi elementi cercando le lettere maiuscole in par_content
			elements = re.findall("[A-Z][a-z0-9]*", par_content[0])

			# Per ogni elemento viene riassegnato un "pedice"
			# moltiplicando il pedice attuale per il coefficiente delle parentesi
			# Tutti gli elementi con i nuovi pedici vengono inseriti in new_string

			for subitem in elements:
				sym = re.findall("[A-Za-z]+", subitem)
				subscript = re.findall("[0-9]+", subitem)

				if not subscript:
					subscript = ["1"]

				new_coeff = int(subscript[0]) * int(par_coeff[0])
				new_string = new_string+sym[0]+str(new_coeff)

			# La parentesi originale viene sostituita da new_string e si ricomincia
			entry = entry.replace(item,new_string,1)

	# Una volta tolte tutte le parentesi, il composto viene diviso in base
	# alle lettere maiuscole per trovare gli elementi
	elements = re.findall("[A-Z][a-z0-9]*", entry)

	# Per ogni elemento prova a calcolare la massa molare, altrimenti restituisce None
	try:
		for subitem in elements:
			sym = re.findall("[A-Za-z]+", subitem)
			subscript = re.findall("[0-9]+", subitem)
			if not subscript:
				subscript = ["1"]
			sum = sum + (ELEMENT_LIST[sym[0]] * float(subscript[0]))
		return sum
	except:
		return None

compound_list = list()

class AddByCompound(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)

		tk.Label(self, text="Compound:").grid(column=0, row=1, pady=10, padx=(10,5), sticky="e")

		self.add_compound_entry = tk.Entry(self, textvariable=new_compound, width=31)
		self.add_compound_entry.grid(column=1, row=1, pady=10, padx=(0,10), columnspan=2)

		tk.Label(self, text="Concentration:").grid(column=0, row=2, pady=10, padx=(10,5))

		self.conc_entry = tk.Entry(self, textvariable=conc_var)
		self.conc_entry.grid(column=1, row=2, pady=10)

		self.conc_unit = ttk.Combobox(self, values=["M", "g/L", "ppm"], width=5, state="readonly")
		self.conc_unit.grid(column=2, row=2, pady=10, padx=10)
		self.conc_unit.set("M")

		self.add_entry_btn = tk.Button(self, text="Add compound/Refresh", command=self.add_compound)
		self.add_entry_btn.grid(column=0, row=3, columnspan=3, sticky="nesw", padx=10, pady=(0,10))

	def add_compound(self):
		"""
		Funzione per aggiungere il composto quando viene premuto il pulsante
		"""
		if new_compound.get() and conc_var.get():
			while True:
				molar_mass = float()
				# Controllare che non sia un doppione
				double_chk = False
				for item in compound_list:
					if item["name"] == new_compound.get() and item["conc"] == conc_var.get() and item["conc_unit"] == self.conc_unit.get():
						double_chk = True

				if double_chk == True:
					break
				# Controllare che concentrazioni e volume abbiano senso
				try:
					float(conc_var.get())
				except:
					tk.messagebox.showerror(title="Error!", message="Invalid compound concentration!")
					break

				if float(conc_var.get()) <= 0:
					tk.messagebox.showerror(title="Error!", message="Concentration must be a positive number!")
					break
				
				try:
					float(volume_entry.get())
				except:
					tk.messagebox.showerror(title="Error!", message="Invalid volume!")
					break

				if float(volume_entry.get()) <= 0:
					tk.messagebox.showerror(title="Error!", message="Volume must be a positive number!")
					break
				
				# Se selezionata molarità, controllare anche se esiste il composto

				if self.conc_unit.get() == "M":
					if type(extract_mm(new_compound.get())) == None or extract_mm(new_compound.get()) == 0.0:
						tk.messagebox.showerror(title="Error!", message="Compound not recognized!")
						break
					else:
						molar_mass = extract_mm(new_compound.get())
						unit_per_ml = float(conc_var.get())*molar_mass/1000
				elif self.conc_unit.get() == "g/L":
					unit_per_ml = float(conc_var.get())/1000
				elif self.conc_unit.get() == "ppm":
					unit_per_ml = float(conc_var.get())/1000000

				compound_list.append({
						"name": new_compound.get(),
						"conc": conc_var.get(),
						"conc_unit": self.conc_unit.get(),
						"unit": "g",
						"unit_per_ml": unit_per_ml
					})
				
				break
		print_entries()

class AddBySolution(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)

		tk.Label(self, text="Initial\nconcentration:").grid(column=0, row=0, pady=10, padx=(10,5))

		self.init_conc_entry = tk.Entry(self, textvariable=init_conc_var)
		self.init_conc_entry.grid(column=1, row=0, pady=10)

		self.init_conc_unit = ttk.Combobox(self, values=["M", "g/L", "wt%"], width=5, state="readonly")
		self.init_conc_unit.grid(column=2, row=0, pady=10, padx=10)
		self.init_conc_unit.set("M")

		tk.Label(self, text="Compound:").grid(column=0, row=1, pady=10, padx=(10,5), sticky="e")

		self.add_compound_entry = tk.Entry(self, textvariable=new_compound, width=31)
		self.add_compound_entry.grid(column=1, row=1, pady=10, padx=(0,10), columnspan=2)

		tk.Label(self, text="Density:").grid(column=0, row=2, pady=10, padx=(10,5), sticky="e")

		self.density_entry = tk.Entry(self, textvariable=density_var)
		self.density_entry.grid(column=1, row=2, pady=10)

		tk.Label(self, text="g/L").grid(column=2, row=2, padx=(5,10), pady=10, sticky="w")

		tk.Label(self, text="Final\nconcentration:").grid(column=0, row=3, pady=10, padx=(10,5))

		self.final_conc_entry = tk.Entry(self, textvariable=conc_var)
		self.final_conc_entry.grid(column=1, row=3, pady=10)

		self.final_conc_unit = ttk.Combobox(self, values=["M", "g/L"], width=5, state="readonly")
		self.final_conc_unit.grid(column=2, row=3, pady=10, padx=10)
		self.final_conc_unit.set("M")

		self.add_entry_btn = tk.Button(self, text="Add solution/Refresh", command=self.add_compound)
		self.add_entry_btn.grid(column=0, row=4, columnspan=3, sticky="nesw", padx=10, pady=(0,10))

	def add_compound(self):
		"""
		Funzione per aggiungere il composto quando viene premuto il pulsante
		"""
		if init_conc_var.get() and new_compound.get() and conc_var.get():
			while True:
				molar_mass = float()
				# Controllare che non sia un doppione
				double_chk = False
				for item in compound_list:
					if item["name"] == new_compound.get() and item["conc"] == conc_var.get() and item["conc_unit"] == self.final_conc_unit.get():
						double_chk = True

				if double_chk == True:
					break

				# Controllare che concentrazioni e volume abbiano senso
				try:
					float(init_conc_var.get())
				except:
					tk.messagebox.showerror(title="Error!", message="Invalid initial concentration!")
					break

				if float(init_conc_var.get()) <= 0:
					tk.messagebox.showerror(title="Error!", message="Initial concentration must be a positive number!")
					break

				try:
					float(conc_var.get())
				except:
					tk.messagebox.showerror(title="Error!", message="Invalid final concentration!")
					break

				if float(conc_var.get()) <= 0:
					tk.messagebox.showerror(title="Error!", message="Final concentration must be a positive number!")
					break
				
				try:
					float(volume_entry.get())
				except:
					tk.messagebox.showerror(title="Error!", message="Invalid volume!")
					break

				if float(volume_entry.get()) <= 0:
					tk.messagebox.showerror(title="Error!", message="Volume must be a positive number!")
					break
				
				# Diversi casi in base alle concentrazioni selezionate
				# Se passo da M a M o da g/L a g/L diluisco e basta
				if self.init_conc_unit.get() == self.final_conc_unit.get():
					unit_per_ml = float(conc_var.get())/(float(init_conc_var.get())*1000)

				# Da M a g/L
				elif self.init_conc_unit.get() == "M" and self.final_conc_unit.get() == "g/L":
					if type(extract_mm(new_compound.get())) == None or extract_mm(new_compound.get()) == 0.0:
						tk.messagebox.showerror(title="Error!", message="Compound not recognized!")
						break
					else:
						molar_mass = extract_mm(new_compound.get())
						unit_per_ml = float(conc_var.get())/(float(init_conc_var.get())*molar_mass*1000)

				# Da g/L a M
				elif self.init_conc_unit.get() == "g/L" and self.final_conc_unit.get() == "M":
					if type(extract_mm(new_compound.get())) == None or extract_mm(new_compound.get()) == 0.0:
						tk.messagebox.showerror(title="Error!", message="Compound not recognized!")
						break
					else:
						molar_mass = extract_mm(new_compound.get())
						unit_per_ml = (float(conc_var.get())*molar_mass)/(float(init_conc_var.get())*1000)				

				# Se viene usata wt% bisogna tirare in ballo la densità
				elif self.init_conc_unit.get() == "wt%":
					try:
						float(density_var.get())
					except:
						tk.messagebox.showerror(title="Error!", message="Invalid density!")
						break

					if float(conc_var.get()) <= 0:
						tk.messagebox.showerror(title="Error!", message="Density must be a positive number!")
						break

					if self.final_conc_unit.get() == "g/L":
						unit_per_ml = (float(conc_var.get()))/(10000*float(density_var.get())*float(init_conc_var.get()))

					elif self.final_conc_unit.get() == "M":
						if type(extract_mm(new_compound.get())) == None or extract_mm(new_compound.get()) == 0.0:
							tk.messagebox.showerror(title="Error!", message="Compound not recognized!")
							break
						else:
							molar_mass = extract_mm(new_compound.get())
							unit_per_ml = (float(conc_var.get())*float(molar_mass))/(10000*float(density_var.get())*float(init_conc_var.get()))

				compound_list.append({
						"name": new_compound.get(),
						"conc": conc_var.get(),
						"conc_unit": self.final_conc_unit.get(),
						"unit": "L",
						"unit_per_ml": unit_per_ml
					})
				
				break
		print_entries()

class DestroyButton(tk.Button):
	def __init__(self, master, compound):
		tk.Button.__init__(self, master, text="X", font=("Helvetica", 6, "bold"), command=lambda: self.destroy_entry(compound["name"], compound["conc"], compound["conc_unit"]), bg="red", fg="white", width=1, height=1)

	def destroy_entry(self, destname, destconc, destconc_unit):
		for item in compound_list:
			if item["name"] == destname and item["conc"] == destconc and item["conc_unit"] == destconc_unit:
				compound_list.remove(item)
		
		print_entries()

def print_entries():
	global entry_list
	entry_list.destroy()

	entry_list = tk.LabelFrame(root)
	entry_list.grid(column=0, row=2, sticky="nesw", padx=10, pady=10)

	tk.Label(entry_list, text="Compound").grid(row=0, column=0)
	tk.Label(entry_list, text="Required").grid(row=0, column=2)

	volume = float(volume_entry.get())

	for item in compound_list:
		pos = compound_list.index(item)
		name_label = item["name"]
		conc_label = item["conc"] + " " + item["conc_unit"]

		if item["unit_per_ml"]*volume > 1:
			required_value = math.trunc(item["unit_per_ml"]*volume*1000)/1000
			required_value = str(required_value) + " " + item["unit"]

		elif item["unit_per_ml"]*volume*1000 > 1:
			required_value = math.trunc(item["unit_per_ml"]*volume*1000000)/1000
			required_value = str(required_value) + " m" + item["unit"]
		else:
			required_value = math.trunc(item["unit_per_ml"]*volume*1000000000)/1000
			required_value = str(required_value) + " μ" + item["unit"]

		tk.Label(entry_list, text=name_label).grid(row=pos+2, column=0, pady=5, padx=5)
		tk.Label(entry_list, text=conc_label).grid(row=pos+2, column=1, pady=5, padx=5)
		tk.Label(entry_list, text=required_value).grid(row=pos+2, column=2, pady=5, padx=5)
		DestroyButton(entry_list, item).grid(row=pos+2, column=3, pady=5, padx=5)

def mode_select(event):
	"""
	Permette di selezionare la modalità di aggiunta composti e modificare la GUI di conseguenza.
	Da bindare alla lista delle modalità disponibili
	"""
	global add_input_frame

	if event.widget.get() == "By compound formula":
		
		add_input_frame.destroy()
		add_input_frame = AddByCompound(add_input_wrapper)
		add_input_frame.pack()

	elif event.widget.get() == "By dilution":
		add_input_frame.destroy()
		add_input_frame = AddBySolution(add_input_wrapper)
		add_input_frame.pack()

root = tk.Tk()
root.title("Molar.py")

new_compound = StringVar()
conc_var = StringVar()
init_conc_var = StringVar()
density_var = StringVar()

# Primo riquadro con volume e selezione modalità
main_settings_wrapper = tk.LabelFrame(root)
main_settings_wrapper.grid(column=0, row=0, padx=10, pady=10, sticky="nesw")

tk.Label(main_settings_wrapper, text="Solution volume:").grid(column=0, row=0, padx=(10,5), pady=10, sticky="e")

volume_entry = tk.Entry(main_settings_wrapper, justify="right", width=1)
volume_entry.grid(column=1, row=0, pady=10, sticky="ew")

tk.Label(main_settings_wrapper, text="mL").grid(column=2, row=0, padx=(5,10), pady=10, sticky="w")

# Selezione della modalità di aggiunta
tk.Label(main_settings_wrapper, text="Mode:").grid(row=1, column=0, padx=(10,5), pady=10, sticky="e")

mode_list = ttk.Combobox(main_settings_wrapper, values=["By compound formula", "By dilution"], state="readonly", width=22)
mode_list.grid(row=1, column=1, padx=(0,10), columnspan=2)
mode_list.set("By compound formula")
mode_list.bind('<<ComboboxSelected>>', mode_select)

# Secondo riquadro che varia in base alla modalità selezionata
add_input_wrapper = tk.LabelFrame(root)
add_input_wrapper.grid(column=0, row=1, padx=10, sticky="nesw")

add_input_frame = AddByCompound(add_input_wrapper)
add_input_frame.pack()

# Terzo riquadro con tabella con i composti da pesare
entry_list = tk.Frame(root)
entry_list.grid(column=0, row=2)

root.mainloop()