# AMIVA-F-test package


AMIVA-F is a machine learning based algorithm, trained to correlate single point mutations
with disease in FLNc.



# General Information:

AMIVA-F requires additionally JAVA and PYMOL installed.
A step by step tutorial on how to install AMIVA-F is given below for different operating systems
Currently it is tested on Anaconda3(Windows 10) but more OS and outside of virtual environments (like anaconda) will be tested soon aswell.

----------------------------------------------------------------------------------------------------------------

Anaconda is a distribution of python programming language that helps with package management and deployment. 
Its available for Windows, Linux and macOS. 
Package versions in Anaconda are managed by an internal package managment system which does not mess with your local computer package depository.
It further simplifies Path dependency problems and is outlined below for a full installation of AMIVA-F tested on Windows in Anaconda3.

# Example setup of Anaconda3 from Windows10:

First download Anaconda from https://www.anaconda.com/products/individual
Click on the downloaded .exe data and follow the instructions.
If you get to the point of advanced installing options:
check Register anaconda3 as your default python3.8 

Afterwards open the anaconda prompt (anaconda3) which you find by entering anaconda prompt into the search bar at the left bottom and simply type:

	conda create -n amivaenv python=3.8

This creates a new virtual environment with python 3.8 named amivaenv which will be used to install AMIVA and its dependencies without polluting your local pythonspace.
After creation enter:
	
	conda activate amivaenv

Which will then activate the new environment.


Then download javabridge from https://www.lfd.uci.edu/~gohlke/pythonlibs/#javabridge (you can check your bitness of your PC by pressing the windows key + i together, then navigate to system and then chose About.) There you will find 
under the title Device specifications your system type(e.g 64.bit operating)
In that case you would then simply download the javabridge‑1.0.19‑cp38‑cp38‑win_amd64.whl which specifies 64 bit and requires Cpython 3.8 (we made the environment at the beginning with python=3.8!)

Now navigate to https://adoptopenjdk.net/ and grab OPEN JDK11 and download latest release.
After downloading, run the .exe file, agree to the terms and continue to the Custom Setup screen.
Here you need to change the Set Java home variable (3rd row) to will be installed on local hard drive!

Click next, install and proceed.

Now everything should be setup for success. Search now for javabridge (this should be normally in your download folder) and enter the specified path to the anaconda prompt:
This could look like below but you need to change your username (in my case there it was adm2, in yours its different).
If you get in general a prompt which asks you to proceed [y]/[n] enter y.	

	pip install C:\Users\adm2\Downloads\javabridge-1.0.19-cp38-cp38-win_amd64.whl
		
Follow afterwards with:

	pip install AMIVA-F

Additionally we require Pymol:

	conda install -c schrodinger pymol

Pymol will ask your permission to install a bunch of files which you accept by entering y again.
Side note: Pymol can't be installed through pip, we therefore refer to the conda packaging service in order to get pymol.

If everything worked and you got no error message, navigate now towards the newly imported packagedirectory
This could look like below but in your case it will again differ at the adm2 part where you might need to change.
If you navigate towards this file directory and you find it, you can simply rightclick on the AMIVA-F.py script e.g and select properties -> 
This will give you the full path which you can simply copy paste to the terminal.
Dont forget to put cd in front!

	cd C:\Users\adm2\anaconda3\envs\amivaenv\Lib\site-packages\AMIVA-F


and there enter:

	python AMIVA-F.py

This will prompt you a GUI which you can interact with and you managed to successfully install AMIVA-F!
		

# Usage of AMIVA-F

AMIVA-F works fully automated and is easy to use, even in the absence of knowledge about the underlying parameters which are used as input for the neural network.

Step 1)

AMIVA-F works at the protein annotation level, therefore if you have mutations of interest in the c notation (DNA), look up the corresponding p.notation.

Once you have your mutation of interest in protein notation, enter it in the entry field location directly above the green button ("Calculate everything for me!").
The required input should look like this:

	M82K             

This input would correspond to the single point mutation at position 82 in FLNc, where the wildtype amino acid (M, Methionine) is substituted
by the mutated amino acid (K, Lysine).
If you by any chance submit a wrong amino acid (the amino acid you specified for the wildtype position is in fact not what you submitted, e.g FLNc position 82
corresponds to methionine, but you wrote S82K, which would correspond to serine), then AMIVA-F automatically corrects you and offers you to proceed calculations with the correct amino acid in in place.

Step 2)

After you entered the mutation of interest e.g M82K into the entry field specified above, click the green button ("Calculate everything for me!")
This button will then automatically grab the correct model structure where your amino acid is located and calculate all input parameters required to predict the pathogenicity of the mutation.
Usually this process is really fast, you will see all entry fields filled and you should normally just check if there is anything left blank.
The 2 last rows in the entryfield (Found posttranslational modification sites, and additional information) are solely there to inform you about potentially interesting sited in close proximity (8Angström cutoff) of the desired mutation spot.
If you are working by any chance on posttranslational modifications or you possess information about additional binding partners, feel free to add them to the library files ( 
Posttranslational_modifications_and_binding_partners\Binding_partners_list.txt and Posttranslational_modifications_and_binding_partners\Posttranslational_modification_list.txt) which will be taken into account when filling out the input parameters.

Step 3) 

Check if every entry field in the form is filled and every radiobutton is selected.
If everything seems fine, proceed by clicking the blue button ("Generate template file").
This will prepare a specific input parameter file which will then be placed into the correct directory and can be directly used for further prediction by AMIVA-F


Step 4)

Click the red button ("Prediction on pathogenicity") and wait a couple of seconds.
In the background, AMIVA-F trains itself with 10x cross validation with additional stratification (details can be seen later in the Trainingset info section of the neighbouring button).
This process takes a couple of seconds but afterwards you should see the following entries:
(In the examplary case of M82K input)




More information can be found at the full tutorial inside the package.
