"""celery配置"""
from celery.schedules import crontab

from conf.settings import CELERY_REDIS_SETTINGS

# from kombu import Queue, Exchange
timezone = 'Asia/Shanghai'
task_serializer = 'json'  # 指定序列化方式
accept_content = ['json']  # 指定任务接受的序列化类型
task_ignore_result = False  
result_serializer = 'json'  # 指定结果序列化方式

# Broker 任务队列中间人
broker_url = 'redis://:%s@%s:%s/%s' % (CELERY_REDIS_SETTINGS['password'], CELERY_REDIS_SETTINGS['host'],
                                       CELERY_REDIS_SETTINGS['port'], CELERY_REDIS_SETTINGS['db'])
# broker_url = 'redis://:@127.0.0.1:6379/8'
redis_max_connections = 5

task_create_missing_queues = True  # 某个程序中出现的队列，在broker中不存在，则立刻创建它
worker_max_tasks_per_child = 1000  # 每个worker执行了多少任务就会死掉
task_default_queue = 'default'

beat_schedule = {
    'live_room_task': {
        'task': 'tasks.live_room_task.check_live_room_mic_user_alive',
        'schedule': 5,
    },
    'team_room_task': {
        'task': 'tasks.team_room_task.clear_all_offline_team',
        'schedule': 5,
    },
    'clear_negative_team_leader': {
        'task': 'tasks.team_room_task.clear_negative_team_leader',
        'schedule': 600,
    },
    'clear_all_offline_together_room': {
        'task': 'tasks.together_room_task.clear_all_offline_together_room',
        'schedule': 600,
    },
    'record_together_room_grab_status': {
        'task': 'tasks.together_room_task.record_together_room_grab_status',
        'schedule': 5,
    },
    'clear_inactive_guild_user': {
        'task': 'tasks.group_task.clear_inactive_guild_user',
        'schedule': crontab(minute='0', hour='4'),
    },
    'delete_audio_video_record': {
        'task': 'tasks.team_room_task.delete_audio_video_record',
        'schedule': 3600,
    },
    'clear_all_offline_couple_room': {
        'task': 'tasks.couple_room_task.clear_all_offline_couple_room',
        'schedule': 600,
    },
    'update_cp_room_online_user_cnt': {
        'task': 'tasks.couple_room_task.update_cp_room_online_user_cnt',
        'schedule': 60,
    },
    'record_user_active_time_task': {
        'task': 'tasks.active_task.record_user_active_time_task',
        'schedule': 3600,
    },
    'clear_inactive_user_time_task': {
        'task': 'tasks.active_task.clear_inactive_user_time_task',
        'schedule': crontab(minute='20', hour='4'),
    },
    'expire_cartoon_suit_current': {
        'task': 'tasks.cartoon_task.expire_cartoon_suit_current',
        'schedule': 60,
    },
    'check_msg_reply_timeout_task': {
        'task': 'tasks.msg_check_task.check_msg_reply_timeout_task',
        'schedule': 60,
    },
    'cancel_quick_match_order': {
        'task': 'tasks.quick_match_task.cancel_quick_match_order',
        'schedule': 300,
    },
    'deal_couple_room_statement_time_out': {
        'task': 'tasks.couple_room_task.deal_couple_room_statement_time_out',
        'schedule': 60,
    },
    # 'reset_diversion_card': {
    #     'task': 'tasks.diversion_card_task.reset_diversion_card',
    #     'schedule': crontab(hour='0', minute='1')
    # },
    'make_fake_boost_reward_cache': {
        'task': 'tasks.couple_room_task.make_fake_boost_reward_cache',
        'schedule': crontab(hour='1', minute='30')
    },
    'anchor_task_month_task': {
        'task': 'tasks.anchor_task.anchor_task_month_task',
        'schedule': crontab(hour='5', minute='1')
    },
    'clear_family_offline': {
        'task': 'tasks.family_task.clear_family_offline',
        'schedule': 300
    },
    'clear_family_team_offline': {
        'task': 'tasks.family_task.clear_family_team_offline',
        'schedule': 300
    },
    'clear_family_game_team_nobody': {
        'task': 'tasks.family_task.clear_family_game_team_nobody',
        'schedule': 300
    },
    'clear_family_switch_record_status': {
        'task': 'tasks.family_task.clear_family_switch_record_status',
        'schedule': 3600
    },
    'clear_family_and_family_team_daliy': {
        'task': 'tasks.family_task.clear_family_and_family_team_daliy',
        'schedule': crontab(hour='23', minute='55')
    },
    'family_rank_refresh_task': {
        'task': 'tasks.family_task.family_rank_refresh_task',
        'schedule': crontab(hour='0', minute='1')
    },
    'near_invite_task': {
        'task': 'tasks.invite_task.near_invite_task',
        'schedule': 60,
    },
    # 'every_thirty_second_invite_task': {
    #     'task': 'tasks.invite_task.every_thirty_second_invite_task',
    #     'schedule': 30,
    # },
    'update_members_task': {
        'task': 'tasks.couple_room_task.update_members_task',
        'schedule': 120,
    },
    'balance_monitor': {
        'task': 'tasks.pay_task.balance_monitor',
        'schedule': 300,
    },
    'clear_voice_chatting_task': {
        'task': 'tasks.couple_room_task.clear_voice_chatting_task',
        'schedule': 60,
    },
    # 'send_only_cp_msg': {
    #     'task': 'tasks.only_cp_msg.send_only_cp_msg',
    #     'schedule': crontab(minute='10', hour='9'),
    # },
    'retry_huifu_payment': {
        'task': 'tasks.pay_task.retry_huifu_payment',
        'schedule': crontab(minute='0', hour='5,15,19'),
    },
    'only_cp_keep_judge': {
        'task': 'tasks.only_cp_keep_task.only_cp_keep_judge',
        'schedule': crontab(hour='0', minute='2')
    },
    'clear_cold_col_data': {
        'task': 'tasks.clear_cold_data_task.clear_cold_col_data',
        'schedule': crontab(hour='3', minute='0')
    },
    # 'check_new_gift_audio_task': {
    #     'task': 'tasks.gift_audio_recognize_task.check_new_gift_audio_task',
    #     'schedule': 10 * 60,
    # },
    # 'submit_recognize_task': {
    #     'task': 'tasks.gift_audio_recognize_task.submit_recognize_task',
    #     'schedule': 10 * 60,
    # },
    # 'get_recognize_task_result': {
    #     'task': 'tasks.gift_audio_recognize_task.get_recognize_task_result',
    #     'schedule': 10 * 60,
    # },
    'cp_together_mic_settle_task': {
        'task': 'tasks.cp_together_mic_task.cp_together_mic_settle_task',
        'schedule': 30,
    },
    'notify_night_activity_start_task': {
        'task': 'tasks.family_night_activity_task.notify_night_activity_start_task',
        'schedule': crontab(hour='19', minute='45'),
    },
    'golden_tiger_system_close': {
        'task': 'tasks.golden_tiger_task.system_close',
        'schedule': 1800,
    },
    'cp_pk_open_room_tips_55': {
        'task': 'tasks.cp_pk_task.open_room_tips',
        'schedule': crontab(minute='55', hour='17-18'),
    },
    'cp_pk_open_room_tips_25': {
        'task': 'tasks.cp_pk_task.open_room_tips',
        'schedule': crontab(minute='25', hour='18-19'),
    },
    'cp_pk_match_18': {
        'task': 'tasks.cp_pk_task.cp_pk_match',
        'schedule': crontab(minute='10,40', hour='18'),
    },
    'cp_pk_match_19': {
        'task': 'tasks.cp_pk_task.cp_pk_match',
        'schedule': crontab(minute='10,40', hour='19'),
    },
}
# queue:  high_task:高优先级任务  long_time_task:长耗时任务(结果不是特别重要的任务)  default:默认优先级任务
task_routes = {
    'tasks.live_room_task.check_live_room_mic_user_alive': {'queue': 'high_task'},
    'tasks.team_room_task.clear_all_offline_team': {'queue': 'high_task'},
    'tasks.team_room_task.clear_negative_team_leader': {'queue': 'high_task'},
    'tasks.together_room_task.clear_all_offline_together_room': {'queue': 'high_task'},
    'tasks.couple_room_task.clear_all_offline_couple_room': {'queue': 'high_task'},
    # 'tasks.push_task.push_p2p_msg': {'queue': 'high_task'},
    # 'tasks.im_task.rcv_im_room_msg': {'queue': 'high_task'},
    'tasks.msg_check_task.check_msg_reply_timeout_task': {'queue': 'high_task'},
    'tasks.cp_together_mic_task.cp_together_mic_settle_task': {'queue': 'high_task'},
    # 匹配任务
    'tasks.cp_pk_task.cp_pk_match': {'queue': 'high_task'},

    # 'tasks.team_room_task.save_audio_video_record': {'queue': 'long_time_task'},
    'tasks.team_room_task.delete_audio_video_record': {'queue': 'long_time_task'},
    # 'tasks.getui_task.user_getui_task': {'queue': 'long_time_task'},
    # 'tasks.getui_task.leader_getui_task': {'queue': 'long_time_task'},
    'tasks.diversion_card_task.reset_diversion_card': {'queue': 'long_time_task'},
    'tasks.family_task.family_rank_refresh_task': {'queue': 'long_time_task'},
    'tasks.gift_audio_recognize_task.check_new_gift_audio_task': {'queue': 'long_time_task'},
    'tasks.gift_audio_recognize_task.submit_recognize_task': {'queue': 'long_time_task'},
    'tasks.gift_audio_recognize_task.get_recognize_task_result': {'queue': 'long_time_task'},
    'tasks.clear_cold_data_task.clear_cold_col_data': {'queue': 'long_time_task'},
    'tasks.invite_task.near_invite_task': {'queue': 'long_time_task'},
    'tasks.family_task.clear_family_offline': {'queue': 'long_time_task'},
    'tasks.family_task.clear_family_team_offline': {'queue': 'long_time_task'},
    'tasks.family_task.clear_family_game_team_nobody': {'queue': 'long_time_task'},
    'tasks.family_task.idle_long_time_queue': {'queue': 'long_time_task'},
    'tasks.family_task.clear_family_switch_record_status': {'queue': 'long_time_task'},
}
imports = (
    'tasks.live_room_task',
    'tasks.team_room_task',
    'tasks.update_anchor_score_task',
    'tasks.dingtalk_task',
    'tasks.leader_task',
    'tasks.together_room_task',
    'tasks.newbie_task',
    'tasks.push_task',
    'tasks.group_task',
    'tasks.im_task',
    'tasks.monitor_task',
    'tasks.couple_room_task',
    'tasks.getui_task',
    'tasks.active_task',
    'tasks.team_card_task',
    'tasks.msg_check_task',
    'tasks.quick_match_task',
    'tasks.cartoon_task',
    'tasks.invite_task',
    'tasks.diversion_card_task',
    'tasks.chatroom_task',
    'tasks.anchor_task',
    'tasks.video_match_task',
    'tasks.p2p_session',
    'tasks.family_task',
    'tasks.airdrop_task',
    'tasks.only_cp_msg',
    'tasks.only_cp_keep_task',
    'tasks.gift_audio_recognize_task',
    'tasks.clear_cold_data_task',
    'tasks.cp_together_mic_task',
    'tasks.family_night_activity_task',
    'tasks.golden_tiger_task',
    'tasks.cp_pk_task',
)

# CELERYD_PREFETCH_MULTIPLIER = 1  # worker预取乘数 每个worker可以额外（除去正在执行的已确认任务）预取的任务数
task_time_limit = 600  # 单个任务的运行时间不超过此值，否则会被SIGKILL信号杀死


