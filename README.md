# Heat Sink Design Project 
This is a sample project that aims to demonstrate various possible Onshape integrations with the REST API. Speicifically, this project demonstrates two alternatives that API calls can be made: (1) simple coding in a Jupyter notebook, and (2) integration to the Onshape user interface with a Python Flask application. 

Correspondingly, more detailed guides to these two integration methods can be found in [this repository](https://github.com/PTC-Education/Onshape-Integration-Guides). To really get started and learn about these methods, it is highly recommended to first go through the integration guides for the basics and then return to this project to see its capability. 

In this project, we first build an Onshape model of a simple heat sink with fins on top for heat dissipation. By varying the width and the spacing of the fins, we use a series of REST API calls to obtain measurements of the heat sink from Onshape. Then, we can algorithmically calculate the varying amount of heat transfer from the heat sink with variables mentioned above. 

![snapshot](/assets/Snapshot.png)

**Note:** Due to the difference in the two integration methods, the same Onshape CAD model was built with two different approach: one with configurations [here](https://cad.onshape.com/documents/90a4d9714ef6b02d6588ec72/w/d59102477548ee2c306f9746/e/ef65b54bd20ceea1d75b8d86), and the other one with variables [here](https://cad.onshape.com/documents/13046f844758cea0ce3bee69/w/dc532bde45fb75c1c623bb25/e/57bf8613c8f6897aca0e0ec5). 

## 1. Jupyter Notebook 
Simply locate and open the document named `Heat_Sink_Demo.ipynb` in this repository. It is recommended to click the badge at the top of the page to "Open in Colab", or you can also upload and open the Jupyter notebook in your Google Drive with Google Colab. 

Without re-running the code, you should be able to see the saved results of the code blocks and get a sense of some of the capabilities of the REST API calls in Onshape. To play around with the parameters and make changes to the code for further exploration, you will need to do the following: 
1. Make a copy to [this Onshape document](https://cad.onshape.com/documents/90a4d9714ef6b02d6588ec72/w/d59102477548ee2c306f9746/e/ef65b54bd20ceea1d75b8d86) in your own Onshape account. 
2. Follow the instructions of [section 2 of this guide](https://github.com/PTC-Education/Onshape-Integration-Guides/blob/main/API_Intro.md#2-generating-your-onshape-api-keys) to create your API keys. Such that you can configure your client to access your copied Onshape document. 
3. Follow the instructions on the Jupyter notebook to configure your client with the API keys you created and copy the URL of your copied Onshape document. Then, you are good to go! 

## 2. Flask application 
