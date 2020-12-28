from django.shortcuts import render
from django.http import HttpResponse
import matplotlib
import csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .forms import Profile_Form
from .models import User_Profile
from django.core.files.storage import FileSystemStorage
import pandas as pd
import seaborn as sns
# Create your views here.
#def home(request):
    #return render(request,'home.html')
def index(request):
    request.session.set_expiry(0)
    if request.session.get('filename',False):
        context = {'upload_file_caption' : request.session['filename']}
    else:
        context = {'upload_file_caption' : "No file uploaded"}
    return render(request,'index.html',context)

def login(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return "EXCEPTION"
        context = {'columns' : fieldnames}

        return render(request,'login.html',context)
    else:
        return render(request,'create.html')
    return render(request,'login.html')

def create_profile(request):
    return render(request, 'create.html')   

def process(request):
    print(request.POST)
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return "EXCEPTION"
        context = {'columns' : fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #if request.method =='POST':
        #print(request.FILES)
        #uploaded_file =request.FILES['filename']
        #name = uploaded_file.name 
        #print(uploaded_file.size)
        #print(uploaded_file.name)
       
        #fs = FileSystemStorage()
        #fs.save(uploaded_file.name,uploaded_file)
    sns_plot = data_handler(dict(request.POST),name)
    sns_plot.figure.savefig('static/images/output.png')
    sns_plot.figure.clf()
    return render(request,'login.html',context)


FILE_TYPES = ['css']

def fileupload(request):
    if request.method =='POST':
       #print(request.FILES)
        if request.session.get('filename',False) :
            del request.session['filename']
        uploaded_file = request.FILES['filename']
        name = uploaded_file.name 
        #print(uploaded_file.size)
        #print(uploaded_file.name)
        request.session['filename'] = name
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
    
    return render(request, 'index.html',{'upload_file_caption' : request.session['filename']})



    

'''def add(request):
    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])
    res = val1 + val2
    print(request.POST)
    return render(request,'result.html',{'result':res})'''  


#To handle and prepare the dataset
def data_handler(req_dict,name):
    dict_attr = {'palette': 'tab10','sort': True, 'output': 'png','hue' : None, 'x' : '', 'y': '', 'plot_type': '', 'filename': '', 'col_list': '', 'vmin':'','vmax':'', 'cbar': True, 'linecolor' : 'blue', 'linewidths':'0.9','annot':None, 'cumulative' : False}
    possible_attr = ['filename','x','y','plot_type','hue','palette','sort','output','vmin','vmax','linecolor','linewidths','annot']
    for i in  possible_attr:
        dict_attr[i] = (req_dict.get(i,['']))[0]
    dict_attr['col_list'] = req_dict.get('col_list','')
    
    #FILENAME
    if dict_attr['filename'] == '':
        dict_attr['filename'] = name
    else:
        dict_attr['sort'] = True
    #SORT
    if dict_attr['sort'] == 'false':
        dict_attr['sort'] = False
    else:
        dict_attr['sort'] = True
    #PALETTE
    if dict_attr['palette'] == '' or dict_attr['palette'] == 'tab10':
        dict_attr['palette'] = 'tab10'
        
    #OUTPUT
    if dict_attr['output'] == '' or dict_attr['output'] == 'png':
        dict_attr['output'] = 'png'
    
    #HUE
    if dict_attr['hue'] == '':
        dict_attr['hue'] = None
    
    #Vmin
    if dict_attr['vmin'] == '':
        dict_attr['vmin'] = None
    
    #Vmax
    if dict_attr['vmax'] == '':
        dict_attr['vmax'] = None
        
    #Cbar
    if dict_attr['cbar'] == 'false':
        dict_attr['cbar'] = False
    else:
        dict_attr['cbar'] = True
    
    #LineColor
    if dict_attr['linecolor'] == '':
        dict_attr['linecolor'] = 'white'
    
    #LineWidths
    if dict_attr['linewidths'] == '':
        dict_attr['linewidths'] = 0
    if type(dict_attr['linewidths']) == type('string'):
        dict_attr['linewidths'] = eval(dict_attr['linewidths'])
        
    #ANNOT
    if dict_attr['annot'] == 'false':
        dict_attr['annot'] = False
    elif dict_attr['annot'] == 'true':
        dict_attr['annot'] = True
    else:
        dict_attr['annot'] = None
    
    #CUMULATIVE
    #if dict_attr['sort'] == 'true':
    #    dict_attr['sort'] = True
  #  else:
    #    dict_attr['sort'] = False
      
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + dict_attr['filename']) #RUNNING
    except:
        return "EXCEPTION"
    
    #print(data['SepalLength'])
    if dict_attr['plot_type'] == 'lineplot':
        return line_plot(data,dict_attr)
    
    elif dict_attr['plot_type'] == 'scatterplot':
        return scatter_plot(data,dict_attr)
    
    elif dict_attr['plot_type'] == 'heatmap':
        return heat_map(data,dict_attr)
    elif dict_attr['plot_type'] == 'histplot':
        return hist_plot(data,dict_attr)
        
    #LINEPLOT
def line_plot(dataset,dict_attr):
    #sns.set('darkgrid')
    #print(dataset)
    #sns.set_context(context=paper)
    print('\n\nWAIT...')
    sns_plot = sns.lineplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'], 
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                            sort = dict_attr['sort'])
    
    if dict_attr['output'].lower() == 'png' or dict_attr['output'] == None:
        #sns_plot.figure.savefig('static/images/output.png')
        #plt.close()
        print('YOUR PLOT IS CREATED!')

        return sns_plot
    
    #SCATTERPLOT
