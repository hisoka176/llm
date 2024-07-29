prompt = f'''
你现在是一个hive sql的专家，给你一些数据表的结构，以及想要查询的指标名称，你从中挑选有用的数据表，给出对应的sql逻辑，并解释原因，
====hive表:gdm.gdm_04_app_rcmd_di====
app_key             	string              	APP标识
version             	string              	APP版本号
device_id           	string              	设备标识符
user_id             	string              	注册id
start_time          	string              	请求时间
message_id          	string              	消息唯一标识
pvid                	string              	请求曝光标识
rank_num            	string              	请求曝光批次号
itemcount           	string              	一次请求曝光内容数量
refreshtype         	string              	请求刷新类型
ab_version          	string              	AB类型
rcmd_type           	string              	是否商投:1商投,0非商投
object_type         	string              	内容类型id，一般不使用业务方上报内容，使用资源池转换后的biz_type
object_id           	string              	内容id对应资源池的biz_id
object_p            	string              	请求曝光内容位置
is_expo             	string              	是否请求曝光：1是0否
sight_show_num      	string              	可见曝光次数
sight_object_p      	string              	可见曝光位置,多个位置以逗号分隔
object_id2          	string              	车系卡片内容
click_num           	string              	点击次数
click_object_p      	string              	点击位置,多个位置以逗号分隔
autoplay_num        	string              	自动播放次数
no_interest         	string              	是否负反馈：0否，剩余为负反馈类型，负反馈名称请关联dim.dim_upload_dim_rcmd_not_interest_list
duration            	string              	取时长请使用gdm_04_app_rcmd_autoplay_and_list_duration_di
finish_read         	string              	取完读请使用gdm_04_app_rcmd_autoplay_and_list_duration_di
is_new_user         	string              	是否是新用户
city_id             	string              	请求曝光城市id
basicid             	string              	透传参数
sdk_version         	string              	sdk版本
original_object_type	string              	原始内容类型id
inner_type          	string              	定制化内容类型id
cyid                	string              	智能营销创意id
rtype               	string              	rtype
bu_id               	string              	部门id
bu_name             	string              	部门name
rtype_name          	string              	业务类型name，与biz_type配对使用
biz_type            	string              	资源池业务类型
business_id         	string              	部门id
business_name       	string              	部门名称
new_rtype           	string              	对智能营销特殊处理后的rtype
attribute           	string              	内容属性，1=商业，2=非商业，用new_rtype转换后的
content_desc        	string              	业务分类:图文/视频/VR等
dt                  	string
if_nst              	string

# Partition Information
# col_name            	data_type           	comment

dt                  	string
if_nst              	string
====hive表:gdm.gdm_rcmd_r_type_mapping_da====
code                	string              	r_type
product             	string              	产品线ID
product_desc        	string              	产品线描述
content_type        	string              	物料类型 ID
content_desc        	string              	物料类型描述
sec_content_type    	string              	子物料类型 ID
sec_content_desc    	string              	子物料类型描述
ext_type            	string              	扩展位
valid_type          	string              	校验位
biz_type            	string              	资源池biz_type
status              	string              	状态位，-1表示不可用
create_time         	string              	创建时间
update_time         	string              	更新时间
created_stime       	string              	创建时间-dba
modified_stime      	string              	修改时间-dba
is_del              	string              	逻辑删除标识-dba
business_id         	string              	业务线id
business_name       	string              	业务线名称
main_type           	string              	大类型id
main_name           	string              	大类型名称
attribute           	string              	内容属性，1=商业，2=非商业
dt                  	string              	日期分区字段

# Partition Information
# col_name            	data_type           	comment

dt                  	string              	日期分区字段
====hive表:gdm_04_general_rcmd_di====
device_id           	string              	设备号
biz_type            	string              	物料类型
biz_id              	string              	物料id
business_name       	string              	部门名称
rtype_name          	string              	rtype名称
attention_cnt       	string              	关注
praise_cnt          	string              	点赞
comment_cnt         	string              	评论
share_cnt           	string              	转发
favorites_cnt       	string              	收藏
danmu_cnt           	string              	弹幕
dt                  	string

# Partition Information
# col_name            	data_type           	comment

dt                  	string
====
'''
