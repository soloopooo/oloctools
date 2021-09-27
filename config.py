# 小工具配置文件，注意引号，逗号，中英文标点，路径可用绝对路径可用相对路径
# 标准python变量写法，自由发挥哦
# 布尔值只可以用True和False 注意大小写
# 字符串记得引号
# 不建议瞎改，改自己懂的就好
# 不想输出的信息可以把大小改成0，把坐标也改成(0, 0)
# 除了写对齐的，其他都是左上为描点，记得自己计算

# 默认已经配置好大部分，略微填写可以直接使用

# 你问我为啥不用多行注释？？因为重构的时候需要，就改了，后来重构失败就...

#
# 自主定义变量区
#     PS:只是图个方便不再重复，没学过编程语言不建议使用，老老实实一个一个改
#

#
# 用户变量配置
#
user_name = 'Freezetime'
user_id = '11350021'
# 用户头像路径
user_avatar = 'resource/image/avatar.jpg'
# osu logo图片目录
osu_image = 'resource/image/osu!.png'
# 个性签名
user_signature = ''
# 已经登录osu官网的浏览器cookie。如何获取？ 百度
cookie = 'XSRF-TOKEN=IITITdazOltarEam6Tlq1rQ6Kxp1PCRT8BvrjwZl8B; osu_session=eyJpdiI6InhlRWwycG8yRlZ5U2taODg5bHN0amc9PSIsInZhbHVlIjoiUzc3UlVneFdHWVphcXJrTmJlbytsb2t6RnJTcDlHQkVhelZ6aFZCOWVqQ3VWRTl5aVZSN09TRmxmbzJwY0hGRm5BQlNzc01hcmUwbTlzaGZzY2g1a3hDVjR1M28wVnRFYm1Yb24vbnhKYnlGQ2hIcjJWS3Rxbi80QU1YMkhFWlNZbklZVnY1eTJDUSt2Rm82a2tjOE93PT0iLCJtYWMiOiI0NjcwYmIwNTU2YzMyOTA1MWNhODk3NjIzNjY5NmJjZTJjM2E0MGJkMDE3ODA2MjBjOWRiNGNkY2NhMjdkM2FiIn0%3D'
# cookie = 'XSRF-TOKEN=IITITdazOltarEam6Tlq1rQ6Kxp1PCRT8BvrjwZl8B; osu_session=eyJpdiI6InhlRWwycG8yRlZ5U2taODg5bHN0amc9PSIsInZhbHVlIjoiUzc3UlVneFdHWVphcXJrTmJlbytsb2t6RnJTcDlHQkVhelZ6aFZCOWVqQ3VWRTl5aVZSN09TRmxmbzJwY0hGRm5BQlNzc01hcmUwbTlzaGZzY2g1a3hDVjR1M28wVnRFYm1Yb24vbnhKYnlGQ2hIcjJWS3Rxbi80QU1YMkhFWlNZbklZVnY1eTJDUSt2Rm82a2tjOE93PT0iLCJtYWMiOiI0NjcwYmIwNTU2YzMyOTA1MWNhODk3NjIzNjY5NmJjZTJjM2E0MGJkMDE3ODA2MjBjOWRiNGNkY2NhMjdkM2FiIn0%3D'
# 代理
proxy_http = "http://localhost:54433"
proxy_https = "https://localhost:54433"

#
# 特殊信息输出打印配置
#

