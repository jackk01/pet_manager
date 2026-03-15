from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.system_config import SystemConfig
from app.models.user import User


def init_db() -> None:
    """
    初始化数据库基础数据
    """
    db = SessionLocal()

    try:
        # 初始化系统配置
        init_system_config(db)

        # 初始化默认管理员用户（开发环境）
        if settings.DEBUG:
            init_default_user(db)

    except Exception as e:
        db.rollback()
        print(f"数据库初始化失败: {e}")
    finally:
        db.close()


def init_system_config(db: Session) -> None:
    """
    初始化系统配置数据
    """
    # 预设疫苗列表
    vaccine_config = db.query(SystemConfig).filter(SystemConfig.config_key == "vaccine_list").first()
    if not vaccine_config:
        default_vaccines = [
            "狂犬疫苗", "犬三联疫苗", "犬五联疫苗", "犬六联疫苗", "犬八联疫苗",
            "猫三联疫苗", "猫四联疫苗", "弓形虫疫苗", "钩端螺旋体疫苗", "支气管炎博德特菌疫苗"
        ]
        db_obj = SystemConfig(
            config_key="vaccine_list",
            config_value=",".join(default_vaccines),
            description="预设疫苗列表"
        )
        db.add(db_obj)
    
    # 消费分类配置
    expense_category_config = db.query(SystemConfig).filter(SystemConfig.config_key == "expense_categories").first()
    if not expense_category_config:
        default_categories = [
            {"value": "food", "label": "食品", "icon": "Food"},
            {"value": "medical", "label": "医疗", "icon": "Medical"},
            {"value": "grooming", "label": "美容", "icon": "Scissors"},
            {"value": "supplies", "label": "用品", "icon": "Box"},
            {"value": "insurance", "label": "保险", "icon": "Ticket"},
            {"value": "other", "label": "其他", "icon": "MoreFilled"}
        ]
        import json
        db_obj = SystemConfig(
            config_key="expense_categories",
            config_value=json.dumps(default_categories, ensure_ascii=False),
            description="消费分类配置"
        )
        db.add(db_obj)
    
    # 健康记录类型配置
    health_record_type_config = db.query(SystemConfig).filter(SystemConfig.config_key == "health_record_types").first()
    if not health_record_type_config:
        default_types = [
            {"value": "visit", "label": "就诊", "icon": "Hospital"},
            {"value": "weight", "label": "体重记录", "icon": "Scale"},
            {"value": "deworming", "label": "驱虫", "icon": "Bug"},
            {"value": "allergy", "label": "过敏记录", "icon": "Warning"},
            {"value": "surgery", "label": "手术", "icon": "Operation"},
            {"value": "other", "label": "其他", "icon": "MoreFilled"}
        ]
        import json
        db_obj = SystemConfig(
            config_key="health_record_types",
            config_value=json.dumps(default_types, ensure_ascii=False),
            description="健康记录类型配置"
        )
        db.add(db_obj)
    
    db.commit()


def init_default_user(db: Session) -> None:
    """
    初始化默认测试用户
    """
    default_user = db.query(User).filter(User.username == "admin").first()
    if not default_user:
        user = User(
            username="admin",
            email="admin@example.com",
            password_hash=get_password_hash("123456"),
            nickname="管理员",
            is_active=True
        )
        db.add(user)
        db.commit()
        print("默认测试用户已创建: admin / 123456")
