# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TbUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MtBlogBlogTag(models.Model):
    blog = models.ForeignKey('TBlog', models.DO_NOTHING, blank=True, null=True)
    blog_tag_id = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)
    blog_is_private = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mt_blog_blog_tag'


class MtSpecialPartSectionBlogs(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    part_section_id = models.CharField(max_length=255)
    blog_id = models.CharField(max_length=255)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'mt_special_part_section_blogs'


class TAdminRole(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    role_name = models.CharField(max_length=100)
    role_intro = models.CharField(max_length=100)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_admin_role'


class TAdminUser(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    user_profile = models.CharField(max_length=255, blank=True, null=True)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    user_intro = models.CharField(max_length=255, blank=True, null=True)
    user_profession = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.CharField(max_length=255, blank=True, null=True)
    role_id = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    login_ip_address = models.CharField(max_length=255, blank=True, null=True)
    last_login_time = models.CharField(max_length=255, blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_admin_user'


class TBlog(models.Model):
    uid = models.CharField(primary_key=True, max_length=100)
    blog_title = models.CharField(max_length=100)
    blog_summary = models.CharField(max_length=255)
    blog_author_id = models.CharField(max_length=100)
    is_original = models.IntegerField()
    origin_address = models.CharField(max_length=255, blank=True, null=True)
    blog_sort_id = models.CharField(max_length=100)
    recommend_level = models.IntegerField()
    clicks = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField()
    is_open_comment = models.IntegerField()
    is_private = models.IntegerField()
    blog_status = models.IntegerField()
    cover_url = models.CharField(max_length=255, blank=True, null=True)
    blog_content = models.TextField()
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_blog'


class TBlogLike(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    blog_id = models.CharField(max_length=255)
    like_person_id = models.CharField(max_length=255)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_blog_like'


class TBlogSort(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    sort_name = models.CharField(max_length=20, blank=True, null=True)
    intro = models.CharField(max_length=255, blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_blog_sort'


class TBlogTag(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    tag_name = models.CharField(max_length=100, blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100, blank=True, null=True)
    update_time = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_blog_tag'


class TBlogTest(models.Model):
    uid = models.CharField(primary_key=True, max_length=100)
    blog_title = models.CharField(max_length=100)
    blog_summary = models.CharField(max_length=100)
    blog_author_id = models.CharField(max_length=100, blank=True, null=True)
    is_original = models.IntegerField()
    blog_sort_id = models.CharField(max_length=100, blank=True, null=True)
    recommend_level = models.IntegerField(blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    is_open_comment = models.IntegerField(blank=True, null=True)
    blog_status = models.IntegerField(blank=True, null=True)
    cover_url = models.CharField(max_length=255, blank=True, null=True)
    blog_content = models.TextField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_blog_test'


class TComments(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    comment_content = models.TextField()
    comment_source = models.IntegerField()
    source_id = models.CharField(max_length=255)
    comment_status = models.IntegerField(blank=True, null=True)
    comment_person_id = models.CharField(max_length=255)
    commented_person_id = models.CharField(max_length=255, blank=True, null=True)
    to_comment_id = models.CharField(max_length=255, blank=True, null=True)
    root_comment_id = models.CharField(max_length=255, blank=True, null=True)
    comment_layer = models.IntegerField()
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_comments'


class TCommentsInform(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    inform_type = models.IntegerField()
    inform_reason = models.TextField()
    inform_person_id = models.CharField(max_length=255)
    inform_comment_id = models.CharField(max_length=255)
    comment_source = models.IntegerField()
    source_id = models.CharField(max_length=255)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_comments_inform'


class TCommentsReaction(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    comment = models.ForeignKey(TComments, models.DO_NOTHING)
    reaction_person_id = models.CharField(max_length=255)
    reaction_content = models.CharField(max_length=255)
    comment_source = models.IntegerField()
    source_id = models.CharField(max_length=255)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_comments_reaction'


class TFile(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    file_original_name = models.CharField(max_length=255, blank=True, null=True)
    file_current_name = models.CharField(max_length=255, blank=True, null=True)
    file_suffix = models.CharField(max_length=10, blank=True, null=True)
    file_sort_id = models.CharField(max_length=100, blank=True, null=True)
    file_sort_name = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.CharField(max_length=100, blank=True, null=True)
    update_time = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_file'


class TFileSort(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    cover_img = models.CharField(max_length=255, blank=True, null=True)
    sort_name = models.CharField(max_length=30, blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100, blank=True, null=True)
    update_time = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_file_sort'


class TRole(models.Model):
    uid = models.CharField(primary_key=True, max_length=32)
    role_name = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField(blank=True, null=True)
    summarize = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    user_uids = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_role'


class TSpecial(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    special_name = models.CharField(max_length=100)
    special_summary = models.CharField(max_length=100, blank=True, null=True)
    cover_url = models.CharField(max_length=255, blank=True, null=True)
    special_sort_id = models.CharField(max_length=255)
    clicks = models.IntegerField(blank=True, null=True)
    is_private = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_special'


class TSpecialPart(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    part_name = models.CharField(max_length=100)
    part_title = models.CharField(max_length=100, blank=True, null=True)
    part_summary = models.CharField(max_length=100, blank=True, null=True)
    special_id = models.CharField(max_length=255)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_special_part'


class TSpecialPartSection(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    section_title = models.CharField(max_length=100)
    special_part_id = models.CharField(max_length=255)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_special_part_section'


class TSpecialSort(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    special_sort_name = models.CharField(max_length=100)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_special_sort'


class TSystemAboutMe(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    admin_user_id = models.CharField(max_length=255)
    intro_detail = models.TextField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_system_about_me'


class TSystemContactWay(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    contact_way = models.CharField(max_length=100)
    way_num = models.CharField(max_length=100, blank=True, null=True)
    way_icon_name = models.CharField(max_length=100, blank=True, null=True)
    icon_color = models.CharField(max_length=20, blank=True, null=True)
    link_address = models.CharField(max_length=255, blank=True, null=True)
    is_show = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_system_contact_way'


class TSystemFriendLink(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    link_name = models.CharField(max_length=100)
    link_intro = models.CharField(max_length=100, blank=True, null=True)
    link_address = models.CharField(max_length=100)
    link_email = models.CharField(max_length=100, blank=True, null=True)
    is_publish = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_system_friend_link'


class TWebUser(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    user_tel = models.CharField(max_length=255, blank=True, null=True)
    user_profile = models.CharField(max_length=255, blank=True, null=True)
    user_wechat = models.CharField(max_length=255, blank=True, null=True)
    user_microblog = models.CharField(max_length=255, blank=True, null=True)
    user_gitee = models.CharField(max_length=255, blank=True, null=True)
    user_github = models.CharField(max_length=255, blank=True, null=True)
    user_qq = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.CharField(max_length=255, blank=True, null=True)
    user_password = models.CharField(max_length=255, blank=True, null=True)
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    user_position = models.CharField(max_length=255, blank=True, null=True)
    user_company = models.CharField(max_length=255, blank=True, null=True)
    user_website = models.CharField(max_length=255, blank=True, null=True)
    user_intro = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    user_identity = models.IntegerField(blank=True, null=True)
    login_ip_address = models.CharField(max_length=255, blank=True, null=True)
    last_login_time = models.CharField(max_length=255, blank=True, null=True)
    account_status = models.IntegerField(blank=True, null=True)
    data_audit_status = models.IntegerField(blank=True, null=True)
    account_source = models.CharField(max_length=20)
    order_num = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=100)
    update_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 't_web_user'


class TbUsers(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    mobile = models.CharField(unique=True, max_length=11)
    tecs = models.CharField(max_length=100)
    email_active = models.IntegerField()
    default_address = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=20)
    gender = models.SmallIntegerField()
    description = models.CharField(max_length=200, blank=True, null=True)
    default_image = models.CharField(max_length=200, blank=True, null=True)
    show_image = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_users'


class TbUsersGroups(models.Model):
    user = models.ForeignKey(TbUsers, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tb_users_groups'
        unique_together = (('user', 'group'),)


class TbUsersUserPermissions(models.Model):
    user = models.ForeignKey(TbUsers, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tb_users_user_permissions'
        unique_together = (('user', 'permission'),)