# 成绩图模板路径
bg_model_dir = "resource/image/image_model/score_new.png"
# 个人信息背景路径
user_info_bg_dir = "resource/image/92191625_1.png"
# 个人信息模板路径
user_info_model_dir = "resource/image/image_model/user_info.png"
# 头像位置
position_avatar = [1134, 489]
# 头像大小
avatar_size = (101, 101)
# pp分布折线图的左上角位置 图像左上为描点
pp_strains_location = [1514, 7]
# pp分布折线图的右下角位置 图像左上为描点
pp_strains_location2 = [1917, 128]
# pp分布折线图的颜色
pp_strains_color = (234, 200, 92)
# pp分布折线图的线宽
pp_strains_line_width = 2
# ur分布折线图的左上角位置 图像左上为描点
ur_strains_location = [1512, 950]
# ur分布折线图的右下角位置 图像左上为描点
ur_strains_location2 = [1917, 1075]
# ur分布折线图的颜色
ur_strains_color = (234, 200, 92)
# ur分布折线图的线宽
ur_strains_line_width = 1
# 获取不到bg使用的背景
bg_if_non = "resource/image/bgifnon.png"
# bg背景暗化程度
bg_dim = 0.5
# bg高斯模糊像素
gaussian_blur = 8
# bg重置大小后的宽度，必须和你的模板宽度一致，最终为成绩图宽度
bg_resize_weight = 1920
# 最终的成绩图高度，也就是你的模板高度
bg_resize_height = 1080
# status图标大小
map_status_size = (70, 70)
# status图标位置
map_status_position = [30, 980]
# status图标路径
map_status_unknown = 'resource/image/map_status/approved.png'
map_status_unsubmitted = 'resource/image/map_status/approved.png'
map_status_pending_wip_graveyard = 'resource/image/map_status/approved.png'
map_status_unused = 'resource/image/map_status/approved.png'
map_status_ranked = 'resource/image/map_status/ranked.png'
map_status_approved = 'resource/image/map_status/approved.png'
map_status_qualified = 'resource/image/map_status/approved.png'
map_status_loved = 'resource/image/map_status/loved.png'
# rank图标大小 (weight, height)
result_rank_size = (250, 250)
# rank图标的位置 [x, y]
position_rank = [960 - 117 - 5, 540 - 125 - 3]
# rank图标路径
result_rank_icon_ssh = 'resource/image/ranking/ranking-XH@2X.png'
result_rank_icon_ss = 'resource/image/ranking/ranking-X@2X.png'
result_rank_icon_sh = 'resource/image/ranking/ranking-SH@2X.png'
result_rank_icon_s = 'resource/image/ranking/ranking-S@2X.png'
result_rank_icon_a = 'resource/image/ranking/ranking-A@2X.png'
result_rank_icon_b = 'resource/image/ranking/ranking-B@2X.png'
result_rank_icon_c = 'resource/image/ranking/ranking-C@2X.png'
result_rank_icon_d = 'resource/image/ranking/ranking-D@2X.png'
result_rank_icon_f = 'resource/image/ranking/f.png'
# mod图标的位置 [x, y]
position_mod = [1770, 210]
# mod图标的大小
size_mod = (123, 83)
# mod图标路径
mod_icon_ap = 'resource/image/mods/AP.png'
mod_icon_at = 'resource/image/mods/at.png'
mod_icon_cn = 'resource/image/mods/cn.png'
mod_icon_dt = 'resource/image/mods/dt.png'
mod_icon_ez = 'resource/image/mods/ez.png'
mod_icon_fl = 'resource/image/mods/fl.png'
mod_icon_hd = 'resource/image/mods/hd.png'
mod_icon_hr = 'resource/image/mods/hr.png'
mod_icon_nc = 'resource/image/mods/nc.png'
mod_icon_nf = 'resource/image/mods/nf.png'
mod_icon_pf = 'resource/image/mods/pf.png'
mod_icon_rx = 'resource/image/mods/rx.png'
mod_icon_sd = 'resource/image/mods/sd.png'
mod_icon_so = 'resource/image/mods/so.png'
mod_icon_tg = 'resource/image/mods/tg.png'
mod_icon_v2 = 'resource/image/mods/v2.png'

# 文字信息输出打印配置:格式xxx = [字体路径, 大小, x, y, (R, G, B), 对齐方式]
#     PS:对齐方式写法：
#         示例:rl  cl
#         格式:{左右对齐}{上下对齐}
#         可用参数:l(left)  c(center)  r(right)  a(above)  b(below)

# 没学过python的format不建议自主修改以下变量
# xxx_format变量:输出格式化，双引号内写入python表达式。
#     PS:g_inf()类的函数可以在package/info.py文件内查看

output_title = ["resource/fonts/Torus-SemiBold.ttf", 48, 960, 760, (255, 255, 255), 'cc']
output_artist = ["resource/fonts/Torus-Regular.ttf", 39, 960, 832, (255, 255, 255), 'cc']
output_cs = ["resource/fonts/Torus-Regular.ttf", 36, 121, 488 - 3, (235, 194, 0), 'lc']
output_ar = ["resource/fonts/Torus-Regular.ttf", 36, 121, 400 - 3, (235, 194, 0), 'lc']
output_od = ["resource/fonts/Torus-Regular.ttf", 36, 121, 661 - 3, (235, 194, 0), 'lc']
output_hp = ["resource/fonts/Torus-Regular.ttf", 36, 121, 575 - 3, (235, 194, 0), 'lc']
output_bid = ["resource/fonts/Torus-Regular.ttf", 36, 121, 833 - 3, (235, 194, 0), 'lc']
output_sid = ["resource/fonts/Torus-Regular.ttf", 36, 121, 747 - 3, (235, 194, 0), 'lc']
output_c300 = ["resource/fonts/Torus-Regular.ttf", 41, 1653, 455 - 3, (255, 142, 211), 'lc']
output_c100 = ["resource/fonts/Torus-Regular.ttf", 41, 1599, 569 - 3, (255, 142, 211), 'lc']
output_c50 = ["resource/fonts/Torus-Regular.ttf", 41, 1610, 672 - 3, (255, 142, 211), 'lc']
output_c0 = ["resource/fonts/Torus-Regular.ttf", 41, 1567, 792 - 3, (255, 142, 211), 'lc']
output_slider_breaks = ["resource/fonts/Torus-Regular.ttf", 41 - 3, 1592, 904, (255, 142, 211), 'cc']
output_stars = ["resource/fonts/Torus-SemiBold.ttf", 39, 960, 134 - 3, (255, 255, 255), 'cc']

