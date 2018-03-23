import time
import datetime

import locale
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from .forms import SquidReportIndex, Login, PPTP
from .models import SquidFullData

# чтобы месяцы писались по-русски
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

# Main Page
def index(request):
    """
    Главная страница, только выводит меню и Сквидварда
    """
    return render(request, 'index.html')


@login_required
def report_index(request):
    """Тут можно выбрать вручную, какие даты нужны по всем
    юзерам, http://10.87.250.26/reports/
    """
    first_date = SquidFullData.objects.raw(
        '''SELECT 1 as id, coalesce(min(datetime), 0) as first
           FROM squidward_squidfulldata
        '''
    )
    last_date = SquidFullData.objects.raw(
        '''SELECT 1 as id, coalesce(max(datetime), 0) as last
    FROM squidward_squidfulldata
        '''
    )
    for raw in first_date:
        first_date = raw.first
    for raw in last_date:
        last_date = raw.last

    first_date = datetime.datetime.fromtimestamp(first_date).strftime('%d %b %Y')
    last_date = datetime.datetime.fromtimestamp(last_date).strftime('%d %b %Y')

    form = SquidReportIndex(request.POST, auto_id='id_%s')
    fromdate = form.fields['date_start']
    untildate = form.fields['date_stop']
    if request.method == 'POST':
        if form.is_valid():
            request.POST.get('')
            fromdate = request.POST.get('date_start')
            untildate = request.POST.get('date_stop')

            date_start = int(
                time.mktime(time.strptime(fromdate, "%m/%d/%Y")))
            date_stop = int(
                time.mktime(time.strptime(untildate, "%m/%d/%Y")))
            return HttpResponseRedirect(
                '/reports/manual/%s_%s/' % (date_start, date_stop)
                )
    form_fields = {'fromdate': fromdate, 'untildate': untildate, 'form': form,
                   'first_date': first_date, 'last_date': last_date}
    return render(request, 'report_index.html', form_fields)


@login_required
def report_manual(request, fromdate, untildate, user_ip=None):
    """
    Сюда перенаправляются данные, введенные из топов за
    неделю, месяц, вручную (без айпи адреса)
    Пример http://10.87.250.26/reports/manual/1518987600_1519506000/
    """
    fromdate, untildate, user_ip = int(fromdate), int(untildate) + 86400, str(user_ip)
    pptpip_sum = SquidFullData.objects.raw('''
      SELECT 1 as id, pptpip, trunc(sum(size)/1000000, 3) as sum
      FROM  squidward_squidfulldata
      WHERE datetime BETWEEN %s AND %s
      GROUP BY pptpip
      ORDER BY sum DESC''' % (fromdate, untildate))

    date_start = datetime.datetime.fromtimestamp(fromdate).strftime('%d %b %Y')
    date_stop = datetime.datetime.fromtimestamp(untildate).strftime('%d %b %Y')

    return render(request, 'report_manual.html', {'pptp_sum': pptpip_sum,
                                                  'date_start': date_start,
                                                  'date_stop': date_stop,
                                                  'fromdate': fromdate,
                                                  'untildate': untildate})


@login_required
def report_manual_user(request, fromdate, untildate, user_ip):
    """
    Сюда направляются данные, когда кликаешь по айпишнику в отчете,
    т.е. более детальная статистика по конкретному юзеру
    Пример http://10.87.250.26/reports/manual/1518987600_1519592400/172.20.10.20
    """
    fromdate, untildate, user_ip = int(fromdate), int(untildate), str(user_ip)
    try:
        pptpip_sum = SquidFullData.objects.raw('''
          SELECT 1 as id,
          pptpip, resource, trunc(sum(size)/1000000, 3) as sum
          FROM  squidward_squidfulldata
          WHERE datetime BETWEEN %d AND %d AND pptpip = '%s'
          GROUP BY pptpip, resource
          ORDER BY sum DESC''' % (fromdate, untildate, user_ip))

    except SquidFullData.DoesNotExist:
        raise Http404('Запись не существует')
    #locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    date_start = datetime.datetime.fromtimestamp(fromdate).strftime('%d %b %Y')
    date_stop = datetime.datetime.fromtimestamp(untildate).strftime('%d %b %Y')

    return render(request, 'report_manual_user.html', {'pptp_sum': pptpip_sum,
                                                        'user_ip': user_ip,
                                                       'date_start': date_start,
                                                       'date_stop': date_stop})






