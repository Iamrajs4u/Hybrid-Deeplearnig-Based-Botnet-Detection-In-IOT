
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

# Create your views here.
from Remote_User.models import ClientRegister_Model,bottleneck_detection,detection_ratio,detection_accuracy


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            detection_accuracy.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def View_Prediction_Of_Attacker_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    ratio = ""
    kword = 'Botnet Attack'
    print(kword)
    obj = bottleneck_detection.objects.all().filter(Q(Prediction=kword))
    obj1 = bottleneck_detection.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)

    ratio12 = ""
    kword12 = 'No Botnet Attack'
    print(kword12)
    obj12 = bottleneck_detection.objects.all().filter(Q(Prediction=kword12))
    obj112 = bottleneck_detection.objects.all()
    count12 = obj12.count();
    count112 = obj112.count();
    ratio12 = (count12 / count112) * 100
    if ratio12 != 0:
        detection_ratio.objects.create(names=kword12, ratio=ratio12)


    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_Attacker_Type_Ratio.html', {'objs': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def View_Prediction_Of_Attacker_Type(request):
    obj =bottleneck_detection.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_Attacker_Type.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Predicted_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Predicted_Datasets.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = bottleneck_detection.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.ID1, font_style)
        ws.write(row_num, 1, my_row.Sender_IP, font_style)
        ws.write(row_num, 2, my_row.Sender_Port, font_style)
        ws.write(row_num, 3, my_row.Target_IP, font_style)
        ws.write(row_num, 4, my_row.Target_Port, font_style)
        ws.write(row_num, 5, my_row.Transport_Protocol, font_style)
        ws.write(row_num, 6, my_row.Duration, font_style)
        ws.write(row_num, 7, my_row.AvgDuration, font_style)
        ws.write(row_num, 8, my_row.PBS, font_style)
        ws.write(row_num, 9, my_row.AvgPBS, font_style)
        ws.write(row_num, 10, my_row.TBS, font_style)
        ws.write(row_num, 11, my_row.PBR, font_style)
        ws.write(row_num, 12, my_row.AvgPBR, font_style)
        ws.write(row_num, 13, my_row.TBR, font_style)
        ws.write(row_num, 14, my_row.Missed_Bytes, font_style)
        ws.write(row_num, 15, my_row.Packets_Sent, font_style)
        ws.write(row_num, 16, my_row.Packets_Received, font_style)
        ws.write(row_num, 17, my_row.SRPR, font_style)
        ws.write(row_num, 18, my_row.Prediction, font_style)

    wb.save(response)
    return response

def train_model(request):
    detection_accuracy.objects.all().delete()

    df = pd.read_csv('Datasets.csv')

    def apply_response(Label):
        if (Label == 0):
            return 0  # No Botnet Attack
        elif (Label == 1):
            return 1  # Botnet Attack

    df['Results'] = df['class'].apply(apply_response)

    cv = CountVectorizer()
    X = df['ID'].apply(str)
    y = df['Results']

    print("ID")
    print(X)
    print("Results")
    print(y)

    X = cv.fit_transform(X)

    models = []
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    X_train.shape, X_test.shape, y_train.shape

    print(X_test)

    print("SGD Classifier")

    from sklearn.linear_model import SGDClassifier
    sgd_clf = SGDClassifier(loss='hinge', penalty='l2', random_state=0)
    sgd_clf.fit(X_train, y_train)
    sgdpredict = sgd_clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, sgdpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, sgdpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, sgdpredict))
    detection_accuracy.objects.create(names="SGD Classifier", ratio=accuracy_score(y_test, sgdpredict) * 100)

    print("Gradient Boosting Classifier")

    from sklearn.ensemble import GradientBoostingClassifier
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(
        X_train,
        y_train)
    clfpredict = clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, clfpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, clfpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, clfpredict))
    models.append(('GradientBoostingClassifier', clf))
    detection_accuracy.objects.create(names="Gradient Boosting Classifier",ratio=accuracy_score(y_test, clfpredict) * 100)

    print("DEEP NEURAL NETWORK(DNN)")
    print("MLP Classifier")
    from sklearn.neural_network import MLPClassifier
    mlpc = MLPClassifier().fit(X_train, y_train)
    y_pred = mlpc.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, y_pred) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))
    models.append(('MLPClassifier', mlpc))
    detection_accuracy.objects.create(names="MLPClassifier-DEEP NEURAL NETWORK(DNN)",ratio=accuracy_score(y_test, y_pred) * 100)


    csv_format = 'Results.csv'
    df.to_csv(csv_format, index=False)
    df.to_markdown

    obj = detection_accuracy.objects.all()
    return render(request,'SProvider/train_model.html', {'objs': obj})