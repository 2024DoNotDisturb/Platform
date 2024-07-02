from flask import Blueprint, jsonify, request, current_app
from model.model import db, AIServices, UserServices, ServiceUsage, User
from sqlalchemy import func, case
from datetime import datetime, timedelta

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/api/services')
def get_services():
    services = AIServices.query.all()
    return jsonify([{'ServiceID': s.ServiceID, 'ServiceName': s.ServiceName} for s in services])

@dashboard.route('/api/subscription-data')
def get_subscription_data():
    service_name = request.args.get('serviceName')
    days = request.args.get('days', default=30, type=int)

    if not service_name:
        return jsonify({'error': 'Missing service name'}), 400

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    query = db.session.query(
        func.date(UserServices.SubscriptionDate).label('date'),
        func.sum(case((UserServices.Status == 'active', 1), else_=0)).label('active'),
        func.sum(case((UserServices.Status == 'inactive', 1), else_=0)).label('inactive'),
        func.sum(case((UserServices.Status == 'canceled', 1), else_=0)).label('canceled')
    ).join(AIServices
    ).filter(
        AIServices.ServiceName == service_name,
        UserServices.SubscriptionDate.between(start_date, end_date)
    ).group_by(
        func.date(UserServices.SubscriptionDate)
    ).order_by(
        func.date(UserServices.SubscriptionDate)
    )

    results = query.all()

    return jsonify([{
        'date': result.date.strftime('%Y-%m-%d'),
        'active': result.active,
        'inactive': result.inactive,
        'canceled': result.canceled
    } for result in results])

@dashboard.route('/api/daily-active-users')
def get_daily_active_users():
    today = datetime.now().date()
    
    active_users = db.session.query(func.count(func.distinct(ServiceUsage.UserID))).filter(
        func.date(ServiceUsage.UsageDate) == today
    ).scalar()

    total_users = db.session.query(func.count(User.UserID)).scalar()

    active_user_ratio = (active_users / total_users) if total_users > 0 else 0

    return {
        'date': today.isoformat(),
        'active_users': active_users,
        'total_users': total_users,
        'active_user_ratio': active_user_ratio
    }

@dashboard.route('/api/daily-service-usage')
def get_daily_service_usage():
    # 오늘 날짜 계산
    today = datetime.now().date()
    
    # 최근 7일간의 데이터를 가져오기 위한 시작 날짜 계산
    start_date = today - timedelta(days=6)

    # 로봇과 루틴 서비스의 ID 가져오기
    robot_service = AIServices.query.filter_by(ServiceName='Robot').first()
    routine_service = AIServices.query.filter_by(ServiceName='SmartRoutine').first()

    if not robot_service or not routine_service:
        return jsonify({'error': 'Services not found'}), 404

    # 각 서비스별 일일 사용량 쿼리
    usage_data = db.session.query(
        func.date(ServiceUsage.UsageDate).label('date'),
        AIServices.ServiceName,
        func.sum(ServiceUsage.UsageAmount).label('total_usage')
    ).join(AIServices).filter(
        ServiceUsage.UsageDate >= start_date,
        AIServices.ServiceID.in_([robot_service.ServiceID, routine_service.ServiceID])
    ).group_by(
        func.date(ServiceUsage.UsageDate),
        AIServices.ServiceName
    ).order_by(
        func.date(ServiceUsage.UsageDate)
    ).all()

    # 결과를 날짜별로 정리
    result = {}
    for usage in usage_data:
        date_str = usage.date.isoformat()
        if date_str not in result:
            result[date_str] = {'Robot': 0, 'SmartRoutine': 0}
        result[date_str][usage.ServiceName] = usage.total_usage

    # 결과를 리스트 형태로 변환
    formatted_result = [
        {
            'date': date,
            'Robot': data['Robot'],
            'SmartRoutine': data['SmartRoutine']
        } for date, data in result.items()
    ]

    return jsonify(formatted_result)

from sqlalchemy import func

@dashboard.route('/api/age-distribution')
def get_age_distribution():
    try:
        current_date = datetime.now().date()
        age_groups = [
            (0, 18), (19, 24), (25, 34), (35, 44),
            (45, 54), (55, 64), (65, float('inf'))
        ]
        
        distribution = []
        total_count = 0

        for start, end in age_groups:
            count = db.session.query(func.count(User.UserID)).filter(
                User.DateOfBirth.isnot(None),
                func.year(func.current_date()) - func.year(User.DateOfBirth) >= start,
                func.year(func.current_date()) - func.year(User.DateOfBirth) <= (end if end != float('inf') else 200)
            ).scalar()
            
            label = f"{start}-{end if end != float('inf') else '+'}"
            distribution.append({"age_group": label, "count": count})
            total_count += count

        if total_count == 0:
            return jsonify({
                "message": "No data available",
                "distribution": [{"age_group": label, "count": 0} for start, end in age_groups for label in [f"{start}-{end if end != float('inf') else '+'}"]]
            }), 204
        else:
            return jsonify(distribution)

    except Exception as e:
        dashboard.logger.error(f"Error in get_age_distribution: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard.route('/')
def dashboard_page():
    return current_app.send_static_file('dashboard.html')