@login_required
def report_index_pptp(request):
    """
    Основная страница с вводом адреса и дат, редиректит
    на страницу с результатами
    Пример http://10.87.250.26/reports/pptp/
    """
    first_date = SquidFullData.objects.raw(
        '''SELECT 1 as id, coalesce(min(datetime), 0) as first
           FROM squidward_squidfulldata
        '''
    )
    last_date = SquidFullData.objects.raw(
        '''SELECT 1 as id, coalesce(max(datetime), 0) as last
    FROM squidward_squidfulldata
        '''
    )
    for raw in first_date:
        first_date = raw.first
    for raw in last_date:
        last_date = raw.last

    first_date = datetime.datetime.fromtimestamp(first_date).strftime('%d %b %Y')
    last_date = datetime.datetime.fromtimestamp(last_date).strftime('%d %b %Y')

    form = PPTP(request.POST, auto_id='id_%s')
    ipaddress = form.fields['ipaddress']
    fromdate = form.fields['date_start']
    untildate = form.fields['date_stop']
    if request.method == 'POST':
        if form.is_valid():
            request.POST.get('')
            fromdate = request.POST.get('date_start')
            untildate = request.POST.get('date_stop')
            ipaddress = request.POST.get('ipaddress')
            date_start = int(
                time.mktime(time.strptime(fromdate, "%m/%d/%Y")))
            date_stop = int(
                time.mktime(time.strptime(untildate, "%m/%d/%Y")))
            return HttpResponseRedirect(
                '/reports/pptp/%d_%d/%s' % (date_start, date_stop, ipaddress)
                )
    form_fields = {'ipaddress': ipaddress,'fromdate': fromdate,
                   'untildate': untildate, 'form': form,
                   'first_date': first_date, 'last_date': last_date}
    return render(request, 'report_index_pptp.html', form_fields)


@login_required
def pptp_manual_user(request, fromdate, untildate, user_ip):
    """

    """
    fromdate, untildate, user_ip = int(fromdate), int(untildate), str(user_ip)
    try:
        result = SquidFullData.objects.raw('''
        SELECT 1 as id,
        to_timestamp(squidward_whitetodb.datetime) as time,
        squidward_whitetodb.pptp_ip as white_ip,
        squidward_graytodb.pptp_ip as gray_ip
        FROM squidward_graytodb INNER JOIN squidward_whitetodb ON
        squidward_graytodb.pptp_id = squidward_whitetodb.pptp_id
        WHERE squidward_graytodb.datetime BETWEEN %d AND %d
        AND squidward_graytodb.pptp_ip = '%s'
        AND squidward_graytodb.datetime - squidward_whitetodb.datetime BETWEEN 1 AND 5
        ORDER by time
        ''' % (fromdate, untildate, user_ip))

    except SquidFullData.DoesNotExist:
        raise Http404('Запись не существует')
    #locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    date_start = datetime.datetime.fromtimestamp(fromdate).strftime('%d %b %Y')
    date_stop = datetime.datetime.fromtimestamp(untildate).strftime('%d %b %Y')
    # for row in result:
    #     human_dates.append(row.time)

    return render(request, 'report_manual_pptp.html', {'result': result,
                                                        'user_ip': user_ip,
                                                       'date_start': date_start,
                                                       'date_stop': date_stop})

@login_required
def report_top_week(request):
    """
    TOP 30 users-downloaders
    """
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    last_mon = today - datetime.timedelta(days=today.weekday(), weeks=1)
    last_mon = int(datetime.datetime.timestamp(last_mon))
    last_sun = last_mon + 6 * 86400


    return HttpResponseRedirect(
        '/reports/manual/%s_%s/' % (last_mon, last_sun)
    )


@login_required
def report_top_month(request):
    """
    TOP 30 users-downloaders
    """
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    last_mon = today - datetime.timedelta(days=today.weekday(), weeks=1)
    last_mon = int(datetime.datetime.timestamp(last_mon))
    day_month_ago = last_mon - 30 * 86400


    return HttpResponseRedirect(
        '/reports/manual/%s_%s/' % (day_month_ago, last_mon)
    )
