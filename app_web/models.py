from django.db import models
import django.utils.timezone as timezone


class User(models.Model):
    """用户"""
    SEX_TYPE = (
        ('W', '女'),
        ('M', '男')
    )
    username = models.CharField('账户', max_length=12)
    sex = models.CharField('性别', max_length=1, choices=SEX_TYPE)
    openid = models.CharField('公众号用户id', max_length=30, unique=True)
    join_time = models.DateTimeField('注册时间', default=timezone.now)
    introduction = models.TextField('自我介绍', null=True, blank=True)
    head_path = models.CharField('头像路径', max_length=255, null=True, blank=True)
    enjoy_music = models.CharField('喜欢的音乐', max_length=255, null=True, blank=True)
    occupation = models.CharField('职业', max_length=100, null=True, blank=True)
    address = models.CharField('所在地', max_length=100, null=True, blank=True)
    native_place = models.CharField('籍贯', max_length=20, null=True, blank=True)
    email = models.CharField('邮箱', max_length=60, null=True, blank=True)
    enjoy = models.TextField('兴趣爱好', null=True, blank=True)

    class Meta:
        app_label = "app_web"

    def __str__(self):
        return self.username


class Article(models.Model):
    """文章"""
    ART_TYPE = (
        ('0', '学习笔记'),
        ('1', '经典语录'),
        ('2', '随记')
    )
    user_id = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE)
    author = models.CharField('作者', max_length=30)
    title = models.CharField('标题', max_length=100)
    content = models.TextField('正文')
    abstract = models.CharField('摘要', max_length=160)
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    revise_time = models.DateTimeField('修改时间', null=True, blank=True)
    type = models.CharField('文章分类', max_length=1, choices=ART_TYPE)

    class Meta:
        app_label = "app_web"

    def __str__(self):
        return self.title


class Mood(models.Model):
    """心情"""
    user_id = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE)
    name = models.CharField('发表人', max_length=30)
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    address = models.CharField('所在地', max_length=100)
    img_url = models.CharField('图片地址', max_length=120)
    content = models.CharField('内容', max_length=300)
    keyword = models.CharField('关键词', max_length=6)
    weather = models.CharField('天气', max_length=10)

    class Meta:
        app_label = "app_web"

    def __str__(self):
        return self.name


class Comment(models.Model):
    """评论"""
    TOPIC_TYPE = (
        ('A', '文章'),
        ('M', '心情')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.CharField('评论人姓名', max_length=30)
    topic_id = models.IntegerField('主题id')
    topic_type = models.CharField('主题类型', max_length=1, choices=TOPIC_TYPE)
    comment_time = models.DateTimeField('评论时间', default=timezone.now)
    content = models.TextField('评论内容')

    class Meta:
        app_label = "app_web"

    def __str__(self):
        return self.from_user


class Reply(models.Model):
    """回复"""
    REPLY_TYPE = (
        ('C', '评论'),
        ('R', '回复')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    from_user = models.CharField('回复人姓名', max_length=30)
    to_user = models.CharField('目标人姓名', max_length=30)
    to_user_id = models.IntegerField('目标人id')
    reply_id = models.IntegerField('回复目标id')
    reply_type = models.CharField('回复类型', max_length=1, choices=REPLY_TYPE)
    reply_time = models.DateTimeField('回复时间', default=timezone.now)
    content = models.TextField('回复内容')

    class Meta:
        app_label = "app_web"

    def __str__(self):
        return self.from_user
