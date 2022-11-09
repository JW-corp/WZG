import subprocess
import pathlib

def execute(strs):
	for isochg in IsoChg_sb:
		args = strs + ' ' + isochg + ' ' + '--closure True'

		print(args)
		subprocess.call(args,shell=True)


if __name__ == "__main__":
	

	# All SB
	low_isochg		= list(range(3,9,1))
	high_isochg		= list(range(8,14,1))
	IsoChg_sb		= []
	
	for l,low in enumerate(low_isochg):
		for h,high in enumerate(high_isochg):
			if l > h:
				continue
			
			name = f"from_{low}_to_{high}"
			IsoChg_sb.append(name)		

	# --Just test for one SB
	#IsoChg_sb = ["from_3_to_8"]

	execute("python FakePhoton_CR_template_DrawOnly2016.py EB_PT1")
	execute("python FakePhoton_CR_template_DrawOnly2016.py EB_PT2")
	execute("python FakePhoton_CR_template_DrawOnly2016.py EB_PT3")
	execute("python FakePhoton_CR_template_DrawOnly2016.py EB_PT4")
	execute("python FakePhoton_CR_template_DrawOnly2016.py EB_PT5")
	execute("python FakePhoton_CR_template_DrawOnly2016.py EE_PT1")
	execute("python FakePhoton_CR_template_DrawOnly2016.py EE_PT2")
