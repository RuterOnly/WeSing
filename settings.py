import yaml

filename = "settings.yaml"
try:
    w =open(filename,'r')
    w.close()
except IOError:
    w = open(filename,'w')
    w.close()

def write_yaml(data: dict):
    # print("【YAML模块】***写入yaml文件数据***")
    with open(filename, 'w') as f:
        # print("【YAML模块】***yamlz载入***")        
        yaml.dump(data, f)
        # print("【YAML模块】***文件关闭***")       
        f.close()
    return

def get_yaml_data():
    # 打开yaml文件
    # print("【YAML模块】***获取yaml文件数据***")
    with open(filename, 'r') as f:
        # print("【YAML模块】***成功打开yaml文件***")
        config_data = yaml.load(f, Loader=yaml.FullLoader)
        # print("【YAML模块】***yamlz载入***")
        f.close()
        # print("【YAML模块】***文件关闭***")
        return config_data

def set_channel(guild_id: str, channel_id: str, channel:str): # 设置频道/信息
    """
    设置频道
     guild_id: 频道ID
     channel_id: 子频道ID 或者 其它需要设置的参数内容
     channel: 要储存频道名称 或者 其它需要设置的参数名称
    """
    config_data = get_yaml_data() 
    if config_data == None:
        config_data = {guild_id + '_'+channel:''}
    config_data[guild_id + '_' + channel]= channel_id
    write_yaml(config_data)
    return

def get_channel(guild_id: str, channel:str):# 获取频道/信息
    """
    获取频道
     guild_id: 频道ID
     channel: 要储存频道名称 或者 其它需要设置的参数名称   
    """
    config_data = get_yaml_data()
    if config_data == None:return ''
    connect = ''
    text =  guild_id + '_' + channel
    if text in str(config_data) == False:return ''
    if text in config_data.keys():connect =config_data[text]
    return  connect 

