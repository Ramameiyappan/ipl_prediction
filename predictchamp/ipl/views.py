from django.shortcuts import render,redirect
from .models import pointtb, matches, playoff

def predict(request):
    team = pointtb.objects.all()
    try:
        match = matches.objects.filter(winner__isnull=True)[0]
        matchno = matches.objects.filter(winner__isnull=False)
        return render(request,'predict.html',{'team':team, 'match':match, 'matno':matchno})
    except:
        return redirect('playoff_view')

def updatetb(request,win,loss,no,tie):
    winner = pointtb.objects.get(team=win)
    loser = pointtb.objects.get(team=loss)
    match = matches.objects.get(no=no)

    winner.matches += 1
    loser.matches += 1

    if tie:
        winner.tie += 1
        winner.point += 1
        loser.tie += 1
        loser.point += 1
        match.tie = 'tie'
        match.winner = 'both'
    else:    
        winner.win += 1
        winner.point += 2
        loser.loss += 1
        match.winner = win
        match.looser = loss
    winner.save()
    loser.save()
    match.save()

    return redirect('predict_view')

def reset(request):
    match = matches.objects.all()
    for i in match:
        if i.winner == None:
            break
        
        if i.tie != 'No':
            winner = pointtb.objects.get(team=i.home)
            loser = pointtb.objects.get(team=i.away)
            winner.tie -= 1
            winner.point -= 1
            loser.tie -= 1
            loser.point -= 1
        else:
            winner = pointtb.objects.get(team=i.winner)
            loser = pointtb.objects.get(team=i.looser)
            winner.win -= 1
            winner.point -= 2
            loser.loss -= 1

        winner.matches -= 1
        loser.matches -= 1
        
        i.winner = None
        i.looser = None
        i.tie = 'No'

        i.save()
        winner.save()
        loser.save()

    playoff.objects.all().delete()
    return redirect('predict_view')

def matchreset(request,mno):
    match = matches.objects.filter(no=mno)[0]

    if match.tie != 'No':
        winner = pointtb.objects.get(team=match.home)
        loser = pointtb.objects.get(team=match.away)
        winner.tie -= 1
        winner.point -= 1
        loser.tie -= 1
        loser.point -= 1
    else:
        winner = pointtb.objects.get(team=match.winner)
        loser = pointtb.objects.get(team=match.looser)
        winner.win -= 1
        winner.point -= 2
        loser.loss -= 1

    winner.matches -= 1
    loser.matches -= 1

    match.winner = None
    match.looser = None
    match.tie = 'No'

    match.save()
    winner.save()
    loser.save()

    return redirect('predict_view')

def playoff_v(request):
    team = pointtb.objects.all()
    check = playoff.objects.count()
    check2 = playoff.objects.last()
    msg = 'Predict the Winner'
    if check==0:
        top4 = pointtb.objects.all()[:2]
        m1 = playoff.objects.create(no=1,team1=top4[0].team,team2=top4[1].team)
        msg = 'Prediction for Semifinal 1'
    elif check==1 and check2 and check2.winner:
        top4 = pointtb.objects.all()[2:4]
        m2 = playoff.objects.create(no=2,team1=top4[0].team,team2=top4[1].team)
        msg = 'Prediction for Eliminator'
    elif check==2 and check2 and check2.winner: 
        top2 = playoff.objects.all()[:2]
        m3 = playoff.objects.create(no=3,team1=top2[0].looser,team2=top2[1].winner)
        msg = 'Prediction for Semifinal 2'
    elif check==3 and check2 and check2.winner:
        top1 = playoff.objects.all()[:3]
        m4 = playoff.objects.create(no=4,team1=top1[0].winner,team2=top1[2].winner)
        msg = 'Prediction for Final'
    elif check==4:
        winner = playoff.objects.get(no=4).winner
        return render(request,'champion.html',{'team':team,'win':winner})
    match = playoff.objects.filter(winner__isnull=True).first()
    return render(request,'final.html',{'team':team, 'match':match, 'msg':msg}) 
       

def updateplaytb(request,win,loss):
    match = playoff.objects.filter(winner__isnull=True).first()
    match.winner = win
    match.looser = loss
    match.save()
    return redirect('playoff_view') 

def playreset(request):
    playoff.objects.all().delete()
    return redirect('predict_view')
