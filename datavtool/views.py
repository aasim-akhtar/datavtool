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
from datetime import datetime,date
# Create your views here.
#def home(request):
    #return render(request,'home.html')
def index(request):
    request.session.set_expiry(0)
    if request.session.get('name',False):
        context = {'upload_file_caption' : request.session['name']}
    else:
        context = {'upload_file_caption' : "No file uploaded"}
    return render(request,'index.html',context)

def line_scatter_plot(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)


            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
        	print("=========")
        	print(request.session['filename'])
        	print("=========")
        	return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'line_scatter_plot.html',context)
    else:
        return render(request,'create.html')
    return render(request,'line_scatter_plot.html')

def line_scatter_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}
    dict_attr['plot_type']=request.POST.get('plot_type','lineplot')  
    dict_attr['x']=request.POST.get('x',None)
    dict_attr['y']=request.POST.get('y',None)
    dict_attr['hue']=request.POST.get('hue',None)
    dict_attr['sort']=request.POST.get('sort',True)
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    dict_attr['palette']=request.POST.get('palette','tab10')
    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None

    if dict_attr['sort'] == 'false':
        dict_attr['sort'] = False
    else:
        dict_attr['sort'] = True

    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    #print(data['SepalLength'])
    if dict_attr['plot_type'] == 'lineplot':
        sns_plot = line_plotter(data,dict_attr)

    if dict_attr['plot_type'] == 'scatterplot':
        sns_plot =  scatter_plotter(data,dict_attr)    
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = request.POST['plot_type']
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.figure.savefig('media/{}.png'.format(file_name))
    sns_plot.figure.savefig('media/{}.pdf'.format(file_name))
    sns_plot.figure.clf()
    return render(request,'line_scatter_plot.html',context)

def box_plot(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)
                

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            print("=========")
            print(request.session['filename'])
            print("=========")
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'box_plot.html',context)
    else:
        return render(request,'create.html')
    return render(request,'box_plot.html')

def box_plot_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}  
    dict_attr['x']=request.POST.get('x',None)
    dict_attr['y']=request.POST.get('y',None)
    dict_attr['hue']=request.POST.get('hue',None)
    dict_attr['saturation']=request.POST.get('saturation',0.75)
    dict_attr['orient']=request.POST.get('orient','v')
    dict_attr['palette']=request.POST.get('palette','tab10')
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    
    
    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None

    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    #print(data['SepalLength'])
    
    sns_plot = box_plotter(data,dict_attr)   
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = 'boxplot'
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.figure.savefig('media/{}.png'.format(file_name))
    sns_plot.figure.savefig('media/{}.pdf'.format(file_name))
    sns_plot.figure.clf()
    return render(request,'box_plot.html',context)

def bar_plot(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            print("=========")
            print(request.session['filename'])
            print("=========")
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'bar_plot.html',context)
    else:
        return render(request,'create.html')
    return render(request,'bar_plot.html')

def bar_plot_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}  
    dict_attr['x']=request.POST.get('x',None)
    dict_attr['y']=request.POST.get('y',None)
    dict_attr['hue']=request.POST.get('hue',None)
    dict_attr['saturation']=request.POST.get('saturation',0.75)
    dict_attr['orient']=request.POST.get('orient','v')
    dict_attr['palette']=request.POST.get('palette','tab10')
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    
    
    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None
    
    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    #print(data['SepalLength'])
    
    sns_plot = bar_plotter(data,dict_attr)   
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = 'barplot'
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.figure.savefig('media/{}.png'.format(file_name))
    sns_plot.figure.savefig('media/{}.pdf'.format(file_name))
    sns_plot.figure.clf()
    return render(request,'bar_plot.html',context)

def rel_plot(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            print("=========")
            print(request.session['filename'])
            print("=========")
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'rel_plot.html',context)
    else:
        return render(request,'create.html')
    return render(request,'rel_plot.html')

