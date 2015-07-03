# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:14:39 2015

@author: christina
"""

# interface for creating PDF files

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os


def generate_pdf(solver_name, meta, incumbent, test_perf, training_perf, param_imp_def, param_imp_not, plots, out_dir):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(os.path.join(out_dir, "index.pdf"))
    
    # Header
    title = Paragraph("Spying on %s" %(solver_name), styles["Heading1"])
    authors = Paragraph("S. Falkner, M. Lindauer and F. Hutter", styles["Normal"])
    URL = Paragraph( "Generated by <a href=\"https://github.com/sfalkner/SpySMAC\"> SpySMAC </a>", styles["Normal"])
    
    # final config
    f_config = Paragraph("Final Configuration", styles["Heading3"])
    config = Paragraph("%s" %(" ".join("%s=%s" %(key, value) for key, 
                                       value in list(incumbent.items()))), styles["Normal"])
    
    #write meta data
    meta_data_header = Paragraph("Meta Data", styles["Heading3"])
    data = [['Solver', solver_name]]
    for key, value in meta:
        data.append([key, value])
    meta_data = Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1,
                      repeatRows=0, repeatCols=0)
    meta_data.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)]))
    
    
    #  write Performance overview
    perf_overview = Paragraph("Performance Overview", styles["Heading3"])
    test_p = Paragraph("Test Performance", styles["Normal"])
    data1 = [[' ', 'Default', 'Configured'],
             ['Average Runtime', '%.2f'%(test_perf["base"]["par1"]), '%.2f'%(test_perf["conf"]["par1"])],
             ['Par10', '%.2f'%(test_perf["base"]["par10"]), '%.2f'%(test_perf["conf"]["par10"])],
             ['Timeouts', '%s/%s'%(test_perf["base"]["tos"], test_perf["n"]), '%s/%s'%(test_perf["conf"]["tos"], test_perf["n"])]]
    test_table = Table(data1, colWidths=None, rowHeights=None, style=None, splitByRow=1,
                      repeatRows=0, repeatCols=0)
    test_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)]))
                      
    train_p = Paragraph("Training Performance", styles["Normal"])
    data2 = [[' ', 'Default', 'Configured'],
             ['Average Runtime', '%.2f'%(training_perf["base"]["par1"]), '%.2f'%(training_perf["conf"]["par1"])],
             ['Par10', '%.2f'%(training_perf["base"]["par10"]), '%.2f'%(training_perf["conf"]["par10"])],
             ['Timeouts', '%s/%s'%(training_perf["base"]["tos"], test_perf["n"]), '%s/%s'%(training_perf["conf"]["tos"], test_perf["n"])]]
    training_table = Table(data2, colWidths=None, rowHeights=None, style=None, splitByRow=1,
                      repeatRows=0, repeatCols=0)
    training_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)]))
    
    # Scatter Plot
    scatterp_h = Paragraph("Scatter Plot", styles["Heading3"])
    test_inst = Image(os.path.join(out_dir,plots["scatter"]["test"]), width=250, height=250)
    train_inst = Image(os.path.join(out_dir,plots["scatter"]["train"]), width=250, height=250)
    data3 = [[test_inst, train_inst]]
    scatter_table = Table(data3, colWidths=None, rowHeights=None, style=None, splitByRow=1,
                      repeatRows=0, repeatCols=0 )
    
    # Summing up                 
    Elements =[title, authors, URL, f_config, config, meta_data_header, 
               meta_data, perf_overview, test_p, test_table, train_p, 
               training_table, scatterp_h, scatter_table]
               
    # CDF Plot
    cdf_h = Paragraph("CDF Plot", styles["Heading3"])
    Elements.append(cdf_h)
    cdf_test_inst = Image(os.path.join(out_dir,plots["cdf"]["test"]), width=250, height=250)
    cdf_train_inst = Image(os.path.join(out_dir,plots["cdf"]["train"]), width=250, height=250)
    data4 = [[cdf_test_inst, cdf_train_inst]]
    cdf_table = Table(data4, colWidths=None, rowHeights=None, style=None, splitByRow=1,
                      repeatRows=0, repeatCols=0 )
    Elements.append(cdf_table)
    
    # Cactus Plot
    cactus_h = Paragraph("Cactus Plot", styles["Heading3"])
    Elements.append(cactus_h)
    cactus_test_inst = Image(os.path.join(out_dir,plots["cactus"]["test"]), width=250, height=250)
    cactus_train_inst = Image(os.path.join(out_dir,plots["cactus"]["train"]), width=250, height=250)
    data5 = [[cactus_test_inst, cactus_train_inst]]
    cactus_table = Table(data5, colWidths=None, rowHeights=None, style=None, splitByRow=1,
                      repeatRows=0, repeatCols=0 )
    Elements.append(cactus_table)

    doc.build(Elements) 

