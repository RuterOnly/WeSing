# -*- coding: utf-8 -*-
# 源码仅供参考学习，请勿使用于其他途径
import asyncio
import datetime
import json
import os
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message
from botpy.types.message import  Embed, EmbedField, Thumbnail
# 读写
from settings import set_channel, get_channel
# 网页访问
import mixiuapi

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 上线了!")
    async def on_at_message_create(self, message: Message):
        instruction = ''
        order_list = message.content.split(' ')  # 空格分开全部命令，存入orderList
        if len(order_list)>=2:
            at_robot_id = order_list[0]
            if at_robot_id  != "<@!" + str(self.robot.id) + ">" or at_robot_id == '':
                 _log.info(f"当前艾特的机器人对象【{at_robot_id}】不是当前正在处理的机器人{self.robot.id}")
            else:
                instruction = order_list[1]
                _log.info(f"当前艾特的机器人对象【{at_robot_id}】处理的指令为{instruction}")
        else:
            try:
                await message.reply(content=f'<@!{message.author.id}>\n请正确输入指令，或者输入需要机器人响应的指令，如下：\n<@!{self.robot.id}> 全民歌单 1\n最前面是艾特的机器人，然后打一个空格。\n之后为要机器人响应的指令，后面还可以跟指令的其它需要参数，但也要用一个空格隔开。')
            except:
                _log.info(f"机器人发送给{message.channel_id}子频道{message.author.id}用户消息失败")
            return
        if '全民K歌' == instruction:
            embed = Embed(
                title="全民K歌",
                prompt='全民K歌',
                thumbnail=Thumbnail(url=message.author.avatar),
                fields=[
                    EmbedField(name = "全民绑定"),
                    EmbedField(name = "全民查询"),
                    EmbedField(name = "全民歌单"),
                    EmbedField(name = "全民查看"),
                    ],)
            try:
                await self.api.post_message(channel_id=message.channel_id, msg_id=message.id, embed=embed)
            except Exception as e:
                 _log.info(f"错误信息：{repr(e)}")
            return
        
        # 全民K歌功能
        if '全民绑定' == instruction:
            if len(order_list) == 3:
                name = order_list[2]
                set_channel(message.author.id,name ,'WeSingUid')
                try:
                    await message.reply(content=f"绑定成功，UID：{name}")
                except Exception as e:
                    _log.info(f"错误信息：{repr(e)}")
                return  
            else:
                try:
                    await message.reply(content="绑定格式不对，请发送 全民绑定 UID\nUID为自己主页网址中的uid= 的值")
                except Exception as e:
                    _log.info(f"错误信息：{repr(e)}")
                return    
        
        if '全民查看' == instruction:
            if len(order_list) == 3:
                song_id = str(int(order_list[2])) # 序号
                UID = get_channel(message.author.id,'WeSingQueryUid')
                pages = get_channel(message.author.id,'WeSingQueryUidPages')
                if UID == '':
                     contents = '您当前还没有查询某位用户的全民K歌信息呢？\n如果想要查看，请发送 全民查询 UID/对象'
                elif pages =='':
                    contents = '您当前还没有查询某位用户的全民K歌歌单某页信息呢？\n如果想要查看，请发送 全民歌单 页数(1/其它页数)'
                else:
                    list = mixiuapi.getWeSingList(UID, pages)
                    if list == [] or list == None:
                        contents = '查询无效，或者无歌，页数无效。'
                        set_channel(message.author.id,'','WeSingQueryUidPages')
                    else:
                        i = 0
                        for text in list:
                            i = i + 1
                            if i == int(song_id):
                                str_time = text['发布时间']
                                time_str_new = str(datetime.datetime.fromtimestamp(float(str_time)))
                                song_url = text['歌曲地址']
                                print(text['歌名'])
                                song =  mixiuapi.getWeSingSingText(song_url)
                                # print(song)
                                WeSingInfo = {
                                    '简介':'',
                                    '封面':'',
                                    '分数':'',
                                    '收听量':'',
                                    '评论量':'',
                                    '歌曲地址':''}
                                if song == WeSingInfo or song == None:
                                    try:
                                        await message.reply(content="查看歌曲信息失败，请等待重试")
                                    except Exception as e:
                                        _log.info(f"错误信息：{repr(e)}")
                                    return
                                song_img_url = song['封面']
                                print("封面：" + song_img_url)
                                if 'http://c.y.qq.com/tplcloud/fcgi-bin/fcg_get_2dcode.fcg' in song_img_url or song_img_url == '//y.gtimg.cn/music/musicbox_v3/img/pics/default.gif':
                                    song_img_url = 'http://img.zcool.cn/community/01a616593bc72fa8012193a3cc6580.png'
                                
                                embed = Embed(
                                title=text['歌名'],
                                prompt='全民K歌',
                                thumbnail=Thumbnail(url=song_img_url),
                                fields=[
                                    EmbedField(name = "发布：" + time_str_new),
                                    EmbedField(name = "简介：" + song['简介']),
                                    EmbedField(name = "分数：" + song['分数']),
                                    EmbedField(name = "收听：" + song['收听量']),
                                    EmbedField(name = "评论：" + song['评论量']),
                                    
                                ],)
        
                                _log.info(json.dumps(embed))
                                try:
                                    await self.api.post_message(channel_id=message.channel_id, msg_id=message.id, embed=embed)# ark =payload)#
                                except Exception as e:
                                    _log.info(f"错误信息：{repr(e)}")
                                return
                        contents = '查询的歌曲序号无效或者请重试'
                try:
                    await message.reply(content=contents)
                except Exception as e:
                    _log.info(f"错误信息：{repr(e)}")
                return  
            else:
                try:
                    await message.reply(content="查看格式不对，请发送 全民查看 歌曲序号\n歌曲序号为刚才查询的页面列表歌曲的序号")
                except Exception as e:
                    _log.info(f"错误信息：{repr(e)}")
                return 
        
        if '全民歌单' == instruction:
            UID = get_channel(message.author.id,'WeSingQueryUid')
            if UID != '':
                if len(order_list) == 3:
                    pages = str(int(order_list[2])) #页数
                else:
                    pages = '1'
                list = mixiuapi.getWeSingList(UID, pages)
                if list == [] or list == None:
                    contents = '查询无效，或者无歌，页数无效。'
                    set_channel(message.author.id,'','WeSingQueryUidPages')
                else:
                    set_channel(message.author.id,pages,'WeSingQueryUidPages')
                    contents = '以下为查询到的用户歌单信息：'
                    i = 0
                    for text in list:
                        i = i + 1
                        contents += '\n序号：' + str(i)
                        contents += '\n歌名：' + text['歌名']
                        str_time = text['发布时间']
                        time_str_new = str(datetime.datetime.fromtimestamp(float(str_time)))
                        contents += '\n发布：' + time_str_new
                    contents += '\n当前为' + pages + '页\n查看某首歌曲\n请发送 全民查看 1\n1 为上面歌单的歌曲序号'

            else:
                contents = '您当前还没有查询某位用户的全民K歌信息呢？\n如果想要查看，请发送 全民查询 UID/对象'
            try:
                await message.reply(content=contents)
            except Exception as e:
                _log.info(f"错误信息：{repr(e)}")
            return

        if '全民查询' == instruction:
            if len(message.mentions) == 2:
                """
                user_send= []
                for member in message.mentions:  # 获取被@的成员
                    if not member.bot:  # 筛掉机器人
                        user_send.append(member.id)
                """
                UID = message.mentions[1]
                UID = get_channel(message.author.id,'WeSingUid') 
                if UID == '':
                    try:
                        await message.reply(content="查询的艾特对象没有绑定全民K歌\n请联系他 发送 全民绑定 UID")
                    except Exception as e:
                        _log.info(f"错误信息：{repr(e)}")
                    return
            elif len(order_list) == 3:
                UID = order_list[2]
            else:
                try:
                    await message.reply(content="查询格式不对，请发送 全民查询 UID/@对象")
                except Exception as e:
                    _log.info(f"错误信息：{repr(e)}")
                return

            images = '' 
            WeSingInfo = {
                '头像':'',
                '昵称':'',
                '等级':'',
                '信息':'',
                '性别':'',
                '年龄':'',
                '地区':'',
                '作品数':'',
                '粉丝数':'',
                '关注数':'',}
            WeSingInfos = mixiuapi.getWeSingInfo(UID)
            if WeSingInfos != WeSingInfo and WeSingInfos != None and WeSingInfos['头像'] != '' and WeSingInfos['头像'] != '//y.gtimg.cn/music/musicbox_v3/img/pics/default.gif':
                    set_channel(message.author.id,UID ,'WeSingQueryUid')
                    set_channel(message.author.id,'','WeSingQueryUidPages')
                    images = WeSingInfos['头像']
                    if 'http://c.y.qq.com/tplcloud/fcgi-bin/fcg_get_2dcode.fcg' in images:
                        images = 'http://img.zcool.cn/community/01a616593bc72fa8012193a3cc6580.png'
                    contents = '\n昵称：'+ WeSingInfos['昵称']
                    contents += '\n等级：'+ WeSingInfos['等级']
                    contents += '\n介绍：'+ WeSingInfos['信息']
                    if WeSingInfos['性别'] == 'boy':
                        contents += '\n性别：♂'
                    else:
                         contents += '\n性别：♀'
                    contents += '\n年龄：'+ WeSingInfos['年龄']
                    contents += '\n地区：'+ WeSingInfos['地区']
                    contents += '\n作品：'+ WeSingInfos['作品数']
                    contents += '\n粉丝：'+ WeSingInfos['粉丝数']
                    contents += '\n关注：'+ WeSingInfos['关注数']
            else:
                    contents = "您查询频繁，或查询无效。"
            try:
                        await message.reply(content=contents)#, image=images)
            except Exception as e:
                    _log.info(f"错误信息：{repr(e)}")
            return    


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True
    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])