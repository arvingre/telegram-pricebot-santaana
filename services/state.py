# 分页用的用户状态缓存：user_id -> (page_number, category_filter)
user_page_state = {}

# 下单会话缓存：user_id -> {'product': str, 'quantity': int, 'step': str}
user_order_state = {}