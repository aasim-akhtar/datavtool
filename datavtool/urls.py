from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.index,name = 'index'),
    path('line_scatter_plot',views.line_scatter_plot,name = 'line_scatter_plot'),
    path('line_scatter_process',views.line_scatter_process,name = 'line_scatter_process'),
    path('box_plot',views.box_plot,name = 'box_plot'),
    path('box_plot_process',views.box_plot_process,name = 'box_plot_process'),
    path('bar_plot',views.bar_plot,name = 'bar_plot'),
    path('bar_plot_process',views.bar_plot_process,name = 'bar_plot_process'),
    path('rel_plot',views.rel_plot,name = 'rel_plot'),
    path('rel_plot_process',views.rel_plot_process,name = 'rel_plot_process'),
    path('swarm_plot',views.swarm_plot,name = 'swarm_plot'),
    path('swarm_plot_process',views.swarm_plot_process,name = 'swarm_plot_process'),
    path('dis_plot',views.dis_plot,name = 'dis_plot'),
    path('dis_plot_process',views.dis_plot_process,name = 'dis_plot_process'),
    path('pair_plot',views.pair_plot,name = 'pair_plot'),
    path('pair_plot_process',views.pair_plot_process,name = 'pair_plot_process'),
    path('joint_plot',views.joint_plot,name = 'joint_plot'),
    path('joint_plot_process',views.joint_plot_process,name = 'joint_plot_process'),
    path('heat_map',views.heat_map,name = 'heat_map'),
    path('heat_map_process',views.heat_map_process,name = 'heat_map_process'),
    path('fileupload', views.fileupload, name = 'fileupload'),
    path('fileupload_process',views.fileupload_process,name = 'fileupload_process'),

]
