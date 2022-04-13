import io
import os
import time
import pstats
import cProfile

from redis_client import rds


BRANCH = os.environ.get('COMMIT_REF_NAME', '')
COMMIT = os.environ.get('COMMIT_SHORT_SHA', '00000000')


class FixLenQueue:
    """使用一个redis的集合记录单个接口最近10次每次接口访问总耗时
    
    http://redisdoc.com/script/eval.html?highlight=call
    """
    PREFIX = '{COMMIT}_'
    _ADD_SC = '''
    redis.call('SADD', KEYS[1], ARGV[3])
    redis.call('RPUSH', KEYS[2], ARGV[1])
    if redis.call('LLEN', KEYS[2]) > tonumber(ARGV[2])
    then
        redis.call('LPOP', KEYS[2])
        return 1
    end
    return 0
    '''

    @classmethod
    def add(cls, commit_tag, entry, content, maxsize=10):
        commit_tag = f'{cls.PREFIX}{commit_tag}'
        proc = rds.register_script(cls._ADD_SC)
        return proc(
            keys=[commit_tag, f'{commit_tag}:{entry}'],
            args=[content, maxsize, entry],
        )

    @classmethod
    def get_commit(cls, commit_tag):
        commit_tag = f'{cls.PREFIX}{commit_tag}'
        entries = rds.smembers(commit_tag)
        return {entry: rds.lrange(
            f'{commit_tag}:{entry}', 0, -1) for entry in entries}


class Profiler:
    """python 性能分析器
    """
    ENTRIES = dict()
    MAXSIZE = 10
    UPDATE = True
    UPDATE_INTERVAL = 300
    TAGS = [
        '{', '<', 'lib/python',
        'site-packages',
        'util/profile.py',
    ]

    @classmethod
    def end(cls, entry, pr):
        # https://blog.csdn.net/qq_38934189/article/details/105976099
        # 用来暂存性能分析结果
        s = io.StringIO()  
        
        # https://blog.csdn.net/weixin_40304570/article/details/79459811
        # 按照累计时间降序获得分析结果
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        cls.handle_result(entry, s.getvalue())

    @classmethod
    def get_profiler(cls, entry):
        """判断是否开始分析，并依据返回分析器对象"""
        if not cls.enter(entry):
            return None
        cls.ENTRIES[entry] = cls.ENTRIES.get(entry, 0) + 1
        pr = cProfile.Profile()
        pr.enable()
        return pr

    @classmethod
    def enter(cls, entry):
        # if BRANCH != 'build_prod':  # 限定特殊分支 build_prod 来分析程序
        #     return False
        last_ts = cls.ENTRIES.get(entry, 0)
        if last_ts > 0 and not cls.UPDATE:  # 是否重新分析该接口
            return False
        now = int(time.time())
        if last_ts + cls.UPDATE_INTERVAL > now:  # 300 s内多次调用不重新分析该接口的性能
            return False
        cls.ENTRIES[entry] = now
        return True

    @classmethod
    def valuable_line(cls, line):
        """丢弃不需要分析的部分包"""
        for tag in cls.TAGS:
            if tag in line:
                return False
        return True

    @classmethod
    def handle_result(cls, entry, rs):
        """重组分析结果并存储到 redis 中"""
        content = '\n'.join(
            line.strip() for line in rs.split('\n') if cls.valuable_line(line))
        FixLenQueue.add(COMMIT, entry, content)
