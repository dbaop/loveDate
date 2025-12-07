from app.models.feedback import Feedback
from app.models.order import Order, OrderStatus
from app.models.user import User
from app.models.therapist import Therapist
from app import db
from sqlalchemy import func


class FeedbackService:
    @staticmethod
    def create_feedback(user_id, order_id, data):
        """创建评价"""
        # 验证订单
        order = Order.query.filter_by(id=order_id, user_id=user_id, status=OrderStatus.COMPLETED).first()
        if not order:
            raise Exception("订单不存在或未完成，无法评价")

        # 检查是否已经评价过
        existing_feedback = Feedback.query.filter_by(order_id=order_id).first()
        if existing_feedback:
            raise Exception("该订单已经评价过")

        # 验证评分范围
        rating = data.get('rating')
        if not rating or rating < 1 or rating > 5:
            raise Exception("评分必须在1-5分之间")

        # 创建评价
        feedback = Feedback(
            order_id=order_id,
            user_id=user_id,
            therapist_id=order.therapist_id,
            rating=rating,
            content=data.get('content'),
            tags=','.join(data.get('tags', [])) if data.get('tags') else None
        )

        # 更新技师的平均评分
        therapist = Therapist.query.get(order.therapist_id)
        if therapist:
            # 计算新的平均评分
            avg_rating = db.session.query(func.avg(Feedback.rating)).filter_by(therapist_id=order.therapist_id).scalar() or 0
            therapist.rating = round(float(avg_rating), 1) if avg_rating else 0

        db.session.add(feedback)
        db.session.commit()
        return feedback

    @staticmethod
    def get_therapist_feedbacks(therapist_id, page, size):
        """获取技师的评价列表"""
        # 验证技师存在
        therapist = Therapist.query.get(therapist_id)
        if not therapist:
            raise Exception("技师不存在")

        # 查询评价并分页
        query = Feedback.query.filter_by(therapist_id=therapist_id)
        query = query.order_by(Feedback.created_at.desc())  # 按时间倒序
        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'size': size
        }

    @staticmethod
    def get_feedback_detail(feedback_id):
        """获取评价详情"""
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            raise Exception("评价不存在")
        return feedback

    @staticmethod
    def update_feedback(user_id, feedback_id, data):
        """更新评价（可选，可限制时间）"""
        feedback = Feedback.query.filter_by(id=feedback_id, user_id=user_id).first()
        if not feedback:
            raise Exception("评价不存在或无权限修改")

        # 这里可以添加时间限制，例如只能在评价后24小时内修改
        # import datetime
        # if (datetime.datetime.now() - feedback.created_at).days > 0:
        #     raise Exception("评价已超过修改期限")

        # 更新评价内容
        if 'rating' in data:
            rating = data['rating']
            if rating < 1 or rating > 5:
                raise Exception("评分必须在1-5分之间")
            feedback.rating = rating

        if 'content' in data:
            feedback.content = data['content']

        if 'tags' in data:
            feedback.tags = ','.join(data['tags']) if data['tags'] else None

        # 更新技师的平均评分
        therapist = Therapist.query.get(feedback.therapist_id)
        if therapist:
            avg_rating = db.session.query(func.avg(Feedback.rating)).filter_by(therapist_id=feedback.therapist_id).scalar() or 0
            therapist.rating = round(float(avg_rating), 1) if avg_rating else 0

        db.session.commit()
        return feedback

    @staticmethod
    def delete_feedback(user_id, feedback_id):
        """删除评价（需要权限控制）"""
        feedback = Feedback.query.filter_by(id=feedback_id, user_id=user_id).first()
        if not feedback:
            raise Exception("评价不存在或无权限删除")

        # 先获取技师ID，用于后续更新评分
        therapist_id = feedback.therapist_id

        # 删除评价
        db.session.delete(feedback)

        # 更新技师的平均评分
        therapist = Therapist.query.get(therapist_id)
        if therapist:
            avg_rating = db.session.query(func.avg(Feedback.rating)).filter_by(therapist_id=therapist_id).scalar() or 0
            therapist.rating = round(float(avg_rating), 1) if avg_rating else 0

        db.session.commit()
        return True

    @staticmethod
    def get_user_feedbacks(user_id, page, size):
        """获取用户的评价历史"""
        query = Feedback.query.filter_by(user_id=user_id)
        query = query.order_by(Feedback.created_at.desc())
        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'size': size
        }