def rel_plot_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}  
    dict_attr['x']=request.POST.get('x',None)
    dict_attr['y']=request.POST.get('y',None)
    dict_attr['hue']=request.POST.get('hue',None)
    dict_attr['size']=request.POST.get('size',None)
    dict_attr['row']=request.POST.get('row',None)
    dict_attr['col']=request.POST.get('col',None)
    dict_attr['kind']=request.POST.get('kind','scatter')
    dict_attr['palette']=request.POST.get('palette','tab10')
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    dict_attr['style2']=request.POST.get('style2',None)
    
    
    if dict_attr['row']!=None and dict_attr['col']!=None:
        dict_attr['row'] = None

    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None
    
    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    #print(data['SepalLength'])
    
    sns_plot = rel_plotter(data,dict_attr)   
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = 'relplot'
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.savefig('media/{}.png'.format(file_name))
    sns_plot.savefig('media/{}.pdf'.format(file_name))
    sns_plot.fig.clf()
    return render(request,'rel_plot.html',context)

def swarm_plot(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            print("=========")
            print(request.session['filename'])
            print("=========")
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'swarm_plot.html',context)
    else:
        return render(request,'create.html')
    return render(request,'swarm_plot.html')

def swarm_plot_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}  
    dict_attr['x']=request.POST.get('x',None)
    dict_attr['y']=request.POST.get('y',None)
    dict_attr['hue']=request.POST.get('hue',None)
    dict_attr['dodge']=request.POST.get('dodge',False)
    dict_attr['orient']=request.POST.get('orient','v')
    dict_attr['size']=request.POST.get('size',5)
    dict_attr['palette']=request.POST.get('palette','tab10')
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    
    if dict_attr['dodge']== 'true':
        dict_attr['dodge'] = True
    else:
        dict_attr['dodge'] = False    

    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None
    
    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    #print(data['SepalLength'])
    
    sns_plot = swarm_plotter(data,dict_attr)   
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = 'swarmplot'
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.figure.savefig('media/{}.png'.format(file_name))
    sns_plot.figure.savefig('media/{}.pdf'.format(file_name))
    sns_plot.figure.clf()
    return render(request,'swarm_plot.html',context)

def pair_plot(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            print("=========")
            print(request.session['filename'])
            print("=========")
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'pair_plot.html',context)
    else:
        return render(request,'create.html')
    return render(request,'pair_plot.html')

def pair_plot_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}  
    dict_attr['vars']=request.POST.get('vars',None)
    dict_attr['hue']=request.POST.get('hue',None)
    dict_attr['kind']=request.POST.get('kind','scatter')
    dict_attr['diag_kind']=request.POST.get('diag_kind','auto')
    dict_attr['palette']=request.POST.get('palette','tab10')
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    

    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None
    
    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    #print(data['SepalLength'])
    
    sns_plot = pair_plotter(data,dict_attr)   
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = 'pairplot'
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.savefig('media/{}.png'.format(file_name))
    sns_plot.savefig('media/{}.pdf'.format(file_name))
    sns_plot.fig.clf()
    return render(request,'pair_plot.html',context)

def dis_plot(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            print("=========")
            print(request.session['filename'])
            print("=========")
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'dis_plot.html',context)
    else:
        return render(request,'create.html')
    return render(request,'dis_plot.html')

def dis_plot_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}  
    dict_attr['x']=request.POST.get('x',None)
    dict_attr['y']=request.POST.get('y',None)
    dict_attr['hue']=request.POST.get('hue',None)
    dict_attr['row']=request.POST.get('row',None)
    dict_attr['col']=request.POST.get('col',None)
    dict_attr['kind']=request.POST.get('kind','hist')
    dict_attr['palette']=request.POST.get('palette','tab10')
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    
    
    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None
    
    if dict_attr['kind'] == 'ecdf':
        if dict_attr['x']!= None and dict_attr['y']!= None:
            dict_attr['y'] = None 

    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    
    
    sns_plot = dis_plotter(data,dict_attr)   
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = 'displot'
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.savefig('media/{}.png'.format(file_name))
    sns_plot.savefig('media/{}.pdf'.format(file_name))
    sns_plot.fig.clf()
    return render(request,'dis_plot.html',context) 