output_pp_current_position = [960 - 3, 920, 'cc']
output_pp_current = ["resource/fonts/Torus-SemiBold.ttf", 66, (222, 0, 255)]
output_str_pp = ["resource/fonts/Torus-SemiBold.ttf", 56, (237, 187, 255)]
output_str_pp_y_offset = 10

output_pp_ss = ["resource/fonts/Torus-Regular.ttf", 41, 448, 240 - 3, (255, 142, 211), 'rc']
output_pp_99 = ["resource/fonts/Torus-Regular.ttf", 41, 381, 342 - 3, (255, 142, 211), 'rc']
output_pp_98 = ["resource/fonts/Torus-Regular.ttf", 41, 347, 460 - 3, (255, 142, 211), 'rc']
output_pp_97 = ["resource/fonts/Torus-Regular.ttf", 41, 330, 568 - 3, (255, 142, 211), 'rc']
output_pp_96 = ["resource/fonts/Torus-Regular.ttf", 41, 348, 673 - 3, (255, 142, 211), 'rc']
output_pp_95 = ["resource/fonts/Torus-Regular.ttf", 41, 390, 795 - 3, (255, 142, 211), 'rc']
output_pp_fc = ["resource/fonts/Torus-Regular.ttf", 41, 472, 903 - 3, (255, 142, 211), 'rc']
output_bpm = ["resource/fonts/Torus-Regular.ttf", 36, 121, 66 - 3, (235, 194, 0), 'lc']
output_user_signature = ["resource/fonts/Torus-Regular.ttf", 0, 0, 0, (255, 255, 255), 'cc']
output_time_day = ["resource/fonts/Torus-Regular.ttf", 31, 650, 492 - 3, (255, 255, 255), 'cc']
output_time_min = ["resource/fonts/Torus-Regular.ttf", 33, 650, 606 - 5, (255, 255, 255), 'cc']
output_note_circle = ["resource/fonts/Torus-Regular.ttf", 36, 121, 146 - 3, (235, 194, 0), 'lc']
output_note_slider = ["resource/fonts/Torus-Regular.ttf", 36, 121, 232 - 3, (235, 194, 0), 'lc']

output_ur = ["resource/fonts/Torus-SemiBold.ttf", 45, 1854, 924, (100, 170, 255), 'rb']
output_ur_format = "round(float(str({0}).format(g_inf.ur())), 2)"

output_mapper = ["resource/fonts/Torus-SemiBold.ttf", 36, 960, 347, (111, 255, 250), 'cc']
output_mapper_format = "'mapped by ' + str({0}).format(g_inf.mapper())"

output_difficulty = ["resource/fonts/Torus-SemiBold.ttf", 36, 960, 301, (111, 255, 250), 'cc']
output_difficulty_format = "str({0}).format(g_inf.difficulty())"

output_player_name = ["resource/fonts/Torus-Regular.ttf", 39, 1244, 540 - 3, (172, 172, 172), 'lc']
output_key_count_k1 = ["resource/fonts/Torus-SemiBold.ttf", 28, 157, 1015 - 3, (235, 194, 0), 'cc']
output_key_count_k2 = ["resource/fonts/Torus-SemiBold.ttf", 28, 236, 1015 - 3, (235, 194, 0), 'cc']
output_key_count_m1 = ["resource/fonts/Torus-SemiBold.ttf", 28, 315, 1015 - 3, (235, 194, 0), 'cc']
output_key_count_m2 = ["resource/fonts/Torus-SemiBold.ttf", 28, 393, 1015 - 3, (235, 194, 0), 'cc']

output_score = ["resource/fonts/Torus-Regular.ttf", 90, 960, 221, (226, 226, 226), 'cc']
output_score_format = "'{:,}'.format(g_inf.score())"

output_max_combo = ["resource/fonts/Torus-Regular.ttf", 41, 1614, 340 - 3, (255, 142, 211), 'lc']
output_max_combo_format = "'{:,}'.format(g_inf.max_combo())"

output_accuracy = ["resource/fonts/Torus-Regular.ttf", 41, 1492, 233 - 3, (255, 142, 211), 'lc']
output_accuracy_format = "str({0}).format(g_inf.accuracy()) + '%'"

output_time_length_full = ["resource/fonts/Torus-Regular.ttf", 36, 121, 318 - 3, (235, 194, 0), 'lc']
output_time_length_full_format = ("str(int((float(str({0}).format(g_inf.time_length_full()))/1000)/60)) + ':' + "
                                  "str(int((float(str({0}).format(g_inf.time_length_full()))/1000)%60))")

output_time_length_now = ["resource/fonts/Torus-Regular.ttf", 36, 121, 318 - 3, (235, 194, 0), 'lc']
output_time_length_now_format = ("str(int((float(str({0}).format(g_inf.time_length_now()))/1000)/60)) + ':' + "
                                 "str(int((float(str({0}).format(g_inf.time_length_now()))/1000)%60))")
# 什么狗屁玩意又臭又长，真亏我写得出来，你们自己看着改改，反正最后要eval这个语句，要一句成表达式，或者你字符串拼接我也不管
