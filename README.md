# AC-Check: A Chrome extension for web accessibility analysis, aggregation and report generation
Project made by Mikel Iturria and supervised by Juan Miguel López as the final degree project of a bachelor degree on Informatics engineering, with a mention on Software engineering for the University of the Basque Country (UPV/EHU).

The report of the project is available, in Spanish, at the next [link](https://drive.google.com/file/d/1SsHwztz9aWI-KaMxSwsF6HW6rLIp7ULM/view?usp=sharing).

## The project

#### Why was the project made?
The aim of this project is making easier the analysis and the creation of a report for an accessibility tester. Also, being able to share that report without any problem. 

#### Features
This project has some interesting features:
- **Automatic generation of reports**: With just clicking a button in the extension, the API generates a report of the web where the user is located with the results for that web on the [AChecker](https://achecker.achecks.ca/checker/index.php) and [AccessMonitor](https://accessmonitor.acessibilidade.gov.pt/) reporters.
- **Manual agreggation of results**: The extension also can aggregate manual reports made and uploaded to the extension by different users without losing information.
- **It is possible to download and share the report**: Also, visualize it in the [W3C report tool](https://www.w3.org/WAI/eval/report-tool/).
- **Mark the conflictive elements**: The code of the conflictive elements detected by the analizers can be clcked and the extension will mark the element in the page adding a red border to it. You can see examples in the demo of the next section.


#### How it works?
A video demo of the project is available in the next [link](https://youtu.be/InkyZ-bUi78).

The API has also a documentation made with _Sphinx_. You can open it by opnening the _index.html_ in ``flask/docs/_build/html/index.html`` 

## Installation
In this section we will describe the instalation on Windows/Linux
#### Before starting 
Before starting the installation, the PC needs to have installed both Python and Git.

#### API installation
Firstly, we will clone the project.
```
git init;
git clone https://github.com/Itusil/TFG.git;
```

Once the project is cloned, we will prepare the API. For that purpouse, we will open the command line in _Linux_ or the PowerShell in _Windows_, and will enter inside the **Flask** folder of the project.

Only in _Windows_, we will change the execution policy of the PowerShell: 
```
powershell Set-ExecutionPolicy RemoteSigned
```

Now, we will delete the **venv** and the **__pycache** folders. Once both folders are deleted, we will create the virtual enviroment:

###### Windows
```
py -3 -m venv venv
```
###### Linux
```
conda create -n tfg_iturria python=3.9
```

Now, we will activate the virtual enviroment and open it.
###### Windows
```
.\venv\Scripts\activate
```
###### Linux
```
source activate tfg_iturria
```

We will notice that the virtual enviroment is activated:

###### Windows
![Virtual enviroment activated on Windows](https://cdn.discordapp.com/attachments/401053836707495936/1000724725678481489/an1_8.jpg)
###### Linux
![Virtual enviroment activated on Linux](https://cdn.discordapp.com/attachments/401053836707495936/1000724725955313765/an1_6.jpg)

We will now install all the complements needed for the project. Inside the virtual enviroment we will run:

###### Windows and Linux
```
$ pip install Flask
$ pip install flask_cors
$ pip install bs4
$ pip install datetime
$ pip install selenium
$ pip install chromedriver-autoinstaller
```

Optionally (but reccomended) we set the enviroment to ``development``
###### Windows
```
$env:FLASK_ENV = "development"
```
###### Linux
```
export FLASK_ENV =development
```

Finally, only in _Linux_, we will give the ChromeDriver execution permission:
###### Linux
```
sudo chmod +x chromedriver
```

Now, we just need to run Flask:
###### Windows and Linux
```
flask run
```

The API will be working correctly:

![Api working](https://cdn.discordapp.com/attachments/401053836707495936/1000727130986004490/an1_5.jpg)

#### Installation of the extension
The installation of the extension is really easy. First we visit ``chrome://extensions/``. Once there, we click in "development mode" and in "load unzipped".

![Loading the extension](https://cdn.discordapp.com/attachments/401053836707495936/1000727778561376267/cargar1.jpg)

We will choose the AC-Check folder of the root of the project and we will see that the extension has been correctly opened.

![Extension is correctly opened](https://cdn.discordapp.com/attachments/401053836707495936/1000727778959822858/cargar2.jpg)

Now, if we visit any page, we will see the side bar created by the extension.

![Sidebar created by the extension](https://cdn.discordapp.com/attachments/401053836707495936/1000728666294210560/ehu1.jpg)

By clicking the icon on the navigation bar, the extension will switch off and the extension will no longer active.

## License

The license of the project is **CC BY-NC-SA 4.0** (Credit must be given to the creator, only noncommercial uses of the work are permitted and adaptations must be shared under the same terms).

![CC BY-NC-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-sa.png)

