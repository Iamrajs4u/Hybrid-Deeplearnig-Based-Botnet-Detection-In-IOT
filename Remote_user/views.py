from django.shortcuts import render, redirect
from django.db.models import Q
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier, VotingClassifier
from .models import ClientRegister_Model, bottleneck_detection, detection_accuracy

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username, password=password)
            request.session["userid"] = enter.id
            return redirect('ViewYourProfile')
        except:
            pass
    return render(request, 'Remote_User/login.html')

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
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'Remote_User/Register1.html', {'object': obj})
    else:
        return render(request, 'Remote_User/Register1.html')

def Predict_Attack_Type_Prediction(request):
    if request.method == "POST":
        ID = request.POST.get('ID')
        Sender_IP = request.POST.get('Sender_IP')
        Sender_Port = request.POST.get('Sender_Port')
        Target_IP = request.POST.get('Target_IP')
        Target_Port = request.POST.get('Target_Port')
        Transport_Protocol = request.POST.get('Transport_Protocol')
        Duration = request.POST.get('Duration')
        AvgDuration = request.POST.get('AvgDuration')
        PBS = request.POST.get('PBS')
        AvgPBS = request.POST.get('AvgPBS')
        TBS = request.POST.get('TBS')
        PBR = request.POST.get('PBR')
        AvgPBR = request.POST.get('AvgPBR')
        TBR = request.POST.get('TBR')
        Missed_Bytes = request.POST.get('Missed_Bytes')
        Packets_Sent = request.POST.get('Packets_Sent')
        Packets_Received = request.POST.get('Packets_Received')
        SRPR = request.POST.get('SRPR')

        df = pd.read_csv('Datasets/Datasets.csv')

        def apply_response(Label):
            if Label == 0:
                return 0  # No Botnet Attack
            elif Label == 1:
                return 1  # Botnet Attack

        df['Results'] = df['class'].apply(apply_response)

        cv = CountVectorizer()
        X = df['ID'].apply(str)
        y = df['Results']

        X = cv.fit_transform(X)

        models = []
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

        # SGD Classifier
        sgd_clf = SGDClassifier(loss='hinge', penalty='l2', random_state=0)
        sgd_clf.fit(X_train, y_train)
        sgdpredict = sgd_clf.predict(X_test)
        models.append(('SGDClassifier', sgd_clf))

        # Gradient Boosting Classifier
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
        clf.fit(X_train, y_train)
        clfpredict = clf.predict(X_test)
        models.append(('GradientBoostingClassifier', clf))

        # MLP Classifier (DNN)
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        models.append(('MLPClassifier', mlpc))

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        ID1 = [ID]
        vector1 = cv.transform(ID1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "").replace("]", "")
        prediction = int(pred)

        if prediction == 0:
            val = 'No Botnet Attack'
        elif prediction == 1:
            val = 'Botnet Attack'

        bottleneck_detection.objects.create(
            ID1=ID, Sender_IP=Sender_IP, Sender_Port=Sender_Port, Target_IP=Target_IP, Target_Port=Target_Port,
            Transport_Protocol=Transport_Protocol, Duration=Duration, AvgDuration=AvgDuration, PBS=PBS, AvgPBS=AvgPBS,
            TBS=TBS, PBR=PBR, AvgPBR=AvgPBR, TBR=TBR, Missed_Bytes=Missed_Bytes, Packets_Sent=Packets_Sent,
            Packets_Received=Packets_Received, SRPR=SRPR, Prediction=val
        )

        return render(request, 'Remote_User/Predict_Attack_Type_Prediction.html', {'objs': val})
    return render(request, 'Remote_User/Predict_Attack_Type_Prediction.html')