def joint_plot(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
            catagorical_fieldnames = []
            data = pd.read_csv("media/" + request.session['filename'])
            for i in fieldnames:
                if len(list(set(data[i]))) <= 10:
                    catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            print("=========")
            print(request.session['filename'])
            print("=========")
            return render(request,'create.html')
        context = {'columns' : fieldnames,'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'joint_plot.html',context)
    else:
        return render(request,'create.html')
    return render(request,'joint_plot.html')

def joint_plot_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames,'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}  
    dict_attr['x']=request.POST.get('x',None)
    dict_attr['y']=request.POST.get('y',None)
    dict_attr['hue']=request.POST.get('hue',None)
    dict_attr['kind']=request.POST.get('kind','hist')
    dict_attr['palette']=request.POST.get('palette','tab10')
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    
    
    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None
    
    if dict_attr['kind']== 'hex' or dict_attr['kind']== 'reg' or dict_attr['kind'] == 'resid':
        dict_attr['hue'] = None

    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    
    
    sns_plot = joint_plotter(data,dict_attr)   
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = 'displot'
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.savefig('media/{}.png'.format(file_name))
    sns_plot.savefig('media/{}.pdf'.format(file_name))
    sns_plot.fig.clf()
    return render(request,'joint_plot.html',context)


def heat_map(request):
    if request.session.get('filename',False):
        try:
            print("=========")
            print(request.session['filename'])
            print("=========")
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            print("=========")
            print(request.session['filename'])
            print("=========")
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        context['file_name'] = 'images/output'
        return render(request,'heat_map.html',context)
    else:
        return render(request,'create.html')
    return render(request,'heat_map.html')


def heat_map_process(request):
    if request.session.get('filename',False):
        try:
            with open("media/" + request.session['filename'], 'r') as infile:
                reader = csv.DictReader(infile)
                fieldnames = list(reader.fieldnames)
                catagorical_fieldnames = []
                data = pd.read_csv("media/" + request.session['filename'])
                for i in fieldnames:
                    if len(list(set(data[i]))) <= 10:
                        catagorical_fieldnames.append(i)

            #data = pd.read_csv("media/" + request.session['filename'],index_col=0,nrows = 0).columns.tolist() #RUNNING
        except:
            return render(request,'create.html')
        context = {'columns' : fieldnames, 'cata_columns' : catagorical_fieldnames}
        name = request.session['filename']
    else:   
        return render(request,'create.html')
    name = request.session['filename']
    #possible_attr = {'plot_type':'lineplot','x': None,'y':None,'hue':None,'sort':True,'palette':'tab10'}
    dict_attr = {}  
    dict_attr['index']=request.POST.get('index',None)
    dict_attr['column']=request.POST.get('column',None)
    dict_attr['values']=request.POST.get('values',None)
    dict_attr['vmin']=request.POST.get('vmin',None)
    dict_attr['vmax']=request.POST.get('vmax',None)
    dict_attr['linewidths']=request.POST.get('linewidths',0)
    dict_attr['robust']=request.POST.get('robust',False)
    dict_attr['palette']=request.POST.get('palette','tab10')
    dict_attr['context']=request.POST.get('context',None)
    dict_attr['style']=request.POST.get('style',None)
    
    
    if dict_attr['context']== 'default':
        dict_attr['context'] = None

    if dict_attr['style'] == 'default':
        dict_attr['style'] = None
    
    if dict_attr['vmin'] == '':
        dict_attr['vmin'] = None

    if dict_attr['vmax'] == '':
        dict_attr['vmax'] = None
        
    if dict_attr['palette'] == '':
        dict_attr['palette'] = 'tab10'
    try:
        #data = pd.read_csv("" + dict_attr['filename'])  #TESTING
        data = pd.read_csv("media/" + name) #RUNNING
    except:
        return render(request,'create.html')
    
    #print(data['SepalLength'])
    
    sns_plot = heat_map_plotter(data,dict_attr)   
            

    #sns_plot = data_handler(request.POST,name,possible_attr)
    #request.session['sns_plot'] = sns_plot
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    plot_type = 'heatmap'
    #fname =  ''.join(name.split('.')[0:-1]) 
    fname = name[:-4]
    file_name = "{}_{}_{}_{}".format(fname,plot_type,d1,current_time)
    context['file_name'] = file_name
    sns_plot.figure.savefig('media/{}.png'.format(file_name))
    sns_plot.figure.savefig('media/{}.pdf'.format(file_name))
    sns_plot.figure.clf()
    return render(request,'heat_map.html',context)

def fileupload(request):
    return render(request, 'create.html')   

def fileupload_process(request):
    if request.method =='POST':
        #print(request.FILES)
        if request.session.get('filename',False) :
            del request.session['filename']
        if request.session.get('name',False) :
            del request.session['name']
            
        uploaded_file = request.FILES['filename']
        name = uploaded_file.name 
        #print(uploaded_file.size)
        #print(uploaded_file.name)
        request.session['name'] = name
        fs = FileSystemStorage()
        file_name = fs.save(uploaded_file.name,uploaded_file)
        print(file_name)

        request.session['filename'] = file_name
    return render(request, 'index.html',{'upload_file_caption' : name})

'''def add(request):
    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])
    res = val1 + val2
    print(request.POST)
    return render(request,'result.html',{'result':res})'''  
        
    #LINEPLOT
def line_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.lineplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'], 
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                            sort = dict_attr['sort'])
    
    
    print('YOUR PLOT IS CREATED!')

    return sns_plot
    
    #SCATTERPLOT
def scatter_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.scatterplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'],
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                              ) 
    
   
        
    print('YOUR PLOT IS CREATED!')
    return sns_plot

    #BOXPLOT