def scatter_plot(dataset,dict_attr):
    #sns.set(style = 'white',context = 'notebook',)
    #print(dataset)
    print('\n\nWAIT...')
    sns_plot = sns.scatterplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'],
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                              ) 
    
    if dict_attr['output'].lower() == 'png' or dict_attr['output'] == None:
        sns_plot.figure.savefig('static/images/output.png')
        
        print('YOUR PLOT IS CREATED!')
        return True

    #HEATMAP
def heat_map(dataset,dict_attr):
    #sns.set(style = 'white',context = 'notebook',)
    #print(dataset)
    print('\n\nWAIT...')
    sns_plot = sns.heatmap(data = dataset[dict_attr['col_list'] ] , cmap = dict_attr['palette'],vmin = dict_attr['vmin'],vmax = dict_attr['vmax'],cbar = dict_attr['cbar'],linecolor = dict_attr['linecolor'], linewidths = dict_attr['linewidths'],annot = dict_attr['annot']) 
    
    if dict_attr['output'].lower() == 'png' or dict_attr['output'] == None:
        sns_plot.figure.savefig('static/images/output.png')
        
        print('YOUR PLOT IS CREATED!')
        return True
    
    #HISTOGRAM
def hist_plot(dataset,dict_attr):
    #sns.set(style = 'white',context = 'notebook',)
    #print(dataset)
    print('\n\nWAIT...')
    sns_plot = sns.distplot(dataset ,
                            x = dict_attr['x'], y = dict_attr['y'],
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                              ) 
    
    if dict_attr['output'].lower() == 'png' or dict_attr['output'] == None:
        sns_plot.figure.savefig('static/images/output.png')
        
        print('YOUR PLOT IS CREATED!')
        return True


'''data_handler({'csrfmiddlewaretoken': ['VeN2LfA9iZbc6hiCN9EKM3E9U0cbtUrkYfAAALfXv0nrtCRwLVi8X95p6P0H9hsP'],
'filename': ['purva'], 'plot_type': ['histplot'], 'x': ['SepalLength'], 'y': ['PetalLength'],
'hue': ['Name'], 'filename': ['iris.csv'],'palette':['tab10'],'sort':['true'],'output':['png'],
'col_list':['SepalLength','PetalLength'], 'vmin':[''],'vmax':[''], 'cbar': ['true'],
'linecolor' : ['blue'], 'linewidths':[''], 'annot':['true'],
'cumulative': ['false']})'''
'''data_handler({'csrfmiddlewaretoken': ['VeN2LfA9iZbc6hiCN9EKM3E9U0cbtUrkYfAAALfXv0nrtCRwLVi8X95p6P0H9hsP'],
'filename': ['purva'], 'plot_type': ['lineplot'], 'y': ['SepalLength'], 'x': ['PetalLength'],
'hue': ['Name'], 'filename': ['iris.csv'],'palette':['tab10'],'sort':['true'],'output':['png']
})'''
    
    
    
#'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'  