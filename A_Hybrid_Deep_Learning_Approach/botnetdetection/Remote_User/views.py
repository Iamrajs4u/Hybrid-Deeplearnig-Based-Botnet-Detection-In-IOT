from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,bottleneck_detection,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def index(request):
    return render(request, 'RUser/index.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city,address=address,gender=gender)

        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html',{'object':obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_Attack_Type_Prediction(request):
    if request.method == "POST":

        if request.method == "POST":

            ID= request.POST.get('ID')
            Sender_IP= request.POST.get('Sender_IP')
            Sender_Port= request.POST.get('Sender_Port')
            Target_IP= request.POST.get('Target_IP')
            Target_Port= request.POST.get('Target_Port')
            Transport_Protocol= request.POST.get('Transport_Protocol')
            Duration= request.POST.get('Duration')
            AvgDuration= request.POST.get('AvgDuration')
            PBS= request.POST.get('PBS')
            AvgPBS= request.POST.get('AvgPBS')
            TBS= request.POST.get('TBS')
            PBR= request.POST.get('PBR')
            AvgPBR= request.POST.get('AvgPBR')
            TBR= request.POST.get('TBR')
            Missed_Bytes= request.POST.get('Missed_Bytes')
            Packets_Sent= request.POST.get('Packets_Sent')
            Packets_Received= request.POST.get('Packets_Received')
            SRPR= request.POST.get('SRPR')

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
        models.append(('SGDClassifier', sgd_clf))

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

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        ID1 = [ID]
        vector1 = cv.transform(ID1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if (prediction == 0):
            val = 'No Botnet Attack'
        elif (prediction == 1):
            val = 'Botnet Attack'

        print(val)
        print(pred1)

        bottleneck_detection.objects.create(
        ID1=ID,
        Sender_IP=Sender_IP,
        Sender_Port=Sender_Port,
        Target_IP=Target_IP,
        Target_Port=Target_Port,
        Transport_Protocol=Transport_Protocol,
        Duration=Duration,
        AvgDuration=AvgDuration,
        PBS=PBS,
        AvgPBS=AvgPBS,
        TBS=TBS,
        PBR=PBR,
        AvgPBR=AvgPBR,
        TBR=TBR,
        Missed_Bytes=Missed_Bytes,
        Packets_Sent=Packets_Sent,
        Packets_Received=Packets_Received,
        SRPR=SRPR,
        Prediction=val)

        return render(request, 'RUser/Predict_Attack_Type_Prediction.html',{'objs': val})
    return render(request, 'RUser/Predict_Attack_Type_Prediction.html')