def box_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.boxplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'], 
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                            saturation = float(dict_attr['saturation']), orient = dict_attr['orient'],
                            )
    
    
    print('YOUR PLOT IS CREATED!')

    return sns_plot
    #BARPLOT
def bar_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.barplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'], 
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                            saturation = float(dict_attr['saturation']), orient = dict_attr['orient'],
                            )
    
    
    print('YOUR PLOT IS CREATED!')

    return sns_plot  
    #SWARMPLOT
def swarm_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.swarmplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'], 
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                            orient = dict_attr['orient'], dodge = dict_attr['dodge'], size = float(dict_attr['size']),
                            )
    
    
    print('YOUR PLOT IS CREATED!')

    return sns_plot   
    #RELPLOT
def rel_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.relplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'], 
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                            style = dict_attr['style2'], col = dict_attr['col'],row = dict_attr['row'],
                            kind = dict_attr['kind'],
                            )
    
    
    print('YOUR PLOT IS CREATED!')

    return sns_plot
    #PAIRPLOT
def pair_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.pairplot(data = dataset ,
                            vars = dict_attr['vars'], 
                            hue = dict_attr['hue'], palette = dict_attr['palette'],
                            kind = dict_attr['kind'], diag_kind = dict_attr['diag_kind'],
                            )
    
    
    print('YOUR PLOT IS CREATED!')

    return sns_plot   
    #DISPLOT
def dis_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.displot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'], 
                            hue = dict_attr['hue'], col = dict_attr['col'],row = dict_attr['row'], kind = dict_attr['kind'],
                            palette = dict_attr['palette'],
                            )
    
    
    print('YOUR PLOT IS CREATED!')

    return sns_plot
    #JOINTPLOT
def joint_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    sns_plot = sns.jointplot(data = dataset ,
                            x = dict_attr['x'], y = dict_attr['y'], 
                            hue = dict_attr['hue'], kind = dict_attr['kind'],
                            palette = dict_attr['palette'],
                            )
    
    
    print('YOUR PLOT IS CREATED!')

    return sns_plot
    
    #HEATMAP
def heat_map_plotter(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
    sns.set_theme(context = dict_attr['context'] , style = dict_attr['style'])
    print('\n\nWAIT...')
    #dataset = dataset.pivot(list(set(dataset[dict_attr['index']])),list(set(dataset[dict_attr['column']])), list(set(dataset[dict_attr['values']])))
    #dataset = dataset.pivot(list(set(dataset[dict_attr['index']])),list(set(dataset[dict_attr['column']])), list(set(dataset[dict_attr['values']])))
    sns_plot = sns.heatmap(data = dataset[[dict_attr['index'],dict_attr['column'],dict_attr['values']]],
     cmap = dict_attr['palette'],robust = dict_attr['robust'], vmin = dict_attr['vmin'],vmax = dict_attr['vmax'], linewidths = float(dict_attr['linewidths']),
     ) 
    
        
    print('YOUR PLOT IS CREATED!')
    return sns_plot
    
    #HISTOGRAM
def hist_plot(dataset,dict_attr):
    #  context must be in paper, notebook, talk, poster
    #  style must be in darkgrid, whitegrid, dark, white, ticks
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