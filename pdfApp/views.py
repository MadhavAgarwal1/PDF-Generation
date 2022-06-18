from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

pathdir =os.getcwd()

def home(request):
    return render(request, 'home.html')

@api_view(['POST'])
def apicall(request):

    content= dict()
    if request.method == 'POST' :
        bodyField = request.POST.get('bodyField') 
        bodyFooter = request.POST.get('bodyFooter')
        viewMode = request.POST.get('mode')
        tabData = request.POST.get('tabData')
        pdfname = request.POST.get('pdfname')

        content['bodyField'] = bodyField
        content['bodyFooter'] = bodyFooter
        content['viewMode'] = viewMode
        content['tabData'] = tabData
        content['pdfname'] = pdfname

        from fpdf import FPDF

        body_content = bodyField
        body_footer = bodyFooter

        #table data
        data = []
        dataRows = tabData.split(";")
        for dataRow in dataRows:
            record = dataRow.split(",")
            data.append(record)
        
        def setupFun():
            pdf.alias_nb_pages()          
            pdf.set_auto_page_break(auto=True, margin=30)       
            pdf.add_page()
            pdf.set_margins(22,50,22)  
            pdf.set_font('helvetica', '', 11)   
            pdf.set_title("Demo Title")

        class PDF(FPDF):   

            def header(self):
                self.image(pathdir+'\pdfApp\static\DezHab_Logo.png', 30,6,20)
                self.set_font('helvetica', '',18)

               #for watermark 
                if viewMode == 'potrait':
                    self.image(pathdir+'\pdfApp\static\Reduced_Logo.png', 84,116,50)  
                if viewMode == 'landscape':
                    pdf.image(pathdir+'\pdfApp\static\Reduced_Logo.png', 114,80,50) 
            
                self.set_xy(50,18)    
                self.cell(145, 10, "DezHab Design and Construction", 0, 1)
                self.line(30,30, self.w - 24,30)   
                self.set_xy(22,40)    

            def footer(self):  
                self.set_xy(27,-20)
                self.set_font('helvetica', '', 11)
                self.line(28,self.get_y(), self.w - 24,self.get_y())       
                self.cell(0, 10,"P.O. Box Suite - 458, Office No - 15A, 4th Floor, A Building, City Vista, Kharadi, Pune 411014", 0, 1,'C')
                self.set_xy(27,-10)  
                self.cell(0, 4,"Website: www.dezhab.com", 0,1,'C')


        #set default as Potrait mode
        pdf = PDF('P', 'mm', 'Letter')
        setupFun()

        #for landscape orientation mode
        if viewMode == 'landscape':
            pdf = PDF('L', 'mm', 'Letter')
            setupFun()


        #variable  body content    
        pdf.multi_cell(0, 8, body_content, 0,'J', 0)  
        print("len is: ",data[0],len(data[0]))
        if len(data[0]) > 1:
            epw = pdf.w - 2*22
            line_height = pdf.font_size * 2.5
            col_width = epw / len(data[0])
            pdf.set_font('helvetica', 'BU', 11)   
            pdf.cell(0, pdf.font_size * 4.5, "TABLE", 0, 1, 'C')
            pdf.set_font('helvetica', '', 11)  

            for row in data:
                if (pdf.y + line_height > pdf.page_break_trigger):
                    for datum in data[0]:   
                        pdf.cell(col_width, line_height, datum,1,0,'C')         #table heading
                    pdf.ln(line_height)
                    if row == data[0]:
                        continue

                #if lesser or extra record is given
                if len(row) < len(data[0]): 
                    for rec in range( len(row), len(data[0]) ):
                        row.append("")   #set default value
                elif len(row) > len(data[0]):
                    for rec in range( len(data[0]), len(row)):
                        row.pop(rec)
                for datum in row:
                    pdf.cell(col_width, line_height, datum,1,0,'C')
                pdf.ln(line_height)

        #footer
        pdf.cell(0,40,body_footer, 0, 1)
        pdf.output(f'{pdfname}.pdf') 

    return Response({"status": 200 , "message": content})


    